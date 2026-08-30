# FAZ 0 — Proje Analizi

> **Süre:** ~1 Gün  
> **Amaç:** PDF'i teknik gereksinimlere çevirmek, projeyi tam olarak anlamak.  
> **Kaynak:** `a-maze-ing.pdf` (42 Kocaeli)

---

## 📌 Projenin Özeti

**A-Maze-ing**, bir labirent oluşturucu ve çözücü Python projesidir.

- Labirenti bir **config dosyasından** okuyarak veya **algoritmik olarak** üretirsin
- Üretilen labirenti **görsel olarak** gösterirsin (Terminal ASCII veya MiniLibX)
- Labirentin **en kısa çözüm yolunu** hesaplar ve gösterirsin
- Labirent oluşturma modülünü **pip ile kurulabilir bağımsız bir paket** olarak yayınlarsın

---

## ✅ ZORUNLU (Mandatory) Gereksinimler

### 1. Config Dosyası (Labirent Girdi Formatı)

```
# Labirent ASCII hex formatında tanımlanır
# Her satır bir hex değeri → 4 bit = 4 duvar (Kuzey/Güney/Doğu/Batı)
# Örnek: 9135... → her karakter bir hücrenin duvar bilgisi
```

| Gereksinim | Detay |
|---|---|
| Config dosyası formatı | Hex tabanlı ASCII, her karakter = 1 hücre |
| Hücre duvar kodlaması | 4 bit: bit3=N, bit2=S, bit1=E, bit0=W |
| Entry/Exit satırları | `entry (x,y)` ve `exit (x,y)` config'in sonunda |
| Komut satırı | `python3 ./a_maze_ing.py config.txt` |

**Config dosyası zorunlu kuralları:**
- Labirent hücreleri hexadecimal ASCII karakterler
- Her satır eşit uzunlukta
- Entry ve exit koordinatları belirtilmeli
- Labirent **perfect maze** olmalı (her hücreye tam 1 yol)

---

### 2. Output Dosyası (Çıktı Formatı)

Program `output_maze.txt` dosyası **üretmeli**:

```
# output_maze.txt örneği:
913955111555515395153
ac2a910282913855692c3a92
...
1,1      # entry (x,y)
19,14    # exit  (x,y)
ESEENEEESSSEENEE...  # Çözüm yolu: N/S/E/W harfleri
```

| Alan | Açıklama |
|---|---|
| Labirent satırları | Hex formatında, aynı config gibi |
| Entry koordinatı | `x,y # entry (x,y)` |
| Exit koordinatı | `x,y # exit (x,y)` |
| Çözüm yolu | N, S, E, W harflerinden oluşan string |

---

### 3. Görsel Gösterim (Visual Representation)

İki seçenekten **biri** zorunlu (biz ikisini de yapacağız → Bonus):

#### 3a. Terminal ASCII Rendering (Zorunlu)
- Duvarları, entry, exit ve çözüm yolunu açıkça göster
- Kullanıcı etkileşimi menüsü:
  1. Yeni labirent oluştur ve göster
  2. En kısa yolu göster / gizle
  3. Duvar renklerini değiştir
  4. Çık

#### 3b. MiniLibX (MLX) ile Grafik Gösterim (Bonus + Zorunlu seçenek)
- Pencerede grafik labirent render'ı
- Aynı kullanıcı etkileşimleri (tuş/tıklama ile)
- "42" pattern'ını labirente gömebilme (Bonus)

---

### 4. Labirent Oluşturma Algoritması

| Kural | Detay |
|---|---|
| Tip | **Perfect maze** → her hücreye tam 1 yol |
| Boyut | Config dosyasından okunur veya parametre olarak alınır |
| Seed | Tekrar üretilebilir olmalı (seed parametresi) |
| Çıktı | Hex formatında config dosyası ile aynı yapıda |

Öğrenilmesi gereken algoritmalar:
- **Recursive Backtracker (DFS)** → En yaygın, başlangıç için iyi
- **Prim's Algorithm** → Random ağaç tabanlı
- **Kruskal's Algorithm** → Edge tabanlı
- **Wilson's Algorithm** → Unbiased random walk (Bonus için)

---

### 5. Kısa Yol Bulma (Shortest Path)

| Gereksinim | Detay |
|---|---|
| Algoritma | Herhangi bir shortest path algoritması |
| Çıktı | N/S/E/W string olarak output dosyasına yaz |
| Görsel | Göster / gizle toggle |

Öğrenilmesi gereken algoritmalar:
- **BFS (Breadth-First Search)** → Garantili kısa yol, başlangıç için ideal
- **Dijkstra** → Ağırlıklı graflar için (unweighted mazede BFS = Dijkstra)
- **A* (A-Star)** → Heuristic tabanlı, daha hızlı (Bonus)

---

### 6. Kod Yeniden Kullanılabilirliği (Code Reusability)

> ⚠️ Bu madde **zorunlu** ve çok önemli!

