# US Bill Comparison Engine

This project provides tools for preprocessing and summarizing United States government bills. The `bill_preprocessor` module cleans raw legislative text and structures it into sections for further analysis.

## Preprocessor Features

- Remove headers, footers, and legal citations
- Identify sections and amendments
- Extract bill metadata
- Handle PDF, HTML, and plain text inputs

Run unit tests with:

```bash
pytest
```

## Summarizer Features

- Multi-level summaries: executive, standard, and detailed
- Extract key numbers and affected parties
- Provide readability score using Flesch-Kincaid grade level

## GovInfo API Client

Use ``GovInfoAPIClient`` to fetch bill data from the GovInfo service.

```python
from govinfo_client import GovInfoAPIClient

client = GovInfoAPIClient(api_key="YOUR_API_KEY")
bills = client.search_bills("infrastructure", congress=118)

for info in bills[:5]:
    document = client.get_bill_document(info["packageId"])
    print(document.metadata.bill_number)
```


