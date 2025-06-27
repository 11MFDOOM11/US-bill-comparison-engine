# US Bill Comparison Engine

This project provides tools for preprocessing United States government bills. The `bill_preprocessor` module cleans raw legislative text and structures it into sections for further analysis. Cleaned text can be sent directly to the OpenAI ChatGPT API for further processing.

## Preprocessor Features

- Remove headers, footers, and legal citations
- Identify sections and amendments
- Extract bill metadata
- Handle PDF, HTML, and plain text inputs
- Produce ChatGPT-ready text via ``prepare_document``

Run unit tests with:

```bash
pytest
```

## ChatGPT Integration

Cleaned bill text can be sent to OpenAI's ChatGPT API using the
``ChatGPTClient`` class.

```python
from pathlib import Path
from chatgpt_client import ChatGPTClient
from bill_preprocessor import BillPreprocessor

pre = BillPreprocessor()
doc = pre.preprocess(Path("example bill.txt").read_text())
clean_text = pre.prepare_document(doc)
client = ChatGPTClient(api_key="YOUR_OPENAI_KEY")
summary = client.complete(clean_text)
print(summary)
```

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


