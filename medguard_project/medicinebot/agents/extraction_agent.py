import ollama
import json

def run_extraction_agent(raw_text: str) -> dict:
    """
    Extracts structured data from raw OCR text using a more robust prompt.
    """
    
    # This new prompt gives examples and tells the AI what NOT to look for.
    prompt = f"""
You are an expert pharmacist. Your job is to parse the raw text from a medicine package and extract specific details.
The raw text is: "{raw_text}"

You MUST extract the following fields.
1.  **Name:** The brand name of the medicine (e.g., "Crocin", "Rantac 150", "Zenadol"). 
    This is almost always at the top and in the largest font.
    This is NOT an instruction (like "Store at room temperature"), a company name (like "GSK"), or an ingredient (like "Paracetamol").
2.  **MFG Date:** The manufacturing date (e.g., "04/2024", "MFG: 05/25").
3.  **Expiry Date:** The expiry date (e.g., "03/2026", "EXP: 04/27").
4.  **MRP:** The price (e.g., "Rs. 25.50", "MRP: ₹30.00").

If a field is not present in the text, you MUST return "Not Found".
Respond ONLY with a valid JSON object in the format below.

Example:
{{
  "Name": "Crocin Advance",
  "MFG Date": "Not Found",
  "Expiry Date": "10/2025",
  "MRP": "Rs. 20.00"
}}

JSON:
"""

    print(f"--- Extraction Agent DEBUG ---\nPrompting with text: {raw_text[:100]}...")

    try:
        response = ollama.chat(model='phi3', messages=[{'role': 'user', 'content': prompt}])
        response_text = response['message']['content']
        
        # Clean the response to ensure it's valid JSON
        # Find the first { and the last }
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            print(f"Extraction Agent ERROR: AI did not return a JSON object. Response: {response_text}")
            return {"Name": "Error: No JSON", "MFG Date": "Error", "Expiry Date": "Error", "MRP": "Error"}

        json_string = response_text[json_start:json_end]
        
        extracted_data = json.loads(json_string)
        
        # Check for expiry
        expiry_date = extracted_data.get('Expiry Date', 'Not Found')
        is_expired = False # Implement date comparison logic here if you want
        
        extracted_data['Is Expired'] = is_expired

        print(f"Extraction Agent: Extracted data -> {extracted_data}")
        return extracted_data

    except json.JSONDecodeError:
        print(f"Extraction Agent ERROR: Failed to decode JSON from AI response. Response: {response_text}")
        return {"Name": "Error: Bad JSON", "MFG Date": "Error", "Expiry Date": "Error", "MRP": "Error"}
    except Exception as e:
        print(f"Extraction Agent ERROR: {e}")
        return {"Name": "Error", "MFG Date": "Error", "Expiry Date": "Error", "MRP": "Error"}
