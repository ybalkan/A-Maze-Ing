# FAZ 12 — MLX Maze Renderer

> **Süre:** 2 Gün  
> **Amaç:** Labirenti MLX penceresiyle grafik olarak çizmek.  
> **Maze → Piksel koordinatlarına dönüşüm.**

---

## 🎯 Hedef

Bu fazın sonunda:
- Labirent hücrelerini ekran koordinatlarına dönüştürebilmelisiniz
- Duvarları çizgi (piksel dizisi) olarak çizebilmelisiniz
- Çözüm yolunu renkli olarak gösterebilmelisiniz

---

## 📖 1. Coordinate Mapping (Koordinat Dönüşümü)

Labirent grid koordinatlarını → ekran piksel koordinatlarına dönüştürme:

### Temel Formül

```
CELL_SIZE = 40   # Her hücre 40×40 piksel

ekran_x = grid_x * CELL_SIZE
ekran_y = grid_y * CELL_SIZE
```

### Örnek

```
Grid hücresi (3, 2) → Ekran konumu:
  x = 3 * 40 = 120 piksel
  y = 2 * 40 = 80  piksel
```

```
                  Ekranda:
Grid:             0    40   80  120  160
(0,0)(1,0)(2,0)   ┌────┬────┬────┬────┐  ← y=0
(0,1)(1,1)(2,1)   │    │    │    │    │
                  ├────┼────┼────┼────┤  ← y=40
(0,2)(1,2)(2,2)   │    │    │    │    │
                  ├────┼────┼────┼────┤  ← y=80
                  │    │    │ ↑  │    │
                  │    │    │(3,2)│   │  ← y=120
                  └────┴────┴────┴────┘
```

---

## 📖 2. Scaling (Ölçekleme)

Pencere boyutuna göre dinamik hücre boyutu:

```python
# SADECE MANTIK
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600
MAZE_WIDTH    = 20   # hücre sayısı
MAZE_HEIGHT   = 15

cell_w = WINDOW_WIDTH  // MAZE_WIDTH    # = 40
cell_h = WINDOW_HEIGHT // MAZE_HEIGHT   # = 40

# Eşit olmayabilir → en küçüğünü kullan (kare hücreler için)
CELL_SIZE = min(cell_w, cell_h)
```

---

## 📖 3. Drawing Walls (Duvar Çizme)

Her hücre için 4 duvar, her duvar = piksel çizgisi:

```python
# SADECE MANTIK

# Hücre (grid_x, grid_y) için:
px = grid_x * CELL_SIZE   # piksel başlangıç x
py = grid_y * CELL_SIZE   # piksel başlangıç y

# NORTH duvarı:    (px, py) → (px+CELL_SIZE, py)
# SOUTH duvarı:    (px, py+CELL_SIZE) → (px+CELL_SIZE, py+CELL_SIZE)
# WEST  duvarı:    (px, py) → (px, py+CELL_SIZE)
# EAST  duvarı:    (px+CELL_SIZE, py) → (px+CELL_SIZE, py+CELL_SIZE)

def draw_line(img, x0, y0, x1, y1, color):
    # Yatay veya dikey çizgi için piksel döngüsü
    if y0 == y1:  # yatay
        for x in range(x0, x1+1):
            put_pixel(img, x, y0, color)
    else:         # dikey
        for y in range(y0, y1+1):
            put_pixel(img, x0, y, color)
```

---

## 📖 4. Renk Şeması

| Eleman | Renk Önerisi | Hex |
|---|---|---|
| Arka plan | Koyu gri | `0x1A1A2E` |
| Duvarlar | Açık mavi | `0x16213E` veya beyaz |
| Yol (passage) | Siyah | `0x000000` |
| Çözüm yolu | Yeşil / sarı | `0x00FF88` |
| Entry | Mavi | `0x0080FF` |
| Exit | Kırmızı | `0xFF4444` |

---

## 📖 5. Tam Render Akışı

```
1. MLX init → Pencere aç
2. Image buffer oluştur
3. Arka planı boyama (fill ile)
4. Her hücre için:
   a. Hangi duvarlar var? (bitmask kontrol)
   b. O duvarları çiz (draw_line)
5. Entry ve Exit'i özel renkle işaretle
6. Çözüm yolu gösterilecekse → path hücrelerini boya
7. Image'ı pencereye koy
8. Event loop → güncelleme gerekirse yeniden render
```

---

## 📖 6. Refresh Stratejisi

Event geldiğinde (tuş, fare) labirenti yeniden çizmek:

```python
# SADECE MANTIK
def render_all(state):
    clear_image(img)          # Önceki frame'i temizle
    draw_maze(img, state.maze)
    if state.show_solution:
        draw_solution(img, state.solution_path)
    mlx_put_image_to_window(mlx, win, img, 0, 0)
```

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| **Coordinate mapping** | **Event system** |
| grid → piksel dönüşümü | Tuş basımı → render refresh |
| Scaling hesaplaması | Çözüm toggle, yeni maze üretme |
| draw_wall fonksiyonu | Pencere boyutlandırma |

---

## ✏️ Mini Görev

### Görev — Koordinat Hesaplama

CELL_SIZE = 30 için şu hücrelerin ekran koordinatlarını hesaplayın:

| Grid (x,y) | Ekran sol üst (px, py) | Ekran sağ alt |
|---|---|---|
| (0, 0) | (0, 0) | (30, 30) |
| (1, 0) | (?, ?) | (?, ?) |
| (2, 3) | (?, ?) | (?, ?) |
| (5, 4) | (?, ?) | (?, ?) |

---

## ❓ Anlama Soruları

1. Grid (5, 3) koordinatı CELL_SIZE=25 için kaçıncı pikselde başlar?
2. Neden duvar çizerken iki komşu hücrenin paylaştığı duvarı **bir kez** çizmek yeterlidir?
3. Çözüm yolunu "toggle" yaparken image buffer'ı komple yeniden mi çizmek daha iyidir, yoksa sadece yol hücrelerini güncellemek mi?
4. Pencere boyutu 800×600, maze 25×20 ise CELL_SIZE ne olur?
5. Entry hücresini nasıl görsel olarak vurgularsınız?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 12 — MLX Maze Renderer
Topics: Coordinate mapping (grid to pixels), scaling,
        drawing walls with pixels, solution path rendering,
        image buffer refresh strategy.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 12 Tamamlandı → Faz 13'e Geçmeye Hazır
