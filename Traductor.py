# Importar librerías necesarias
import fitz # PyMuPDF
import requests #para interactuar con la API de DeepL
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Configurar las opciones de la API de DeepL

deepl_api_url = 'https://api-free.deepl.com/v2/translate'
deepl_api_key = 'f7184267-72a8-4b0e-8526-1fe017f753d7:fx'

def extraer_texto_pdf(input_pdf):
    # Esta función extrae el texto de un archivo PDF conservando las posiciones.
    doc = fitz.open(input_pdf)
    paginas = []
    
    for i in range(len(doc)):
        pagina = doc[i]
        blocks = pagina.getText("blocks")
        contenido = [{"text": j[4], "bbox": j[:4]} for j in blocks]
        
        #Este for es exactamente igual a lo que se encuentra en el for de arriba, pero con un parámetro extra.
        # for j in blocks:
        #     contenido = [{"text": j[4], "bbox": j[:4]}]
        
        paginas.append(contenido)
        
    doc.close()
    return paginas

def traducir_texto(texto, origen = "EN", destino = "ES"):
    """Traduce del ingés al español."""
    
    headers =  {
        "authorization": f"DeepL-Auth-Key {deepl_api_key}"
        
    }
    
    data = {
        "text": texto,
        "source_lang": origen,
        "target_lang": destino
    }
    
    response = requests.post(deepl_api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        raise Exception(f"Error en la traducción: {response.status_code}, {response.text}")
    



























# headers = {
#     'Ocp-Apim-Subscription-Key': '<your-subscription-key>',
#     'Content-Type': 'application/json'
# }


# from googletrans import Translator
# translator = Translator()
# translated_text = translator.translate('veritas lux mea', src='la', dest='es')
# print(f"La traducción de 'veritas lux mea' a español es: {translated_text.text}")