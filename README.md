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


