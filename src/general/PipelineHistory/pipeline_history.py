import re
import PyPDF2
from typing import List, Any

class PDFTextExtractor:
    """
    Classe responsável por extrair texto de um arquivo PDF.
    
    Métodos:
        __init__(self, filename: str): Inicializa a classe com o nome do arquivo PDF.
        extract_text(self) -> List[str]: Extrai o texto de cada página do PDF e retorna como uma lista de strings.
    """
    
    def __init__(self, filename: str):
        """
        Inicializa a classe com o caminho do arquivo PDF.
        
        :param filename: O caminho para o arquivo PDF.
        """
        self.filename = filename

    def extract_text(self) -> List[str]:
        """
        Extrai o texto de cada página do PDF.
        
        :return: Uma lista onde cada item é o texto de uma página do PDF.
        """
        text_by_page = []
        try:
            with open(self.filename, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page_text = reader.pages[page_num].extract_text()
                    text_by_page.append(page_text)
        except Exception as e:
            print(f"Erro ao ler o PDF: {e}")
        return text_by_page


class TextCleaner:
    """
    Classe responsável por limpar e formatar o texto extraído de um PDF usando regex.
    
    Métodos:
        __init__(self): Inicializa a classe sem parâmetros.
        clean_text(self, text: str) -> str: Aplica regras de limpeza em uma string.
        clean_text_list(self, texts: List[str]) -> List[str]: Aplica a limpeza em uma lista de strings.
    """
    
    def __init__(self):
        """
        Inicializa a classe TextCleaner.
        """
        pass
    
    def clean_text(self, text: str) -> str:
        """
        Aplica regex para limpar e formatar o texto.
        
        :param text: O texto a ser limpo.
        :return: O texto limpo e formatado.
        """
        # Remove múltiplos espaços em branco
        text = re.sub(r'\s+', ' ', text)
        
        # Remove caracteres especiais indesejados, mantendo pontuações básicas
        text = re.sub(r'[^\w\s,.!?]', '', text)
        
        # Remove espaços extras no início e no fim
        text = text.strip()
        
        return text

    def clean_text_list(self, texts: List[str]) -> List[str]:
        """
        Limpa uma lista de textos.
        
        :param texts: Lista de textos para limpar.
        :return: Lista de textos limpos.
        """
        return [self.clean_text(text) for text in texts]


class PDFTextProcessingPipeline:
    """
    Classe responsável por integrar o processo de extração e limpeza de texto de um PDF.
    
    Métodos:
        __init__(self, filename: str): Inicializa a classe com o nome do arquivo PDF.
        process_pdf(self) -> List[str]: Extrai e limpa o texto de um PDF e retorna uma lista de strings limpas.
    """
    
    def __init__(self, filename: str):
        """
        Inicializa o pipeline com o caminho para o arquivo PDF.
        
        :param filename: O caminho do arquivo PDF.
        """
        self.filename = filename
        self.extractor = PDFTextExtractor(filename)
        self.cleaner = TextCleaner()

    def process_pdf(self) -> List[str]:
        """
        Extrai e limpa o texto do PDF.
        
        :return: Lista de strings com o texto limpo e formatado.
        """
        # Extrair o texto do PDF
        raw_text_list = self.extractor.extract_text()

        # Limpar o texto extraído
        cleaned_text_list = self.cleaner.clean_text_list(raw_text_list)

        return cleaned_text_list



