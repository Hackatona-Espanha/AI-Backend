import random
import string
import PyPDF2
from typing import Dict, Any

class PDFExtractor:
    def __init__(self, filename: str):
        self.filename = filename
        self.text = self._extract_text()
        self.id = self._generate_id()
    
    def _extract_text(self) -> str:
        try:
            with open(self.filename, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
                return text
        except Exception as e:
            print(f"Erro ao extrair o texto: {e}")
            return ""

    def _generate_id(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def get_data(self) -> Dict[str, Any]:
        return [{
            'id': self.id,
            'metadata': {
                'embedding': 'none por enquanto',
                'text': self.text,
                'filename': self.filename
            }
        }]

