# pcgs-api

Python client for the [PCGS Public API](https://www.pcgs.com/publicapi).

## Installation

```bash
pip install pcgs-api
```

Requires Python 3.12+.

## Authentication

All requests are authenticated with a Bearer token. Generate an API key at
[pcgs.com/publicapi/documentation](https://www.pcgs.com/publicapi/documentation)
(requires a free PCGS account).

The client reads the key from the `PCGS_ACCESS_TOKEN` environment variable by
default. A `.env` file is a convenient place to store it during development:

```bash
# .env
PCGS_ACCESS_TOKEN=your_key_here
```

Or pass it directly:

```python
from pcgs_api import PCGSClient

client = PCGSClient(api_key="your_key_here")
```

## Quick start

Plain method names are synchronous and work in any Python script:

```python
from pcgs_api import PCGSClient

client = PCGSClient()
coin = client.get_coin_facts_by_cert_no("38109793", retrieve_all_data=True)
print(coin.name, coin.grade, coin.price_guide_value)
print(f"{client.remaining_calls_today} calls remaining")
```

For async codebases, append `_async` to any method name:

```python
import asyncio
from pcgs_api import PCGSClient

async def main():
    async with PCGSClient() as client:
        coin = client.get_coin_facts_by_cert_no("38109793", retrieve_all_data=True)
        print(coin.name, coin.grade, coin.price_guide_value)

asyncio.run(main())
```

## Rate limiting

Free-tier accounts are limited to **1,000 requests per day**. The client
tracks usage automatically and raises `RateLimitExceeded` before making a call
that would exceed the limit. For higher limits, contact
[dealer@pcgs.com](mailto:dealer@pcgs.com).

```python
from pcgs_api import PCGSClient, RateLimitExceeded

client = PCGSClient(daily_limit=1_000)
print(client.calls_this_session)    # calls since instantiation
print(client.calls_today)           # calls today (resets at midnight)
print(client.remaining_calls_today)

try:
    coin = client.get_coin_facts_by_cert_no("38109793")
except RateLimitExceeded as e:
    print(e)  # includes the date the limit resets
```

The `daily_limit` parameter can be raised if you have a commercial licence:

```python
client = PCGSClient(daily_limit=10_000)
```

## Sync vs async

Every endpoint method is available in two forms:

| Form | Example | When to use |
|---|---|---|
| Plain name | `client.get_coin_facts_by_cert_no(...)` | Scripts, notebooks, simple tools |
| `_async` suffix | `await client.get_coin_facts_by_cert_no_async(...)` | Async applications, frameworks |

Both forms share the same rate-limit counters and call tracking.

For async usage, the `async with PCGSClient() as client:` context manager
reuses a single connection pool across calls. Sync calls open and close a
connection per request automatically — no lifecycle management needed.

---

## Endpoints

### Coin detail

#### `get_coin_facts_by_cert_no(cert_no, retrieve_all_data=False)`

Look up a certified coin by its 7–8 digit certificate number.

```python
# Basic lookup
coin = client.get_coin_facts_by_cert_no("38109793")

# Full data: includes images, auction prices realized, and population
coin = client.get_coin_facts_by_cert_no("38109793", retrieve_all_data=True)

print(coin.name)             # "1966 25C SMS"
print(coin.grade)            # "SP66"
print(coin.price_guide_value)# 16.0
print(coin.population)       # 1224
print(coin.pop_higher)       # 1662
print(coin.has_true_view_image)  # True

for img in coin.images or []:
    print(img.thumbnail, img.fullsize)
```

Returns a `CoinFacts` object. When `retrieve_all_data=False` (the default),
`images`, `auction_list`, and population fields may be absent.

> **Note:** Certificate numbers are the 7–8 digit numbers printed on the
> PCGS holder. They are distinct from PCGS specification numbers.

#### `get_coin_facts_by_grade(pcgs_no, grade_no, plus_grade=False)`

Look up coin facts by PCGS specification number and numeric grade.

```python
coin = client.get_coin_facts_by_grade("2986", grade_no=65)

print(coin.name)    # "1977 1C, RD"
print(coin.mintage) # "4469930000"
```

> **Note:** This endpoint does not return pricing or auction data. Use
> `get_coin_facts_by_cert_no(..., retrieve_all_data=True)` for that.

#### `get_coin_facts_by_barcode(barcode, grading_service)`

Look up a coin using the barcode on the holder. `grading_service` must be
`"PCGS"` or `"NGC"`.

```python
coin = client.get_coin_facts_by_barcode("123456789012", "PCGS")
```

#### `get_apr_by_cert_no(cert_no)`

Fetch the auction price history for a specific certified coin.

```python
result = client.get_apr_by_cert_no("49771606")

print(result.name)   # "1934 5C"
print(result.grade)  # "MS65"

for auction in result.auctions or []:
    print(auction.date, auction.auctioneer, auction.price)
    # "08-2024", "Stack's Bowers", 145.0
```

#### `get_apr_by_grade(pcgs_no, grade_no, plus_grade=False, start_date=None, end_date=None, number_of_records=100)`

Fetch auction price history across all coins of a given type and grade.
Dates use `mm-dd-yyyy` format.

```python
result = client.get_apr_by_grade(
    "3972",
    grade_no=65,
    start_date="01-01-2024",
    end_date="12-31-2024",
    number_of_records=10,
)

for auction in result.auctions or []:
    print(auction.sale_name, auction.price)
```

#### `get_apr_by_barcode(barcode, grading_service, start_date=None, end_date=None)`

Fetch auction price history using a holder barcode.

```python
result = client.get_apr_by_barcode("123456789012", "PCGS")
```

#### `get_coin_images_by_cert_no(cert_no)`

Fetch all available image URLs for a certified coin.

```python
result = client.get_coin_images_by_cert_no("38109793")

print(result.has_true_view_image)  # True
for img in result.images or []:
    print(img.url, img.resolution, img.description)
    # "https://...jpg", "6000x3000", "Max"
```

---

### Banknote detail

#### `get_banknote_by_cert_no(cert_no, language_code=None)`

Fetch banknote certification details by certificate number.

```python
result = client.get_banknote_by_cert_no("12345678")

if result.is_valid_request and result.banknote:
    note = result.banknote
    print(note.year, note.denomination, note.grade)
```

#### `get_banknote_by_grade(pcgs_no, grade_no)`

Fetch banknote records by PCGS specification number and grade.

```python
result = client.get_banknote_by_grade("123456", grade_no=65)

for note in result.banknotes or []:
    print(note.cert_no, note.grade)
```

#### `get_banknote_images_by_cert_no(cert_no)`

Fetch images for a certified banknote.

```python
result = client.get_banknote_images_by_cert_no("12345678")

print(result.has_obverse_image, result.has_reverse_image)
for img in result.images:
    print(img.url)
```

---

### Orders

Order endpoints only return orders associated with the account that owns the
API key.

#### `get_orders_by_submission_no(submission_no)`

```python
result = client.get_orders_by_submission_no("1234567")

for order in result.orders or []:
    print(order.submission_no, order.order_status, order.item_count)
    for line in order.order_lines or []:
        print(line.cert_no, line.display_grade)
```

#### `get_orders_by_date_range(start_date, end_date, page_no=1, page_size=10)`

Dates use `mm-dd-yyyy` format. Results are paginated.

```python
result = client.get_orders_by_date_range(
    start_date="01-01-2025",
    end_date="03-31-2025",
    page_no=1,
    page_size=25,
)

for order in result.orders or []:
    print(order.order_no, order.date_received, order.order_status)
```

---

## Response models

All responses are [Pydantic v2](https://docs.pydantic.dev/) models. Fields
use `snake_case` in Python, mirroring the `PascalCase` keys in the JSON
response. Every response includes:

| Field | Type | Description |
|---|---|---|
| `is_valid_request` | `bool` | `True` if the request was understood |
| `server_message` | `str` | Status or error message from the API |

When `is_valid_request` is `True` but no matching record exists, the API
returns `"No data found"` in `server_message` and `None` (or an empty list)
for the data fields.

### Key models

| Model | Used by |
|---|---|
| `CoinFacts` | All `get_coin_facts_*` methods |
| `AuctionResponse` | `get_apr_by_cert_no` |
| `AuctionListResponse` | `get_apr_by_grade`, `get_apr_by_barcode` |
| `CoinImagesResponse` | `get_coin_images_by_cert_no` |
| `BanknoteResponse` | `get_banknote_by_cert_no` |
| `BanknotesResponse` | `get_banknote_by_grade` |
| `BanknoteImagesResponse` | `get_banknote_images_by_cert_no` |
| `OrdersResponse` | Both order methods |

All models are importable from `pcgs_api.schema`:

```python
from pcgs_api.schema import CoinFacts, AuctionItem, OrderDetail
```
