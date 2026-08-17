import os
import ast
import sqlite3
from datetime import datetime


def db_path(cwd_path=os.getcwd()):
    """Path to the single SQLite database."""
    return os.path.join(cwd_path, 'db', 'cv.db')


def _connect(cwd_path=os.getcwd()):
    os.makedirs(os.path.join(cwd_path, 'db'), exist_ok=True)
    conn = sqlite3.connect(db_path(cwd_path))
    conn.execute('PRAGMA journal_mode = WAL')
    conn.row_factory = sqlite3.Row
    return conn


_CORE_SCHEMA = '''
CREATE TABLE IF NOT EXISTS cameras (
    cam_name        TEXT PRIMARY KEY,
    shape_zone      TEXT NOT NULL,
    face_zone       TEXT NOT NULL,
    frame           TEXT NOT NULL,
    hour_start      INTEGER NOT NULL,
    hour_end        INTEGER NOT NULL,
    mean_threshold  INTEGER NOT NULL,
    window_next     INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS days (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    photos   INTEGER NOT NULL DEFAULT 0,
    s        TEXT NOT NULL DEFAULT 'auto',
    PRIMARY KEY (cam_name, date)
);
CREATE TABLE IF NOT EXISTS visitors (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    hour     INTEGER NOT NULL,
    count    INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);
CREATE TABLE IF NOT EXISTS no_seller_time (
    cam_name         TEXT NOT NULL,
    date             TEXT NOT NULL,
    hour             INTEGER NOT NULL,
    absence_minutes  INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);
CREATE TABLE IF NOT EXISTS evstat (
    cam_name    TEXT NOT NULL,
    date        TEXT NOT NULL,
    hour        INTEGER NOT NULL,
    count_real  INTEGER NOT NULL,
    count_auto  INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);
CREATE TABLE IF NOT EXISTS evstat_day (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    sum_real INTEGER NOT NULL,
    sum_auto INTEGER NOT NULL,
    err      INTEGER NOT NULL,
    mape     INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date)
);
CREATE TABLE IF NOT EXISTS shape_db_info (
    cam_name        TEXT NOT NULL,
    file_name       TEXT NOT NULL,
    first_day       TEXT NOT NULL,
    last_day        TEXT NOT NULL,
    number_of_lines INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS processed_images (
    cam_name  TEXT NOT NULL,
    file_name TEXT NOT NULL,
    PRIMARY KEY (cam_name, file_name)
);
CREATE TABLE IF NOT EXISTS real_viscount (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    hour     INTEGER NOT NULL,
    count    INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);
CREATE TABLE IF NOT EXISTS shapes_locs (
    cam_name          TEXT NOT NULL,
    origin_file_name  TEXT NOT NULL,
    uid8              TEXT NOT NULL,
    day               TEXT NOT NULL,
    shape_y1          INTEGER NOT NULL,
    shape_y2          INTEGER NOT NULL,
    shape_x1          INTEGER NOT NULL,
    shape_x2          INTEGER NOT NULL,
    shape_zone_coords TEXT,
    shape_zone        INTEGER NOT NULL,
    face_zone_coords  TEXT,
    face_zone         INTEGER NOT NULL,
    PRIMARY KEY (cam_name, origin_file_name, uid8)
);
CREATE INDEX IF NOT EXISTS idx_shapes_cam_day  ON shapes_locs (cam_name, day);
CREATE INDEX IF NOT EXISTS idx_shapes_cam_uid8 ON shapes_locs (cam_name, uid8);
'''

def init_db(cwd_path=os.getcwd()):
    conn = _connect(cwd_path)
    conn.executescript(_CORE_SCHEMA)
    conn.commit()
    conn.close()


# --- camconfig ---

def _as_tuple(value):
    if isinstance(value, str):
        return tuple(ast.literal_eval(value))
    return tuple(value)


def load_camconfig(cwd_path=os.getcwd()):
    """Return camconfig as list of dicts, compatible with the old CSV fields."""
    init_db(cwd_path)
    conn = _connect(cwd_path)
    rows = conn.execute('SELECT * FROM cameras').fetchall()
    conn.close()
    return [{
        'cam_name': r['cam_name'],
        'shape_zone': r['shape_zone'],
        'face_zone': r['face_zone'],
        'frame': r['frame'],
        'work_hours': f"({r['hour_start']}, {r['hour_end']})",
        'vis_count_alg': f"({r['mean_threshold']}, {r['window_next']})",
    } for r in rows]


