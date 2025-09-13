import re
from typing import Dict, List, Any, Tuple

class RuleProcessor:
    """Rule-based extraction processor"""
    
    def __init__(self):
        self.default_rules = {
            'title': [
                r'^(.+?)(?:\n|$)',  # First line as title
                r'(?i)title:\s*(.+?)(?:\n|$)',  # Title: pattern
                r'(?i)subject:\s*(.+?)(?:\n|$)'  # Subject: pattern
            ],
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            'phone': [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                r'\(\d{3}\)\s*\d{3}[-.]?\d{4}'
            ],
            'date': [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
            ]
        }
    
    def apply_rules(self, content: str, rules: Dict = None) -> Tuple[Dict[str, Any], float]:
        """Apply extraction rules to content"""
        if rules is None:
            rules = self.default_rules
        
        extracted = {}
        confidence_scores = []
        
        for field, patterns in rules.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                extracted[field] = matches[0] if len(matches) == 1 else matches
                confidence_scores.append(0.9)  # High confidence for rule matches
            else:
                confidence_scores.append(0.3)  # Low confidence for no matches
        
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        return extracted, overall_confidence
    
    def extract_basic_fields(self, content: str) -> Dict[str, Any]:
        """Extract basic fields using simple heuristics"""
        lines = content.split('\n')
        
        # Basic extraction
        title = lines[0].strip() if lines else ""
        word_count = len(content.split())
        line_count = len(lines)
        
        return {
            'title': title,
            'word_count': word_count,
            'line_count': line_count,
            'has_structured_data': any(char in content for char in [':', '|', '\t'])
        }