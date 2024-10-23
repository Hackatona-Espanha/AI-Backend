import base64
import boto3
import json
import os
import random
from typing import Dict, Any

class StableDiffusionImageGenerator:
    """
    Classe responsável por gerar imagens utilizando o modelo Stable Diffusion através do serviço AWS Bedrock Runtime.
    
    Atributos:
        client (boto3.Client): Cliente para interagir com o serviço AWS Bedrock Runtime.
    
    Métodos:
        __init__(self): Inicializa o cliente AWS Bedrock Runtime.
        generate_image(prompt: str, style_preset: str, cfg_scale: int, steps: int): Gera uma imagem com base no prompt fornecido.
        save_image(base64_image_data: str, output_dir: str) -> str: Salva a imagem gerada em um diretório local.
    """
    
    def __init__(self, region_name: str = "us-east-1"):
        """
        Inicializa o gerador de imagens Stable Diffusion com a configuração da região AWS.
        """
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = "stability.stable-diffusion-xl-v1"
    
    def generate_image(self, prompt: str, style_preset: str = "photographic", cfg_scale: int = 10, steps: int = 30) -> Dict[str, Any]:
        """
        Gera uma imagem com base no prompt fornecido utilizando o modelo Stable Diffusion.

        :param prompt: Descrição da imagem que deseja gerar.
        :param style_preset: O estilo da imagem (e.g., 'photographic').
        :param cfg_scale: Escala de orientação de configuração.
        :param steps: Número de passos para a geração da imagem.
        :return: Dicionário contendo a imagem gerada em base64.
        """
        seed = random.randint(0, 4294967295)

        native_request = {
            "text_prompts": [{"text": prompt}],
            "style_preset": style_preset,
            "seed": seed,
            "cfg_scale": cfg_scale,
            "steps": steps,
        }

        request = json.dumps(native_request)

        response = self.client.invoke_model(modelId=self.model_id, body=request)

        model_response = json.loads(response["body"].read())

        return model_response["artifacts"][0]["base64"]
    
    def save_image(self, base64_image_data: str, output_dir: str = "output") -> str:
        """
        Salva a imagem gerada em um diretório local.

        :param base64_image_data: Dados da imagem em base64.
        :param output_dir: Diretório para salvar a imagem.
        :return: Caminho para o arquivo salvo.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        i = 1
        while os.path.exists(os.path.join(output_dir, f"stability_{i}.png")):
            i += 1

        image_data = base64.b64decode(base64_image_data)

        image_path = os.path.join(output_dir, f"stability_{i}.png")
        with open(image_path, "wb") as file:
            file.write(image_data)

        print(f"The generated image has been saved to {image_path}")
        return image_path



