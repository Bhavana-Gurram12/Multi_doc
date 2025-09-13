# Multi-Format Document Parser - Technical Architecture

## Processing States

```mermaid
stateDiagram-v2
    [*] --> Uploaded
    Uploaded --> Parsing
    Parsing --> SignatureExtraction
    SignatureExtraction --> PatternMatching
    
    PatternMatching --> RuleBased: Pattern Found
    PatternMatching --> ConfidenceCheck: No Pattern
    
    ConfidenceCheck --> RuleBased: High Confidence
    ConfidenceCheck --> AIProcessing: Low Confidence
    
    RuleBased --> JSONGeneration
    AIProcessing --> PatternLearning
    PatternLearning --> JSONGeneration
    
    JSONGeneration --> LogGeneration
    LogGeneration --> Complete
    Complete --> [*]
```

## Key Technical Components

| Component | Technology | Function |
|-----------|------------|----------|
| **Frontend** | Streamlit | Web UI, File Upload, Results Display |
| **Parser Engine** | PyPDF2, python-docx, BeautifulSoup4 | Multi-format document parsing |
| **AI Engine** | Google Gemini 1.5 Flash | Complex document understanding |
| **Rule Engine** | Python Regex, Pattern Matching | Fast rule-based extraction |
| **Schema Validation** | Pydantic | Data model validation |
| **Storage** | JSON Files | Pattern persistence |
| **Orchestration** | Python Classes | Pipeline coordination |