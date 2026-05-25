import easyocr
import cv2
import fitz  # PyMuPDF library
import os

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    image = cv2.imread(image_path)
    result = reader.readtext(image, detail=0)
    return " ".join(result)

def extract_text_from_pdf(pdf_path):
    # 1. Open the PDF file using PyMuPDF
    doc = fitz.open(pdf_path)
    final_extracted_text = ""
    
    # EasyOCR reader ni ready ga unchuko
    reader = easyocr.Reader(['en'])

    print(f"Total Pages Found in PDF: {len(doc)}")
    
    # 2. Loop through every page of the PDF
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Target: Prathi page ni high resolution image (pixmap) la marchali
        pix = page.get_pixmap(dpi=150) 
        image_path = f"temp_page_{page_num}.png"
        pix.save(image_path)  # Temporarily save image
        
        # 3. Pass this image to EasyOCR to extract handwriting
        print(f"Scanning Handwritten Text from Page {page_num + 1}...")
        image = cv2.imread(image_path)
        result = reader.readtext(image, detail=0)
        
        page_text = " ".join(result)
        final_extracted_text += page_text + " "
        
        # 4. Clean up: Temporary image ni delete cheseddam space free avvadaniki
        if os.path.exists(image_path):
            os.remove(image_path)
            
    return final_extracted_text.strip()