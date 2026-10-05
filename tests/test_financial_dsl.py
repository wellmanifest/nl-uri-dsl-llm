import json
from pathlib import Path
import jsonschema
import pytest

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"


def test_financial_spec_exists_and_declares_rules():
    spec_path = SPEC_DIR / "FINANCIAL_TRANSACTIONS_TAXONOMY_DSL.md"
    assert spec_path.exists()
    content = spec_path.read_text(encoding="utf-8")
    assert "NUL-010" in content
    assert "NUL-011" in content
    assert "NUL-012" in content
    assert "NUL-013" in content
    assert "NUL-014" in content
    assert "DSL CAPITALIZE" in content
    assert "DOSSIER_STATUS" in content
    assert "MATCHED_EXACT" in content
    assert "MATCHED_INTERNAL_TRANSFER" in content
    assert "urn:fin:" in content


def test_financial_dossier_schema_with_urns():
    schema_path = SCHEMA_DIR / "financial-dossier.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

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
                "CASE_URN": "urn:fin:dossier:2026.06:CASE_2026_06_OVH_PL6985175",
                "DOSSIER_STATUS": "PENDING_PORTAL_DOWNLOAD",
                "CONFIDENCE_LEVEL": "CONFIDENCE_HIGH",
                "COUNTERPARTY": "OVH Sp. z o.o.",
                "COST_CATEGORY": "IT_INFRASTRUCTURE",
                "SOURCE_NODE": {
                    "CHANNEL": "PORTAL_SAAS_VENDOR",
                    "SOURCE_URN": "urn:fin:source:portal:www-ovhcloud-com",
                    "EMAIL_URN": "urn:fin:email:msg:2026.06.28_ovhcloud_twoja_faktura",
                    "PROVIDER_ID": "www-ovhcloud-com",
                    "PORTAL_URL": "https://help.ovhcloud.com/csm/"
                },
                "DOCUMENT_NODE": {
                    "DOCUMENT_PRESENCE": "DOCUMENT_NOT_DOWNLOADED",
                    "DOCUMENT_URN": "urn:fin:doc:invoice:PL6985175",
                    "INVOICE_NUMBER": "PL6985175",
                    "GROSS_AMOUNT": 67.64,
                    "CURRENCY": "PLN"
                },
                "TRANSACTION_NODE": {
                    "PAYMENT_STATE": "PAYMENT_SETTLED",
                    "PAYMENT_METHOD": "CARD_ONLINE_ECOMMERCE",
                    "TRANSACTION_URN": "urn:fin:txn:bank:alior_pln:20260628_ovh_6764",
                    "BOOKED_AMOUNT": -67.64,
                    "CURRENCY": "PLN"
                },
                "CONFIRMATION_NODE": {
                    "CONFIRMATION_TYPE": "BANK_STATEMENT_LINE",
                    "CONFIRMATION_URN": "urn:fin:artifact:statement:bank-alior:wyciag_2026_06",
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


def test_financial_dossier_schema_rejects_missing_case_urn():
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
                # Missing CASE_URN!
                "DOSSIER_STATUS": "MATCHED_EXACT",
                "SOURCE_NODE": {
                    "CHANNEL": "PORTAL_SAAS_VENDOR",
                    "SOURCE_URN": "urn:fin:source:portal:www-ovhcloud-com"
                },
                "DOCUMENT_NODE": {"DOCUMENT_PRESENCE": "DOCUMENT_PRESENT"},
                "TRANSACTION_NODE": {"PAYMENT_STATE": "PAYMENT_SETTLED", "PAYMENT_METHOD": "CARD_ONLINE_ECOMMERCE"},
                "CONFIRMATION_NODE": {"CONFIRMATION_TYPE": "BANK_STATEMENT_LINE"},
                "DISCREPANCY_ANALYSIS": {}
            }
        ]
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_dossier, schema=schema)


def test_financial_dossier_schema_rejects_invalid_urn_format():
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
                "CASE_URN": "not-a-valid-urn",  # Invalid URN format!
                "DOSSIER_STATUS": "MATCHED_EXACT",
                "SOURCE_NODE": {
                    "CHANNEL": "PORTAL_SAAS_VENDOR",
                    "SOURCE_URN": "urn:fin:source:portal:www-ovhcloud-com"
                },
                "DOCUMENT_NODE": {"DOCUMENT_PRESENCE": "DOCUMENT_PRESENT"},
                "TRANSACTION_NODE": {"PAYMENT_STATE": "PAYMENT_SETTLED", "PAYMENT_METHOD": "CARD_ONLINE_ECOMMERCE"},
                "CONFIRMATION_NODE": {"CONFIRMATION_TYPE": "BANK_STATEMENT_LINE"},
                "DISCREPANCY_ANALYSIS": {}
            }
        ]
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_dossier, schema=schema)


def test_financial_source_schema_with_urns():
    schema_path = SCHEMA_DIR / "financial-source.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    valid_source = {
        "SCHEMA": "wellmanifest.faktury.source/v1",
        "SOURCE_ID": "paypal-firmowy",
        "SOURCE_URN": "urn:fin:source:paypal:paypal-firmowy",
        "SOURCE_CHANNEL_TYPE": "WALLET_PAYPAL",
        "CATEGORY": "TRANSACTION_CHANNELS",
        "NAME": "PayPal Konto Firmowe",
        "MONTH": "2026.06",
        "BASE_CURRENCY": "PLN",
        "SUPPORTED_CURRENCIES": ["PLN", "EUR", "USD"],
        "DATA_FILES": [
            {
                "FILE_NAME": "transactions_2026_06.csv",
                "FILE_URN": "urn:fin:artifact:csv:transactions_2026_06",
                "FILE_FORMAT": "PAYPAL_CSV_EXPORT"
            }
        ],
        "INGESTION_STATUS": "STATUS_OK",
        "REQUIRES_MANUAL_ATTENTION": False
    }

    jsonschema.validate(instance=valid_source, schema=schema)
