import google.generativeai as genai
import json
from typing import Dict, Any

class GeminiProcessor:
    """AI processor using Gemini 1.5 Flash for outliers only"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.cost_per_token = 0.000001  # Approximate cost
    
    def extract_structured_data(self, content: str, doc_type: str) -> Dict[str, Any]:
        """Use AI to extract structured data from complex documents"""
        prompt = f"""
        Extract key information from this {doc_type} document and return as JSON:
        
        Document content:
        {content[:2000]}  # Limit content to control costs
        
        Return JSON with these fields:
        - title: document title
        - key_fields: important data fields found
        - summary: brief summary
        - confidence: confidence score 0-1
        
        Return only valid JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            
            # Estimate cost based on token usage
            estimated_tokens = len(prompt.split()) + len(response.text.split())
            cost = estimated_tokens * self.cost_per_token
            
            return {
                'extracted_data': result,
                'cost': cost,
                'tokens_used': estimated_tokens
            }
        except Exception as e:
            return {
                'extracted_data': {'error': str(e)},
                'cost': 0,
                'tokens_used': 0
            }
    
    def should_use_ai(self, content: str, confidence_score: float) -> bool:
        """Determine if AI processing is needed"""
        # Use AI only for low confidence or complex documents
        return confidence_score < 0.7 or len(content) > 5000