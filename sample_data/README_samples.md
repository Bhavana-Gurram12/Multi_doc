# Sample Test Documents

This folder contains sample documents to test the Multi-Format Document Parser:

## Test Files

1. **invoice_sample.txt** - Invoice with structured billing data
   - Tests: Contact extraction, financial data, dates
   - Expected: High confidence with rule-based parsing

2. **email_sample.txt** - Business email with metrics
   - Tests: Email parsing, contact info, structured data
   - Expected: Good pattern recognition

3. **report_sample.html** - HTML sales report
   - Tests: HTML parsing, table data extraction
   - Expected: Clean structured output

4. **contract_sample.txt** - Service agreement
   - Tests: Complex document structure, multiple parties
   - Expected: May trigger AI fallback for complex extraction

## Testing Strategy

1. **Upload all files** to test multi-format processing
2. **Try with/without Gemini API key** to see rule vs AI processing
3. **Use sender names** like "TechCorp" or "ABC Company" to test pattern learning
4. **Re-upload same files** to verify pattern recognition and cost savings

## Expected Behavior

- First upload: May use AI for complex documents
- Second upload: Should use learned rules (faster, cheaper)
- Different senders: Should learn separate patterns
- Cost should decrease with pattern learning