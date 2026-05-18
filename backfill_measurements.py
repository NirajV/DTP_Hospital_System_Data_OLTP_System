"""
Backfill Clinical Measurements
==============================
Pivots existing `encounter_vitals` rows into the new `clinical_measurements`
table, one row per non-null metric column. Idempotent: re-runs skip
(encounter_id, type_id, recorded_at) triplets already present.

Prerequisites
-------------
  1. create_schema_measurements.sql has been applied
  2. dml_07_measurements_reference.sql has been loaded (units + types)
  3. At least one row in `users` with user_type='admin' (used as fallback
     recorded_by when encounter_vitals.recorded_by is NULL or unmapped)

Usage
-----
    python backfill_measurements.py             # backfill all
    python backfill_measurements.py --dry-run   # report only, no writes
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from decimal import Decimal

from database_connection import DatabaseConnection

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
LOG_DIR = "Fake_Data_Log"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(
    LOG_DIR, f"backfill_measurements_{datetime.now():%Y%m%d_%H%M%S}.log"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger("backfill_measurements")

# ----------------------------------------------------------------------
# Mapping: encounter_vitals column -> measurement_types.type_code
# ----------------------------------------------------------------------
VITAL_COLUMN_TO_TYPE = {
    "blood_pressure_systolic":  "bp_systolic",
    "blood_pressure_diastolic": "bp_diastolic",
    "heart_rate":               "heart_rate",
    "respiratory_rate":         "respiratory_rate",
    "temperature":              "temperature_f",   # encounter_vitals stores Fahrenheit
    "oxygen_saturation":        "oxygen_saturation",
    "weight":                   "weight_lb",
    "height":                   "height_in",
    "bmi":                      "bmi",
    "pain_score":               "pain_score",
}


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def load_type_lookup(db: DatabaseConnection) -> dict:
    """Return {type_code: (type_id, default_unit_id, low, high)}."""
    rows = db.execute_select(
        "SELECT type_code, type_id, default_unit_id, "
        "normal_range_low, normal_range_high FROM measurement_types"
    )
    if not rows:
        logger.error("measurement_types is empty. Run dml_07_measurements_reference.sql first.")
        sys.exit(1)
    return {
        r["type_code"]: (
            r["type_id"],
            r["default_unit_id"],
            r["normal_range_low"],
            r["normal_range_high"],
        )
        for r in rows
    }


def resolve_fallback_user(db: DatabaseConnection) -> int:
    """Pick any admin user as the fallback recorder."""
    rows = db.execute_select(
        "SELECT user_id FROM users WHERE user_type='admin' AND is_active=1 LIMIT 1"
    )
    if not rows:
        logger.error("No active admin user found — cannot assign fallback recorded_by.")
        sys.exit(1)
    uid = rows[0]["user_id"]
    logger.info(f"Fallback recorded_by user_id = {uid}")
    return uid


def compute_abnormal(value, low, high) -> bool:
    if value is None or (low is None and high is None):
        return False
    v = Decimal(str(value))
    if low is not None and v < Decimal(str(low)):
        return True
    if high is not None and v > Decimal(str(high)):
        return True
    return False


def already_migrated(db: DatabaseConnection) -> set:
    """Return set of (encounter_id, type_id, recorded_at) already in clinical_measurements."""
    rows = db.execute_select(
        "SELECT encounter_id, type_id, recorded_at FROM clinical_measurements"
    )
    return {(r["encounter_id"], r["type_id"], r["recorded_at"]) for r in (rows or [])}


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def backfill(dry_run: bool = False) -> None:
    logger.info("=" * 60)
    logger.info(f"Backfill start  dry_run={dry_run}  log={LOG_PATH}")
    logger.info("=" * 60)

    with DatabaseConnection() as db:
        type_lookup = load_type_lookup(db)
        missing_types = [c for c in VITAL_COLUMN_TO_TYPE.values() if c not in type_lookup]
        if missing_types:
            logger.error(f"Missing required measurement_types: {missing_types}")
            sys.exit(1)

        fallback_user = resolve_fallback_user(db)
        existing = already_migrated(db)
        logger.info(f"Already-migrated rows in clinical_measurements: {len(existing)}")

        # Read source rows joined to encounters for patient_id
        select_cols = ", ".join(f"v.{c}" for c in VITAL_COLUMN_TO_TYPE.keys())
        source_sql = f"""
            SELECT
                v.vital_id, v.encounter_id, v.recorded_datetime,
                v.recorded_by, e.patient_id,
                {select_cols}
            FROM encounter_vitals v
            JOIN encounters e ON e.encounter_id = v.encounter_id
            ORDER BY v.vital_id
        """
        source_rows = db.execute_select(source_sql) or []
        logger.info(f"Source encounter_vitals rows: {len(source_rows)}")

        batch = []
        skipped_dupes = 0
        for row in source_rows:
            for col, type_code in VITAL_COLUMN_TO_TYPE.items():
                value = row.get(col)
                if value is None:
                    continue
                type_id, default_unit_id, low, high = type_lookup[type_code]
                if default_unit_id is None:
                    logger.warning(f"type_code={type_code} has no default_unit_id — skipped")
                    continue
                key = (row["encounter_id"], type_id, row["recorded_datetime"])
                if key in existing:
                    skipped_dupes += 1
                    continue

                # encounter_vitals.recorded_by is a staff/nurse id (per schema comment),
                # not necessarily a users.user_id — fall back to admin.
                recorded_by = fallback_user

                batch.append((
                    row["encounter_id"],
                    row["patient_id"],
                    type_id,
                    default_unit_id,
                    Decimal(str(value)),
                    None,                                # value_text
                    recorded_by,
                    row["recorded_datetime"],
                    compute_abnormal(value, low, high),
                    f"backfilled from encounter_vitals.vital_id={row['vital_id']}",
                ))

        logger.info(f"Rows queued for insert: {len(batch)}")
        logger.info(f"Rows skipped (duplicates): {skipped_dupes}")

        if not batch:
            logger.info("Nothing to insert. Exiting.")
            return

        if dry_run:
            logger.info("Dry-run — no INSERTs executed. First 3 rows preview:")
            for r in batch[:3]:
                logger.info(f"  {r}")
            return

        insert_sql = """
            INSERT INTO clinical_measurements
                (encounter_id, patient_id, type_id, unit_id,
                 value_numeric, value_text, recorded_by, recorded_at,
                 is_abnormal, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        ok = db.execute_many(insert_sql, batch)
        if ok:
            logger.info(f"Backfill complete: {len(batch)} rows inserted.")
        else:
            logger.error("Backfill failed — see prior error log lines.")
            sys.exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill encounter_vitals into clinical_measurements.")
    parser.add_argument("--dry-run", action="store_true", help="report only, do not insert")
    args = parser.parse_args()
    backfill(dry_run=args.dry_run)
