import sys
import re
import os
from collections import Counter
from typing import Dict, List, Tuple, Set, Optional

# Windows terminalinde Türkçe karakterlerin bozulmasını engellemek için
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


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


# Temel Gömülü Türkçe Dolgu Kelimeleri (Harici dosya bulunamadığında kullanılır)
DEFAULT_TURKISH_STOPWORDS: Set[str] = {
    # Zamirler
    "ben", "sen", "o", "biz", "siz", "onlar", "bana", "sana", "ona", "bize", "size", "onlara",
    "beni", "seni", "onu", "bizi", "sizi", "onları", "bende", "sende", "onda", "bizde", "sizde",
    "onlarda", "benden", "senden", "ondan", "bizden", "sizden", "onlardan", "benim", "senin",
    "onun", "bizim", "sizin", "onların", "kendi", "kendisi", "kendim", "kendin", "kendimiz",
    "kendiniz", "kendileri", "kendine", "kendini", "kendinde", "kendinden", "kendisinden",
    "kendisinin", "kim", "kimi", "kime", "kimde", "kimden", "kimin", "kimisi", "kimse",
    "kimseye", "kimseyi", "kimseden", "kimsenin", "ne", "neyi", "neye", "nede", "neden",
    "neyin", "nesi", "neler", "nereye", "nerede", "nereden", "neresi", "neredeyse",
    "burası", "şurası", "orası", "buraya", "şuraya", "oraya", "burada", "şurada", "orada",
    "buradan", "şuradan", "oradan", "burayı", "şurayı", "orayı", "bu", "şu", "buna", "şuna",
    "bunda", "şunda", "bundan", "şundan", "bunu", "şunu", "bunun", "şunun", "bunlar", "şunlar",
    "bunlara", "şunlara", "bunları", "şunları", "bunlarda", "şunlarda", "bunlardan", "şunlardan",
    "bunların", "şunların", "hepsi", "hepsine", "hepsini", "hepsinde", "hepsinden", "hepsinin",
    "herkes", "herkese", "herkesi", "herkeste", "herkesten", "herkesin", "hiçbir", "hiçbiri",
    "hiçbirine", "hiçbirini", "hiçbirinde", "hiçbirinden", "hiçbirinin", "birçoğu", "bazı",
    "bazısı", "bazıları", "bazılarına", "bazılarını", "bazılarında", "bazılarından", "biri",
    "birisi", "birine", "birini", "birinde", "birinden", "birinin", "birkaçı", "tümü", "çoğu",
    "birbiri", "birbirine", "birbirini", "birbirinde", "birbirinden",

    # Bağlaçlar
    "ve", "veya", "veyahut", "yahut", "ya", "de", "da", "dahi", "bile", "ama", "fakat",
    "lakin", "ancak", "yalnız", "oysa", "oysaki", "halbuki", "meğer", "meğerse", "madem",
    "mademki", "çünkü", "zira", "ki", "ile", "hem", "gerek", "ister", "olsun", "ayrıca",
    "üstelik", "hatta", "nitekim", "demek", "yani",

    # Edatlar & İlgeçler
    "için", "gibi", "kadar", "göre", "doğru", "karşı", "karşın", "rağmen", "dolayı", "ötürü",
    "beri", "yana", "itibaren", "itibariyle", "itibarıyla", "üzere", "vasıtasıyla", "yoluyla",
    "aracılığıyla", "nedeniyle", "sebebiyle", "takdirde", "sürece", "boyunca", "esnasında",
    "sırasında", "zarfında", "halinde", "dair", "ait", "ilişkin", "yönelik", "nazaran",

    # Zarflar
    "daha", "en", "pek", "çok", "az", "biraz", "fazla", "hayli", "oldukça", "büsbütün",
    "tamamen", "gayet", "kısmen", "derhal", "hemen", "henüz", "şimdi", "demin", "artık",
    "hala", "hâlâ", "halen", "evvel", "sonra", "ansızın", "birden", "birdenbire", "aniden",
    "öyle", "böyle", "şöyle", "nasıl", "niçin", "niye", "asla", "katiyen", "kesinlikle",
    "mutlaka", "muhakkak", "kuşkusuz", "şüphesiz", "elbette", "tabii", "tabiki", "tabi",
    "sanki", "güya", "adeta", "âdeta", "keşke", "bari", "tek", "salt", "sırf", "sadece",
    "yalnızca", "zaten", "genelde", "genellikle", "çoğunlukla", "bazen", "nadiren", "sıklıkla",
    "devamlı", "sürekli", "daima", "hep", "yeniden", "yine", "gene", "tekrar", "özellikle",
    "bilhassa", "aslında",

    # Soru & Ek Fiil & Durum Sözcükleri
    "mı", "mi", "mu", "mü", "mısın", "misin", "musun", "müsün", "mıyız", "miyiz", "muyuz",
    "müyüz", "mısınız", "misiniz", "musunuz", "müsünüz", "mıdır", "midir", "mudur", "müdür",
    "mıydı", "miydi", "muydu", "müydü", "mıysa", "miyse", "acaba", "hani", "peki", "tamam",
    "hayır", "evet", "yok", "var", "vardı", "yoktu", "yoksa", "varsa", "şey", "şeyler",

    # Yardımcı Fiil ve Ek-Eylem Çekimleri
    "olmak", "olan", "olarak", "oldu", "olduk", "oldular", "olduğu", "olduğunu", "olduğuna",
    "olduğunda", "olur", "olurlar", "olmaz", "olsun", "olmalı", "olabilir", "olması", "olup",
    "etmek", "eden", "ederek", "etti", "ettik", "ettiler", "ettiği", "ettiğini", "ettiğine",
    "ettiğinde", "eder", "ederler", "etmez", "etse", "etmeli", "edebilir", "etmesi", "edip",
    "yapmak", "yapan", "yaparak", "yaptı", "yaptık", "yaptığı", "yaptığını", "yapar", "yapmaz",
    "ise", "idi", "imiş", "ken", "iken",

    # Sayılar & Miktar Belirteçleri
    "sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on",
    "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan", "yüz", "bin",
    "milyon", "milyar", "trilyon", "birinci", "ikinci", "üçüncü", "ilk", "son", "tek", "çift",
    "tüm", "bütün", "her", "hiç", "birkaç", "tane", "adet", "defa", "kere", "kez", "sefer"
}


