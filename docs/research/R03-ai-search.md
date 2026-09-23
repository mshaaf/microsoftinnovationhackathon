# R03: Azure AI Search

Checked 2026-09-23.

## Answer
- **Tier: Free.** 50 MB, 3 indexes, one per subscription, no expiry. It's plenty for about 40 markdown pages. Limits: no semantic ranker (except in a few regions), no managed identity, so use the **query key** from the backend.
- **Skip vectors.** BM25 keyword search over short, curated FAQ chunks is enough and removes the embedding model, the integrated-vectorization skillset, and a second deployment. Upgrade path: add a vector field plus integrated vectorization if eval citation relevance falls short.
- **Index schema** (`navigator-kb`):
  `id` (key), `content` (searchable, analyzer `en.microsoft` or `es.microsoft` by lang), `title` (searchable), `url`, `agency`, `lang` (filterable), `topic` (filterable), `fetched_at`.
- **Chunking:** split each curated markdown file on `##` headings, and cap chunks at about 1,200 characters. Every chunk keeps its page's `url` and `title` so every hit is citable.
- Python: `azure-search-documents`. `SearchIndexClient.create_or_update_index(...)` makes the upload idempotent, then `SearchClient.upload_documents(...)`.

**Important:** see R15. fema.gov blocks scripted fetches (HTTP 403). The index is built from our curated `fixtures/kb/*.md` files, so the **mock and live searches use the same content**.

## Evidence
- https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity
- https://learn.microsoft.com/en-us/azure/search/search-try-for-free
- https://learn.microsoft.com/en-us/azure/search/semantic-search-overview

## Env
`AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY` (query key at runtime; admin key only for `make index`), `AZURE_SEARCH_INDEX=navigator-kb`.
