import os
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
from config.schema import DocumentSchema, ProcessingLog
from src.parsers.document_parser import DocumentParser
from src.rules.signature_engine import SignatureEngine
from src.utils.rule_processor import RuleProcessor
from src.ai.gemini_processor import GeminiProcessor

class MainProcessor:
    """Main document processing pipeline"""
    
    def __init__(self, gemini_api_key: str = None):
        self.parser = DocumentParser()
        self.signature_engine = SignatureEngine()
        self.rule_processor = RuleProcessor()
        self.ai_processor = GeminiProcessor(gemini_api_key) if gemini_api_key else None
        
        # Load existing signatures
        self.signature_engine.load_signatures('data/signatures.json')
    
    def process_document(self, file_path: str, sender: str = None) -> Tuple[DocumentSchema, ProcessingLog]:
        """Process single document through hybrid pipeline"""
        start_time = time.time()
        doc_id = str(uuid.uuid4())
        
        log = ProcessingLog(document_id=doc_id)
        log.steps.append("Started processing")
        
        # Step 1: Parse document
        content, metadata, doc_type = self.parser.parse_document(file_path)
        log.steps.append(f"Parsed {doc_type} document")
        
        # Step 2: Extract signature
        signature = self.signature_engine.extract_signature(content, metadata)
        log.steps.append(f"Extracted signature: {signature}")
        
        # Step 3: Try rule-based extraction
        existing_rules = self.signature_engine.get_rules(signature, sender)
        if existing_rules:
            extracted_fields, confidence = self.rule_processor.apply_rules(content, existing_rules)
            log.rules_applied.append(f"Applied existing rules for signature {signature}")
            processing_method = "rule_based"
        else:
            extracted_fields, confidence = self.rule_processor.apply_rules(content)
            log.rules_applied.append("Applied default rules")
            processing_method = "rule_based"
        
        # Step 4: AI fallback if needed
        ai_cost = 0.0
        if self.ai_processor and (confidence < 0.7 or not existing_rules):
            log.steps.append("Using AI for low confidence document")
            ai_result = self.ai_processor.extract_structured_data(content, doc_type)
            
            if 'extracted_data' in ai_result and not ai_result['extracted_data'].get('error'):
                extracted_fields.update(ai_result['extracted_data'])
                confidence = max(confidence, ai_result['extracted_data'].get('confidence', 0.5))
                processing_method = "ai_assisted"
                log.ai_usage = True
                ai_cost = ai_result.get('cost', 0.0)
                
                # Learn new pattern if AI was successful
                if confidence > 0.8:
                    self.signature_engine.learn_pattern(signature, extracted_fields, sender)
                    log.steps.append("Learned new pattern from AI extraction")
        
        # Step 5: Create normalized output
        basic_fields = self.rule_processor.extract_basic_fields(content)
        
        # Ensure title is a string
        title = extracted_fields.get('title') or basic_fields.get('title')
        if isinstance(title, list) and title:
            title = title[0]
        elif not isinstance(title, str):
            title = str(title) if title else None
            
        document = DocumentSchema(
            document_id=doc_id,
            title=title,
            content=content,
            metadata=metadata,
            extracted_fields=extracted_fields,
            source_type=doc_type,
            processed_at=datetime.now(),
            confidence_score=confidence,
            processing_method=processing_method
        )
        
        # Complete log
        processing_time = time.time() - start_time
        log.processing_time = processing_time
        log.cost_estimate = ai_cost
        log.steps.append(f"Completed in {processing_time:.2f}s")
        
        return document, log
    
    def save_signatures(self):
        """Save learned signatures"""
        self.signature_engine.save_signatures('data/signatures.json')