import json
from src.GenerateHistory.Generate.run_history import PDFEducationalStoryGenerator
from src.GenerateHistory.Generate.run_history_image import StoryToImagePromptPipeline
from src.GenerateHistory.Generate.run_image import StoryImagePipeline


def save_json(output_data, filename="output.json"):
    """
    Salva a estrutura final gerada pelo pipeline em um arquivo JSON.
    
    :param output_data: A estrutura final a ser salva.
    :param filename: O nome do arquivo onde o JSON será salvo.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"Estrutura final salva em {filename}")


def main(pdf_filename: str, language: str = "inglês", region_name: str = "us-east-1"):
    """
    Função principal que executa todo o pipeline do projeto:
    1. Extrai o texto de um PDF e gera as partes da história.
    2. Gera prompts de imagem para cada parte da história.
    3. Gera imagens baseadas nos prompts e converte-as para base64.
    
    :param pdf_filename: Caminho para o arquivo PDF.
    :param language: Idioma escolhido para os prompts de imagem (padrão: "inglês").
    :param region_name: Região do gerador de imagens (padrão: "us-east-1").
    :return: Estrutura final contendo as histórias e as imagens em base64.
    """
    
    # Etapa 1: Extrai o texto do PDF e gera as histórias
    print("Iniciando extração e geração das histórias a partir do PDF...")
    story_generator = PDFEducationalStoryGenerator(pdf_filename)
    story_structure = story_generator.run_pipeline()

    # Exibe a estrutura retornada após a geração das histórias
    print("\nHistórias geradas e prompts de imagem:")
    for part in story_structure:
        print(f"Parte da História: {part['story_part']}")
        print(f"Prompt gerado para imagem: {part['prompt_img']}\n")

    # Etapa 2: Gera prompts de imagem para cada parte da história
    print("Gerando prompts de imagem para as histórias...")
    story_pipeline = StoryToImagePromptPipeline(story_structure, language)
    results = story_pipeline.process_story_parts()

    # Exibe os prompts gerados para as imagens
    print("\nPrompts de imagem gerados:")
    for result in results:
        print(f"História: {result['story']}")
        print(f"Prompt gerado para imagem: {result['prompt_img']}\n")

    # Etapa 3: Gera imagens em base64 com base nos prompts de imagem
    print("Gerando imagens em base64 a partir dos prompts...")
    story_image_pipeline = StoryImagePipeline(results, region_name=region_name)
    updated_stories = story_image_pipeline.process_images()

    # Exibe as histórias finais com as imagens em base64
    print("\nHistórias finais com imagens em base64:")
    for story in updated_stories:
        print(f"História: {story['story']}")
        print(f"Imagem gerada (base64): {story['img'][:50]}... [truncated]\n")

    # Retorna a estrutura final contendo as histórias e as imagens geradas em base64
    return updated_stories


if __name__ == "__main__":
    # Definir o caminho para o PDF
    pdf_filename = "./src/documents/sodapdf-converted_correct.pdf"

    # Executa a main com o arquivo PDF
    final_structure = main(pdf_filename)

    # Salva a estrutura final em um arquivo JSON
    save_json(final_structure, filename="output.json")

    # Exibe a estrutura final retornada pela main
    print("\nEstrutura final gerada pelo pipeline:")
    for item in final_structure:
        print(f"História: {item['story']}")
        print(f"Imagem (base64): {item['img'][:50]}... [truncated]")
