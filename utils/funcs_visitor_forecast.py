"""Weekly visitor-traffic forecast with Facebook Prophet.

The module predicts the number of visitors per main camera for the next
6 months (24 weeks), week by week (Mon-Sun), and evaluates the just-closed
week against the actual weekly sum (sMAPE).

The expensive part (Prophet) runs in its own venv (``.venv-forecast``). The
pipeline does a cheap in-process gate first (``should_run_forecast``) and only
then launches the forecast script via ``launch_visitor_forecast`` (subprocess),
so the heavy environment is started at most once a week, not on every
vis_count_noseller_pipeline call.

The gate is a no-op unless a full week has closed after the stores' closing
time (``get_border_monday`` returns the next Monday only on Sunday evening past
``max_hour``) AND every main camera has been counted through that Sunday.
"""

import os
import sys
import ast
import subprocess
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.db as db

FORECAST_WEEKS = 24  # 6 months ahead


def _short_name(name):
    return name[:-1] if name[-1].isdigit() else name


def get_date_of_weekday(current_date, target_weekday):
    """'Mon' -> most recent/current Monday; 'Sun' -> upcoming/current Sunday."""
    weekday_map = {'Mon': 0, 'Sun': 6}
    delta_days = weekday_map[target_weekday] - current_date.weekday()
    return current_date + timedelta(days=delta_days)


def get_main_camnames(cwd_path=os.getcwd()):
    """Short names of the traffic-relevant (main) cameras, sorted."""
    camconfig = db.load_camconfig(cwd_path)
    return sorted({
        _short_name(c['cam_name'])
        for c in camconfig
        if not c['cam_name'][-1].isdigit() or c['cam_name'][-1] == '1'
    })


def get_border_monday(cwd_path=os.getcwd()):
    """Monday that closes the current forecast week.

    On Sunday evening after the stores close (past the latest work-hours end)
    the just-finished week is complete, so the border moves to the next Monday.
    Otherwise it is the current week's Monday.
    """
    cur_dt = datetime.today()
    camconfig = db.load_camconfig(cwd_path)
    max_hour = max(ast.literal_eval(c['work_hours'])[1] for c in camconfig)

    min_sun_time = get_date_of_weekday(cur_dt, 'Sun').replace(hour=max_hour, minute=0, second=0)
    max_sun_time = get_date_of_weekday(cur_dt, 'Sun').replace(hour=23, minute=59, second=59)

    if cur_dt < min_sun_time:
        border_mon = get_date_of_weekday(cur_dt, 'Mon').date()
    elif min_sun_time <= cur_dt <= max_sun_time:
        border_mon = get_date_of_weekday(cur_dt, 'Mon').date() + timedelta(days=7)
    else:
        border_mon = get_date_of_weekday(cur_dt, 'Mon').date()

    return pd.to_datetime(border_mon)


def get_hist_df(cam_name, cwd_path=os.getcwd()):
    """Full daily visitor history (ds, y) for a main camera."""
    return db.read_visitors_daily(cam_name, cwd_path)


def get_true_df(cam_name, cwd_path, start_mon, border_mon):
    """Actual daily visitors in [start_mon, border_mon) — the eval window."""
    hist = db.read_visitors_daily(cam_name, cwd_path)
    return hist[(hist['ds'] >= start_mon) & (hist['ds'] < border_mon)].copy()


def initialize_visitor_forecast(cwd_path, cam_names, border_mon):
    """Determine start_mon and the unchanged past part (eval_part) of the forecast.

    start_mon = the first week that needs (re)prediction: the next Monday after
    the last recorded real week, or border_mon - 28 days when no real data yet.
    """
    expected_cols = ['date']
    for cam in cam_names:
        expected_cols.extend([f'{cam}_pred', f'{cam}_real', f'{cam}_mape'])

    df = db.read_visitor_forecast_all(cwd_path)
    if df.empty:
        df = pd.DataFrame(columns=expected_cols)
    else:
        existing_cols = [col for col in expected_cols if col in df.columns]
        df = df[existing_cols]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = np.nan
        df = df[expected_cols]
        df['date'] = pd.to_datetime(df['date'])

    real_cols = [c for c in df.columns if c.endswith('_real')]
    df_with_real = df[(df[real_cols] > 0).any(axis=1)] if real_cols else pd.DataFrame()
    if not df_with_real.empty:
        start_mon = df_with_real['date'].max() + pd.Timedelta(days=7)
    else:
        start_mon = border_mon - pd.Timedelta(days=28)

    eval_part = df[df['date'] < start_mon].copy()
    return start_mon, eval_part


def get_last_day_pred(cwd_path, cam_name):
    """First future week's prediction from the previous run (continuity lock)."""
    df = db.read_visitor_forecast_all(cwd_path)
    if df.empty:
        return None

    pred_col, real_col = f'{cam_name}_pred', f'{cam_name}_real'
    if pred_col not in df.columns or real_col not in df.columns:
        return None

    future_forecast = df[df[real_col] == 0]
    if future_forecast.empty:
        return None

    last_day_pred = future_forecast[pred_col].iloc[0]
    if pd.notna(last_day_pred) and last_day_pred != 0:
        return last_day_pred
    return None


