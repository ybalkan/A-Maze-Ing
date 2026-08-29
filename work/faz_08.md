# FAZ 08 — Validation (Doğrulama)

> **Süre:** 1 Gün  
> **Amaç:** Üretilen labirentin geçerli olup olmadığını doğrulamak.  
> **Hatalı labirent → hatalı output → değerlendirme başarısız!**

---

## 🎯 Hedef

Bu fazın sonunda:
- Geçerli bir labirentin kriterlerini listeleyebilmelisiniz
- Bağlantısız (disconnected) ve geçersiz (invalid) maze arasındaki farkı bilmelisiniz
- Temel test stratejilerini uygulayabilmelisiniz

---

## 📖 Öğrenilecek Kavramlar

### 1. Connected Maze (Bağlantılı Labirent)

> Tüm hücreler birbirine ulaşılabilir olmalıdır.

```
Geçerli (Connected):        Geçersiz (Disconnected):
┌───────────────┐           ┌───┬───────────┐
│               │           │   │           │
│   ╔═══╗       │           │   │   ╔═══╗   │
│   ║   ║       │           │   │   ║   ║   │
│   ╚═══╝       │           │   │   ╚═══╝   │
│               │           │   │           │
└───────────────┘           └───┴───────────┘
                             ↑ Bu bölgeye ulaşılamıyor!
```

**Test:** BFS/DFS ile entry'den başla. Tüm hücrelere ulaşılabildi mi?

---

### 2. Perfect Maze Kriterleri

| Kriter | Açıklama | Test Yöntemi |
|---|---|---|
| **Connected** | Her hücreye ulaşılabilir | BFS → visited count == total cells |
| **No Cycle** | Döngü yok | Spanning tree node/edge sayısı: edges = nodes - 1 |
| **Unique Path** | İki nokta arası tek yol | Perfect maze = spanning tree |
| **Correct Size** | Boyut config ile eşleşiyor | `len(grid) == height and len(grid[0]) == width` |
| **Wall Consistency** | A↔B duvarı tutarlı | `A.walls[E] == B.walls[W]` |

---

### 3. Invalid Maze Türleri

#### 3a. Disconnected Maze
```
Bir veya daha fazla hücreye ulaşılamıyor.
BFS tüm hücreleri dolaşmaz → hata!
```

#### 3b. Cyclic Maze
```
İki hücre arasında birden fazla yol var.
Perfect maze değil, braided maze olabilir.
(Bonus için ayrı doğrulama gerekir)
```

#### 3c. Wall Inconsistency
```
Hücre A'nın EAST duvarı var ama
Hücre B'nin (A'nın doğusundaki) WEST duvarı yok!
→ Tutarsız duvar durumu
```

#### 3d. Invalid Entry/Exit
```
Entry veya exit koordinatı grid dışında
veya duvarla çevrili bir hücreye işaret ediyor.
```

---

### 4. Validation Stratejileri

#### Strateji 1 — Connectivity Check
```python
# SADECE MANTIK
def is_connected(maze, entry):
    visited = bfs(maze, entry)
    return len(visited) == maze.total_cells
```

#### Strateji 2 — Edge Count Check
```python
# Perfect maze: edges == nodes - 1
def is_perfect(maze):
    edges = count_open_passages(maze)
    nodes = maze.width * maze.height
    return edges == nodes - 1
```

#### Strateji 3 — Wall Symmetry Check
```python
# Her hücre çifti için duvar tutarlılığını kontrol et
def walls_are_consistent(maze):
    for each cell (x, y):
        if cell has no EAST wall:
            neighbour = cell at (x+1, y)
            assert neighbour has no WEST wall
```

---

### 5. Testing Strategies (Test Yaklaşımları)

| Test Türü | Açıklama |
|---|---|
| **Unit Test** | Tek bir fonksiyonu izole et (örn: wall removal) |
| **Integration Test** | Generate → Solve pipeline |
| **Edge Case** | 1×1 maze, 1×N maze, çok büyük maze |
| **Property Test** | Her üretilen maze perfect olmalı |
| **Regression Test** | Bilinen seed + beklenen output |

---

## ✏️ Mini Görev

### Görev 1 — Validation Listesi

Kağıtta şu soruları yanıtlayın:
1. 5×5 perfect maze'de kaç açık duvar (passage) olmalıdır?  
   *(İpucu: nodes = 25, edges = nodes - 1 = ?)*
2. Wall consistency hangi hücre çiftlerinde kontrol edilmeli?
3. Entry'nin geçerli olup olmadığı nasıl kontrol edilir?

### Görev 2 — Edge Cases

Şu özel durumları düşünün:
- 1×1 maze → giriş = çıkış?
- 1×5 maze → tek koridor, doğrulaması nasıl?
- Entry ve exit aynı hücrede olabilir mi?

---

## ❓ Anlama Soruları

1. Connected maze ile perfect maze arasındaki fark nedir?
2. `edges == nodes - 1` koşulu neden perfect maze'i garanti eder?
3. Wall inconsistency neden oluşabilir? Nasıl önlenirdi?
4. Büyük bir maze'de (100×100) connectivity check ne kadar sürer?
5. Validation kodunu maze üretildikten sonra mı, üretim sırasında mı çalıştırmalısınız?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 08 — Validation
Topics: Connected maze, Invalid maze types, Wall consistency,
        Testing strategies, edge cases, perfect maze properties.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 08 Tamamlandı → Faz 09'a Geçmeye Hazır
