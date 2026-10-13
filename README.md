# Turkish Text Analyzer (Türkçe Metin Ayrıştırıcı ve Stopword Temizleyici)

Saf Python standart kütüphaneleri kullanılarak geliştirilmiş, harici bağımlılık gerektirmeyen, Türkçe dil kurallarına (büyük/küçük harf dönüşümleri ve karakter seti) uyumlu metin ayrıştırma, frekans analizi ve dolgu kelimesi (stopword) temizleme aracı.

---

## Özellikler

- **Harici Bağımlılık Yok**: Yalnızca standart Python kütüphaneleri (`re`, `collections`, `sys`) kullanılır. `pip install` gerektirmez.
- **Türkçe Harf Uyumluluğu**: Python'ın varsayılan `.lower()` metodunun yol açtığı `I -> i` hatasını önleyen özel `turkish_lower` fonksiyonu (`I -> ı`, `İ -> i`).
- **Kapsamlı Stopword Listesi**: Türkçede en sık kullanılan dolgu kelimeleri, bağlaçlar ve edatları barındıran zengin liste.
- **Detaylı Frekans & İstatistik Raporu**:
  - Toplam kelime sayısı
  - Çıkarılan stopword sayısı
  - Kalan anlamlı kelime sayısı
  - Benzersiz kelime sayısı
  - En sık geçen kelimelerin frekansları ve yüzde oranları
- **Etkileşimli (Interactive) CLI**: Kendi metninizi konsola yapıştırabilir veya boş bırakıp Enter'a basarak hazır test metnini inceleyebilirsiniz.

---

## Kurulum & Çalıştırma

Projeyi klonlayın:
```bash
git clone https://github.com/ysinduman/turkish-text-analyzer.git
cd turkish-text-analyzer
```

Programı çalıştırın:
```bash
python text_analyzer.py
```

---

## Kod İçinde Kullanım (Kütüphane Olarak)

```python
from text_analyzer import analyze_text, print_analysis_report

metin = "Yapay zeka ve veri bilimi geleceğin en önemli teknolojileridir."

# Analiz sonucunu sözlük (dict) olarak alma
sonuclar = analyze_text(metin)

# Veya konsola biçimlendirilmiş rapor yazdırma
print_analysis_report(sonuclar)
```

### Örnek Çıktı:
```text
============================================================
 METİN KELİME ANALİZ RAPORU
============================================================
Toplam Kelime Sayısı         : 4
Çıkarılan Stopword Sayısı    : 2
Kalan Anlamlı Kelime Sayısı  : 2
Benzersiz Anlamlı Kelime     : 2
------------------------------------------------------------

 En Sık Geçen Anlamlı Kelimeler (İlk 10):
   1. meyveleri       :   1 kez (%50.0)
   2. severim         :   1 kez (%50.0)

 Çıkarılan Bazı Stopword'ler:
   1. ben             :   1 kez
   2. çok             :   1 kez
============================================================
```

---

## Lisans
MIT
