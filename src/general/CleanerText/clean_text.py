from typing import List, Dict, Any
import re

class TextCleaner:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    def clean_text(self, text: str) -> str:
        # Remove múltiplos espaços em branco
        text = re.sub(r'\s+', ' ', text)
        
        # Remove caracteres especiais (mantendo pontuações básicas)
        text = re.sub(r'[^\w\s,.!?]', '', text)
        
        # Remove espaços em branco no início e no fim
        text = text.strip()
        
        return text

    def clean_structure(self) -> List[Dict[str, Any]]:
        cleaned_data = []
        for entry in self.data:
            if isinstance(entry, dict) and 'metadata' in entry and 'text' in entry['metadata']:
                cleaned_text = self.clean_text(entry['metadata']['text'])
                entry['metadata']['text'] = cleaned_text
            cleaned_data.append(entry)
        return cleaned_data