def save_camconfig(camconfig, cwd_path=os.getcwd()):
    init_db(cwd_path)
    conn = _connect(cwd_path)
    conn.execute('DELETE FROM cameras')
    for cam in camconfig:
        hour_start, hour_end = _as_tuple(cam['work_hours'])
        mean_threshold, window_next = _as_tuple(cam['vis_count_alg'])
        conn.execute(
            'INSERT INTO cameras VALUES (?,?,?,?,?,?,?,?)',
            (cam['cam_name'], str(cam['shape_zone']), str(cam['face_zone']),
             str(cam['frame']), hour_start, hour_end, mean_threshold, window_next))
    conn.commit()
    conn.close()


# --- shapes (unified table) ---

def _shape_location_tuple(v):
    """Normalize shape_location: str '[y1, y2, x1, x2]' or list [y1,y2,x1,x2] -> (y1,y2,x1,x2)."""
    if isinstance(v, str):
        parts = [int(float(x)) for x in v.strip('[]').replace(' ', '').split(',')]
    elif isinstance(v, (list, tuple)):
        parts = [int(float(x)) for x in v]
    else:
        parts = [0, 0, 0, 0]
    return tuple(parts)


def write_shapes(cam_name, df, cwd_path=os.getcwd(), mode='append'):
    init_db(cwd_path)
    conn = _connect(cwd_path)
    if mode == 'replace':
        conn.execute('DELETE FROM shapes_locs WHERE cam_name = ?', (cam_name,))
    if df.empty:
        conn.commit()
        conn.close()
        return

    locs = df['shape_location'].apply(_shape_location_tuple)
    sc = df['shape_zone_coords'].where(df['shape_zone_coords'].notna(), None)
    fc = df['face_zone_coords'].where(df['face_zone_coords'].notna(), None)
    rows = list(zip(
        [cam_name] * len(df),
        df['origin_file_name'].astype(str),
        df['uid8'].astype(str),
        df['uid8'].astype(str).str[:6],
        locs.map(lambda t: t[0]), locs.map(lambda t: t[1]),
        locs.map(lambda t: t[2]), locs.map(lambda t: t[3]),
        sc, df['shape_zone'].fillna(0).astype(int),
        fc, df['face_zone'].fillna(0).astype(int),
    ))
    conn.executemany(
        'INSERT OR REPLACE INTO shapes_locs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', rows)
    conn.commit()
    conn.close()


def read_shapes(cam_name, cwd_path=os.getcwd()):
    """Return the shapes DataFrame in the exact CSV column layout."""
    import pandas as pd
    conn = _connect(cwd_path)
    df = pd.read_sql_query(
        'SELECT origin_file_name, uid8, shape_y1, shape_y2, shape_x1, shape_x2, '
        'shape_zone_coords, shape_zone, face_zone_coords, face_zone '
        'FROM shapes_locs WHERE cam_name = ? ORDER BY origin_file_name', conn, params=(cam_name,))
    conn.close()
    if df.empty:
        return df
    df['shape_location'] = (
        '[' + df['shape_y1'].astype(str) + ', ' + df['shape_y2'].astype(str) + ', '
        + df['shape_x1'].astype(str) + ', ' + df['shape_x2'].astype(str) + ']')
    return df[['origin_file_name', 'uid8', 'shape_location', 'shape_zone_coords',
               'shape_zone', 'face_zone_coords', 'face_zone']]


# --- visitors / no_seller_time (wide <-> long) ---

def _hour_cols(df):
    return [c for c in df.columns if str(c).isdigit()]


