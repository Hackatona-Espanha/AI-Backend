from typing import List, Dict

class ImagePromptFormatter:
    """
    Classe responsável por formatar o prompt de criação de imagem com base em um segmento de história para crianças autistas,
    disponível em três línguas: Espanhol, Português e Inglês.

    Métodos:
        __init__(self, language: str): Inicializa a classe com o idioma escolhido.
        format_prompt(self, story_segment: str) -> str: Formata o prompt com base no idioma selecionado.
    """

    def __init__(self, language: str):
        """
        Inicializa o formatador de prompt com o idioma escolhido.
        
        :param language: O idioma desejado (português, inglês ou espanhol).
        """
        self.language = language.lower()
        self.prompts = {
            "português": self._format_prompt_portuguese,
            "inglês": self._format_prompt_english,
            "espanhol": self._format_prompt_spanish
        }

    def _format_prompt_portuguese(self, story_segment: str) -> str:
        """
        Formata o prompt em português.

        :param story_segment: O segmento de história que será inserido no prompt.
        :return: Uma string formatada com o prompt em português.
        """
        return f"""
        
        Você tem a tarefa de criar um prompt de imagem claro, específico e conciso com base em um fragmento de uma história. Seu objetivo é capturar os principais elementos visuais do texto e traduzi-los em um prompt que pode ser usado para gerar uma imagem.

        <story_segment>
        {story_segment}
        </story_segment>

        Diretrizes para criar o prompt de imagem:
        1. Concentre-se nos elementos visualmente mais marcantes ou importantes do fragmento da história
        2. Seja específico sobre cores, texturas, iluminação e composição quando relevante
        3. Mantenha o prompt conciso, idealmente não mais do que 2-3 frases
        4. Use uma linguagem simples e direta.
        5. Evite conceitos abstratos ou metáforas.
        6. Inclua detalhes sensoriais que uma criança autista pode achar envolventes.
        7. Use adjetivos descritivos para melhorar a qualidade visual
        
        Com base neste fragmento da história, crie um prompt de imagem claro e específico. O prompt deve ser detalhado o suficiente para gerar uma imagem vívida, mas conciso o suficiente para ser facilmente compreendido por uma IA de geração de imagens.

        Escreva seu prompt final dentro das tags <image_prompt>.
        """

    def _format_prompt_english(self, story_segment: str) -> str:
        """
        Formata o prompt em inglês.

        :param story_segment: O segmento de história que será inserido no prompt.
        :return: Uma string formatada com o prompt em inglês.
        """
        return f"""
        You are tasked with creating a clear, specific, and concise image prompt based on a story fragment. Your goal is to capture the key visual elements of the text and translate them into a prompt that can be used to generate an image.

        <story_segment>
        {story_segment}
        </story_segment>

        Guidelines for creating the image prompt:
        1. Focus on the most visually striking or important elements of the story fragment
        2. Be specific about colors, textures, lighting, and composition where relevant
        3. Keep the prompt concise, ideally no more than 2-3 sentences
        4. Use simple, direct language.
        5. Avoid abstract concepts or metaphors.
        6. Include sensory details that an autistic child might find engaging.
        7. Use descriptive adjectives to enhance visual quality

        Based on this story fragment, create a clear and specific image prompt. The prompt should be detailed enough to generate a vivid image, but concise enough to be easily understood by an image-generating AI.

        Write your final prompt inside the <image_prompt> tags.
        
        """

    def _format_prompt_spanish(self, story_segment: str) -> str:
        """
        Formata o prompt em espanhol.

        :param story_segment: O segmento de história que será inserido no prompt.
        :return: Uma string formatada com o prompt em espanhol.
        """
        return f"""
    Su tarea es crear una imagen clara, específica y concisa basada en un fragmento de una historia. Su objetivo es capturar los elementos visuales clave del texto y traducirlos en un mensaje que pueda usarse para generar una imagen.

    <segmento_historia>
    {story_segment}
    </story_segment>

    Directrices para crear el mensaje de imagen:
    1. Céntrese en los elementos visualmente más impactantes o importantes del fragmento de la historia.
    2. Sea específico sobre colores, texturas, iluminación y composición cuando sea relevante.
    3. Mantenga el mensaje conciso, idealmente no más de 2 o 3 oraciones.
    4. Utilice un lenguaje sencillo y directo.
    5. Evite conceptos abstractos o metáforas.
    6. Incluya detalles sensoriales que un niño autista pueda encontrar atractivos.
    7. Utilice adjetivos descriptivos para mejorar la calidad visual.

    A partir de este fragmento de historia, cree una imagen clara y específica. El mensaje debe ser lo suficientemente detallado como para generar una imagen vívida, pero lo suficientemente conciso como para que una IA de imágenes lo entienda fácilmente.

    Escriba su mensaje final dentro de las etiquetas <image_prompt>.
        """

    def format_prompt(self, story_segment: str) -> str:
        """
        Formata o prompt com base no idioma selecionado.

        :param story_segment: O segmento de história que será inserido no prompt.
        :return: A string formatada com o prompt no idioma selecionado.
        :raises ValueError: Se o idioma não for suportado.
        """
        if self.language in self.prompts:
            return self.prompts[self.language](story_segment)
        else:
            raise ValueError(f"Idioma não suportado: {self.language}. Escolha entre português, inglês ou espanhol.")
