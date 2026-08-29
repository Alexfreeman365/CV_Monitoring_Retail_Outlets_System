import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from utils import db


class DatabaseIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def connect(self):
        path = Path(db.db_path(self.root))
        path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(path)

    def table_names(self):
        with closing(self.connect()) as conn:
            return {
                row[0] for row in conn.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")
            }

    def create_odfr_database(self, include_retail_pollution=False):
        with closing(self.connect()) as conn:
            conn.executescript(
                """
                CREATE TABLE cameras (
                    cam_name TEXT PRIMARY KEY,
                    shape_zone TEXT NOT NULL,
                    face_zone TEXT NOT NULL,
                    frame TEXT NOT NULL,
                    hour_start INTEGER NOT NULL,
                    hour_end INTEGER NOT NULL,
                    mean_threshold INTEGER NOT NULL,
                    window_next INTEGER NOT NULL
                );
                CREATE TABLE shapes_locs (
                    cam_name TEXT NOT NULL,
                    origin_file_name TEXT NOT NULL,
                    uid8 TEXT NOT NULL,
                    day TEXT NOT NULL,
                    shape_y1 INTEGER NOT NULL,
                    shape_y2 INTEGER NOT NULL,
                    shape_x1 INTEGER NOT NULL,
                    shape_x2 INTEGER NOT NULL,
                    shape_zone_coords TEXT,
                    shape_zone INTEGER NOT NULL,
                    face_zone_coords TEXT,
                    face_zone INTEGER NOT NULL,
                    PRIMARY KEY (cam_name, origin_file_name, uid8)
                );
                CREATE TABLE shape_alarm_notif (cam_name TEXT PRIMARY KEY);
                CREATE TABLE faces (uid81 TEXT PRIMARY KEY);
                CREATE TABLE processed_fshapes (
                    cam_name TEXT NOT NULL,
                    uid8 TEXT NOT NULL,
                    PRIMARY KEY (cam_name, uid8)
                );
                CREATE TABLE sysconfig (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE cleared_days (day TEXT PRIMARY KEY);
                """
            )
            if include_retail_pollution:
                conn.executescript(
                    """
                    CREATE TABLE days (
                        cam_name TEXT NOT NULL,
                        date TEXT NOT NULL,
                        photos INTEGER NOT NULL DEFAULT 0,
                        s TEXT NOT NULL DEFAULT 'auto',
                        PRIMARY KEY (cam_name, date)
                    );
                    CREATE TABLE visitors (
                        cam_name TEXT NOT NULL,
                        date TEXT NOT NULL,
                        hour INTEGER NOT NULL,
                        count INTEGER NOT NULL,
                        PRIMARY KEY (cam_name, date, hour)
                    );
                    CREATE TABLE no_seller_time (
                        cam_name TEXT, date TEXT, hour INTEGER, absence_minutes INTEGER
                    );
                    CREATE TABLE evstat (
                        cam_name TEXT, date TEXT, hour INTEGER,
                        count_real INTEGER, count_auto INTEGER
                    );
                    CREATE TABLE evstat_day (
                        cam_name TEXT, date TEXT, sum_real INTEGER, sum_auto INTEGER,
                        err INTEGER, mape INTEGER
                    );
                    CREATE TABLE real_viscount (
                        cam_name TEXT, date TEXT, hour INTEGER, count INTEGER
                    );
                    INSERT INTO visitors VALUES ('shop', '2026-08-25', 10, 1);
                    """
                )

    def test_empty_database_bootstraps_retail_schema_and_identity(self):
        self.assertTrue(db.database_is_uninitialized(self.root))

        db.init_db(self.root)

        self.assertEqual(db.identify_database(self.root), db.RETAIL_PROJECT_ID)
        self.assertTrue({
            'cameras', 'visitors', 'no_seller_time', 'evstat', 'evstat_day',
            'real_viscount', 'visitor_forecast', 'shapes_locs',
        }.issubset(self.table_names()))
        with closing(self.connect()) as conn:
            self.assertEqual(
                conn.execute('PRAGMA application_id').fetchone()[0],
                db.RETAIL_APPLICATION_ID,
            )
            self.assertEqual(
                conn.execute('PRAGMA user_version').fetchone()[0],
                db.RETAIL_SCHEMA_VERSION,
            )

    def test_legacy_retail_database_is_adopted(self):
        with closing(self.connect()) as conn:
            conn.executescript(db._CORE_SCHEMA)

        self.assertEqual(db.identify_database(self.root), db.RETAIL_PROJECT_ID)
        db.init_db(self.root)

        with closing(self.connect()) as conn:
            self.assertEqual(
                conn.execute('PRAGMA application_id').fetchone()[0],
                db.RETAIL_APPLICATION_ID,
            )

    def test_polluted_odfr_wins_over_retail_signature_and_rejects_bootstrap(self):
        self.create_odfr_database(include_retail_pollution=True)
        before = self.table_names()

        self.assertEqual(db.identify_database(self.root), db.ODFR_PROJECT_ID)
        with self.assertRaises(db.DatabaseIdentityError):
            db.init_db(self.root)

        self.assertEqual(self.table_names(), before)
        self.assertFalse(db.visitors_exist('shop', self.root))

    def test_shared_camera_config_operations_work_for_odfr(self):
        self.create_odfr_database()
        camconfig = [{
            'cam_name': 'shop1',
            'shape_zone': '(0, 10, 0, 10)',
            'face_zone': '(5, 10, 0, 10)',
            'frame': '(0, 10, 0, 10)',
            'work_hours': (10, 21),
            'vis_count_alg': (2, 2),
        }]

        db.save_camconfig(camconfig, self.root)

        self.assertEqual(db.load_camconfig(self.root), [{
            **camconfig[0],
            'work_hours': '(10, 21)',
            'vis_count_alg': '(2, 2)',
        }])
        self.assertFalse({'visitors', 'evstat'}.intersection(self.table_names()))

    def test_shared_shapes_round_trip_works_for_odfr(self):
        import pandas as pd

        self.create_odfr_database()
        source = pd.DataFrame([{
            'origin_file_name': '260825120000.jpg',
            'uid8': '2608251200000000000001',
            'shape_location': [1, 10, 2, 20],
            'shape_zone_coords': '(0, 10, 0, 20)',
            'shape_zone': 1,
            'face_zone_coords': None,
            'face_zone': 0,
        }])

        db.write_shapes('shop1', source, self.root)
        restored = db.read_shapes('shop1', self.root)

        self.assertEqual(len(restored), 1)
        self.assertEqual(restored.iloc[0]['uid8'], source.iloc[0]['uid8'])
        self.assertFalse({'visitors', 'evstat'}.intersection(self.table_names()))

    def test_retail_analytics_round_trip_after_explicit_bootstrap(self):
        import pandas as pd

        db.init_db(self.root)
        source = pd.DataFrame([{
            'date': '2026-08-25',
            '10': 3,
            '11': 4,
            'sum': 7,
            's': 'auto',
        }])

        db.write_visitors('shop', source, self.root, mode='replace')
        restored = db.read_visitors('shop', self.root)

        self.assertEqual(restored.iloc[0]['10'], 3)
        self.assertEqual(restored.iloc[0]['11'], 4)
        self.assertEqual(restored.iloc[0]['sum'], 7)

    def test_unknown_nonempty_database_is_not_claimed(self):
        with closing(self.connect()) as conn:
            conn.execute('CREATE TABLE alien_data (id INTEGER PRIMARY KEY)')
        before = self.table_names()

        self.assertEqual(db.identify_database(self.root), db.UNKNOWN_PROJECT_ID)
        with self.assertRaises(db.DatabaseIdentityError):
            db.init_db(self.root)

        self.assertEqual(self.table_names(), before)

    def test_default_cwd_is_resolved_at_call_time(self):
        original = os.getcwd()
        other = self.root / 'other'
        other.mkdir()
        try:
            os.chdir(self.root)
            first = db.db_path()
            os.chdir(other)
            second = db.db_path()
        finally:
            os.chdir(original)

        self.assertEqual(first, str(self.root / 'db' / 'cv.db'))
        self.assertEqual(second, str(other / 'db' / 'cv.db'))


if __name__ == '__main__':
    unittest.main()