def read_visitors(cam_name, cwd_path=os.getcwd()):
    import pandas as pd
    conn = _connect(cwd_path)
    df = pd.read_sql_query('SELECT date, hour, count FROM visitors WHERE cam_name = ?', conn, params=(cam_name,))
    days = pd.read_sql_query('SELECT date, s FROM days WHERE cam_name = ?', conn, params=(cam_name,))
    conn.close()
    if df.empty:
        return pd.DataFrame(columns=['date', 'sum', 's'])
    wide = df.pivot(index='date', columns='hour', values='count').fillna(0).astype(int).reset_index()
    wide.columns.name = None
    wide.columns = [str(c) for c in wide.columns]
    wide['sum'] = wide[[c for c in wide.columns if c != 'date']].sum(axis=1)
    if not days.empty:
        wide = wide.merge(days, on='date', how='left')
    if 's' not in wide.columns:
        wide['s'] = 'auto'
    wide['s'] = wide['s'].fillna('auto')
    hours = [c for c in wide.columns if str(c).isdigit()]
    return wide[['date'] + sorted(hours) + ['sum', 's']]


def write_visitors(cam_name, df, cwd_path=os.getcwd(), mode='append'):
    import pandas as pd
    init_db(cwd_path)
    conn = _connect(cwd_path)
    hours = [c for c in _hour_cols(df)]
    rows = []
    for _, r in df.iterrows():
        date = pd.to_datetime(r['date']).strftime('%Y-%m-%d')
        for h in hours:
            rows.append((cam_name, date, int(h), int(r[h])))
        s = str(r.get('s', 'auto')) if 's' in df.columns else 'auto'
        conn.execute('INSERT INTO days (cam_name, date, s) VALUES (?,?,?) '
                     'ON CONFLICT(cam_name, date) DO UPDATE SET s = excluded.s',
                     (cam_name, date, s))
    if mode == 'replace':
        conn.execute('DELETE FROM visitors WHERE cam_name = ?', (cam_name,))
    conn.executemany('INSERT OR REPLACE INTO visitors VALUES (?,?,?,?)', rows)
    conn.commit()
    conn.close()


def read_no_seller(cam_name, cwd_path=os.getcwd()):
    import pandas as pd
    conn = _connect(cwd_path)
    df = pd.read_sql_query('SELECT date, hour, absence_minutes FROM no_seller_time WHERE cam_name = ?', conn, params=(cam_name,))
    days = pd.read_sql_query('SELECT date, photos FROM days WHERE cam_name = ?', conn, params=(cam_name,))
    conn.close()
    if df.empty:
        return pd.DataFrame(columns=['date', 'sum', 'photos'])
    wide = df.pivot(index='date', columns='hour', values='absence_minutes').fillna(0).astype(int).reset_index()
    wide.columns.name = None
    wide.columns = [str(c) for c in wide.columns]
    wide['sum'] = wide[[c for c in wide.columns if c != 'date']].sum(axis=1)
    if not days.empty:
        wide = wide.merge(days, on='date', how='left')
    if 'photos' not in wide.columns:
        wide['photos'] = 0
    wide['photos'] = wide['photos'].fillna(0).astype(int)
    hours = [c for c in wide.columns if str(c).isdigit()]
    return wide[['date'] + sorted(hours) + ['sum', 'photos']]


def write_no_seller(cam_name, df, cwd_path=os.getcwd(), mode='append'):
    import pandas as pd
    init_db(cwd_path)
    conn = _connect(cwd_path)
    hours = [c for c in _hour_cols(df)]
    rows = []
    for _, r in df.iterrows():
        date = pd.to_datetime(r['date']).strftime('%Y-%m-%d')
        for h in hours:
            rows.append((cam_name, date, int(h), int(r[h])))
        if 'photos' in df.columns:
            conn.execute('INSERT INTO days (cam_name, date, photos) VALUES (?,?,?) '
                         'ON CONFLICT(cam_name, date) DO UPDATE SET photos = excluded.photos',
                         (cam_name, date, int(r['photos'])))
    if mode == 'replace':
        conn.execute('DELETE FROM no_seller_time WHERE cam_name = ?', (cam_name,))
    conn.executemany('INSERT OR REPLACE INTO no_seller_time VALUES (?,?,?,?)', rows)
    conn.commit()
    conn.close()


# --- evstat (wide <-> long) ---

def _parse_mape(value):
    if isinstance(value, str):
        return int(round(float(value.replace(',', '.')) * 100))
    return int(value)


