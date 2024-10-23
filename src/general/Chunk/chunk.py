import random
import string
from typing import List, Dict, Any

class ChunkedText:
    def __init__(self, data: List[Dict[str, Any]], chunk_size: int, overlap: int):
        self.data = data
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def _generate_id(self) -> str:
        """Gera um ID aleatório"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def _create_chunks(self, text: str) -> List[str]:
        """Divide o texto em chunks, considerando o tamanho do chunk e o overlap"""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks

    def chunk_structure(self) -> List[Dict[str, Any]]:
        """Gera a estrutura replicada para cada chunk do texto"""
        chunked_data = []
        for entry in self.data:
            if 'metadata' in entry and 'text' in entry['metadata']:
                text = entry['metadata']['text']
                chunks = self._create_chunks(text)
                for chunk in chunks:
                    new_entry = {
                        'id': self._generate_id(),
                        'metadata': {
                            'embedding': entry['metadata'].get('embedding', 'none por enquanto'),
                            'text': chunk,
                            'filename': entry['metadata'].get('filename', '')
                        }
                    }
                    chunked_data.append(new_entry)
        return chunked_data

# Exemplo de uso:
data = [{
    'id': '0XeLRkpJQxFh',
    'metadata': {
        'embedding': 'none por enquanto',
        'text': 'ROMA ANTIGA Prof. João RochaLINHA DO TEMPO 753 a.C. 509 a.C. 27 a.C. 476 d.C. MONARQUIA Fundação de Roma Domínio Etrusco Conflitos plebeus patrícios Formação das estruturas sociais e políticas romanasREPÚBLICA Predomínio do Senado Guerras Púnicas Expansionismo militar Roma como superpotência Revoltas de escravosIMPÉRIO Auge da dominação romana PaxRomana Problemas fronteiriços com bárbaros Divisão do Império Queda de Roma a.C. d.C.FORMAÇÃO APenínsula Itálica foi ocupada por a .',
        'filename': './src/documents/Roma Antiga.pdf'
    }
}]

chunk_size = 100
overlap = 20

chunker = ChunkedText(data, chunk_size, overlap)
chunked_data = chunker.chunk_structure()

# Exibir resultado:
for entry in chunked_data:
    print(entry)
