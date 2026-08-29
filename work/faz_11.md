# FAZ 11 — MLX Temelleri

> **Süre:** 2-3 Gün  
> **Amaç:** MiniLibX ile grafik pencere oluşturma ve temel çizim yapmayı öğrenmek.  
> **Şimdi grafik dünyasına geçiyoruz.**

---

## 🎯 Hedef

Bu fazın sonunda:
- MLX penceresi açabilmelisiniz
- Temel şekiller çizebilmelisiniz
- Klavye eventlerine tepki verebilmelisiniz
- Event loop mantığını anlayabilmelisiniz

---

## 📖 MiniLibX Nedir?

MiniLibX, 42 School tarafından geliştirilen **hafif grafik kütüphanesidir**.

```
MLX = Window + Image + Event System
```

| Özellik | Açıklama |
|---|---|
| **Pencere** | OS'un native penceresi |
| **Image buffer** | Pikselleri bellekte tutan yapı |
| **Event hooks** | Klavye, fare, pencere kapama |
| **Put pixel** | Tek tek piksel boyama |

---

## 📖 1. Window (Pencere)

### Temel Akış

```python
# SADECE MANTIK
mlx = mlx_init()                        # MLX bağlantısını başlat
win = mlx_new_window(mlx, 800, 600, "A-Maze-ing")  # Pencere aç
mlx_loop(mlx)                           # Event loop başlat (bloklayan!)
```

### Pencere Koordinat Sistemi

```
(0,0) ──────────────── (width,0)
  │                        │
  │       PENCERE          │
  │                        │
(0,height) ───── (width,height)
```

> ⚠️ Sol üst köşe (0,0) — y aşağı doğru artar!

---

## 📖 2. Event Loop

```
Event loop = sonsuz döngü
Her iterasyonda:
  - Kullanıcı inputu var mı? → Hook'ları çağır
  - Render gerekiyor mu? → Ekranı güncelle
  - Pencere kapatıldı mı? → Çık
```

### Hook Sistemi

```python
# SADECE MANTIK
def key_handler(keycode, param):
    if keycode == ESC_KEY:
        close_window()
    elif keycode == ENTER_KEY:
        toggle_solution()

mlx_key_hook(win, key_handler, None)   # Klavye hook'u kaydet
mlx_hook(win, DESTROY_EVENT, ...)      # Pencere kapama hook'u
mlx_loop(mlx)                          # Döngü başlat
```

---

## 📖 3. Drawing (Çizim)

### Pixel Çizimi

```python
# SADECE MANTIK
def put_pixel(img, x, y, color):
    # color = 0xRRGGBB formatında (hex)
    img.data[x + y * img.width] = color

# Renk örnekleri:
WHITE = 0xFFFFFF
BLACK = 0x000000
RED   = 0xFF0000
GREEN = 0x00FF00
BLUE  = 0x0000FF
```

### Image Buffer

```python
# SADECE MANTIK
img = mlx_new_image(mlx, width, height)   # Boş image yarat
# ... pikselleri doldur ...
mlx_put_image_to_window(mlx, win, img, 0, 0)  # Ekrana göster
```

**Neden image buffer?**

```
Doğrudan piksel çizmek → Her piksel için sys call → YAVAŞ
Image buffer → Bellekte doldur, bir kerede ekrana bas → HIZLI
```

---

## 📖 4. Images (Görüntüler)

### XPM Dosyası (42'nin image formatı)

```
/* XPM */
static char *image_data[] = {
"4 4 2 1",
". c #000000",  /* siyah */
"# c #FFFFFF",  /* beyaz */
"####",
"#..#",
"#..#",
"####"
};
```

```python
# SADECE MANTIK
img = mlx_xpm_file_to_image(mlx, "texture.xpm", &w, &h)
mlx_put_image_to_window(mlx, win, img, x, y)
```

---

## 📖 5. Keyboard Events

Yaygın tuş kodları:

| Tuş | Kod (macOS) |
|---|---|
| ESC | 53 |
| ENTER | 36 |
| Boşluk | 49 |
| OK (←) | 123 |
| Sağ (→) | 124 |
| Aşağı (↓) | 125 |
| Yukarı (↑) | 126 |
| W | 13 |
| A | 0 |
| S | 1 |
| D | 2 |

> ⚠️ Tuş kodları işletim sistemine göre değişir!

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| **Rendering pipeline** | **Event system** |
| mlx_init, window, image buffer | key_hook, mouse_hook, destroy_hook |
| put_pixel, renk formatı | Event loop mantığı |
| Birlikte: 100×100 renkli kare çizin | |

---

## ✏️ Mini Görev

### Görev 1 — Renk Hesaplama

Şu renklerin hex değerlerini hesaplayın:

| Renk | R | G | B | Hex |
|---|---|---|---|---|
| Kırmızı | 255 | 0 | 0 | `0xFF0000` |
| Yeşil | 0 | 255 | 0 | `?` |
| Mavi | 0 | 0 | 255 | `?` |
| Sarı | 255 | 255 | 0 | `?` |
| Mor | 128 | 0 | 128 | `?` |

### Görev 2 — Event Flow

Event loop'u şematik olarak çizin:
1. Kullanıcı 'S' tuşuna basar
2. key_handler çağrılır
3. Ne yapılmalı? (çözüm yolunu toggle)
4. Ekran nasıl güncellenir?

---

## ❓ Anlama Soruları

1. Event loop neden `mlx_loop()` ile başlar ve bloklayan bir döngüdür?
2. Image buffer neden doğrudan piksel çizmekten daha hızlıdır?
3. `0xRRGGBB` formatında sarı renk nasıl ifade edilir?
4. `mlx_hook` ile `mlx_key_hook` arasındaki fark nedir?
5. Pencere kapatma hook'u olmadan ne olur?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 11 — MLX Temelleri
Topics: MiniLibX, Window, Event Loop, Drawing, Images,
        Keyboard Events, pixel colors (0xRRGGBB), image buffer.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 11 Tamamlandı → Faz 12'ye Geçmeye Hazır