def _mape_to_str(mape_int):
    if mape_int == 0:
        return "0,0"
    if mape_int < 100 and mape_int % 10 == 0:
        return f"0,{mape_int // 10}"
    if mape_int < 100:
        return f"0,{mape_int:02d}"
    return str(mape_int / 100).replace('.', ',')


def write_evstat(cam_name, df, cwd_path=os.getcwd(), mode='replace'):
    import pandas as pd
    init_db(cwd_path)
    conn = _connect(cwd_path)
    hours = [c for c in _hour_cols(df)]
    if mode == 'replace':
        conn.execute('DELETE FROM evstat WHERE cam_name = ?', (cam_name,))
        conn.execute('DELETE FROM evstat_day WHERE cam_name = ?', (cam_name,))
    for date, grp in df.groupby('date'):
        date = pd.to_datetime(date).strftime('%Y-%m-%d')
        real = grp[grp['s'] == 'real']
        auto = grp[grp['s'] == 'auto']
        if real.empty or auto.empty:
            continue
        r, a = real.iloc[0], auto.iloc[0]
        for h in hours:
            conn.execute('INSERT OR REPLACE INTO evstat VALUES (?,?,?,?,?)',
                         (cam_name, date, int(h), int(r[h]), int(a[h])))
        conn.execute('INSERT OR REPLACE INTO evstat_day VALUES (?,?,?,?,?,?)',
                     (cam_name, date, int(r['sum']), int(a['sum']),
                      int(r['err']), _parse_mape(r['mape'])))
    conn.commit()
    conn.close()


def read_evstat(cam_name, cwd_path=os.getcwd()):
    import pandas as pd
    conn = _connect(cwd_path)
    ev = pd.read_sql_query('SELECT date, hour, count_real, count_auto FROM evstat WHERE cam_name = ?', conn, params=(cam_name,))
    day = pd.read_sql_query('SELECT date, sum_real, sum_auto, err, mape FROM evstat_day WHERE cam_name = ?', conn, params=(cam_name,))
    conn.close()
    if ev.empty:
        return pd.DataFrame(columns=['date', 'sum', 's', 'err', 'mape'])
    rows = []
    for date in sorted(ev['date'].unique()):
        d = day[day['date'] == date]
        if d.empty:
            continue
        d = d.iloc[0]
        real_row = {'date': date, 's': 'real', 'sum': d['sum_real'],
                    'err': d['err'], 'mape': _mape_to_str(d['mape'])}
        auto_row = {'date': date, 's': 'auto', 'sum': d['sum_auto'],
                    'err': d['err'], 'mape': _mape_to_str(d['mape'])}
        for _, rr in ev[ev['date'] == date].iterrows():
            real_row[str(rr['hour'])] = rr['count_real']
            auto_row[str(rr['hour'])] = rr['count_auto']
        rows.append(real_row)
        rows.append(auto_row)
    df = pd.DataFrame(rows)
    hours = sorted([c for c in df.columns if str(c).isdigit()])
    return df[['date'] + hours + ['sum', 's', 'err', 'mape']]


# --- processed_images (last_day_processed_imgs) ---

def read_last_day_processed(cam_name, cwd_path=os.getcwd()):
    conn = _connect(cwd_path)
    rows = conn.execute(
        'SELECT file_name FROM processed_images WHERE cam_name = ? ORDER BY rowid', (cam_name,)).fetchall()
    conn.close()
    return [r['file_name'] for r in rows]


def write_last_day_processed(file_names, cam_name, cwd_path=os.getcwd()):
    init_db(cwd_path)
    conn = _connect(cwd_path)
    conn.execute('DELETE FROM processed_images WHERE cam_name = ?', (cam_name,))
    conn.executemany(
        'INSERT INTO processed_images VALUES (?,?)',
        [(cam_name, str(f)) for f in file_names])
    conn.commit()
    conn.close()


# --- shape_db_info ---

def read_shape_db_info(cwd_path=os.getcwd()):
    import pandas as pd
    conn = _connect(cwd_path)
    df = pd.read_sql_query('SELECT * FROM shape_db_info', conn)
    conn.close()
    if df.empty:
        return df
    df = df.rename(columns={
        'cam_name': 'Camera', 'file_name': 'File_name',
        'first_day': 'First_day', 'last_day': 'Last_day',
        'number_of_lines': 'Number_of_lines'})
    return df


