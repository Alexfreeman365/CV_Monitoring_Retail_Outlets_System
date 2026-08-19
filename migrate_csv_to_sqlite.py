import os
import sys

import pandas as pd

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.db as db


def migrate(cwd_path):
    """One-shot CSV -> SQLite migration. CSV files stay as a cold backup."""
    db_dir = os.path.join(cwd_path, 'db')
    db.init_db(cwd_path)

    camconfig_csv = os.path.join(db_dir, 'camconfig.csv')
    if os.path.exists(camconfig_csv):
        camconfig = pd.read_csv(camconfig_csv).to_dict('records')
        db.save_camconfig(camconfig, cwd_path)
        print('camconfig:', len(camconfig), 'cameras')

    for f in sorted(os.listdir(db_dir)):
        if f.endswith('_shapes_locs.csv'):
            cam_name = f[:-len('_shapes_locs.csv')]
            df = pd.read_csv(os.path.join(db_dir, f))
            db.write_shapes(cam_name, df, cwd_path, mode='replace')
            print('shapes:', cam_name, len(df), 'rows')

    for f in sorted(os.listdir(db_dir)):
        if f.endswith('_visitors.csv'):
            cam = f[:-len('_visitors.csv')]
            df = pd.read_csv(os.path.join(db_dir, f))
            db.write_visitors(cam, df, cwd_path, mode='replace')
            print('visitors:', cam, len(df), 'days')

    for f in sorted(os.listdir(db_dir)):
        if f.endswith('_noSeller_time.csv'):
            cam = f[:-len('_noSeller_time.csv')]
            df = pd.read_csv(os.path.join(db_dir, f))
            db.write_no_seller(cam, df, cwd_path, mode='replace')
            print('no_seller:', cam, len(df), 'days')

    for f in sorted(os.listdir(db_dir)):
        if f.endswith('_evstat.csv'):
            cam = f[:-len('_evstat.csv')]
            df = pd.read_csv(os.path.join(db_dir, f))
            db.write_evstat(cam, df, cwd_path, mode='replace')
            print('evstat:', cam, len(df), 'rows')

    sdi = os.path.join(db_dir, 'shape_db_info.csv')
    if os.path.exists(sdi):
        df = pd.read_csv(sdi)
        db.write_shape_db_info(df, cwd_path)
        print('shape_db_info:', len(df), 'rows')

    for f in sorted(os.listdir(db_dir)):
        if f.endswith('_last_day_processed_imgs.csv'):
            cam = f[:-len('_last_day_processed_imgs.csv')]
            imgs = pd.read_csv(os.path.join(db_dir, f)).iloc[:, 0].astype(str).tolist()
            db.write_last_day_processed(imgs, cam, cwd_path)
            print('processed_images:', cam, len(imgs), 'files')

    xls_path = os.path.join(db_dir, '1_real_viscount.xlsx')
    if os.path.exists(xls_path):
        xls = pd.ExcelFile(xls_path)
        for sheet in xls.sheet_names:
            if sheet.endswith('_arc'):
                continue
            df = pd.read_excel(xls, sheet)
            db.write_real_viscount(sheet, df, cwd_path, mode='replace')
            print('real_viscount:', sheet, len(df), 'days')
        xls.close()

    # Visitor forecast (wide CSV: date + {cam}_pred/_real/_mape, N shops).
    forecast_csv = os.path.join(db_dir, 'visitor_forecast_actual.csv')
    if os.path.exists(forecast_csv):
        df = pd.read_csv(forecast_csv)
        db.write_visitor_forecast_all(df, cwd_path)
        print('visitor_forecast:', len(df), 'weeks')

    print('Migration done ->', db.db_path(cwd_path))


if __name__ == '__main__':
    cwd = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    migrate(cwd)
