"""
validator.py

Sprint 1
Data Quality Validation (Version 1)

Rules Implemented

DQ-01 Primary Key Duplicate
DQ-02 Missing company_id
DQ-03 Missing year
DQ-04 Duplicate (company_id, year)
DQ-05 Empty Rows
"""

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


class DataValidator:

    def __init__(self):

        self.failures = []

    def log_failure(self, dataset, rule, severity, row, message):

        self.failures.append(
            {
                "dataset": dataset,
                "rule": rule,
                "severity": severity,
                "row": row,
                "message": message,
            }
        )

    def validate(self, datasets):

        for dataset_name, df in datasets.items():

            # -------------------------------
            # DQ-01 Duplicate Primary Key
            # -------------------------------

            if "id" in df.columns:

                duplicate_ids = df[df["id"].duplicated()]

                for idx in duplicate_ids.index:

                    self.log_failure(
                        dataset_name,
                        "DQ-01",
                        "CRITICAL",
                        int(idx),
                        "Duplicate Primary Key",
                    )

            # -------------------------------
            # DQ-02 Missing company_id
            # -------------------------------

            if "company_id" in df.columns:

                missing = df[df["company_id"].isna()]

                for idx in missing.index:

                    self.log_failure(
                        dataset_name,
                        "DQ-02",
                        "CRITICAL",
                        int(idx),
                        "company_id missing",
                    )

            # -------------------------------
            # DQ-03 Missing year
            # -------------------------------

            if "year" in df.columns:

                missing = df[df["year"].isna()]

                for idx in missing.index:

                    self.log_failure(
                        dataset_name, "DQ-03", "WARNING", int(idx), "year missing"
                    )

            # -------------------------------
            # DQ-04 Duplicate company-year
            # -------------------------------

            if "company_id" in df.columns and "year" in df.columns:

                dup = df.duplicated(subset=["company_id", "year"], keep=False)

                duplicate_rows = df[dup]

                for idx in duplicate_rows.index:

                    self.log_failure(
                        dataset_name,
                        "DQ-04",
                        "WARNING",
                        int(idx),
                        "Duplicate Company-Year",
                    )

            # -------------------------------
            # DQ-05 Empty Rows
            # -------------------------------

            empty_rows = df[df.isnull().all(axis=1)]

            for idx in empty_rows.index:

                self.log_failure(
                    dataset_name, "DQ-05", "WARNING", int(idx), "Completely Empty Row"
                )

        self.save_report()

    def save_report(self):

        report = pd.DataFrame(self.failures)

        report_path = OUTPUT_DIR / "validation_failures.csv"

        report.to_csv(report_path, index=False)

        print("\n" + "=" * 60)

        print("Validation Completed")

        print("=" * 60)

        print(f"Failures : {len(report)}")

        print(f"Saved : {report_path}")

        print("=" * 60)
