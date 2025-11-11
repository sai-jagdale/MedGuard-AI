# medicinebot/agents/barcode_agent.py

from PIL import Image
from pyzbar.pyzbar import decode

def run_barcode_agent(image_file):
    """
    Decodes the first barcode found in the provided image file object.
    
    :param image_file: A Django InMemoryUploadedFile object.
    :return: Decoded barcode data (str) or None.
    """
    try:
        # Open the image file object
        img = Image.open(image_file)
        
        barcodes = decode(img)
        
        if barcodes:
            return barcodes[0].data.decode('utf-8')
        else:
            return None
            
    except Exception as e:
        print(f"Barcode decoding error: {e}")
        return None