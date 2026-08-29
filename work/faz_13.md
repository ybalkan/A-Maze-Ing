# FAZ 13 — Bonus Features

> **Süre:** 3-4 Gün  
> **Amaç:** PDF'de belirtilen bonus özellikleri eklemek.  
> **Bu fazda yaratıcılığınızı kullanırsınız.**

---

## 🎯 Bonus Listesi (PDF'den)

| # | Bonus | Öncelik |
|---|---|---|
| B1 | **Braided Maze** | Yüksek |
| B2 | **Çoklu Algoritmalar** | Yüksek |
| B3 | **Üretim Animasyonu** | Orta |
| B4 | **Real-time Solving** | Orta |
| B5 | **Algorithm Switching** | Düşük |
| B6 | **Regenerate** | Düşük |
| B7 | **Zoom** | Düşük |

---

## 📖 B1 — Braided Maze (Çıkmazsız Labirent)

### Nedir?

```
Perfect maze   : Her noktaya TEK yol → bazı hücreler çıkmaz sokak
Braided maze   : Cycle'lar var → hiçbir hücre çıkmaz sokak değil
```

### Nasıl Üretilir?

```python
# SADECE MANTIK
# 1. Önce perfect maze üret
# 2. Dead-end hücreleri bul (yalnızca 1 açık geçiti olan hücreler)
# 3. Dead-end'in kapalı duvarlarından birini rastgele kaldır
# 4. → Cycle oluştu, artık dead-end değil

def remove_dead_ends(maze):
    for cell in maze.cells:
        if count_open_walls(cell) == 1:   # Dead-end
            random_wall = random.choice(cell.closed_walls)
            remove_wall(cell, random_wall)  # Cycle ekle
```

### Doğrulama

PDF'deki analysis script: `--max-dead-ends 0` ile kontrol edilir.

```
max_dead_ends = max dead-end count allowed
0 → hiç dead-end olmamalı
```

---

## 📖 B2 — Çoklu Algoritmalar

### Desteklenmesi Gereken Algoritmalar

| Algoritma | Zorluk | Görünüm |
|---|---|---|
| Recursive Backtracker | Kolay | Uzun tüneller |
| Prim's | Orta | Organik |
| Kruskal's | Zor | Dengeli |
| Wilson's | Zor | Unbiased |

### Seçim Mekanizması

```python
# SADECE MANTIK
class MazeGenerator:
    ALGORITHMS = {
        "backtracker": RecursiveBacktracker,
        "prim":        PrimsAlgorithm,
        "kruskal":     KruskalsAlgorithm,
    }

    def generate(self, algorithm="backtracker"):
        algo_class = self.ALGORITHMS[algorithm]
        return algo_class(self.width, self.height, self.seed).run()
```

---

## 📖 B3 — Üretim Animasyonu

### Fikir

Labirent üretilirken her adımı görsel olarak göster:

```
Adım 1: Tüm duvarlar kapalı → gri grid
Adım 2: (0,0)'dan EAST duvarı kaldırıldı → o geçit açıldı
Adım 3: ...
Her adımda ekrana yaz → animasyon!
```

### Uygulama Yaklaşımı

```python
# SADECE MANTIK
def generate_with_animation(maze, mlx_state):
    for step in generate_steps(maze):   # Generator fonksiyon
        apply_step(maze, step)          # Bir duvar kaldır
        render(mlx_state, maze)         # Ekrana yaz
        mlx_loop_hook(...)              # Yavaşlatmak için delay
```

### Generator Fonksiyon Mantığı

```python
# SADECE MANTIK
def generate_steps():
    ...
    yield (current_cell, next_cell, direction)  # Her adımı emit et
    ...
```

---

## 📖 B4 — Real-time Solving (Canlı Çözüm)

### Fikir

BFS/DFS çalışırken her adımı animasyonla göster:

```
Başlangıç → her ziyaret edilen hücreyi renkle göster
           → çözüm bulununca yolu farklı renkle vurgula
```

### Renk Şeması

| Durum | Renk |
|---|---|
| Ziyaret edilmemiş | Gri |
| Queue'da (BFS frontier) | Sarı |
| Ziyaret edilmiş | Mavi |
| Çözüm yolu | Yeşil |

---

## 📖 B5 — Algorithm Switching

### Fikir

Kullanıcı tuşa basarak farklı algoritma seçer, labirent yeniden üretilir:

```
[1] Recursive Backtracker
[2] Prim's Algorithm
[3] Kruskal's Algorithm
```

---

## 📖 B6 — Regenerate (Yeniden Üretim)

Kullanıcı istediğinde yeni seed ile yeni labirent:

```
R tuşu → yeni seed ile yeni maze
S tuşu → aynı seed ile aynı maze (reset)
```

---

## 📖 B7 — Zoom (Yakınlaştırma)

Fare scroll veya +/- tuşlarıyla zoom:

```python
# SADECE MANTIK
CELL_SIZE_MIN = 10
CELL_SIZE_MAX = 80

def zoom_in():
    CELL_SIZE = min(CELL_SIZE + 5, CELL_SIZE_MAX)
    render()

def zoom_out():
    CELL_SIZE = max(CELL_SIZE - 5, CELL_SIZE_MIN)
    render()
```

---

## ✏️ Uygulama Sırası (Öneri)

1. **B1 — Braided Maze** → Maze generator'a ekle (sadece algoritma)
2. **B2 — Çoklu Algoritmalar** → Strateji pattern ile temiz uygula
3. **B3 — Animasyon** → Generator fonksiyon + MLX refresh
4. **B4 — Real-time Solving** → BFS'e yield ekle + MLX render
5. **B5/B6/B7** → Küçük eklemeler, son haftaya bırak

---

## ❓ Anlama Soruları

1. Braided maze ile perfect maze arasındaki temel fark nedir?
2. Animasyon için neden `yield` (generator) kullanmak iyi bir yaklaşımdır?
3. Çoklu algoritma desteği için "Strategy Pattern" neden uygundur?
4. Real-time BFS animasyonunda `visited` set'i ne zaman güncellenir?
5. Zoom özelliği için hangi state'in güncellenmesi gerekir?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 13 — Bonus Features
Topics: Braided maze, multiple algorithms (Strategy Pattern),
        generation animation (generator functions), real-time solving,
        zoom, regenerate.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 13 Tamamlandı → Faz 14'e Geçmeye Hazır
