import re
from langdetect import detect, LangDetectException
from src.general.PipelineHistory.pipeline_history import PDFTextProcessingPipeline
from src.GenerateHistory.Prompts.generate_history import EducationalStoryPromptFormatter
from src.general.ModelTextGenerator.model_text_generator import Claude3SonnetInvoker
from typing import List, Dict


class PDFEducationalStoryGenerator:
    """
    Classe responsável por:
    1. Extrair e limpar o texto de um PDF.
    2. Detectar o idioma do conteúdo extraído.
    3. Formatar um prompt educacional com base no idioma e conteúdo.
    4. Invocar o modelo Claude 3 para gerar uma história educacional.
    5. Capturar e armazenar todas as tags <part> geradas pelo modelo.
    """

    def __init__(self, pdf_filename: str):
        """
        Inicializa a classe com o caminho do arquivo PDF.
        
        :param pdf_filename: O caminho do arquivo PDF.
        """
        self.pdf_filename = pdf_filename
        self.pipeline = PDFTextProcessingPipeline(pdf_filename)
        self.language_map = {
            'pt': 'português',
            'en': 'inglês',
            'es': 'espanhol'
        }
    
    def process_pdf(self) -> str:
        """
        Processa o PDF e retorna o texto limpo.
        
        :return: O texto limpo extraído do PDF.
        """
        cleaned_text = self.pipeline.process_pdf()
        return ' '.join(cleaned_text)  # Junta todas as páginas em uma única string.
    
    def detect_language(self, text: str) -> str:
        """
        Detecta o idioma do texto utilizando a biblioteca langdetect.
        
        :param text: O texto do qual será detectado o idioma.
        :return: O idioma detectado como 'português', 'inglês' ou 'espanhol'.
        """
        if not text.strip():
            raise ValueError("O texto está vazio. Não é possível detectar o idioma.")

        try:
            detected_language_code = detect(text)
            if detected_language_code in self.language_map:
                return self.language_map[detected_language_code]
            else:
                raise ValueError(f"Idioma detectado não suportado: {detected_language_code}")
        except LangDetectException:
            raise ValueError("Não foi possível detectar o idioma do texto. O conteúdo pode estar vazio ou insuficiente.")

    def generate_prompt(self, text: str, language: str) -> str:
        """
        Formata o prompt educacional com base no idioma detectado.
        
        :param text: O conteúdo educacional a ser formatado.
        :param language: O idioma detectado.
        :return: O prompt formatado para a história educacional.
        """
        prompt_formatter = EducationalStoryPromptFormatter(language)
        return prompt_formatter.format_prompt(text)
    
    def generate_story(self, prompt: str) -> str:
        """
        Invoca o modelo Claude 3 para gerar a história com base no prompt.
        
        :param prompt: O prompt formatado.
        :return: A resposta gerada pelo modelo Claude 3.
        """
        claude_invoker = Claude3SonnetInvoker()
        return claude_invoker.invoke_claude(prompt)

    def extract_parts(self, story: str) -> list:
        """
        Extrai todas as tags <part> do texto gerado pela história.
        
        :param story: A história gerada pelo modelo contendo tags <part>.
        :return: Uma lista de strings, cada uma correspondendo a um conteúdo dentro das tags <part>.
        """
        parts = re.findall(r'<part>(.*?)</part>', story, re.DOTALL)
        return parts
    
    def run_pipeline(self) -> list:
        """
        Executa todo o pipeline de extração de texto, detecção de idioma, formatação de prompt e geração da história.
        Retorna a lista de partes da história com o conteúdo gerado.
        """
        results = []

        # Etapa 1: Processar o PDF e extrair o texto limpo
        print("Extraindo e limpando o texto do PDF...")
        extracted_text = self.process_pdf()
        print("Texto extraído com sucesso.")

        # Etapa 2: Detectar o idioma do texto
        print("Detectando o idioma do texto...")
        try:
            language = self.detect_language(extracted_text)
            print(f"Idioma detectado: {language}.")
        except ValueError as e:
            print(f"Erro: {e}")
            return results  # Retorna uma lista vazia caso haja erro

        # Etapa 3: Gerar o prompt com base no idioma detectado
        print("Gerando o prompt educacional...")
        prompt = self.generate_prompt(extracted_text, language)
        print("Prompt gerado com sucesso.")

        # Etapa 4: Invocar o modelo Claude 3 para gerar a história
        print("Gerando a história educacional com Claude 3...")
        story = self.generate_story(prompt)
        print("História gerada com sucesso.")

        # Etapa 5: Extrair as tags <part> do texto gerado
        print("Extraindo as tags <part> da história gerada...")
        parts = self.extract_parts(story)
        print(f"Total de {len(parts)} partes extraídas.")

        # Formatar o resultado para cada parte
        for i, part in enumerate(parts, 1):
            result = {
                'story_part': part,
                'prompt_img': f"Prompt para a parte {i} gerado pelo Claude 3."
            }
            results.append(result)

        return results



