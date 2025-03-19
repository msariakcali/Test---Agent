import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """
    PDF dosyasından metin çıkarır.
    
    Args:
        pdf_path (str): PDF dosyasının yolu
        
    Returns:
        str: PDF'ten çıkarılan metin
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF dosyası bulunamadı: {pdf_path}")
    
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return None
