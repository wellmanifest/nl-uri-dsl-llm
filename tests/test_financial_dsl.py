import json
from pathlib import Path
import jsonschema
import pytest

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"


def test_financial_spec_exists():
    spec_path = SPEC_DIR / "FINANCIAL_TRANSACTIONS_TAXONOMY_DSL.md"
    assert spec_path.exists()
    content = spec_path.read_text(encoding="utf-8")
    assert "NUL-010" in content
    assert "NUL-011" in content
    assert "NUL-012" in content
    assert "NUL-013" in content
    assert "DSL CAPITALIZE" in content
    assert "DOSSIER_STATUS" in content
    assert "MATCHED_EXACT" in content
    assert "MATCHED_INTERNAL_TRANSFER" in content


def test_financial_dossier_schema():
    schema_path = SCHEMA_DIR / "financial-dossier.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    # Valid dossier
    valid_dossier = {
        "SCHEMA": "wellmanifest.faktury.dossier/v1",
        "MONTH": "2026.06",
        "AUDIT_SUMMARY": {
            "TOTAL_CASES": 1,
            "STATUS_MATCHED_EXACT": 1,
            "COMPLETION_RATE_PERCENT": 100.0
        },
        "CASES": [
            {
                "CASE_ID": "CASE_2026_06_OVH_PL6985175",
                "DOSSIER_STATUS": "PENDING_PORTAL_DOWNLOAD",
                "CONFIDENCE_LEVEL": "CONFIDENCE_HIGH",
                "COUNTERPARTY": "OVH Sp. z o.o.",
                "COST_CATEGORY": "IT_INFRASTRUCTURE",
                "SOURCE_NODE": {
                    "CHANNEL": "PORTAL_SAAS_VENDOR",
                    "PROVIDER_ID": "www-ovhcloud-com",
                    "PORTAL_URL": "https://help.ovhcloud.com/csm/"
                },
                "DOCUMENT_NODE": {
                    "DOCUMENT_PRESENCE": "DOCUMENT_NOT_DOWNLOADED",
                    "INVOICE_NUMBER": "PL6985175",
                    "GROSS_AMOUNT": 67.64,
                    "CURRENCY": "PLN"
                },
                "TRANSACTION_NODE": {
                    "PAYMENT_STATE": "PAYMENT_SETTLED",
                    "PAYMENT_METHOD": "CARD_ONLINE_ECOMMERCE",
                    "BOOKED_AMOUNT": -67.64,
                    "CURRENCY": "PLN"
                },
                "CONFIRMATION_NODE": {
                    "CONFIRMATION_TYPE": "BANK_STATEMENT_LINE",
                    "CONFIRMATION_FILE_REF": "bank-alior/wyciag.csv"
                },
                "DISCREPANCY_ANALYSIS": {
                    "LAG_CALENDAR_DAYS": 1,
                    "LAG_BUSINESS_DAYS": 0,
                    "AMOUNT_DELTA": 0.0,
                    "LLM_EXPLANATION": "Płatność autoryzowana w niedzielę, rozliczona w poniedziałek."
                }
            }
        ]
    }

    jsonschema.validate(instance=valid_dossier, schema=schema)


def test_financial_dossier_schema_rejects_uncapitalized_status():
    schema_path = SCHEMA_DIR / "financial-dossier.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    invalid_dossier = {
        "SCHEMA": "wellmanifest.faktury.dossier/v1",
        "MONTH": "2026.06",
        "AUDIT_SUMMARY": {
            "TOTAL_CASES": 1,
            "COMPLETION_RATE_PERCENT": 100.0
        },
        "CASES": [
            {
                "CASE_ID": "CASE_1",
                "DOSSIER_STATUS": "pending_portal_download",  # Lowercase violation of NUL-010!
                "SOURCE_NODE": {"CHANNEL": "PORTAL_SAAS_VENDOR"},
                "DOCUMENT_NODE": {"DOCUMENT_PRESENCE": "DOCUMENT_PRESENT"},
                "TRANSACTION_NODE": {"PAYMENT_STATE": "PAYMENT_SETTLED", "PAYMENT_METHOD": "CARD_ONLINE_ECOMMERCE"},
                "CONFIRMATION_NODE": {"CONFIRMATION_TYPE": "BANK_STATEMENT_LINE"},
                "DISCREPANCY_ANALYSIS": {}
            }
        ]
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_dossier, schema=schema)


def test_financial_source_schema():
    schema_path = SCHEMA_DIR / "financial-source.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    valid_source = {
        "SCHEMA": "wellmanifest.faktury.source/v1",
        "SOURCE_ID": "paypal-firmowy",
        "SOURCE_CHANNEL_TYPE": "WALLET_PAYPAL",
        "CATEGORY": "TRANSACTION_CHANNELS",
        "NAME": "PayPal Konto Firmowe",
        "MONTH": "2026.06",
        "BASE_CURRENCY": "PLN",
        "SUPPORTED_CURRENCIES": ["PLN", "EUR", "USD"],
        "DATA_FILES": [
            {
                "FILE_NAME": "transactions_2026_06.csv",
                "FILE_FORMAT": "PAYPAL_CSV_EXPORT"
            }
        ],
        "INGESTION_STATUS": "STATUS_OK",
        "REQUIRES_MANUAL_ATTENTION": False
    }

    jsonschema.validate(instance=valid_source, schema=schema)
