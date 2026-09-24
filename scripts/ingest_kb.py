"""Upload fixtures/kb/*.md chunks to Azure AI Search (idempotent). Run via `make index`."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.adapters.search.chunking import load_kb


def main() -> int:
    endpoint, key = os.getenv("AZURE_SEARCH_ENDPOINT"), os.getenv("AZURE_SEARCH_KEY")
    if not endpoint or not key:
        print(
            "AZURE_SEARCH_ENDPOINT / AZURE_SEARCH_KEY not set (see P1-09); nothing to index"
        )
        return 0
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchableField,
        SearchIndex,
        SimpleField,
    )

    name = os.getenv("AZURE_SEARCH_INDEX", "navigator-kb")
    cred = AzureKeyCredential(key)
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        # ponytail: en analyzer for all; per-language analyzer needs two fields or two indexes
        SearchableField(name="content", analyzer_name="en.microsoft"),
        SearchableField(name="title"),
        SimpleField(name="url", type="Edm.String"),
        SimpleField(name="agency", type="Edm.String"),
        SimpleField(name="lang", type="Edm.String", filterable=True),
        SimpleField(name="topic", type="Edm.String", filterable=True),
        SimpleField(name="fetched_at", type="Edm.String"),
    ]
    SearchIndexClient(endpoint, cred).create_or_update_index(
        SearchIndex(name=name, fields=fields)
    )
    chunks = load_kb()
    SearchClient(endpoint, name, cred).upload_documents(chunks)  # upload = upsert by id
    print(f"indexed {len(chunks)} chunks into {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
