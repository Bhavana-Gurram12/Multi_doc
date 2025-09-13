from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentSchema(BaseModel):
    """Normalized JSON schema for all document types"""
    document_id: str
    title: Optional[str] = None
    content: str
    metadata: Dict[str, Any] = {}
    extracted_fields: Dict[str, Any] = {}
    source_type: str  # pdf, docx, html, email, scan
    processed_at: datetime
    confidence_score: float
    processing_method: str  # rule_based, ai_assisted, hybrid

class ProcessingLog(BaseModel):
    """Human-readable interpretation log"""
    document_id: str
    steps: List[str] = []
    rules_applied: List[str] = []
    ai_usage: bool = False
    cost_estimate: float = 0.0
    processing_time: float = 0.0
    warnings: List[str] = []