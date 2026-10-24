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
The first run creates `pagecheck.db` in the project directory. No configuration is
needed; set `DATABASE_URL` to point at another database.

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

**Check state lives in a database, not in the process.** `POST /checks` answers
immediately and the background task writes the outcome later, so the two halves need
somewhere they can both see. A dict in the process works until the process restarts —
and it stops working entirely the moment the service runs more than one instance,
because each one would only know about its own checks. The database is that shared
place, and the application now keeps no state of its own between requests.

## Tests

```bash
pytest
```

30 tests cover the three modules separately: `analyzer` 12, `main` 13, `fetcher` 5. CI runs them on every push and
pull request, plus weekly on a schedule to catch dependency drift.

## Not yet

- Results now persist in a database, but the hosted instance keeps its SQLite file on an
  ephemeral filesystem: the free tier spins down after 15 minutes idle and wipes it. A
  hosted Postgres is the next step.
- No limit on concurrent checks.
- No LLM-based scoring of page content.
