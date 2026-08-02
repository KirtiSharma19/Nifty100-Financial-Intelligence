import os
from pathlib import Path

REPORT_FOLDER = Path("reports/tearsheets")

pdfs = list(REPORT_FOLDER.glob("*.pdf"))

print("=" * 60)
print("VERIFYING TEARSHEETS")
print("=" * 60)

print(f"Total PDFs Found : {len(pdfs)}")
print()

small_files = []

for pdf in sorted(pdfs):

    size_kb = pdf.stat().st_size / 1024

    print(f"{pdf.name:<55} {size_kb:.2f} KB")

    if size_kb < 5:
        small_files.append(pdf.name)

print()
print("=" * 60)

if small_files:
    print("Small PDFs Found:")
    for f in small_files:
        print(" -", f)
else:
    print("All PDFs look good.")

print("=" * 60)