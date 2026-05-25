from google import genai

def process_notes_with_ai(extracted_text):
    client = genai.Client(api_key='AIzaSyCoJyXzQfuliwVfCFoiIuTH_38FApc9D1o')
    
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