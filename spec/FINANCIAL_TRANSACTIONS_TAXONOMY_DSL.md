# Financial Transactions and Invoice Taxonomy DSL Profile
## wellmanifest.faktury.nl-uri-dsl-llm / v1

- **Standard**: `wellmanifest/nl-uri-dsl-llm`
- **Specification ID**: `financial-dsl-v1`
- **Profile Status**: `normative-profile`
- **Applicable Domains**: `faktury`, `fin`, `banking`, `ksef`, `accounting`, `reconciliation`

---

## 1. Wprowadzenie i Ramy Architektoniczne

Niniejsza specyfikacja rozszerza standard **`wellmanifest/nl-uri-dsl-llm`** o dziedzinę finansowo-księgową, audyt operacji gospodarczych oraz pojednanie wieloźródłowe (Multi-Source Financial Reconciliation).

W środowiskach autonomicznych agentów AI i modeli LLM swobodne, naturalnojęzykowe opisy transakcji i statusów prowadzą do dryfu semantycznego, halucynacji kwot i pomijania istotnych zdarzeń podatkowych. Niniejszy profil narzuca deterministyczny, oparty o wielkie litery (**DSL CAPITALIZE**) słownik tokenów sterujących, jednoznaczną adresację RFC 3986 URI/URN dla każdego dowodu księgowego oraz schemat 5-węzłowej Teczki Sprawy (**Dossier Evidence Envelope**).

---

## 2. Normatywne Reguły Jakości (NUL-010 .. NUL-013)

### NUL-010 (Financial DSL Capitalize Token Determinism)
Wszystkie statusy spraw (`DOSSIER_STATUS`), typy źródeł (`SOURCE_CHANNEL_TYPE`), metody płatności (`PAYMENT_METHOD`), kategorie kosztów i przychodów oraz zdarzenia logowania (`LOG_EVENT`) **MUSZĄ** być zapisywane jako tokeny `SCREAMING_SNAKE_CASE` (DSL CAPITALIZE).
Zabrania się stosowania w polach sterujących wartości o zmiennej wielkości liter, spacji lub znaków diakrytycznych. Zapewnia to natychmiastową walidację mikroskalową (regex `^[A-Z0-9_]+$`) oraz odporność na halucynacje LLM.

### NUL-011 (Dossier Evidence Envelope RFC 3986 Addressing)
Każde zdarzenie gospodarcze oraz każde źródło danych musi być jednoznacznie adresowalne za pomocą Action URI lub Resource URN:
- **Operation URI**: `faktury://reconcile/EXECUTE.MATCH?month=YYYY.MM`
- **Dossier URN**: `urn:fin:dossier:YYYY_MM_ID`
- **Source URN**: `urn:fin:source:CHANNEL_ID`
- **Document URN**: `urn:fin:doc:INVOICE_HASH`

### NUL-012 (Internal Transfer vs Tax Event Demarcation)
Algorytm pojednania oraz model LLM **MUSZĄ** bezwzględnie rozróżniać transfery między rachunkami własnymi (`MATCHED_INTERNAL_TRANSFER`, np. zasilenie konta PayPal z rachunku bankowego lub wypłata z PayU) od operacji przychodowo-kosztowych.
Transfery wewnętrzne pod rygorem błędu walidacji nie mogą zwiększać obrotu ani kosztów uzyskania przychodów (KUP).

### NUL-013 (Payment Gateway Fee Auto-Splitting)
Wpływy i wypływy realizowane za pośrednictwem procesorów płatności (PayPal, Stripe, PayU, Przelewy24), w których operator potrąca prowizję u źródła (`Fee`), **MUSZĄ** być automatycznie rozbijane w teczce sprawy na:
1. Kwotę brutto należności (pokrywającą fakturę lub zamówienie).
2. Odrębny koszt prowizji operacyjnej (`FEE_AMOUNT` zakwalifikowany do `BANK_FEE_COMMISSION`).
Status teczki w takim przypadku przyjmuje wartość `MATCHED_FEE_SPLIT`.

---

## 3. Zunifikowana Taksonomia Kanałów Źródłowych

Struktura katalogowa w systemie plików danego okresu obrachunkowego `[YYYY.MM]/` przyjmuje format:

