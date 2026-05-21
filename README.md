# afin-nip-client

A Python client for looking up Polish company data by NIP (tax identification number) via the [AFIN](https://afin.net) API.

Returns structured data from GUS REGON, company name, address, administrative area, and entity classification.

---

## Features

- NIP validation (length + checksum) before any network call
- Typed, immutable dataclasses for all returned data
- Context manager support for automatic session cleanup
- Descriptive exceptions for every failure mode

## Requirements

- Python >= 3.14
- `requests`

## Installation

```bash
uv sync

# or alternatively with pip:
pip install requests
```

## Quick Start

```python
import json
from afin_nip_client.client import AfinClient

with AfinClient() as client:
    info = client.get("000-00-00-000")  # this obviously would fail, use your own NIP

print(json.dumps(info.to_dict()))
```

Output:

```json
{
  "regon": "000000000",
  "nip": "0000000000",
  "name": "MOJA FIRMA",
  "address": {
    "street": "ul. Ptasia 67",
    "building_number": "67",
    "postal_code": "00-000",
    "city": "Warszawa",
    "post_office": "6"
  },
  "area": {
    "voivodeship": "MAZOWIECKIE",
    "county": "Warszawa",
    "community": "Śródmieście"
  },
  "classification": { "entity_type_raw": "37", "silos_code_raw": "P" }
}
```

## API Reference

### `AfinClient(timeout=10.0)`

| Method          | Description                                                    |
| --------------- | -------------------------------------------------------------- |
| `get(nip)`      | Fetch company info. Accepts `str` or `int`, strips non-digits. |
| `validate(nip)` | Validate a cleaned 10-digit NIP string. Raises on failure.     |
| `close()`       | Close the underlying `requests.Session`.                       |

### `CompanyInfo`

| Field            | Type                   | Description                         |
| ---------------- | ---------------------- | ----------------------------------- |
| `nip`            | `str`                  | Tax ID (10 digits)                  |
| `regon`          | `str`                  | Statistical number                  |
| `name`           | `str`                  | Company name                        |
| `address`        | `Address`              | Street, building, postal code, city |
| `area`           | `AdministrativeArea`   | Voivodeship / county / community    |
| `classification` | `EntityClassification` | Entity type and SILOS code          |

`CompanyInfo.to_dict()` returns a plain `dict` suitable for JSON serialization.

### `EntityClassification`

| Property            | Type                 | Description                                   |
| ------------------- | -------------------- | --------------------------------------------- |
| `entity_type`       | `EntityType \| None` | `P` legal, `F` natural, `LP`/`LF` local units |
| `silos`             | `SilosKind \| None`  | CEIDG, agricultural, other, etc.              |
| `is_legal_entity`   | `bool`               | `True` for `P` / `LP`                         |
| `is_natural_person` | `bool`               | `True` for `F` / `LF`                         |

## Exceptions

| Exception          | Raised when                      |
| ------------------ | -------------------------------- |
| `NipLengthError`   | NIP is not 10 digits             |
| `NipChecksumError` | NIP fails checksum validation    |
| `InvalidNipError`  | API reports NIP as unknown       |
| `EmptyResponse`    | API returned an empty body       |
| `InvalidResponse`  | API response could not be parsed |
| `AfinApiError`     | Network or HTTP error            |

All except `NipLengthError` / `NipChecksumError` inherit from `AfinError`.
