# Bill Analyzer - Comparison Engine

## Project Overview
This is a political fact-checking tool that compares media statements to actual bill content using NLP.

## Development Guidelines
- Use Python 3.11+
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Include type hints for all functions
- Create unit tests for all comparison functions

## Key Components to Build
1. Bill text preprocessor
2. Statement claim extractor
3. Semantic similarity engine
4. Accuracy scoring algorithm
5. Bias detection system

## Libraries in Use
- transformers: For BERT-based text analysis
- sentence-transformers: For semantic similarity
- spacy: For NLP preprocessing
- scikit-learn: For ML classification

## Testing Strategy
- Use pytest for unit testing
- Create mock bill/statement data
- Test edge cases (short statements, legal jargon)

## Code Style
- Use descriptive variable names
- Maximum line length: 88 characters
- Use dataclasses for structured data
- Implement proper error handling