| Gereksinim | Detay |
|---|---|
| Sınıf adı | `MazeGenerator` (veya benzeri) |
| Paket adı | `mazegen-*` (örn: `mazegen-1.0.0-py3-none-any.whl`) |
| Dağıtım | `pip` ile kurulabilir `.tar.gz` veya `.whl` |
| Dokümantasyon | Nasıl instantiate edilir, parametreler, örnek |
| LICENSE.md | Zorunlu, açık kaynak lisans seçimi |

**Paket arayüzü şunları desteklemeli:**
```python
from mazegen import MazeGenerator

gen = MazeGenerator(size=20, seed=42)
maze = gen.generate()
solution = gen.solve(entry=(1,1), exit=(19,14))
```

---

### 7. README.md Gereksinimleri

**Zorunlu bölümler:**
```
*This project has been created as part of the 42 curriculum by <login1>[, <login2>...].*

## Description
## Instructions
## Resources
```

**Ek zorunlu içerik (bu projede):**
- Config dosyasının tam yapısı ve formatı
- Seçilen labirent oluşturma algoritması
- Neden bu algoritmayı seçtiniz
- Kodun hangi kısmı yeniden kullanılabilir
- Ekip rolleri ve proje yönetimi
- Planlama ve nasıl evrildi
- Ne iyi çalıştı, ne geliştirilebilirdi
- Kullanılan araçlar

---

## ⭐ BONUS Gereksinimler

| # | Bonus | Açıklama |
|---|---|---|
| B1 | **Braided Maze** | Dead-end (çıkmaz) olmayan labirent. `--max-dead-ends 0` ile doğrulanabilir |
| B2 | **Çoklu Algoritmalar** | Birden fazla labirent üretme algoritması desteği |
| B3 | **Üretim Animasyonu** | Labirent oluştururken adım adım animasyon |
| B4 | **MLX Grafik Gösterim** | MiniLibX ile pencere tabanlı render |
| B5 | **"42" Pattern** | Duvar renklerini "42" şeklinde ayarlama seçeneği |

---

## 🛠️ Kullanılacak Teknolojiler

| Teknoloji | Kullanım Amacı |
|---|---|
| **Python 3** | Ana dil |
| **MiniLibX (MLX)** | Grafik pencere (bonus) |
| **setuptools / build** | `pip` paketi oluşturma |
| **venv / virtualenv** | Geliştirme ortamı |
| **Git** | Versiyon kontrolü |
| **LICENSE.md** | Açık kaynak lisanslama (MIT, GPL, vs.) |

---

## 📚 Faz 0'da Öğrenilecekler

### Requirement Analysis
- [ ] PDF'deki her chapter'ı okuyup madde madde not al
- [ ] Zorunlu ile bonus'u birbirinden net ayır
- [ ] Hangi şartın nerede kontrol edildiğini anla (evaluation script)

### Feature Breakdown
- [ ] Config okuma → hex decode → 2D grid yapısı
- [ ] Labirent üretme → perfect maze algoritması
- [ ] Kısa yol bulma → BFS/Dijkstra
- [ ] Terminal render → ASCII duvar çizimi
- [ ] MLX render → grafik pencere (bonus)
- [ ] Output dosyası yazma
- [ ] pip paketi oluşturma

### Milestone Mantığı
- [ ] Her faz bir çalışan çıktı üretmeli
- [ ] Bonus'lar mandatory tamamlandıktan sonra eklenmeli
- [ ] Test edilmeden bir sonraki faza geçilmemeli

---

## 🗂️ Teslim Kriterleri (Delivery Criteria)

| Kriter | Açıklama |
|---|---|
| Git repo | Proje Git'te olmalı |
| `mazegen-*.whl` veya `.tar.gz` | Repo kök dizininde pip paketi |
| `LICENSE.md` | Repo kök dizininde |
| `README.md` | Repo kök dizininde, tüm zorunlu bölümlerle |
| Çalışır program | `python3 ./a_maze_ing.py config.txt` çalışmalı |
| Output dosyası | `output_maze.txt` doğru formatta üretilmeli |
| Görsel | Terminal veya MLX ile labirent görüntülenmeli |

### Değerlendirme Sırasında Sorulan Şeyler:
1. Virtualenv/venv içinde `pip install mazegen-*.whl` çalıştırılacak
2. Paket tekrar build edilecek (source'dan)
3. Config dosyası verilecek, çıktı kontrol edilecek
4. En kısa yol doğruluk kontrolü yapılacak
5. Görsel render gösterilecek
6. README içeriği sorgulanacak

---

## 🧠 Faz 0 Çıktısı (Bu Dosyanın Amacı)

Bu faz tamamlandığında elimizde olacaklar:

- [x] Tüm zorunlu gereksinimlerin listesi
- [x] Tüm bonus gereksinimlerin listesi
- [x] Teslim kriterlerinin listesi
- [x] Kullanılacak teknoloji stack'i
- [x] Öğrenilmesi gereken konular
- [ ] **Faz 1'e geçmeye hazır** → Proje kurulumu ve dosya yapısı

---

## 🔗 Sonraki Adım

**→ Faz 1:** Geliştirme ortamı kurulumu, dosya yapısı, hex parsing ve config okuma.
