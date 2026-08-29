import os
import ast
import sqlite3
from datetime import datetime
from urllib.parse import quote


RETAIL_PROJECT_ID = 'cv_monitoring_retail_outlets_system'
ODFR_PROJECT_ID = 'odfr'
UNKNOWN_PROJECT_ID = 'unknown'
MISSING_DATABASE = 'missing'
EMPTY_DATABASE = 'empty'

# SQLite application_id is a 32-bit file-format marker (ASCII "CVRO").
RETAIL_APPLICATION_ID = 0x4356524F
ODFR_APPLICATION_ID = 0x4F444652  # reserved for the ODFR owner project
RETAIL_SCHEMA_VERSION = 1

# ODFR is checked first: a database polluted by an old Retail initializer may
# also contain every table in _RETAIL_SIGNATURE.
_ODFR_SIGNATURE = frozenset({
    'shape_alarm_notif', 'faces', 'processed_fshapes', 'sysconfig', 'cleared_days',
})
_RETAIL_SIGNATURE = frozenset({
    'days', 'visitors', 'no_seller_time', 'evstat', 'evstat_day', 'real_viscount',
})
_SHARED_PROJECTS = frozenset({RETAIL_PROJECT_ID, ODFR_PROJECT_ID})
_RETAIL_ONLY = frozenset({RETAIL_PROJECT_ID})


class DatabaseIdentityError(RuntimeError):
    """The selected cv.db is missing, unknown, or owned by another project."""


class DatabaseSchemaError(RuntimeError):
    """A known project database does not provide a required compatible table."""


def _cwd(cwd_path=None):
    return os.path.abspath(os.fspath(cwd_path)) if cwd_path is not None else os.getcwd()


def db_path(cwd_path=None):
    """Path to the single SQLite database."""
    return os.path.join(_cwd(cwd_path), 'db', 'cv.db')


def _readonly_uri(path):
    # Encoding the entire Windows path also supports UNC paths; a file://host
    # authority is rejected by standard SQLite builds on Windows.
    return 'file:' + quote(os.path.abspath(path), safe='') + '?mode=ro'


def _connect(cwd_path=None, read_only=False):
    root = _cwd(cwd_path)
    path = db_path(root)
    if read_only:
        if not os.path.isfile(path):
            raise DatabaseIdentityError(f'Database does not exist: {path}')
        conn = sqlite3.connect(_readonly_uri(path), uri=True, timeout=15)
    else:
        os.makedirs(os.path.join(root, 'db'), exist_ok=True)
        conn = sqlite3.connect(path, timeout=15)
    conn.execute('PRAGMA busy_timeout = 15000')
    if not read_only:
        conn.execute('PRAGMA journal_mode = WAL')
    conn.row_factory = sqlite3.Row
    return conn


def _table_names(conn):
    return {
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")
    }


def identify_database(cwd_path=None):
    """Return the owner project id without changing the database.

    Legacy databases with application_id=0 are recognized by project-specific
    table signatures. ODFR wins over Retail so an already polluted ODFR database
    is still classified correctly.
    """
    path = db_path(cwd_path)
    if not os.path.exists(path):
        return MISSING_DATABASE
    if os.path.getsize(path) == 0:
        return EMPTY_DATABASE
    try:
        conn = _connect(cwd_path, read_only=True)
        application_id = conn.execute('PRAGMA application_id').fetchone()[0]
        tables = _table_names(conn)
        conn.close()
    except sqlite3.DatabaseError as error:
        raise DatabaseIdentityError(f'Cannot identify SQLite database {path}: {error}') from error

    if application_id == RETAIL_APPLICATION_ID:
        return RETAIL_PROJECT_ID
    if application_id == ODFR_APPLICATION_ID:
        return ODFR_PROJECT_ID
    if application_id != 0:
        return UNKNOWN_PROJECT_ID
    if _ODFR_SIGNATURE.issubset(tables):
        return ODFR_PROJECT_ID
    if _RETAIL_SIGNATURE.issubset(tables):
        return RETAIL_PROJECT_ID
    if not tables:
        return EMPTY_DATABASE
    return UNKNOWN_PROJECT_ID


def database_is_uninitialized(cwd_path=None):
    return identify_database(cwd_path) in {MISSING_DATABASE, EMPTY_DATABASE}