def _calc_smape(r, p):
    """sMAPE scaled x 10000: 0 = no data, 1 = ~perfect, N = sMAPE*10000."""
    if pd.isna(r) or r == 0:
        return 0
    val = 2 * abs(r - p) / (abs(r) + abs(p))
    val = round(val, 2)
    if val == 0:
        return 1
    return int(round(val * 10000))


def _gate(cwd_path):
    """Cheap pre-check (no Prophet). Returns (cam_names, border_mon, start_mon,
    eval_part) when it is time to forecast, otherwise None."""
    cam_names = get_main_camnames(cwd_path)
    if not cam_names:
        return None

    border_mon = get_border_monday(cwd_path)
    start_mon, eval_part = initialize_visitor_forecast(cwd_path, cam_names, border_mon)
    if (border_mon - start_mon).days <= 0:
        return None

    # Multi-shop guard: every main camera must be counted through the Sunday
    # that just closed, otherwise the eval week would be incomplete.
    week_end = border_mon - pd.Timedelta(days=1)
    for cam_name in cam_names:
        hist = db.read_visitors_daily(cam_name, cwd_path)
        if hist.empty or hist['ds'].max() < week_end:
            return None

    return cam_names, border_mon, start_mon, eval_part


def should_run_forecast(cwd_path=os.getcwd()):
    """Cheap gate for the pipeline: True only when it is time to forecast."""
    return _gate(cwd_path) is not None


def _fit_prophet(hist_df):
    import logging
    # Suppress benign noise only (app logging stays intact):
    # - prophet.plot logs an error when plotly is missing (we don't use it);
    # - cmdstanpy INFO logs "Chain [1] start/done processing".
    logging.getLogger('prophet.plot').setLevel(logging.CRITICAL)
    logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

    from prophet import Prophet  # lazy import: heavy, forecast venv only
    model = Prophet(
        growth='linear',
        seasonality_mode='multiplicative',
        yearly_seasonality=False,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.1,
    )
    model.fit(hist_df)
    return model


def run_visitor_forecast(cwd_path=os.getcwd()):
    """Full forecast: gate + train + predict + write SQLite + export CSV."""
    gate = _gate(cwd_path)
    if gate is None:
        return
    cam_names, border_mon, start_mon, eval_part = gate

    full_data = pd.DataFrame()

    for cam_name in cam_names:
        print(f'Processing camera: {cam_name}')

        hist_df = get_hist_df(cam_name, cwd_path)
        hist_df = hist_df[hist_df['ds'] < border_mon].copy()

        last_day_pred = get_last_day_pred(cwd_path, cam_name)

        # Mask non-working January holidays (days 1-8) of past years as NaN.
        jan_holidays_mask = (hist_df['ds'].dt.month == 1) & (hist_df['ds'].dt.day <= 8)
        hist_df.loc[jan_holidays_mask, 'y'] = np.nan

        model = _fit_prophet(hist_df)
        future = model.make_future_dataframe(
            periods=(border_mon - start_mon).days + 7 * FORECAST_WEEKS)
        forecast = model.predict(future)

        pred_df = forecast[['ds', 'yhat']][forecast['ds'] >= start_mon].copy()
        true_df = get_true_df(cam_name, cwd_path, start_mon, border_mon)

        df = pred_df.set_index('ds').join(true_df.set_index('ds'), how='left')
        weekly_df = df.resample('W-MON', label='left', closed='left').sum().round().astype('int')

        pred_col, real_col, mape_col = f'{cam_name}_pred', f'{cam_name}_real', f'{cam_name}_mape'
        weekly_df.reset_index(inplace=True)
        weekly_df.columns = ['date', pred_col, real_col]

        # Keep the previously published value for the first week (continuity).
        if last_day_pred is not None:
            weekly_df.at[weekly_df.index[0], pred_col] = last_day_pred

        weekly_df[mape_col] = weekly_df.apply(
            lambda row: _calc_smape(row[real_col], row[pred_col]), axis=1)

        if full_data.empty:
            full_data = weekly_df.copy()
        else:
            full_data = full_data.merge(weekly_df, on='date', how='left')

    full_data = pd.concat([eval_part, full_data], ignore_index=True)
    full_data = full_data[:-1].copy()  # drop the partial last week

    db.write_visitor_forecast_all(full_data, cwd_path)
    db.export_forecast_csv(cwd_path)
    print('visitor_forecast: updated')


def _forecast_python(cwd_path):
    if os.name == 'nt':
        return os.path.join(cwd_path, '.venv-forecast', 'Scripts', 'python.exe')
    return os.path.join(cwd_path, '.venv-forecast', 'bin', 'python')


def launch_visitor_forecast(cwd_path=os.getcwd()):
    """Launch the forecast script in its dedicated venv (subprocess)."""
    python = _forecast_python(cwd_path)
    script = os.path.abspath(__file__)
    if not (os.path.exists(python) and os.path.exists(script)):
        print('visitor_forecast: dedicated venv/script not found, skipped')
        return False
    subprocess.run([python, script, cwd_path], cwd=cwd_path, check=False)
    return True


if __name__ == '__main__':
    run_visitor_forecast(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
