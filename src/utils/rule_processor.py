import re
from typing import Dict, List, Any, Tuple

class RuleProcessor:
    """Completely dynamic extraction processor"""
    
    def __init__(self):
        pass
    
    def apply_rules(self, content: str, rules: Dict = None) -> Tuple[Dict[str, Any], float]:
        """Dynamically extract all structured data from content"""
        extracted = {}
        
        # Extract all key-value patterns
        kv_patterns = [
            r'([A-Za-z][A-Za-z0-9\s]{1,30})\s*:+\s*([^\n:]{1,200})',
            r'([A-Za-z][A-Za-z0-9\s]{1,30})\s*-\s*([^\n-]{1,200})',
            r'^([A-Za-z][A-Za-z0-9\s]{1,30})\s+([A-Z0-9][^\n]{1,100})$'
        ]
        
        for pattern in kv_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            for key, value in matches:
                key = key.strip()
                value = value.strip()
                if len(key) > 2 and len(value) > 0 and not value.isspace():
                    clean_key = re.sub(r'[^a-zA-Z0-9_]', '_', key.lower())
                    extracted[clean_key] = value
        
        # Extract all structured patterns
        all_patterns = self._discover_patterns(content)
        for pattern_type, values in all_patterns.items():
            if values:
                extracted[pattern_type] = values if len(values) > 1 else values[0]
        
        confidence = min(0.9, 0.3 + (len(extracted) * 0.1))
        return extracted, confidence
    
    def _discover_patterns(self, content: str) -> Dict[str, List[str]]:
        """Automatically discover and extract all data patterns"""
        patterns = {}
        
        # Auto-detect emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        if emails: patterns['emails'] = list(set(emails))
        
        # Auto-detect phone numbers
        phones = re.findall(r'(?:\+91[\s-]?)?\d{2,4}[\s-]\d{6,8}', content)
        phones = [p for p in phones if len(re.sub(r'\D', '', p)) >= 10]
        if phones: patterns['phones'] = list(set(phones))
        
        # Auto-detect amounts/currency
        amounts = re.findall(r'(?:₹|Rs\.?|INR|USD|\$)\s*[0-9,]+(?:\.\d{2})?', content)
        if amounts: patterns['amounts'] = list(set(amounts))
        
        # Auto-detect dates
        dates = re.findall(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})\b', content)
        if dates: patterns['dates'] = list(set(dates))
        
        # Auto-detect codes (alphanumeric sequences)
        codes = re.findall(r'\b[A-Z0-9]{4,15}\b', content)
        codes = [c for c in codes if not c.isdigit() and len(c) >= 4]
        if codes: patterns['codes'] = list(set(codes))
        
        # Auto-detect URLs
        urls = re.findall(r'https?://[^\s]+', content)
        if urls: patterns['urls'] = list(set(urls))
        
        # Auto-detect table data
        if '|' in content:
            table_data = re.findall(r'\|([^|\n]+)\|', content)
            if table_data: patterns['table_data'] = [t.strip() for t in table_data if t.strip()]
        
        return patterns
    
    def extract_basic_fields(self, content: str) -> Dict[str, Any]:
        """Extract document metadata"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        return {
            'document_title': lines[0] if lines else "",
            'total_lines': len(lines),
            'word_count': len(content.split()),
            'character_count': len(content)
        }
    
    def extract_all_data(self, content: str) -> Dict[str, Any]:
        """Extract all data dynamically from document"""
        extracted_data, confidence = self.apply_rules(content)
        basic_fields = self.extract_basic_fields(content)
        sections = self._identify_sections(content)
        
        all_data = {**basic_fields, **extracted_data}
        if sections:
            all_data['document_sections'] = sections
        all_data['extraction_confidence'] = confidence
            
        return all_data
    
    def _identify_sections(self, content: str) -> List[Dict[str, str]]:
        """Auto-identify document sections"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        sections = []
        current_section = {'title': '', 'content': ''}
        
        for line in lines:
            # Auto-detect headers (short lines, caps, or numbered)
            is_header = (len(line) < 60 and 
                        (line.isupper() or 
                         re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*:?$', line) or
                         re.match(r'^\d+\.', line) or
                         line.endswith(':')))
            
            if is_header and current_section['content']:
                sections.append(current_section)
                current_section = {'title': line, 'content': ''}
            elif is_header:
                current_section['title'] = line
            else:
                current_section['content'] += line + '\n'
        
        if current_section['content']:
            sections.append(current_section)
            
        return sections