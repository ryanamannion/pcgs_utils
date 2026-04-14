# collectorsuniverse.com SpecSearch API

Reverse-engineered internal AJAX search endpoint used by the PCGS/PSA autocomplete
search on `www.collectorsuniverse.com`. No API key required — just browser-like headers.

## Base URL

```
https://www.collectorsuniverse.com/SpecSearch/Search/{company}
```

## Supported Companies

| `{company}` | Description |
|-------------|-------------|
| `PCGS` | US coins (Professional Coin Grading Service) |
| `PSA` | Sports cards / trading cards (Professional Sports Authenticator) |

Other values tested (NGC, BGS, SGC, PMG, CSG) return 404.

## Required Headers

The server returns **403** without these:

```
User-Agent: Mozilla/5.0 ...
X-Requested-With: XMLHttpRequest
Referer: https://www.collectorsuniverse.com/
```

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `term` | string | — | **Required.** Search term |
| `searchType` | string | — | Match mode (see below) |
| `maxresults` | int | 25 | Max results returned (25 when omitted) |
| `ancestorCategoryId` | int | — | Filter by category ID (e.g. `2` = Dollars) |
| `includeTypeCoins` | bool | `false` | Include type coins |
| `includeworld` | bool | `false` | Include world coins alongside US results |
| `worldOnly` | bool | `false` | Return only world coins (changes response schema) |
| `pricedgrades` | bool | `false` | Filter to coins with price guide grades |
| `priceguideonly` | bool | `false` | Only return coins in the price guide |
| `popOnly` | bool | `false` | Only population report coins |
| `includePopOnly` | bool | `false` | Include pop-only coins |
| `canReceive` | bool | `false` | Filter to coins PCGS can currently receive |
| `auctionpriceonly` | bool | `false` | Only coins with auction price history |
| `coinfactsActive` | bool | `false` | Only CoinFacts-linked coins |
| `pcgsCurrencyOnly` | bool | `false` | PCGS currency only |
| `callback` | string | — | JSONP wrapper function name (omit for plain JSON) |
| `_` | int | — | Cache-buster timestamp (any integer works) |

### `searchType` Values

| Value | Behavior |
|-------|----------|
| `LastTermWildCard` | Wildcard on the last word of `term` |
| `StartsWith` | Results start with `term` |
| `Contains` | Results contain `term` anywhere |
| `Exact` | Exact match |

## Response Schemas

### PCGS — US Coins (default)

```json
[
  {
    "specno": "7072",
    "description": "1878 8TF $1",
    "year": "1878",
    "mintmark": "1878 8TF",
    "category": "Dollars, Morgan Dollar",
    "denomination": "$1",
    "prefix": "MS",
    "holder": "...",
    "countryname": "The United States of America",
    "ancestorcategoryid": "2",
    "imageurl": "http://images.pcgs.com/...Preview.jpg",
    "hoverimageurl": "http://images.pcgs.com/...Hover.jpg",
    "score": "569.18%"
  }
]
```

### PCGS — World Coins (`worldOnly=true`)

Different field set returned when `worldOnly=true`:

```json
[
  {
    "specno": "...",
    "description": "...",
    "year": "...",
    "denomination": "...",
    "countryname": "...",
    "catalogno1": "...",
    "catalogno2": "...",
    "currvariety": "...",
    "bankname": "...",
    "score": "..."
  }
]
```

### PSA — Sports / Trading Cards

```json
[
  {
    "specno": "0105001180",
    "description": "1909-11 T206 UNKNOWN BACK HARRY DAVIS PHIL.",
    "year": "1909-11",
    "sport": "BASEBALL CARDS",
    "publisher": "UNKNOWN BACK",
    "category": "Sport, BASEBALL CARDS, 1909-11, UNKNOWN BACK, T206 UNKNOWN BACK",
    "score": "145.74%"
  }
]
```

## Notes

- Default result cap is **25**. Use `maxresults=N` to get fewer or more.
- The `specno` returned maps to the PCGS specification number, which can be
  used with the official `api.pcgs.com` endpoints (e.g. `GetCoinFactsByGrade`).
- The `_` cache-buster parameter must be present but its value is not validated
  (any integer works).
- No authentication or session cookies are required.
- Image URLs use `http://` (not `https://`) — upgrade manually if needed.

## Python Wrapper

See `packages/pcgs_api/src/pcgs_api/spec_search.py` for a typed client.

```python
from pcgs_api.spec_search import SpecSearchClient

client = SpecSearchClient()

# Search PCGS coins
results = client.search_pcgs("morgan", max_results=10)
for coin in results:
    print(coin.specno, coin.description, coin.category)

# Search PSA cards
cards = client.search_psa("babe ruth", max_results=5)
for card in cards:
    print(card.specno, card.description, card.sport)

# Filter to a specific category
dollars = client.search_pcgs("1921", ancestor_category_id=2)
```
