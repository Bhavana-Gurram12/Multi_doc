# import re
# from typing import Dict, List, Any, Tuple

# class RuleProcessor:
#     """Advanced extraction processor using multiple approaches"""
    
#     def __init__(self):
#         pass
    
#     def extract_all_data(self, content: str) -> Dict[str, Any]:
#         """Extract everything without keyword assumptions"""
#         extracted = {}
        
#         # Raw content
#         extracted['full_text'] = content
#         extracted['lines'] = content.split('\n')
#         extracted['words'] = content.split()
        
#         # Extract all patterns found
#         extracted['all_numbers'] = re.findall(r'\d+(?:[.,]\d+)*', content)
#         extracted['all_text_sequences'] = re.findall(r'[A-Za-z]+', content)
#         extracted['all_mixed_sequences'] = re.findall(r'[A-Za-z0-9]+', content)
#         extracted['all_special_chars'] = re.findall(r'[^A-Za-z0-9\s]', content)
        
#         # Extract any email-like patterns
#         extracted['email_patterns'] = re.findall(r'\S+@\S+\.\S+', content)
        
#         # Extract any phone-like patterns
#         extracted['phone_patterns'] = re.findall(r'\+?\d[\d\s\-\(\)]{7,}\d', content)
        
#         # Extract any date-like patterns
#         extracted['date_patterns'] = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}', content)
        
#         # Extract any currency-like patterns
#         extracted['currency_patterns'] = re.findall(r'[₹$]?\s*\d+(?:[,.]\d+)*', content)
        
#         # Extract any code-like patterns
#         extracted['code_patterns'] = re.findall(r'\b[A-Z0-9]{3,}\b', content)
        
#         # Extract sentences
#         extracted['sentences'] = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
        
#         # Extract paragraphs
#         extracted['paragraphs'] = [p.strip() for p in content.split('\n\n') if p.strip()]
        
#         return extracted
    
#     def apply_rules(self, content: str, rules: Dict = None) -> Tuple[Dict[str, Any], float]:
#         """Extract everything - no rules, no filtering"""
#         extracted = self.extract_all_data(content)
#         confidence = 1.0  # Always confident since we extract everything
#         return extracted, confidence
    
#     def extract_basic_fields(self, content: str) -> Dict[str, Any]:
#         """Extract basic document metadata"""
#         lines = [line.strip() for line in content.split('\n') if line.strip()]
        
#         return {
#             'title': lines[0] if lines else "",
#             'word_count': len(content.split()),
#             'line_count': len(lines)
#         }






import re
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter


class RuleProcessor:
    """Fully Dynamic Document Processor (No Keywords or Hardcoded Entities)"""

    def __init__(self):
        pass

    def extract_all_data(self, content: str) -> Dict[str, Any]:
        """Main extraction pipeline: structure, context, metadata"""
        extracted = {}
        extracted.update(self._extract_structure(content))
        extracted.update(self._extract_contextual(content))
        extracted['metadata'] = self._extract_dynamic_metadata(content)
        return extracted

    def _extract_structure(self, content: str) -> Dict[str, Any]:
        """Extract structural elements: headers, tables, sections"""
        structure = {}
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        # Headers: visually distinct lines (caps, punctuated, short)
        headers = [line for line in lines if len(line) < 80 and 
                   (line.isupper() or re.match(r'.+[:\-]$', line))]
        structure['headers'] = headers

        # Tables: lines with tabular spacing or 3+ data chunks
        table_rows = []
        for line in lines:
            tokens = re.split(r'\s{2,}|\t+', line)
            if len(tokens) >= 3 and all(re.search(r'\w+', t) for t in tokens):
                table_rows.append(tokens)
        if table_rows:
            structure['table_rows'] = table_rows

        # Sections: split into logical blocks by header-like lines
        sections = defaultdict(list)
        current_section = "section_0"
        section_count = 0
        for line in lines:
            if re.match(r'^[A-Za-z0-9\s\-\/]{2,50}[:\-]$', line):
                section_count += 1
                current_section = f"section_{section_count}"
                continue
            sections[current_section].append(line)
        structure['sections'] = dict(sections)

        return structure

    def _extract_contextual(self, content: str) -> Dict[str, Any]:
        """Extract generic patterns, key-values, words/numbers, sentences"""
        contextual = {}
        kv_pairs = {}

        # Generic key-value pairs (colon, dash, or space-separated)
        patterns = [
            r'([^\n:]{2,50})\s*[:\-]\s*([^\n]{1,100})',
            r'^([^\n]{2,40})\s+([A-Z0-9#\-\/]{3,})$'
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                key = re.sub(r'\W+', '_', match.group(1).strip().lower())
                value = match.group(2).strip()
                if value:
                    kv_pairs[key] = value

        contextual['key_value_pairs'] = kv_pairs

        # Unique words (longer than 2 chars) and numbers
        contextual['unique_words'] = list(set(re.findall(r'\b[A-Za-z]{3,}\b', content)))
        contextual['unique_numbers'] = list(set(re.findall(r'\b\d+\b', content)))

        # Sentences (basic sentence splitter)
        sentences = re.split(r'(?<=[.?!])\s+', content.strip())
        contextual['sentences'] = sentences

        return contextual

    def _extract_dynamic_metadata(self, content: str) -> Dict[str, Any]:
        """Dynamic metadata: title, stats, top words, date patterns"""
        metadata = {}
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        all_words = re.findall(r'\b\w+\b', content)

        # Title candidates: short, prominent lines at the top
        title_candidates = [
            line for line in lines[:5]
            if len(line) > 5 and (line.isupper() or len(line.split()) <= 6)
        ]
        metadata['title_candidates'] = title_candidates

        # Extract date-like patterns (generic date formats)
        date_pattern = r'\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b'
        metadata['dates'] = re.findall(date_pattern, content)

        # Document stats
        metadata['word_count'] = len(all_words)
        metadata['line_count'] = len(lines)
        metadata['char_count'] = len(content)

        # Top non-common words
        words_filtered = [
            word.lower() for word in all_words
            if word.isalpha() and len(word) > 2
        ]
        metadata['top_keywords'] = Counter(words_filtered).most_common(10)

        # Line length stats
        line_lengths = [len(line) for line in lines]
        metadata['avg_line_length'] = sum(line_lengths) / len(line_lengths) if line_lengths else 0
        metadata['max_line_length'] = max(line_lengths) if line_lengths else 0

        return metadata

    def apply_rules(self, content: str, rules: Dict = None) -> Tuple[Dict[str, Any], float]:
        """No rules applied - just full dynamic extraction"""
        extracted = self.extract_all_data(content)
        return extracted, 1.0  # Always confident

    def extract_basic_fields(self, content: str) -> Dict[str, Any]:
        """Alias for metadata"""
        return self._extract_dynamic_metadata(content)
