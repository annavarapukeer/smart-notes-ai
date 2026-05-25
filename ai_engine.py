from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
def process_notes_with_ai(extracted_text):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert academic assistant. Process the following raw text:
    
    TASK:
    1. Provide the [CLEANED_TEXT]: Fix all spelling/grammar mistakes from the OCR.
    2. Provide the [SUMMARY]: A concise summary of the key points.
    3. Provide the [QUIZ]: 5 Multiple Choice Questions.
    4. Provide the [ANSWERS]: The correct options.

    FORMAT:
    [CLEANED_TEXT]
    (Cleaned content here)
    
    [SUMMARY]
    (Summary here)
    
    [QUIZ]
    (Questions here)
    
    [ANSWERS]
    (Answers here)

    RAW TEXT:
    {extracted_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Gemini Cloud Error: {str(e)}"