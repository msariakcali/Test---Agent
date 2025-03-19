import os
import sys

def setup_environment():
    """
    Gerekli kütüphaneleri kurar ve ortamı hazırlar
    """
    print("Gerekli kütüphaneler kuruluyor...")
    os.system("pip install -r requirements.txt")
    print("Kurulum tamamlandı!")

if __name__ == "__main__":
    setup_environment()
    
    print("\n===== PDF Soru Üretme ve Doğrulama Sistemi =====\n")
    
    # Python'un modülleri doğru konumdan yüklemesini sağla
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from main import main
    main()