def parse_and_clean_words(text: str) -> List[str]:
    """
    Metni kelimelere ayrıştırır, noktalama işaretlerini ve sayıları temizler,
    Türkçe kurallara uygun olarak küçük harfe çevirir.
    """
    lowered = turkish_lower(text)
    # Sadece Türkçe ve Latin harflerden oluşan kelimeleri yakalar
    words = re.findall(r"[abcçdefgğhıijklmnoöprsştuüvyz]+", lowered)
    return words


def load_stopwords_from_file(file_path: str = "stopwords.txt") -> Set[str]:
    """
    stopwords.txt dosyasından kelimeleri okur ve temiz bir küme (set) olarak döner.
    Dosyadaki boş satırları, yorumları (#) ve çok kelimeli satırları kelime kelime ayrıştırır.
    """
    stopwords = set()
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Satırdaki her kelimeyi ayrıştır ve Türkçe kuralla küçült
                    words = parse_and_clean_words(line)
                    stopwords.update(words)
        except Exception as e:
            print(f"[Uyarı] '{file_path}' dosyası okunamadı: {e}. Varsayılan liste kullanılıyor.")
            return set(DEFAULT_TURKISH_STOPWORDS)
    else:
        return set(DEFAULT_TURKISH_STOPWORDS)
    return stopwords


# Aktif Stopwords Kümesi (varsayılan olarak stopwords.txt varsa onu, yoksa DEFAULT'u yükler)
CURRENT_STOPWORDS: Set[str] = load_stopwords_from_file("stopwords.txt")


def add_stopwords(words: List[str] | Set[str]):
    """Stopword listesine dinamik olarak yeni kelimeler ekler."""
    global CURRENT_STOPWORDS
    for w in words:
        cleaned = parse_and_clean_words(w)
        CURRENT_STOPWORDS.update(cleaned)


def remove_stopwords(words: List[str] | Set[str]):
    """Stopword listesinden belirli kelimeleri çıkarır."""
    global CURRENT_STOPWORDS
    for w in words:
        cleaned = parse_and_clean_words(w)
        CURRENT_STOPWORDS.difference_update(cleaned)


def analyze_text(text: str, custom_stopwords: Optional[Set[str]] = None) -> Dict:
    """
    Metni analiz eder:
    - Kelime ayrıştırma
    - Stopword filtreleme
    - Frekans analizi
    """
    stopwords = CURRENT_STOPWORDS if custom_stopwords is None else custom_stopwords
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
        "aktif_stopword_havuzu_sayisi": len(stopwords),
        "en_cok_gecen_kelimeler": word_counts.most_common(10),
        "cikarilan_stopword_frekanslari": stopword_counts.most_common(10),
        "temiz_kelimeler_listesi": filtered_words,
        "butun_kelime_frekanslari": dict(word_counts),
    }


def print_analysis_report(analysis: Dict):
    """Analiz sonuçlarını düzenli bir tablo şeklinde ekrana yazdırır."""
    print("=" * 60)
    print(" METİN KELİME ANALİZ RAPORU")
    print("=" * 60)
    print(f"Toplam Kelime Sayısı         : {analysis['toplam_kelime_sayisi']}")
    print(f"Çıkarılan Stopword Sayısı    : {analysis['cikarilan_stopword_sayisi']}")
    print(f"Kalan Anlamlı Kelime Sayısı  : {analysis['filtrelenmis_kelime_sayisi']}")
    print(f"Benzersiz Anlamlı Kelime     : {analysis['benzersiz_kelime_sayisi']}")
    print(f"Kullanılan Stopword Havuzu   : {analysis['aktif_stopword_havuzu_sayisi']} kelime")
    print("-" * 60)
    
    print("\n En Sık Geçen Anlamlı Kelimeler (İlk 10):")
    if analysis["en_cok_gecen_kelimeler"]:
        for rank, (word, count) in enumerate(analysis["en_cok_gecen_kelimeler"], start=1):
            percentage = (count / max(analysis['filtrelenmis_kelime_sayisi'], 1)) * 100
            print(f"  {rank:2d}. {word:<15} : {count:3d} kez (%{percentage:.1f})")
    else:
        print("  (Anlamlı kelime bulunamadı, tüm kelimeler stopword olarak elendi)")

    print("\n Çıkarılan Bazı Stopword'ler:")
    if analysis["cikarilan_stopword_frekanslari"]:
        for rank, (sw, count) in enumerate(analysis["cikarilan_stopword_frekanslari"], start=1):
            print(f"  {rank:2d}. {sw:<15} : {count:3d} kez")
    else:
        print("  (Metinde stopword tespit edilmedi)")
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print(" TÜRKÇE METİN AYRIŞTIRICI & KELİME ANALİZ ARACI")
    print(f" (Yüklü Stopword Havuzu: {len(CURRENT_STOPWORDS)} kelime)")
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
