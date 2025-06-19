# Bill Analyzer - Bill Summarizer Module

## Project Overview
This module creates concise, accessible summaries of complex government legislation using advanced NLP techniques.

## Development Guidelines
- Use Python 3.11+
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Include type hints for all functions
- Create unit tests for all summarization functions

## Key Components to Build
1. Bill text preprocessor (clean legal formatting)
2. Section identifier (titles, subsections, amendments)
3. Key provision extractor (funding, policy changes, timelines)
4. Multi-level summarizer (1-sentence, paragraph, detailed)
5. Readability optimizer (convert legal jargon to plain English)

## Libraries in Use
- transformers: For BERT/T5 based summarization
- spacy: For legal document structure analysis
- sumy: For extractive summarization
- textstat: For readability analysis

## Summarization Requirements
- 3 summary levels: Executive (1 sentence), Standard (1 paragraph), Detailed (3-5 paragraphs)
- Extract key numbers (dollar amounts, dates, percentages)
- Identify affected parties (citizens, businesses, government agencies)
- Highlight controversial or significant provisions
- Convert legal language to accessible English

## Testing Strategy
- Use real bills from different policy areas
- Test on various bill lengths (5 pages to 500+ pages)
- Validate summary accuracy against manual summaries
- Measure readability improvements

## Code Style
- Use descriptive variable names
- Maximum line length: 88 characters
- Use dataclasses for structured data
- Implement proper error handling for malformed bills
