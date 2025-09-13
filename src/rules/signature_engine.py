import json
import hashlib
from typing import Dict, List, Any
from datetime import datetime

class SignatureEngine:
    """Learn and reuse document signatures/patterns"""
    
    def __init__(self):
        self.signatures = {}
        self.sender_patterns = {}
        self.version = "1.0"
    
    def extract_signature(self, content: str, metadata: Dict) -> str:
        """Extract document signature for pattern matching"""
        lines = content.split('\n')[:10]
        structure = [len(line.strip()) > 0 for line in lines]
        signature = hashlib.md5(str(structure).encode()).hexdigest()[:8]
        return signature
    
    def learn_pattern(self, signature: str, extraction_rules: Dict, sender: str = None):
        """Learn new extraction pattern"""
        if sender:
            if sender not in self.sender_patterns:
                self.sender_patterns[sender] = {}
            self.sender_patterns[sender][signature] = {
                'rules': extraction_rules,
                'version': self.version,
                'learned_at': datetime.now().isoformat()
            }
        else:
            self.signatures[signature] = {
                'rules': extraction_rules,
                'version': self.version,
                'learned_at': datetime.now().isoformat()
            }
    
    def get_rules(self, signature: str, sender: str = None) -> Dict:
        """Get extraction rules for signature"""
        if sender and sender in self.sender_patterns:
            return self.sender_patterns[sender].get(signature, {}).get('rules', {})
        return self.signatures.get(signature, {}).get('rules', {})
    
    def save_signatures(self, filepath: str):
        """Persist learned signatures"""
        data = {
            'signatures': self.signatures,
            'sender_patterns': self.sender_patterns,
            'version': self.version
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_signatures(self, filepath: str):
        """Load saved signatures"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.signatures = data.get('signatures', {})
                self.sender_patterns = data.get('sender_patterns', {})
                self.version = data.get('version', '1.0')
        except FileNotFoundError:
            pass