def write_shape_db_info(df, cwd_path=os.getcwd()):
    init_db(cwd_path)
    conn = _connect(cwd_path)
    conn.execute('DELETE FROM shape_db_info')
    conn.executemany(
        'INSERT INTO shape_db_info VALUES (?,?,?,?,?)',
        list(zip(df['Camera'].astype(str), df['File_name'].astype(str),
                 df['First_day'].astype(str), df['Last_day'].astype(str),
                 df['Number_of_lines'].astype(int))))
    conn.commit()
    conn.close()


def build_shape_db_info(cam_names, cwd_path=os.getcwd()):
    """Build the shape_db_info DataFrame from the per-camera shapes tables."""
    import pandas as pd
    conn = _connect(cwd_path)
    rows = []
    for cam_name in cam_names:
        try:
            first, last, n = conn.execute(
                'SELECT MIN(day), MAX(day), COUNT(*) FROM shapes_locs WHERE cam_name = ?',
                (cam_name,)).fetchone()
        except sqlite3.OperationalError:
            continue
        if n is None or n == 0:
            continue
        rows.append({'Camera': cam_name, 'File_name': f'{cam_name}_shapes_locs.csv',
                     'First_day': datetime.strptime(first, '%y%m%d').date(),
                     'Last_day': datetime.strptime(last, '%y%m%d').date(),
                     'Number_of_lines': n})
    conn.close()
    return pd.DataFrame(rows)


def shapes_exist(cam_name, cwd_path=os.getcwd()):
    conn = _connect(cwd_path)
    try:
        n = conn.execute('SELECT COUNT(*) FROM shapes_locs WHERE cam_name = ?', (cam_name,)).fetchone()[0]
    except sqlite3.OperationalError:
        n = 0
    conn.close()
    return n > 0


def shapes_count(cam_name, cwd_path=os.getcwd()):
    conn = _connect(cwd_path)
    try:
        n = conn.execute('SELECT COUNT(*) FROM shapes_locs WHERE cam_name = ?', (cam_name,)).fetchone()[0]
    except sqlite3.OperationalError:
        n = 0
    conn.close()
    return n


def visitors_exist(cam_name, cwd_path=os.getcwd()):
    conn = _connect(cwd_path)
    n = conn.execute('SELECT COUNT(*) FROM visitors WHERE cam_name = ?', (cam_name,)).fetchone()[0]
    conn.close()
    return n > 0


def read_real_viscount(cam_name, cwd_path=os.getcwd()):
    """Return the manual count in the wide layout used by the Excel sheet."""
    import pandas as pd
    conn = _connect(cwd_path)
    df = pd.read_sql_query('SELECT date, hour, count FROM real_viscount WHERE cam_name = ?', conn, params=(cam_name,))
    conn.close()
    if df.empty:
        return pd.DataFrame(columns=['date', 'sum', '*'])
    wide = df.pivot(index='date', columns='hour', values='count').fillna(0).astype(int).reset_index()
    wide.columns.name = None
    wide.columns = [str(c) for c in wide.columns]
    wide['sum'] = wide[[c for c in wide.columns if c != 'date']].sum(axis=1)
    wide['*'] = None
    hours = [c for c in wide.columns if str(c).isdigit()]
    wide = wide[['date'] + sorted(hours) + ['sum', '*']]
    wide['date'] = pd.to_datetime(wide['date'])
    return wide


def write_real_viscount(cam_name, df, cwd_path=os.getcwd(), mode='replace'):
    import pandas as pd
    init_db(cwd_path)
    conn = _connect(cwd_path)
    hours = [c for c in _hour_cols(df)]
    rows = []
    for _, r in df.iterrows():
        date = pd.to_datetime(r['date']).strftime('%Y-%m-%d')
        for h in hours:
            rows.append((cam_name, date, int(h), int(r[h])))
    if mode == 'replace':
        conn.execute('DELETE FROM real_viscount WHERE cam_name = ?', (cam_name,))
    conn.executemany('INSERT OR REPLACE INTO real_viscount VALUES (?,?,?,?)', rows)
    conn.commit()
    conn.close()
