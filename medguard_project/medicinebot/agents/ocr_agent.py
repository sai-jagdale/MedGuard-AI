import os
from django.conf import settings
from google.cloud import vision
from google.oauth2 import service_account

def run_ocr_agent(image_file):
    """
    Agent 1: Extracts text from an image using the Google Cloud Vision API.
    """
    try:
        key_path = os.path.join(settings.BASE_DIR, 'gcloud_key.json')
        credentials = service_account.Credentials.from_service_account_file(key_path)
        client = vision.ImageAnnotatorClient(credentials=credentials)

        content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        
        if response.error.message:
            raise Exception(f"Google Vision API Error: {response.error.message}")

        if response.full_text_annotation:
            extracted_text = response.full_text_annotation.text
            print(f"--- OCR Agent DEBUG --- \nText read: '{extracted_text.strip()}'")
            return extracted_text.strip()
        else:
            print("--- OCR Agent DEBUG --- \nNo text found by Google Vision API.")
            return None
        
    except Exception as e:
        print(f"OCR Agent ERROR: {e}")
        return None