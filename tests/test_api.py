from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


# ============================================================
# HEALTH
# ============================================================

def test_health_endpoint():
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "db_row_counts" in data
    assert "uptime_seconds" in data
    assert "version" in data


# ============================================================
# COMPANIES
# ============================================================

def test_companies_endpoint():
    response = client.get(
        "/api/v1/companies"
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "companies" in data
    assert data["count"] >= 1


def test_company_profile():
    response = client.get(
        "/api/v1/companies/TCS"
    )

    assert response.status_code == 200

    data = response.json()

    assert "company_id" in data
    assert "company_name" in data


def test_invalid_company_profile():
    response = client.get(
        "/api/v1/companies/INVALID_COMPANY"
    )

    assert response.status_code == 404


# ============================================================
# P&L
# ============================================================

def test_company_profit_loss():
    response = client.get(
        "/api/v1/companies/TCS/pl"
    )

    assert response.status_code == 200

    data = response.json()

    assert "company_id" in data
    assert "history" in data


def test_profit_loss_year_filter():
    response = client.get(
        "/api/v1/companies/TCS/pl",
        params={
            "from_year": "2020-01",
            "to_year": "2024-01",
        },
    )

    assert response.status_code == 200


# ============================================================
# BALANCE SHEET
# ============================================================

def test_balance_sheet():
    response = client.get(
        "/api/v1/companies/TCS/bs"
    )

    assert response.status_code == 200

    data = response.json()

    assert "history" in data


# ============================================================
# CASH FLOW
# ============================================================

def test_cashflow():
    response = client.get(
        "/api/v1/companies/TCS/cashflow"
    )

    assert response.status_code == 200

    data = response.json()

    assert "history" in data


# ============================================================
# RATIOS
# ============================================================

def test_ratios():
    response = client.get(
        "/api/v1/companies/TCS/ratios"
    )

    assert response.status_code == 200

    data = response.json()

    assert "ratios" in data
    assert "scores" in data


# ============================================================
# TEARSHEET
# ============================================================

def test_tearsheet():
    response = client.get(
        "/api/v1/companies/TCS/tearsheet"
    )

    assert response.status_code == 200

    data = response.json()

    assert "company" in data
    assert "profitability" in data
    assert "growth" in data
    assert "leverage" in data
    assert "cash_flow" in data
    assert "valuation" in data
    assert "scores" in data


# ============================================================
# SCREENER
# ============================================================

def test_screener():
    response = client.get(
        "/api/v1/screener"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "results" in data


def test_screener_roe_filter():
    response = client.get(
        "/api/v1/screener",
        params={
            "min_roe": 20
        },
    )

    assert response.status_code == 200


def test_screener_pagination():
    response = client.get(
        "/api/v1/screener",
        params={
            "page": 1,
            "page_size": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10


# ============================================================
# SECTORS
# ============================================================

def test_sectors():
    response = client.get(
        "/api/v1/sectors"
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "sectors" in data


def test_invalid_sector():
    response = client.get(
        "/api/v1/sectors/INVALID_SECTOR"
    )

    assert response.status_code == 404


# ============================================================
# PEERS
# ============================================================

def test_peers():
    response = client.get(
        "/api/v1/peers/TCS"
    )

    assert response.status_code == 200

    data = response.json()

    assert "company" in data
    assert "peers" in data


def test_invalid_peer_company():
    response = client.get(
        "/api/v1/peers/INVALID_COMPANY"
    )

    assert response.status_code == 404


# ============================================================
# VALUATION
# ============================================================

def test_valuation():
    response = client.get(
        "/api/v1/valuation/TCS"
    )

    assert response.status_code == 200

    data = response.json()

    assert "market_cap_crore" in data
    assert "pe_ratio" in data
    assert "pb_ratio" in data


def test_invalid_valuation_company():
    response = client.get(
        "/api/v1/valuation/INVALID_COMPANY"
    )

    assert response.status_code == 404


# ============================================================
# PORTFOLIO
# ============================================================

def test_portfolio():
    response = client.get(
        "/api/v1/portfolio"
    )

    assert response.status_code == 200

    data = response.json()

    assert "company_count" in data
    assert "companies" in data
    assert "sector_distribution" in data
    assert "statistics" in data


# ============================================================
# DOCUMENTS
# ============================================================

def test_documents():
    response = client.get(
        "/api/v1/documents"
    )

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "documents" in data


def test_invalid_document():
    response = client.get(
        "/api/v1/documents/not_a_real_document"
    )

    assert response.status_code == 404