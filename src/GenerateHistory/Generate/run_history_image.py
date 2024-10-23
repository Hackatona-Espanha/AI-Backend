import re
from typing import List, Dict
from src.GenerateHistory.Prompts.generate_prompt_image import ImagePromptFormatter
from src.general.ModelTextGenerator.model_text_generator import Claude3SonnetInvoker

class StoryToImagePromptPipeline:
    """
    Classe responsável por processar cada parte da história gerada e passar para o prompt de imagem e Claude 3.
    
    Métodos:
        __init__(self, story_parts: List[str], language: str): Inicializa a classe com a lista de partes da história e o idioma.
        process_story_parts(self) -> List[Dict[str, str]]: Processa cada parte da história, gera o prompt e armazena a resposta.
    """
    
    def __init__(self, story_parts: List[Dict[str, str]], language: str):
        """
        Inicializa a classe com a lista de partes da história e o idioma escolhido para o prompt de imagem.
        
        :param story_parts: Lista contendo as partes da história gerada.
        :param language: O idioma em que os prompts de imagem serão gerados (português, inglês ou espanhol).
        """
        self.story_parts = story_parts
        self.language = language
        self.prompt_formatter = ImagePromptFormatter(language)
        self.claude_invoker = Claude3SonnetInvoker()
    
    def _extract_image_prompt(self, generated_text: str) -> str:
        """
        Extrai o conteúdo entre as tags <image_prompt> e </image_prompt> do texto gerado.
        
        :param generated_text: O texto gerado pelo modelo Claude 3 que contém o prompt de imagem.
        :return: O prompt de imagem extraído ou uma string vazia se as tags não forem encontradas.
        """
        match = re.search(r'<image_prompt>(.*?)</image_prompt>', generated_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return "Prompt não encontrado."

    def process_story_parts(self) -> List[Dict[str, str]]:
        """
        Processa cada parte da história, gera o prompt de imagem e passa o prompt para o Claude 3.
        Armazena o resultado em uma estrutura de dados contendo a história e o prompt gerado.
        
        :return: Lista de dicionários com a história e o prompt de imagem gerado para cada parte.
        """
        results = []
        
        for part in self.story_parts:
            try:
                # Gera o prompt de imagem para a parte da história
                formatted_prompt = self.prompt_formatter.format_prompt(part['story_part'])
                
                # Envia o prompt para o modelo Claude 3
                generated_prompt = self.claude_invoker.invoke_claude(formatted_prompt)
                
                # Extrai o prompt da imagem gerado entre as tags <image_prompt>
                image_prompt = self._extract_image_prompt(generated_prompt)
                
                # Armazena a parte da história e o prompt gerado em uma estrutura de dados
                result = {
                    'story': part['story_part'],
                    'prompt_img': image_prompt
                }
                results.append(result)
                
            except ValueError as e:
                print(f"Erro ao processar a parte da história: {e}")
        
        return results


