import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def process_notes_with_ai(extracted_text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing from environment variables."

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an advanced academic AI tutor. Process the following raw handwritten OCR text into an organized learning ecosystem.
    
    CRITICAL FORMATTING INSTRUCTIONS:
    - Output your entire response using the clear section divider tags: [CLEANED_TEXT], [SUMMARY], [CONCEPT_TREE], [REVISION_TIERS], [FLASHCARDS], [QUIZ], and [ANSWERS].
    
    - Under [CONCEPT_TREE], build a hierarchical bullet-point tree structure showing main topic down to subtopics (e.g., Main Topic -> Subtopic -> Details).
    
    - Under [REVISION_TIERS], generate a 1-sentence "Exam-Day Ultra Short Note" followed by a 3-bullet point "7-Day Core Concepts" summary.
    
    - Under [FLASHCARDS], generate exactly 4 to 5 critical technical terms or definitions found in the context. Format each flashcard on a single new line using a strict colon separator like this:
      Term Name : Precise clear definition string here
      Key Component : Structural explanation statement here
      
    - Under [QUIZ], generate exactly 5 multiple-choice questions based on the text context.
    Format each question EXACTLY like this:
      Q1: Question text here
      A) Option one
      B) Option two
      C) Option three
      D) Option four
      
    - Under [ANSWERS], list the correct option key for each question like this:
      Q1: B
      Q2: A
      Q3: C
      Q4: D
      Q5: A

    RAW EXTRACTED TEXT STACK:
    {extracted_text}
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI Generation processing failure: {str(e)}"