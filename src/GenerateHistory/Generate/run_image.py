from typing import List, Dict
from src.general.ModelImageGenerator.model_image_generator import StableDiffusionImageGenerator

class StoryImagePipeline:
    """
    Classe responsável por processar cada parte da história gerada e gerar uma imagem baseada no prompt_img.
    
    Métodos:
        __init__(self, stories_with_prompts: List[Dict[str, str]]): Inicializa a classe com a estrutura contendo a história e o prompt da imagem.
        process_images(self) -> List[Dict[str, str]]: Processa cada prompt de imagem e gera a imagem correspondente em base64, atualizando a estrutura.
    """

    def __init__(self, stories_with_prompts: List[Dict[str, str]], region_name: str = "us-east-1"):
        """
        Inicializa a classe com a lista de histórias e seus prompts de imagem.
        
        :param stories_with_prompts: Lista contendo as histórias e os prompts de imagem.
        :param region_name: A região para inicializar o gerador de imagens do Stable Diffusion.
        """
        self.stories_with_prompts = stories_with_prompts
        self.image_generator = StableDiffusionImageGenerator(region_name=region_name)
    
    def _generate_image_base64(self, prompt: str) -> str:
        """
        Gera a imagem a partir do prompt utilizando o Stable Diffusion e retorna a imagem em formato base64.
        
        :param prompt: O prompt de imagem utilizado para gerar a imagem.
        :return: A string base64 da imagem gerada.
        """
        base64_image = self.image_generator.generate_image(prompt)
        return base64_image

    def process_images(self) -> List[Dict[str, str]]:
        """
        Processa cada prompt_img gerando a imagem em formato base64 e atualiza a estrutura.
        
        :return: Lista atualizada de dicionários contendo a história e a imagem gerada em base64.
        """
        results = []

        for story in self.stories_with_prompts:
            try:
                # Gera a imagem em base64 com base no prompt_img
                base64_image = self._generate_image_base64(story['prompt_img'])
                
                # Atualiza a estrutura com a imagem gerada em base64
                result = {
                    'story': story['story'],
                    'img': base64_image
                }
                results.append(result)

            except Exception as e:
                print(f"Erro ao gerar a imagem para o prompt: {story['prompt_img']} - Erro: {e}")
        
        return results




