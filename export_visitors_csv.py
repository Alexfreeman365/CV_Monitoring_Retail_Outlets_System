"""CLI wrapper: mirror SQLite visitors/no_seller to legacy CSV for the dashboard.

The export also runs automatically at the end of vis_count_noseller_pipeline.
Run manually with: python export_visitors_csv.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import utils.db as db


if __name__ == '__main__':
    db.export_dashboard_csv()
