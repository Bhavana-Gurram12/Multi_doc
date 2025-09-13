import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.main_processor import MainProcessor
    print("[OK] MainProcessor imported successfully")
    
    processor = MainProcessor()
    print("[OK] MainProcessor created successfully")
    
    # Test with sample file
    test_file = "sample_data/invoice_sample.txt"
    if os.path.exists(test_file):
        document, log = processor.process_document(test_file)
        print(f"[OK] Processed document: {document.title}")
        print(f"[OK] Confidence: {document.confidence_score}")
        print(f"[OK] Method: {document.processing_method}")
        print(f"[OK] Steps: {len(log.steps)}")
    else:
        print("[ERROR] Sample file not found")
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()