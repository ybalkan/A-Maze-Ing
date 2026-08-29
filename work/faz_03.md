# FAZ 03 — Maze Representation

> **Süre:** 2 Gün  
> **Amaç:** Labirentin bellekte nasıl temsil edileceğine karar vermek.  
> **En kritik tasarım aşaması.**

---

## 🎯 Hedef Sorular

Bu faz boyunca şu sorulara cevap arayacaksınız:

1. **Hücre nasıl tutulacak?** → Hangi veri yapısı?
2. **Dört duvar nasıl tutulacak?** → Bit, bool array, set?
3. **Komşuluk nasıl bulunacak?** → Koordinat hesabı mı, lookup tablosu mu?

---

## 📖 Öğrenilecek Kavramlar

### 1. 2D Grid Temsili

Bir labirenti bellekte tutmanın farklı yolları:

#### Yöntem 1 — List of Lists
```python
grid = [[Cell() for _ in range(width)] for _ in range(height)]
cell = grid[row][col]
```

#### Yöntem 2 — Dictionary (Coordinate → Cell)
```python
grid = {}
grid[(x, y)] = Cell(...)
cell = grid[(2, 3)]
```

#### Yöntem 3 — 1D Array (Flatten)
```python
grid = [Cell() for _ in range(width * height)]
cell = grid[row * width + col]
```

#### Yöntem 4 — Wall Array (Ayrı duvar matrisi)
```python
h_walls = [[True]*width  for _ in range(height+1)]  # yatay duvarlar
v_walls = [[True]*(width+1) for _ in range(height)]  # dikey duvarlar
```

#### Yöntem 5 — Bit Encoded (PDF'in yöntemi)
```python
# Her hücre = 1 integer (4 bit = 4 duvar)
grid = [[0xF] * width for _ in range(height)]
# 0xF = 1111 = tüm duvarlar kapalı
```

---

### 2. Koordinat Sistemi

| Soru | Seçenek A | Seçenek B |
|---|---|---|
| Nereden başlar? | (0,0) sol-üst | (0,0) sol-alt |
| Erişim sırası? | `grid[row][col]` | `grid[y][x]` |
| Yön hesabı? | North = row-1 | North = y+1 |

> ⚠️ **PDF'de** koordinatlar `(x, y)` formatında verilir. Dikkat!

```
(0,0) ─── (1,0) ─── (2,0)
  │                   │
(0,1) ─── (1,1) ─── (2,1)
  │                   │
(0,2) ─── (1,2) ─── (2,2)
```

---

### 3. Neighbour Discovery (Komşu Bulma)

4 yönlü komşuluk:

```python
DIRECTIONS = {
    'N': (0, -1),   # y azalır
    'S': (0, +1),   # y artar
    'E': (+1, 0),   # x artar
    'W': (-1, 0),   # x azalır
}

def get_neighbours(x, y, width, height):
    neighbours = []
    for direction, (dx, dy) in DIRECTIONS.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbours.append((direction, nx, ny))
    return neighbours
```

**Sınır kontrolü:** Köşe, kenar ve iç hücreler kaç komşuya sahip?

| Hücre Tipi | Komşu Sayısı |
|---|---|
| Köşe hücre | 2 |
| Kenar hücre | 3 |
| İç hücre | 4 |

---

### 4. Duvarı Kaldırma (Wall Removal)

İki hücre arasındaki duvar kaldırıldığında **her iki hücre** güncellenmeli:

```
Hücre A (2,1) ile Hücre B (3,1) arasında EAST duvarı:
- A'dan EAST duvarı kaldır
- B'den WEST duvarı kaldır
```

```python
OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

def remove_wall(cell_a, direction, cell_b):
    cell_a.walls &= ~Wall[direction]
    cell_b.walls &= ~Wall[OPPOSITE[direction]]
```

---

## ✏️ Mini Görev

> **5 farklı temsil yöntemi için karşılaştırma tablosu çıkarın.**

| Yöntem | Bellek | Erişim Hızı | Kolay mı? | PDF Uyumlu? |
|---|---|---|---|---|
| List of Lists | Orta | O(1) | ✅ | - |
| Dictionary | Yüksek | O(1) avg | ✅ | - |
| 1D Array | Düşük | O(1) | ⚠️ | - |
| Ayrı Wall Array | Yüksek | O(1) | ⚠️ | - |
| Bit Encoded | Çok Düşük | O(1) | ❌ | ✅ |

---

## ❓ Anlama Soruları

1. `grid[row][col]` ile `grid[y][x]` aynı mı? Ne zaman farklılık yaratır?
2. Komşu hücreyi bulmak için neden `0 <= nx < width` kontrolü gerekir?
3. İki hücre arasındaki duvarı kaldırırken neden iki güncelleme gerekir?
4. Bit encoded yöntemde `0xF` neden "tüm duvarlar kapalı" anlamına gelir?
5. Perfect maze için duvar kaldırma işlemi hangi kurala uymalıdır?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 03 — Maze Representation
Topics: 2D Grid, Coordinate Systems, Neighbour Discovery, wall removal.
We need to choose how to store cells, walls and neighbours in memory.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 03 Tamamlandı → Faz 04'e Geçmeye Hazır
