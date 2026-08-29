# FAZ 06 — Solver (Labirent Çözücü)

> **Süre:** 2 Gün  
> **Amaç:** Entry noktasından Exit noktasına en kısa yolu bulmak.  
> **Çıktı:** N/S/E/W string → `output_maze.txt`'e yazılır.

---

## 🎯 Hedef

Bu fazın sonunda:
- BFS ve DFS ile labirent çözebilmelisiniz
- En kısa yolu yeniden oluşturabilmelisiniz (path reconstruction)
- İki yaklaşım arasındaki farkı açıklayabilmelisiniz

---

## 📖 Kavramlar

### Labirent Çözümü = Graf Arama Problemi

```
Maze → Graph dönüşümü:
- Her hücre = Node
- İki hücre arasında açık duvar = Edge
- Entry = Source node
- Exit = Target node
- Çözüm = Entry'den Exit'e giden Path
```

---

## 📖 BFS Solver (Shortest Path)

> BFS, **unweighted graph**'ta her zaman en kısa yolu bulur.

### Çalışma Mantığı

```
1. Queue'ya Entry hücresini ekle
2. Her hücre için: hangi hücreden gelindi? (parent map)
3. Exit'e ulaşılınca → parent map'i geriye doğru izle
4. Path = [Exit, ..., Entry] → tersine çevir
```

### Path Reconstruction

```python
# SADECE MANTIK
def reconstruct_path(parent_map, entry, exit):
    path = []
    current = exit
    while current != entry:
        prev = parent_map[current]
        direction = get_direction(prev, current)  # "N", "S", "E", "W"
        path.append(direction)
        current = prev
    path.reverse()
    return "".join(path)  # örn: "ESEENEE..."
```

### BFS Solver Özellikleri

| Özellik | BFS Solver |
|---|---|
| En kısa yol | ✅ Garanti |
| Zaman | O(N) — N = hücre sayısı |
| Bellek | O(N) — tüm hücreleri saklar |
| PDF uyumu | ✅ (output N/S/E/W string) |

---

## 📖 DFS Solver (First Found Path)

> DFS, bulduğu **ilk yolu** döndürür — en kısa olmayabilir.

### Çalışma Mantığı

```
1. Stack'a Entry hücresini ekle
2. Her adımda en derin hücreye git
3. Exit'e ulaşınca dur
4. Path, stack'taki elemanlardan oluşur
```

### DFS Solver Özellikleri

| Özellik | DFS Solver |
|---|---|
| En kısa yol | ❌ Garanti değil |
| Zaman | O(N) |
| Bellek | O(path length) |
| Kullanım amacı | Debug, alternatif gösterim |

---

## ⚖️ Karşılaştırma

| | BFS Solver | DFS Solver |
|---|---|---|
| Yol türü | **Shortest path** | First found path |
| Garantili kısa yol | ✅ | ❌ |
| Bellek | Daha fazla | Daha az |
| PDF çıktısı için | ✅ Doğru seçim | ⚠️ Yanlış olabilir |

---

## 📄 Output Formatı (PDF'den)

Çözüm yolu `output_maze.txt` dosyasına şu formatta yazılır:

```
# Labirent satırları (hex)
913955111555515395153
...
# Koordinatlar
1,1      # entry (x,y)
19,14    # exit  (x,y)
# Çözüm
ESEENEEESSSEENEESENEE
```

### Direction String Kuralları

| Hareket | Karakter |
|---|---|
| Yukarı (y azalır) | `N` |
| Aşağı (y artar) | `S` |
| Sağa (x artar) | `E` |
| Sola (x azalır) | `W` |

---

## ✏️ Mini Görev

```
Labirent:
S ─ A ─ B
    │    
    C ─ D
         │
    F ─ E
```

1. BFS ile S'den E'ye giden en kısa yolu bulun
2. Her adımda queue'nun içeriğini yazın
3. Path reconstruction'ı geriye doğru izleyin
4. Yön string'ini oluşturun: `E...S...` gibi

---

## ❓ Anlama Soruları

1. Neden BFS en kısa yolu garanti eder, DFS etmez?
2. "Path reconstruction" neden entry'den başlamaz, exit'ten başlar?
3. Perfect maze'de BFS her zaman tek bir çözüm yolu bulur — neden?
4. Çözüm yolunu N/S/E/W string'e dönüştürmek için iki komşu hücre arasındaki yön nasıl belirlenir?
5. BFS solver'da `parent_map`'in rolü nedir?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 06 — Solver
Topics: BFS Solver, DFS Solver, Path Reconstruction,
        shortest path vs first found path, N/S/E/W direction string.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 06 Tamamlandı → Faz 07'ye Geçmeye Hazır
