def extract_text_with_ocr(file_path: Path) -> str:
    print("⚠ No selectable text found. Running OCR...")

  #This poopler_path we need to install
    poppler_path = r"C:\Release-25.12.0-0\poppler-25.12.0\Library\bin"
  
    images = pdf2image.convert_from_path(file_path, poppler_path=poppler_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)
    
    print("OCR function")    
    text = text.strip()
    with open("ocr.txt", "w", encoding="utf-8") as f:
        f.write(text)

    return text
