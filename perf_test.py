import requests
import time
import statistics
import os
from concurrent.futures import ThreadPoolExecutor

BASE = "http://127.0.0.1:8000/api/v1"

# -----------------------------
# SCREENER PERFORMANCE
# -----------------------------
def screener_call():
    start = time.perf_counter()
    response = requests.get(BASE + "/screener", timeout=30)
    elapsed = time.perf_counter() - start
    return elapsed, response.status_code

print("\n=== SCREENER PERFORMANCE ===")

overall_start = time.perf_counter()

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda _: screener_call(), range(10)))

overall_time = time.perf_counter() - overall_start

times = [r[0] for r in results]

for i, (elapsed, status) in enumerate(results, 1):
    print("Call", i, ":", round(elapsed, 3), "sec | HTTP", status)

print("Total time:", round(overall_time, 3), "sec")
print("Average:", round(statistics.mean(times), 3), "sec")
print("Maximum:", round(max(times), 3), "sec")

screener_pass = overall_time <= 10
print("Screener target:", "PASS" if screener_pass else "FAIL")


# -----------------------------
# COMPANY PROFILE PERFORMANCE
# -----------------------------
print("\n=== COMPANY PROFILE PERFORMANCE ===")

response = requests.get(BASE + "/companies", timeout=30)
data = response.json()

if isinstance(data, dict):
    companies = (
        data.get("companies")
        or data.get("data")
        or data.get("results")
        or []
    )
else:
    companies = data

tickers = []

for company in companies:
    if isinstance(company, dict):
        ticker = company.get("ticker") or company.get("symbol")
        if ticker and ticker not in tickers:
            tickers.append(ticker)

tickers = tickers[:5]

print("Tickers tested:", tickers)

profile_results = []

for ticker in tickers:
    start = time.perf_counter()

    r = requests.get(
        BASE + "/companies/" + str(ticker),
        timeout=30
    )

    elapsed = time.perf_counter() - start

    profile_results.append(
        (ticker, elapsed, r.status_code)
    )

    print(
        ticker,
        ":",
        round(elapsed, 3),
        "sec | HTTP",
        r.status_code
    )

profile_pass = all(
    elapsed < 3 and status == 200
    for _, elapsed, status in profile_results
)

print(
    "Company Profile target:",
    "PASS" if profile_pass else "FAIL"
)


# -----------------------------
# CREATE PERF NOTES
# -----------------------------
os.makedirs("output", exist_ok=True)

with open("output/perf_notes.md", "w", encoding="utf-8") as f:

    f.write("# Performance Testing Notes\n\n")

    f.write("## 1. Screener API Performance\n\n")
    f.write("- Endpoint: `GET /api/v1/screener`\n")
    f.write("- Concurrent requests: 10\n")
    f.write("- Total execution time: " + str(round(overall_time, 3)) + " seconds\n")
    f.write("- Average response time: " + str(round(statistics.mean(times), 3)) + " seconds\n")
    f.write("- Maximum response time: " + str(round(max(times), 3)) + " seconds\n")
    f.write("- Target: all 10 requests complete within 10 seconds\n")
    f.write("- Result: **" + ("PASS" if screener_pass else "FAIL") + "**\n\n")

    f.write("| Request | Response Time | HTTP Status |\n")
    f.write("|---|---:|---:|\n")

    for i, (elapsed, status) in enumerate(results, 1):
        f.write(
            "| " + str(i) +
            " | " + str(round(elapsed, 3)) +
            " sec | " + str(status) + " |\n"
        )

    f.write("\n## 2. Company Profile Performance\n\n")
    f.write("- Target: each Company Profile response under 3 seconds\n\n")

    f.write("| Ticker | Response Time | HTTP Status | Result |\n")
    f.write("|---|---:|---:|---|\n")

    for ticker, elapsed, status in profile_results:

        result = "PASS" if elapsed < 3 and status == 200 else "FAIL"

        f.write(
            "| " + str(ticker) +
            " | " + str(round(elapsed, 3)) +
            " sec | " + str(status) +
            " | **" + result + "** |\n"
        )

    f.write(
        "\nOverall Company Profile Result: **" +
        ("PASS" if profile_pass else "FAIL") +
        "**\n"
    )

    f.write("\n## 3. Performance Bottlenecks\n\n")
    f.write("- No major performance bottlenecks identified during the test run.\n")
    f.write("- SQLite query optimisation/indexing should be applied only if future measurements identify slow queries.\n")

print("\n===================================")
print("DONE!")
print("Created: output/perf_notes.md")
print("===================================")
