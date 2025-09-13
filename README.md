# Multi-Format Document Parser

A hybrid document processing system that produces normalized JSON from various document formats while minimizing AI costs through intelligent rule learning.

## Architecture

**Hybrid Pipeline Approach:**
1. **Document Ingestion** - Multi-format parsing (PDF, DOCX, HTML, TXT)
2. **Signature Learning** - Pattern recognition and rule extraction
3. **Rule-Based Processing** - Fast, cost-effective parsing
4. **AI Fallback** - Gemini 1.5 Flash for outliers only
5. **JSON Normalization** - Consistent output schema

## Key Features

✅ **Normalized Output** - Single JSON schema for all document types
✅ **Cost Optimization** - Rule-based processing, AI only for outliers
✅ **Layout Learning** - Learns patterns per sender/globally with versioning
✅ **Interpretability** - Human-readable processing logs
✅ **Streamlit Interface** - Complete web app with all required features

## Quick Start

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run Application:**
```bash
streamlit run app.py
```

3. **Upload Documents:**
   - Support: PDF, DOCX, HTML, TXT
   - Optional: Add Gemini API key for AI processing
   - Optional: Specify sender for pattern learning

## Project Structure

```
Multi_doc/
├── app.py                          # Streamlit interface
├── requirements.txt                # Dependencies
├── config/
│   └── schema.py                   # JSON schema definitions
├── src/
│   ├── main_processor.py           # Main processing pipeline
│   ├── parsers/
│   │   └── document_parser.py      # Multi-format parsing
│   ├── rules/
│   │   └── signature_engine.py     # Pattern learning engine
│   ├── utils/
│   │   └── rule_processor.py       # Rule-based extraction
│   └── ai/
│       └── gemini_processor.py     # AI fallback processor
├── data/                           # Processed data storage
└── logs/                           # Processing logs
```

## Cost Optimization Strategy

- **Rule-Based First:** Uses learned patterns for fast processing
- **AI Sparingly:** Only for low confidence or new patterns
- **Pattern Learning:** Automatically learns from successful AI extractions
- **Sender-Specific Rules:** Handles per-sender document quirks
- **Versioning:** Maintains rule stability across updates

## Usage

1. Upload multiple documents of any supported format
2. System automatically detects format and applies appropriate parser
3. Uses existing rules if document signature is recognized
4. Falls back to AI only if confidence is low or pattern is new
5. Learns new patterns from successful AI extractions
6. Provides normalized JSON output with processing logs