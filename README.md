# PageCheck

![CI](https://github.com/spssspss0712/pagecheck/actions/workflows/ci.yml/badge.svg)

A small HTTP service that fetches a web page and reports basic on-page SEO
signals. Built to evaluate landing pages for small businesses and startups.

**Live API docs: https://pagecheck.onrender.com/docs** — try it in the browser.
(Hosted on a free tier; the first request may take ~50s to wake the service.)

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## API

### `POST /checks`

Submit a URL. The service returns `202 Accepted` with a check id straight away;
the page is fetched and analysed in the background. An invalid URL is rejected
with `422`.

```bash
curl -X POST http://127.0.0.1:8000/checks \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com"}'
```

```json
{
  "id": "3f2a...",
  "status": "queued",
  "url": "https://example.com/",
  "created_at": "2026-10-07T09:12:33.481Z"
}
```

### `GET /checks/{check_id}`

Poll for the result. An unknown `check_id` returns `404`.

When the check completes:

```json
{
  "id": "3f2a...",
  "status": "done",
  "url": "https://example.com/",
  "created_at": "2026-10-07T09:12:33.481Z",
  "result": {
    "has_title": true,
    "has_meta_description": false,
    "h1_count": 1
  }
}
```

When the fetch fails:

```json
{
  "id": "3f2a...",
  "status": "failed",
  "url": "https://example.com/",
  "created_at": "2026-10-07T09:12:33.481Z",
  "error": "..."
}
```

### `GET /health`

Liveness check. Returns `200` while the service is up.

## Checks performed

| Field | What it reports |
|---|---|
| `has_title` | A `<title>` exists and is not empty or whitespace |
| `has_meta_description` | A `<meta name="description">` exists with non-empty content |
| `h1_count` | Number of `<h1>` tags on the page |

## Design notes

**`POST /checks` returns immediately instead of waiting for the result.**
Fetching an arbitrary URL is an unpredictable network operation — it can take
seconds, or hang. Holding the request open would tie this API's response time
to a third party's server. The check is queued as a background task and the
client polls for the outcome.

**A failed fetch is a status, not an exception.** `run_check` catches
`FetchError` and records `status: "failed"` along with the message. A client
asking about a check always gets a well-formed answer about where that check
stands — "it failed, and here is why" is a result, not an API error.

**`analyze_page` is a pure function.** It takes an HTML string and returns a
dict; it performs no I/O. That is why the analyzer carries the largest test
suite of the three modules — every case is a string in and a dict out, with no
network and no mocking.

## Tests

```bash
pytest
```

25 tests cover the three modules separately: `analyzer` 12, `main` 8, `fetcher` 5. CI runs them on every push and
pull request, plus weekly on a schedule to catch dependency drift.

## Not yet

- Results are held in memory, so they are lost on restart.
- No limit on concurrent checks.
- No LLM-based scoring of page content.