def _require_tables(cwd_path, table_names, allowed_projects):
    project_id = identify_database(cwd_path)
    path = db_path(cwd_path)
    if project_id in {MISSING_DATABASE, EMPTY_DATABASE}:
        raise DatabaseIdentityError(
            f'Database is not initialized: {path}. Run the owning project bootstrap first.')
    if project_id == UNKNOWN_PROJECT_ID:
        raise DatabaseIdentityError(f'Database belongs to an unknown project: {path}')
    if project_id not in allowed_projects:
        raise DatabaseIdentityError(
            f'Operation is not allowed for project {project_id!r}: {path}')

    conn = _connect(cwd_path, read_only=True)
    missing = set(table_names) - _table_names(conn)
    conn.close()
    if missing:
        raise DatabaseSchemaError(
            f'Database {path} lacks required table(s): {", ".join(sorted(missing))}')
    return project_id


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
CREATE TABLE IF NOT EXISTS visitor_forecast (
    cam_name TEXT NOT NULL,          -- short name of the main camera (shop)
    date     TEXT NOT NULL,          -- ISO Monday (week start)
    pred     INTEGER NOT NULL,       -- predicted weekly visitors
    real     INTEGER NOT NULL,       -- actual weekly visitors (0 = no data / future)
    mape     INTEGER NOT NULL,       -- sMAPE x 10000 (0 = no data, 1 = ~perfect)
    PRIMARY KEY (cam_name, date)
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

def init_db(cwd_path=None):
    """Bootstrap or migrate the Retail database, never a foreign database."""
    project_id = identify_database(cwd_path)
    path = db_path(cwd_path)
    if project_id not in {MISSING_DATABASE, EMPTY_DATABASE, RETAIL_PROJECT_ID}:
        raise DatabaseIdentityError(
            f'Refusing to apply the Retail schema to project {project_id!r}: {path}')

    conn = _connect(cwd_path)
    current_version = conn.execute('PRAGMA user_version').fetchone()[0]
    if current_version > RETAIL_SCHEMA_VERSION:
        conn.close()
        raise DatabaseSchemaError(
            f'Database schema version {current_version} is newer than supported '
            f'version {RETAIL_SCHEMA_VERSION}: {path}')
    conn.executescript(_CORE_SCHEMA)
    conn.execute(f'PRAGMA application_id = {RETAIL_APPLICATION_ID}')
    conn.execute(f'PRAGMA user_version = {RETAIL_SCHEMA_VERSION}')
    conn.commit()
    conn.close()


# --- camconfig ---

def _as_tuple(value):
    if isinstance(value, str):
        return tuple(ast.literal_eval(value))
    return tuple(value)


def load_camconfig(cwd_path=None):
    """Return camconfig as list of dicts, compatible with the old CSV fields."""
    _require_tables(cwd_path, {'cameras'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
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


def save_camconfig(camconfig, cwd_path=None):
    _require_tables(cwd_path, {'cameras'}, _SHARED_PROJECTS)
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


def write_shapes(cam_name, df, cwd_path=None, mode='append'):
    _require_tables(cwd_path, {'shapes_locs'}, _SHARED_PROJECTS)
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


def read_shapes(cam_name, cwd_path=None):
    """Return the shapes DataFrame in the exact CSV column layout."""
    import pandas as pd
    _require_tables(cwd_path, {'shapes_locs'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
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


def read_visitors(cam_name, cwd_path=None):
    import pandas as pd
    _require_tables(cwd_path, {'visitors', 'days'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
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


def write_visitors(cam_name, df, cwd_path=None, mode='append'):
    import pandas as pd
    _require_tables(cwd_path, {'visitors', 'days'}, _RETAIL_ONLY)
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


def read_no_seller(cam_name, cwd_path=None):
    import pandas as pd
    _require_tables(cwd_path, {'no_seller_time', 'days'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
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


def write_no_seller(cam_name, df, cwd_path=None, mode='append'):
    import pandas as pd
    _require_tables(cwd_path, {'no_seller_time', 'days'}, _RETAIL_ONLY)
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


# --- dashboard CSV export (temporary) ---

def _short_name(name):
    return name[:-1] if name[-1].isdigit() else name


def export_dashboard_csv(cwd_path=None):
    """Mirror visitors/no_seller to legacy CSV (dashboard link) in db/."""
    cwd_path = _cwd(cwd_path)
    camconfig = load_camconfig(cwd_path)
    short_names = sorted({_short_name(c['cam_name']) for c in camconfig})
    for sn in short_names:
        vis = read_visitors(sn, cwd_path)
        if not vis.empty:
            vis.to_csv(os.path.join(cwd_path, 'db', f'{sn}_visitors.csv'), index=False)
        ns = read_no_seller(sn, cwd_path)
        if not ns.empty:
            ns.to_csv(os.path.join(cwd_path, 'db', f'{sn}_noSeller_time.csv'), index=False)


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


def write_evstat(cam_name, df, cwd_path=None, mode='replace'):
    import pandas as pd
    _require_tables(cwd_path, {'evstat', 'evstat_day'}, _RETAIL_ONLY)
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


def read_evstat(cam_name, cwd_path=None):
    import pandas as pd
    _require_tables(cwd_path, {'evstat', 'evstat_day'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
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

def read_last_day_processed(cam_name, cwd_path=None):
    _require_tables(cwd_path, {'processed_images'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
    rows = conn.execute(
        'SELECT file_name FROM processed_images WHERE cam_name = ? ORDER BY rowid', (cam_name,)).fetchall()
    conn.close()
    return [r['file_name'] for r in rows]


def write_last_day_processed(file_names, cam_name, cwd_path=None):
    _require_tables(cwd_path, {'processed_images'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path)
    conn.execute('DELETE FROM processed_images WHERE cam_name = ?', (cam_name,))
    conn.executemany(
        'INSERT INTO processed_images VALUES (?,?)',
        [(cam_name, str(f)) for f in file_names])
    conn.commit()
    conn.close()


# --- shape_db_info ---

def read_shape_db_info(cwd_path=None):
    import pandas as pd
    _require_tables(cwd_path, {'shape_db_info'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
    df = pd.read_sql_query('SELECT * FROM shape_db_info', conn)
    conn.close()
    if df.empty:
        return df
    df = df.rename(columns={
        'cam_name': 'Camera', 'file_name': 'File_name',
        'first_day': 'First_day', 'last_day': 'Last_day',
        'number_of_lines': 'Number_of_lines'})
    return df


def write_shape_db_info(df, cwd_path=None):
    _require_tables(cwd_path, {'shape_db_info'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path)
    conn.execute('DELETE FROM shape_db_info')
    conn.executemany(
        'INSERT INTO shape_db_info VALUES (?,?,?,?,?)',
        list(zip(df['Camera'].astype(str), df['File_name'].astype(str),
                 df['First_day'].astype(str), df['Last_day'].astype(str),
                 df['Number_of_lines'].astype(int))))
    conn.commit()
    conn.close()


def export_shape_db_info_csv(cwd_path=None):
    """Mirror shape_db_info to legacy CSV (dashboard link) in db/."""
    cwd_path = _cwd(cwd_path)
    df = read_shape_db_info(cwd_path)
    if not df.empty:
        df.to_csv(os.path.join(cwd_path, 'db', 'shape_db_info.csv'), index=False)


def build_shape_db_info(cam_names, cwd_path=None):
    """Build the shape_db_info DataFrame from the per-camera shapes tables."""
    import pandas as pd
    _require_tables(cwd_path, {'shapes_locs'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
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


def shapes_exist(cam_name, cwd_path=None):
    _require_tables(cwd_path, {'shapes_locs'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
    n = conn.execute(
        'SELECT COUNT(*) FROM shapes_locs WHERE cam_name = ?', (cam_name,)).fetchone()[0]
    conn.close()
    return n > 0


def shapes_count(cam_name, cwd_path=None):
    _require_tables(cwd_path, {'shapes_locs'}, _SHARED_PROJECTS)
    conn = _connect(cwd_path, read_only=True)
    n = conn.execute(
        'SELECT COUNT(*) FROM shapes_locs WHERE cam_name = ?', (cam_name,)).fetchone()[0]
    conn.close()
    return n


def visitors_exist(cam_name, cwd_path=None):
    if identify_database(cwd_path) != RETAIL_PROJECT_ID:
        return False
    _require_tables(cwd_path, {'visitors'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
    n = conn.execute(
        'SELECT COUNT(*) FROM visitors WHERE cam_name = ?', (cam_name,)).fetchone()[0]
    conn.close()
    return n > 0


def read_real_viscount(cam_name, cwd_path=None):
    """Return the manual count in the wide layout used by the Excel sheet."""
    import pandas as pd
    _require_tables(cwd_path, {'real_viscount'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
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


def write_real_viscount(cam_name, df, cwd_path=None, mode='replace'):
    import pandas as pd
    _require_tables(cwd_path, {'real_viscount'}, _RETAIL_ONLY)
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


# --- visitor_forecast ---

def _forecast_mape_to_int(value):
    """sMAPE to int (x 10000). Accepts CSV string ('0,12'/'0,0001'/'0'/'0,0') or int."""
    if value is None:
        return 0
    if isinstance(value, str):
        s = value.strip()
        if s in ('', '0', '0,0'):
            return 0
        return int(round(float(s.replace(',', '.')) * 10000))
    return int(value)


def _forecast_mape_to_str(value):
    """int sMAPE (x 10000) back to CSV string ('0,12'/'0,0001'/'0')."""
    if value is None or value == 0:
        return '0'
    if value == 1:
        return '0,0001'
    return str(value / 10000).replace('.', ',')


def read_visitor_forecast_all(cwd_path=None):
    """Wide forecast DataFrame: date + {cam}_pred/{cam}_real/{cam}_mape (int mape)."""
    import pandas as pd
    _require_tables(cwd_path, {'visitor_forecast'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
    df = pd.read_sql_query(
        'SELECT cam_name, date, pred, real, mape FROM visitor_forecast', conn)
    conn.close()
    if df.empty:
        return pd.DataFrame(columns=['date'])

    cams = sorted(df['cam_name'].unique())
    parts = []
    for c in cams:
        sub = df[df['cam_name'] == c][['date', 'pred', 'real', 'mape']].copy()
        sub = sub.rename(columns={'pred': f'{c}_pred', 'real': f'{c}_real', 'mape': f'{c}_mape'})
        parts.append(sub)
    wide = parts[0]
    for sub in parts[1:]:
        wide = wide.merge(sub, on='date', how='outer')
    wide['date'] = pd.to_datetime(wide['date'])
    cols = ['date'] + [f'{c}_{k}' for c in cams for k in ('pred', 'real', 'mape')]
    return wide.sort_values('date').reset_index(drop=True)[cols]


def write_visitor_forecast_all(df, cwd_path=None):
    """Write a wide forecast DataFrame (date + {cam}_pred/_real/_mape) to long format."""
    import pandas as pd
    _require_tables(cwd_path, {'visitor_forecast'}, _RETAIL_ONLY)
    conn = _connect(cwd_path)
    conn.execute('DELETE FROM visitor_forecast')
    if df.empty:
        conn.commit()
        conn.close()
        return

    cams = sorted({c.rsplit('_', 1)[0] for c in df.columns if c.endswith('_pred')})
    rows = []
    for _, r in df.iterrows():
        date = pd.to_datetime(r['date']).strftime('%Y-%m-%d')
        for c in cams:
            pred = int(r[f'{c}_pred']) if pd.notna(r.get(f'{c}_pred')) else 0
            real = int(r[f'{c}_real']) if pd.notna(r.get(f'{c}_real')) else 0
            mape = _forecast_mape_to_int(r.get(f'{c}_mape'))
            rows.append((c, date, pred, real, mape))
    conn.executemany('INSERT INTO visitor_forecast VALUES (?,?,?,?,?)', rows)
    conn.commit()
    conn.close()


def export_forecast_csv(cwd_path=None):
    """Mirror visitor_forecast to legacy CSV (dashboard link), mape as '0,12' strings."""
    import pandas as pd
    cwd_path = _cwd(cwd_path)
    wide = read_visitor_forecast_all(cwd_path)
    if wide.empty:
        return
    for col in wide.columns:
        if col.endswith('_mape'):
            wide[col] = wide[col].apply(_forecast_mape_to_str)
    wide.to_csv(os.path.join(cwd_path, 'db', 'visitor_forecast.csv'), index=False)


def read_visitors_daily(cam_name, cwd_path=None):
    """Daily visitor sums as Prophet-ready DataFrame (ds=datetime, y=int)."""
    import pandas as pd
    _require_tables(cwd_path, {'visitors'}, _RETAIL_ONLY)
    conn = _connect(cwd_path, read_only=True)
    df = pd.read_sql_query(
        'SELECT date AS ds, SUM(count) AS y FROM visitors '
        'WHERE cam_name = ? GROUP BY date ORDER BY date',
        conn, params=(cam_name,))
    conn.close()
    if df.empty:
        return pd.DataFrame(columns=['ds', 'y'])
    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = df['y'].astype(int)
    return df[['ds', 'y']]
