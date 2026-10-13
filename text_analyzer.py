import sys
import re
from collections import Counter
from typing import Dict, List, Tuple, Set

# Windows terminalinde Türkçe karakterlerin bozulmasını engellemek için
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Standart Türkçe Dolgu Kelimeleri (Stopwords) Listesi
TURKISH_STOPWORDS: Set[str] = {
    "acaba", "altı", "ama", "ancak", "artık", "asla", "aslında", "az",
    "bana", "bazen", "bazı", "bazıları", "bazısına", "belki", "ben", "beni", "benim",
    "beri", "beş", "bile", "bin", "bir", "biraz", "biri", "birkaç", "birkaçı", "birlikte",
    "biz", "bize", "bizi", "bizim", "böyle", "böylece", "bu", "buna", "bunda", "bundan",
    "bunu", "bunun", "burada", "bütün", "çoğu", "çoğuna", "çoğunu", "çok", "çünkü",
    "da", "daha", "dahi", "de", "defa", "değil", "diye", "doksan", "dokuz", "dolayı",
    "dört", "elli", "en", "fakat", "gibi", "göre", "halen", "hangi", "hangisi", "hani",
    "hatta", "hem", "henüz", "hep", "hepsi", "hepsine", "hepsini", "her", "herkes",
    "herkese", "herkesi", "hiç", "hiçbir", "hiçbiri", "için", "iki", "ile", "ilgili",
    "ise", "itibaren", "itibariyle", "kadar", "karşın", "katrilyon", "kendi", "kendine",
    "kendini", "kendisi", "kırk", "kim", "kime", "kimi", "kimse", "madem", "mı", "mi",
    "milyar", "milyon", "mu", "mü", "nasıl", "ne", "neden", "nerde", "nerede", "nereye",
    "nesi", "neyse", "niçin", "niye", "ona", "ondan", "onlar", "onlara", "onlardan",
    "onların", "onlarca", "onu", "onun", "otuz", "oysa", "öyle", "pek", "rağmen",
    "sadece", "sanki", "sekiz", "seksen", "sen", "senden", "seni", "senin", "siz",
    "sizden", "size", "sizi", "sizin", "sonra", "şayet", "şey", "şeyler", "şimdi",
    "şöyle", "şu", "şuna", "şunda", "şundan", "şunlar", "şunu", "şunun", "tabi",
    "tamam", "tarafından", "trilyon", "tüm", "üç", "üzere", "var", "vardı", "ve",
    "veya", "veyahut", "ya", "yahut", "yalnız", "yani", "yedi", "yetmiş", "yine",
    "yok", "yoksa", "yüz", "zaten"
}


def turkish_lower(text: str) -> str:
    """
    Türkçe karakter kurallarına uygun olarak metni küçük harfe çevirir.
    Standart str.lower() 'I' harfini 'i' yapar. Bu fonksiyon 'I' -> 'ı', 'İ' -> 'i' yapar.
    """
    tr_map = {
        ord("I"): "ı",
        ord("İ"): "i",
    }
    return text.translate(tr_map).lower()


def parse_and_clean_words(text: str) -> List[str]:
    """
    Metni kelimelere ayrıştırır, noktalama işaretlerini ve sayıları temizler,
    Türkçe kurallara uygun olarak küçük harfe çevirir.
    """
    lowered = turkish_lower(text)
    # Sadece Türkçe ve Latin harflerden oluşan kelimeleri yakalar
    words = re.findall(r"[abcçdefgğhıijklmnoöprsştuüvyz]+", lowered)
    return words


def analyze_text(text: str, custom_stopwords: Set[str] = None) -> Dict:
    """
    Girilen metni analiz eder:
    - Kelime ayrıştırma
    - Stopword filtreleme
    - Frekans analizi
    """
    stopwords = TURKISH_STOPWORDS if custom_stopwords is None else custom_stopwords
    all_words = parse_and_clean_words(text)
    
    total_words = len(all_words)
    filtered_words = [w for w in all_words if w not in stopwords]
    removed_stopwords = [w for w in all_words if w in stopwords]
    
    word_counts = Counter(filtered_words)
    stopword_counts = Counter(removed_stopwords)
    
    return {
        "toplam_kelime_sayisi": total_words,
        "filtrelenmis_kelime_sayisi": len(filtered_words),
        "cikarilan_stopword_sayisi": len(removed_stopwords),
        "benzersiz_kelime_sayisi": len(word_counts),
        "en_cok_gecen_kelimeler": word_counts.most_common(10),
        "cikarilan_stopword_frekanslari": stopword_counts.most_common(10),
        "temiz_kelimeler_listesi": filtered_words,
        "butun_kelime_frekanslari": dict(word_counts),
    }


def print_analysis_report(analysis: Dict):
    """Analiz sonuçlarını okunabilir bir formatta ekrana basar."""
    print("=" * 60)
    print(" METİN KELİME ANALİZ RAPORU")
    print("=" * 60)
    print(f"Toplam Kelime Sayısı         : {analysis['toplam_kelime_sayisi']}")
    print(f"Çıkarılan Stopword Sayısı    : {analysis['cikarilan_stopword_sayisi']}")
    print(f"Kalan Anlamlı Kelime Sayısı  : {analysis['filtrelenmis_kelime_sayisi']}")
    print(f"Benzersiz Anlamlı Kelime     : {analysis['benzersiz_kelime_sayisi']}")
    print("-" * 60)
    
    print("\n En Sık Geçen Anlamlı Kelimeler (İlk 10):")
    for rank, (word, count) in enumerate(analysis["en_cok_gecen_kelimeler"], start=1):
        percentage = (count / max(analysis['filtrelenmis_kelime_sayisi'], 1)) * 100
        print(f"  {rank:2d}. {word:<15} : {count:3d} kez (%{percentage:.1f})")

    print("\n Çıkarılan Bazı Stopword'ler:")
    for rank, (sw, count) in enumerate(analysis["cikarilan_stopword_frekanslari"], start=1):
        print(f"  {rank:2d}. {sw:<15} : {count:3d} kez")
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print(" TÜRKÇE METİN AYRIŞTIRICI & KELİME ANALİZ ARACI")
    print("=" * 60)
    
    kullanici_metni = input("\nAnaliz edilecek metni girin (Örnek metin için boş bırakıp Enter'a basın):\n> ").strip()
    
    if not kullanici_metni:
        print("\n[Bilgi] Metin girilmedi, varsayılan örnek metin analiz ediliyor...\n")
        kullanici_metni = """
        Yapay zeka ve makine öğrenmesi günümüzde çok hızlı bir şekilde gelişiyor. 
        Bu gelişmeler ile birlikte veri analizi, doğal dil işleme gibi alanlar daha da önem kazandı. 
        Ancak veri temizliği ve metin ayrıştırma adımları olmadan başarılı bir model eğitmek neredeyse imkansızdır. 
        Biz de bu yüzden veriyi dikkatle inceliyor ve en iyi sonucu almak için çalışıyoruz.
        """
        
    sonuc = analyze_text(kullanici_metni)
    print_analysis_report(sonuc)
