import requests
import json
import os
from PIL import Image
import PIL
import config

API_KEY: str = config.ocrspace_api_key

class Configuration:
    def __init__(self):
        self.image_file_path: str | None = None
        self.ocr_engine_number: int | None = None
        self.language: str | None = None
        self.use_scale: bool | None = None

    def SetLanguage(self, lang: str | None) -> None:
        self.language = lang

    def SetOCREngineNumber(self, ocr: int | None) -> None:
        self.ocr_engine_number = ocr

    def SetScale(self, scale: bool | None) -> None:
        self.use_scale = scale

    def SetImageFilePath(self, image: str | None) -> None:
        self.image_file_path = image

def Request(image, scale=True, ocr=1, language="eng", api_key=API_KEY) -> str:
    payload = {"scale": scale, "OCREngine": ocr, "apikey": api_key, "language": language}

    with open(image, "rb") as file:
        request = requests.post(
            "https://api.ocr.space/parse/image",
            files={image: file},
            data=payload
        )
    response = request.content.decode()
    return response

def RunClient(configuration: Configuration) -> str:
    image_file_path = configuration.image_file_path
    ocr_engine_number = configuration.ocr_engine_number
    language = configuration.language
    use_scale = configuration.use_scale

    # resize if image exceeds max dimensions of 10000 pixels (free OCR.space limit)
    image_file_path_root, image_file_path_extension = os.path.splitext(image_file_path)
    if image_file_path_extension.lower() != "pdf":
        image = Image.open(image_file_path)
        image_width, image_height = image.size

        if image_width > 9999 or image_height > 9999:
            image.thumbnail((9999, 9999))
            image.save(image_file_path)

        # overwrite image using PIL to ensure it's saved in a compatible format
        image.thumbnail((image_width , image_height))
        image.save(image_file_path)

    ocrspace_response = Request(image=image_file_path, scale=use_scale, ocr=ocr_engine_number, language=language, api_key=API_KEY)
    ocrspace_response = json.loads(ocrspace_response)

    # print the parsed text to console
    if ocrspace_response.get("ParsedResults"):
        detected_text = ocrspace_response["ParsedResults"][0]["ParsedText"]
        processing_time = ocrspace_response["ProcessingTimeInMilliseconds"]
        return f"Detected text:\n{detected_text}\n\nProcessing time:\n{processing_time} milliseconds"