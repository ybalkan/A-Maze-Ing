# FAZ 00 — Proje Analizi

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

| Gereksinim | Detay |
|---|---|
| Config dosyası formatı | Hex tabanlı ASCII, her karakter = 1 hücre |
| Hücre duvar kodlaması | 4 bit: bit3=N, bit2=S, bit1=E, bit0=W |
| Entry/Exit satırları | `entry (x,y)` ve `exit (x,y)` config'in sonunda |
| Komut satırı | `python3 ./a_maze_ing.py config.txt` |

### 2. Output Dosyası

```
913955111555515395153
ac2a910282913855692c3a92
1,1      # entry (x,y)
19,14    # exit  (x,y)
ESEENEEESSSEENEE...  # Çözüm yolu: N/S/E/W
```

### 3. Görsel Gösterim

- Terminal ASCII render (zorunlu)
- MiniLibX grafik render (bonus)
- Menü: yeni üret / yolu göster-gizle / renk değiştir / çık

### 4. Labirent Oluşturma

- **Perfect maze** → her hücreye tam 1 yol
- Seed ile tekrar üretilebilir

### 5. Kısa Yol Bulma

- Herhangi bir shortest path algoritması
- Çıktı N/S/E/W string olarak

### 6. pip Paketi (Zorunlu!)

```python
from mazegen import MazeGenerator
gen = MazeGenerator(size=20, seed=42)
maze = gen.generate()
solution = gen.solve(entry=(1,1), exit=(19,14))
```

- Paket adı: `mazegen-*`
- `.whl` veya `.tar.gz` olarak repo kökünde
- `LICENSE.md` zorunlu

### 7. README Gereksinimleri

Zorunlu bölümler: Description · Instructions · Resources  
Proje spesifik: config formatı, algoritma seçimi nedeni, ekip rolleri, planlama süreci

---

## ⭐ BONUS Gereksinimler

| # | Bonus | Açıklama |
|---|---|---|
| B1 | **Braided Maze** | Dead-end olmayan labirent (`--max-dead-ends 0`) |
| B2 | **Çoklu Algoritmalar** | Birden fazla üretme algoritması desteği |
| B3 | **Üretim Animasyonu** | Adım adım animasyon |
| B4 | **MLX Grafik** | MiniLibX ile pencere render |
| B5 | **"42" Pattern** | Duvar renkleriyle "42" yazısı |

---

## 🛠️ Kullanılacak Teknolojiler

| Teknoloji | Kullanım Amacı |
|---|---|
| Python 3 | Ana dil |
| MiniLibX (MLX) | Grafik pencere |
| setuptools / build | pip paketi oluşturma |
| venv / virtualenv | Geliştirme ortamı |
| Git | Versiyon kontrolü |

---

## 🗂️ Teslim Kriterleri

| Kriter | Açıklama |
|---|---|
| Git repo | Proje Git'te olmalı |
| `mazegen-*.whl` | Repo kökünde |
| `LICENSE.md` | Repo kökünde |
| `README.md` | Tüm zorunlu bölümlerle |
| `python3 ./a_maze_ing.py config.txt` | Çalışmalı |
| `output_maze.txt` | Doğru formatta üretilmeli |

---

## ✔️ Faz 00 Tamamlandı → Faz 01'e Geçmeye Hazır