| Prefiks katalogu | Typ kanału (`SOURCE_CHANNEL_TYPE`) | Typowe formaty plików | Rola w obiegu |
| :--- | :--- | :--- | :--- |
| `bank-[ID]/` | `BANK_ACCOUNT_TRADITIONAL` | `.csv`, `.xlsx`, `.xml`, `.mt940`, `.pdf`, `.p7s` | Wyciągi i potwierdzenia bankowe |
| `paypal-[ID]/` | `WALLET_PAYPAL` | `.csv`, `.pdf` | Historia portfela PayPal i prowizje |
| `stripe-[ID]/` | `GATEWAY_STRIPE` | `.csv` | Raporty balance transactions i wypłaty |
| `revolut-[ID]/` | `MULTICURRENCY_REVOLUT` | `.csv`, `.xlsx` | Transakcje wielowalutowe |
| `bramka-[ID]/` | `PAYMENT_GATEWAY_AGGREGATOR`| `.csv`, `.xlsx` | Zestawienia wpłat PayU / P24 / Tpay |
| `karta-[ID]/` | `CORPORATE_CARD` | `.csv`, `.pdf` | Transakcje kartą fizyczną / wirtualną |
| `ksef-[ID]/` | `GOV_KSEF_GATEWAY` | `.pdf`, `.xml`, `.upo.xml` | Faktury ustrukturyzowane KSeF / wFirma |
| `allegro-[ID]/`| `MARKETPLACE_ALLEGRO` | `.json`, `.csv`, `.pdf` | Zamówienia B2B i faktury Allegro |
| `www-[DOMENA]/`| `PORTAL_SAAS_VENDOR` | `.pdf`, `source.yaml` | Pobrane faktury z portali (OVH, Google) |
| `emaile/` | `EMAIL_IMAP_STORE` | `.eml`, `.txt`, `.html`, `.json`, `.pdf` | Wyczyszczone foldery e-maili |
| `koszty/` | `LOCAL_COST_STORE` | `.pdf`, `.xml` | Tradycyjne faktury zakupowe |
| `przychody/` | `LOCAL_REVENUE_STORE` | `.pdf`, `.xml` | Faktury sprzedaży własnej |

---

## 4. Schemat 5-Węzłowej Teczki Sprawy (`DOSSIER_NODE`)

Każdy przypadek pojednania w pliku `dossier.yaml` składa się z 5 ustrukturyzowanych węzłów:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      DOSSIER ENVELOPE (CASE_ID)                        │
├─────────────────┬─────────────────┬──────────────────┬─────────────────┤
│  SOURCE_NODE    │  DOCUMENT_NODE  │ TRANSACTION_NODE │CONFIRMATION_NODE│
│  Kanał źródłowy │  Faktura / Plik │ Operacja w Banku │ Dowód / Wyciąg  │
├─────────────────┴─────────────────┴──────────────────┴─────────────────┤
│                          DISCREPANCY_ANALYSIS                          │
│          Analiza przesunięć (weekendy), różnic walut i notatka LLM     │
└────────────────────────────────────────────────────────────────────────┘
```

1. **`SOURCE_NODE`**: Informacja o pochodzeniu powiadomienia (e-mail, portal www, KSeF, Allegro).
2. **`DOCUMENT_NODE`**: Metadane faktury (numer, kwota brutto, waluta, data wystawienia, ścieżka do pliku).
3. **`TRANSACTION_NODE`**: Dane operacji pieniężnej (data operacji, data księgowania, kwota, metoda płatności, konto).
4. **`CONFIRMATION_NODE`**: Źródło dowodowe transakcji (linia w wyciągu CSV, plik PDF potwierdzenia przelewu, podpis S/MIME).
5. **`DISCREPANCY_ANALYSIS`**: Wyliczone różnice dni kalendarzowych i roboczych (lag), spread walutowy, automatyczna notatka analityczna LLM oraz wymagana akcja.

---

## 5. Tokeny Stanów i Metod: DSL CAPITALIZE

### 5.1. Statusy Sprawy (`DOSSIER_STATUS`)
- `MATCHED_EXACT`: Kwota, termin i kontrahent w 100% zgodne.
- `MATCHED_FX_NBP`: Kwota w walucie przeliczona kursem NBP z dnia $D-1$.
- `MATCHED_FEE_SPLIT`: Kwota dopasowana po skompensowaniu prowizji bramki.
- `MATCHED_INTERNAL_TRANSFER`: Transfer między własnymi rachunkami.
- `PENDING_PORTAL_DOWNLOAD`: Brak pliku PDF faktury – oczekuje w portalu lub KSeF.
- `UNMATCHED_BANK_OUTFLOW`: Wydatek z konta bez powiązanego dokumentu.
- `UNMATCHED_BANK_INFLOW`: Wpływ na konto bez faktury sprzedaży.
- `UNPAID_INVOICE`: Faktura bez odpowiadającego wypływu z konta firmowego.
- `AMOUNT_DISCREPANCY`: Rozbieżność kwoty przekraczająca tolerancję.

### 5.2. Metody Płatności (`PAYMENT_METHOD`)
- `BANK_TRANSFER_STANDARD`
- `BANK_TRANSFER_EXPRESS`
- `CARD_ONLINE_ECOMMERCE`
- `CARD_TERMINAL_POS`
- `PAYPAL_EXPRESS_CHECKOUT`
- `STRIPE_PAYMENT_INTENT`
- `BLIK_MOBILE_CODE`
- `DIRECT_DEBIT_SEPA`
- `ATM_CASH_WITHDRAWAL`
- `BANK_FEE_COMMISSION`
