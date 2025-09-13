import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.parsers.document_parser import DocumentParser
    print("[OK] DocumentParser imported successfully")
    
    parser = DocumentParser()
    print("[OK] DocumentParser created successfully")
    
    # Test with sample file
    test_file = "sample_data/invoice_sample.txt"
    if os.path.exists(test_file):
        content, metadata, doc_type = parser.parse_document(test_file)
        print(f"[OK] Parsed {doc_type}: {len(content)} characters")
        print(f"[OK] Title: {content[:50]}...")
    else:
        print("[ERROR] Sample file not found")
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()