from typing import List, Dict

class EducationalStoryPromptFormatter:
    """
    Classe responsável por formatar o prompt de criação de história educacional para crianças autistas
    em três línguas: Espanhol, Português e Inglês.
    
    Métodos:
        __init__(self, language: str): Inicializa a classe com o idioma escolhido.
        format_prompt(self, educational_content: str) -> str: Formata o prompt com base no idioma selecionado.
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
    
    def _format_prompt_portuguese(self, educational_content: str) -> str:
        """
        Formata o prompt em português.

        :param educational_content: O conteúdo educacional que será inserido no prompt.
        :return: Uma string formatada com o prompt em português.
        """
        return f"""
        Você tem a tarefa de criar uma história educacional para crianças autistas com base em um determinado conteúdo educacional. Seu objetivo é dividir o conteúdo em 6 partes e criar um segmento de história para cada parte. Aqui estão suas instruções:

        1. Primeiro, você receberá um conteúdo educacional. Leia-o cuidadosamente para entender os principais conceitos e informações.

        <educational_content>
        {educational_content}
        </educational_content>

        2. Divida o conteúdo educacional em 6 partes distintas. Cada parte deve conter um conceito-chave ou informação do conteúdo original.

        3. Para cada uma das 6 partes, crie um segmento de história curta que incorpore as informações educacionais de uma forma envolvente e fácil de entender para crianças autistas. Tenha em mente as seguintes diretrizes:

        a. Use uma linguagem simples e clara.
        b. Evite metáforas, expressões idiomáticas ou conceitos abstratos que podem ser difíceis de entender.
        c. Inclua exemplos concretos e descrições visuais.
        d. Use a repetição para reforçar pontos importantes.
        e. Incorpore detalhes sensoriais quando apropriado.
        f. Torne a história interativa fazendo perguntas simples ou incentivando a imaginação.
        g. Gere em no máximo 2 paragráfos, histórias breves, paragráfos curtos.

        4. Cada segmento da história deve ser educativo e se relacionar diretamente com o conteúdo do material original.

        5. Formate cada parte da história usando tags HTML. Use o seguinte formato:

        <part>
        [Insira seu segmento de história aqui]
        </part>

        6. Certifique-se de criar exatamente 6 partes, cada uma incluída em seu próprio conjunto de tags <part>.

        7. Seja criativo com sua narrativa, mas sempre priorize o valor educacional e garanta que as informações-chave do conteúdo original sejam transmitidas com precisão.
        """
    
    def _format_prompt_english(self, educational_content: str) -> str:
        """
        Formata o prompt em inglês.

        :param educational_content: O conteúdo educacional que será inserido no prompt.
        :return: Uma string formatada com o prompt em inglês.
        """
        return f"""
        Your task is to create an educational story for autistic children based on a given educational content. Your goal is to divide the content into 6 parts and create a story segment for each part. Here are your instructions:

        1. First, you will receive educational content. Read it carefully to understand the key concepts and information.

        <educational_content>
        {educational_content}
        </educational_content>

        2. Divide the educational content into 6 distinct parts. Each part should contain a key concept or information from the original content.

        3. For each of the 6 parts, create a short story segment that incorporates the educational information in an engaging and easy-to-understand way for autistic children. Keep the following guidelines in mind:

        a. Use simple and clear language.
        b. Avoid metaphors, idiomatic expressions, or abstract concepts that may be difficult to understand.
        c. Include concrete examples and visual descriptions.
        d. Use repetition to reinforce important points.
        e. Incorporate sensory details when appropriate.
        f. Make the story interactive by asking simple questions or encouraging imagination.

        4. Each story segment should be educational and directly relate to the content of the original material.

        5. Format each part of the story using HTML tags. Use the following format:

        <part>
        [Insert your story segment here]
        </part>

        6. Make sure to create exactly 6 parts, each included in its own set of <part> tags.

        7. Be creative with your storytelling, but always prioritize educational value and ensure that the key information from the original content is conveyed accurately.
        """
    
    def _format_prompt_spanish(self, educational_content: str) -> str:
        """
        Formata o prompt em espanhol.

        :param educational_content: O conteúdo educacional que será inserido no prompt.
        :return: Uma string formatada com o prompt em espanhol.
        """
        return f"""
        Tienes la tarea de crear una historia educativa para niños autistas basada en un contenido educativo determinado. Tu objetivo es dividir el contenido en 6 partes y crear un segmento de historia para cada parte. Aquí tienes tus instrucciones:

        1. Primero, recibirás un contenido educativo. Léelo con cuidado para entender los conceptos e información clave.

        <educational_content>
        {educational_content}
        </educational_content>

        2. Divide el contenido educativo en 6 partes distintas. Cada parte debe contener un concepto clave o información del contenido original.

        3. Para cada una de las 6 partes, crea un segmento de historia breve que incorpore la información educativa de manera atractiva y fácil de entender para los niños autistas. Ten en cuenta las siguientes pautas:

        a. Usa un lenguaje simple y claro.
        b. Evita metáforas, expresiones idiomáticas o conceptos abstractos que puedan ser difíciles de entender.
        c. Incluye ejemplos concretos y descripciones visuales.
        d. Usa la repetición para reforzar los puntos importantes.
        e. Incorpora detalles sensoriales cuando sea apropiado.
        f. Haz que la historia sea interactiva haciendo preguntas simples o incentivando la imaginación.

        4. Cada segmento de la historia debe ser educativo y estar directamente relacionado con el contenido del material original.

        5. Formatea cada parte de la historia usando etiquetas HTML. Usa el siguiente formato:

        <part>
        [Inserta tu segmento de historia aquí]
        </part>

        6. Asegúrate de crear exactamente 6 partes, cada una incluida en su propio conjunto de etiquetas <part>.

        7. Sé creativo con tu narrativa, pero siempre prioriza el valor educativo y asegúrate de que la información clave del contenido original se transmita con precisión.
        """
    
    def format_prompt(self, educational_content: str) -> str:
        """
        Formata o prompt com base no idioma selecionado.

        :param educational_content: O conteúdo educacional que será inserido no prompt.
        :return: A string formatada com o prompt no idioma selecionado.
        :raises ValueError: Se o idioma não for suportado.
        """
        if self.language in self.prompts:
            return self.prompts[self.language](educational_content)
        else:
            raise ValueError(f"Idioma não suportado: {self.language}. Escolha entre português, inglês ou espanhol.")


