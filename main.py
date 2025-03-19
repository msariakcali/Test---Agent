import os
import sys
from dotenv import load_dotenv

# Python modül yolunu ayarla - bu satır çok önemli!
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Şimdi doğrudan fonksiyonu import edelim
from pdf_reader import extract_text_from_pdf
from question_generator import QuestionGenerator
from question_verifier import QuestionVerifier

# .env dosyasından API anahtarını yükle
load_dotenv()

def main():
    """
    Ana uygulama fonksiyonu
    """
    # PDF dosya yolunu belirt
    pdf_path = "D:\\openaisdkpdfsoru\\pdfsoru.pdf"
    print(f"PDF dosyası okunuyor: {pdf_path}")
    
    # PDF dosyasından metin çıkar
    content = extract_text_from_pdf(pdf_path)
    
    if not content:
        print("PDF içeriği okunamadı.")
        return
    
    print(f"PDF başarıyla okundu. {len(content)} karakter içeriyor.")
    
    # Soru üreteci ve doğrulayıcı oluştur
    generator = QuestionGenerator()
    verifier = QuestionVerifier()
    
    # İçeriği çevir (gerekirse)
    translation_needed = input("PDF içeriği çevrilmeli mi? (E/H): ").strip().upper() == "E"
    if translation_needed:
        print("İçerik çevriliyor...")
        content = generator.translate_content(content)
        print("İçerik çevirisi tamamlandı.")
    
    # Sorular üret
    num_questions = int(input("Kaç soru üretmek istersiniz? (Varsayılan: 5): ") or "5")
    print(f"{num_questions} adet soru üretiliyor...")
    questions = generator.generate_questions(content, num_questions)
    
    # Soruları göster
    print("\n===== ÜRETİLEN SORULAR =====\n")
    for i, question in enumerate(questions, 1):
        print(f"SORU {i}: {question['question']}")
        print(f"A) {question['options']['A']}")
        print(f"B) {question['options']['B']}")
        print(f"C) {question['options']['C']}")
        print(f"D) {question['options']['D']}")
        print(f"DOĞRU CEVAP: {question['correct_answer']}")
        print(f"AÇIKLAMA: {question['explanation']}")
        print("\n" + "-"*50 + "\n")
    
    # Soruları doğrula
    verification_needed = input("Üretilen soruları doğrulamak istiyor musunuz? (E/H): ").strip().upper() == "E"
    if verification_needed:
        print("\nSorular doğrulanıyor...")
        verification_results = verifier.verify_questions(questions, content)
        
        # Doğrulama sonuçlarını göster
        print("\n===== DOĞRULAMA SONUÇLARI =====\n")
        for i, result in enumerate(verification_results, 1):
            print(f"SORU {i} DOĞRULAMASI:")
            print(result["verification"])
            print("\n" + "-"*50 + "\n")
    
    # Sonuçları kaydet
    save_needed = input("Sonuçları dosyaya kaydetmek istiyor musunuz? (E/H): ").strip().upper() == "E"
    if save_needed:
        with open("uretilen_sorular.txt", "w", encoding="utf-8") as f:
            for i, question in enumerate(questions, 1):
                f.write(f"SORU {i}: {question['question']}\n")
                f.write(f"A) {question['options']['A']}\n")
                f.write(f"B) {question['options']['B']}\n")
                f.write(f"C) {question['options']['C']}\n")
                f.write(f"D) {question['options']['D']}\n")
                f.write(f"DOĞRU CEVAP: {question['correct_answer']}\n")
                f.write(f"AÇIKLAMA: {question['explanation']}\n\n")
                
                if verification_needed:
                    f.write(f"DOĞRULAMA:\n{verification_results[i-1]['verification']}\n\n")
                f.write("-"*50 + "\n\n")
        
        print(f"Sonuçlar başarıyla 'uretilen_sorular.txt' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
