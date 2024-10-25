import base64
import json
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
import time
import httpx

class VoiceGenerator:
    """
    Classe responsável por gerar áudio a partir de texto utilizando a API ElevenLabs e adicioná-lo à estrutura recebida em base64.
    
    Métodos:
        __init__(self, api_key: str, model: str = "eleven_multilingual_v2", timeout: int = 60): 
        Inicializa a classe com a API Key e o modelo de voz, com timeout configurável.
        generate_audio(self, text: str, voice_name: str = "Brian"): Gera o áudio a partir de um texto usando a voz especificada.
        save_audio_as_base64(self, audio): Converte o áudio em base64 e retorna a string.
        process_story_structure(self, stories: list): Processa a estrutura de histórias e adiciona o áudio gerado em base64.
        save_structure_to_json(self, updated_stories: list, filename: str): Salva a estrutura atualizada em um arquivo JSON.
    """
    
    def __init__(self, api_key: str, model: str = "eleven_multilingual_v2", timeout: int = 60):
        """
        Inicializa o gerador de voz com a API Key, o modelo de voz e define o timeout para requisições.
        
        :param api_key: Chave de API da ElevenLabs.
        :param model: O modelo de voz a ser utilizado (padrão: "eleven_multilingual_v2").
        :param timeout: Tempo limite em segundos para as requisições à API (padrão: 60 segundos).
        """
        self.client = ElevenLabs(api_key=api_key, timeout=timeout)
        self.model = model
        self.timeout = timeout

    def generate_audio(self, text: str, voice_name: str = "Brian", stability: float = 0.75, similarity_boost: float = 0.75, retries: int = 3):
        """
        Gera o áudio a partir de um texto, usando o nome da voz especificada e os ajustes de voz (stability, similarity).
        Implementa uma política de retries em caso de falha na conexão.

        :param text: Texto a ser convertido em áudio.
        :param voice_name: Nome da voz a ser utilizada (padrão: "Brian").
        :param stability: Estabilidade da voz (padrão: 0.75).
        :param similarity_boost: Nível de boost de similaridade da voz (padrão: 0.75).
        :param retries: Número de tentativas em caso de erro de conexão (padrão: 3).
        :return: O áudio gerado pela API em bytes.
        """
        # Configurações de voz
        voice_settings = VoiceSettings(
            stability=stability,
            similarity_boost=similarity_boost,
        )
        
        attempt = 0
        while attempt < retries:
            try:
                # Obtém todas as vozes disponíveis e seleciona a voz pelo nome
                voices = self.client.voices.get_all().voices
                selected_voice = next((voice for voice in voices if voice.name == voice_name), None)
                
                if not selected_voice:
                    raise ValueError(f"Voz '{voice_name}' não encontrada nas vozes disponíveis.")
                
                # Gera o áudio (retorna um gerador)
                audio_generator = self.client.generate(
                    text=text,
                    voice=Voice(voice_id=selected_voice.voice_id, settings=voice_settings),
                    model=self.model
                )
                
                # Concatena os chunks do gerador para obter o áudio completo em bytes
                audio_bytes = b''.join(audio_generator)

                return audio_bytes
            except httpx.ConnectTimeout:
                attempt += 1
                print(f"Tentativa {attempt} de {retries}: Timeout ao conectar-se. Tentando novamente em 5 segundos...")
                time.sleep(5)
            except Exception as e:
                print(f"Erro ao gerar o áudio: {e}")
                break
        
        raise Exception(f"Falha ao gerar o áudio após {retries} tentativas.")

    def save_audio_as_base64(self, audio: bytes) -> str:
        """
        Converte o áudio gerado em base64 e retorna a string.
        
        :param audio: O áudio gerado pela API ElevenLabs.
        :return: A string base64 representando o áudio.
        """
        return base64.b64encode(audio).decode('utf-8')

    def process_story_structure(self, stories: list) -> list:
        """
        Processa a estrutura de histórias, gerando o áudio para cada 'story' e adiciona o áudio em base64.
        
        :param stories: Lista contendo as histórias e imagens em base64.
        :return: Lista atualizada com o campo "audio" adicionado.
        """
        updated_stories = []
        
        for story_data in stories:
            story_text = story_data.get("story", "")
            try:
                # Gera o áudio para a história
                generated_audio = self.generate_audio(text=story_text, voice_name="Brian")
                
                # Converte o áudio gerado em base64
                audio_base64 = self.save_audio_as_base64(generated_audio)
                
                # Adiciona o campo "audio" na estrutura
                story_data["audio"] = audio_base64
                updated_stories.append(story_data)
                
            except Exception as e:
                print(f"Erro ao gerar o áudio para a história: {e}")
        
        return updated_stories

    def save_structure_to_json(self, updated_stories: list, filename: str):
        """
        Salva a estrutura atualizada contendo as histórias, imagens e áudio em um arquivo JSON.
        
        :param updated_stories: A lista de histórias atualizada com o campo "audio".
        :param filename: O nome do arquivo onde os dados serão salvos.
        """
        with open(filename, 'w') as file:
            json.dump(updated_stories, file, indent=4)
        print(f"Estrutura salva no arquivo JSON: {filename}")


# Exemplo de uso da classe VoiceGenerator
if __name__ == "__main__":
    # Substitua pela sua chave de API da ElevenLabs
    API_KEY = "YOUR_API_KEY"
    
    # Inicializa o gerador de voz
    voice_generator = VoiceGenerator(api_key=API_KEY)

    # Estrutura de exemplo com histórias e imagens
    stories = [
        {"story": "Era uma vez um castelo antigo onde morava um rei muito sábio.", "img": "base64_image_data"},
        {"story": "Em uma floresta distante, havia um coelho curioso que adorava aventuras.", "img": "base64_image_data"}
    ]

    # Processa a estrutura, adicionando o áudio para cada história
    updated_stories = voice_generator.process_story_structure(stories)

    # Salva a estrutura atualizada em um arquivo JSON
    voice_generator.save_structure_to_json(updated_stories, 'updated_stories_with_audio.json')
