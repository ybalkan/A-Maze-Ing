# FAZ 04 — DFS ve BFS

> **Süre:** 3 Gün  
> **Amaç:** İki temel graf arama algoritmasını anlamak.  
> **Bu faz çok önemli — hem üretim hem çözüm için kullanılır.**

---

## 🎯 Hedef

Bu fazın sonunda DFS ve BFS'i:
- Kağıt üzerinde elle yürütebilmelisiniz
- Aralarındaki farkı açıklayabilmelisiniz
- Hangi problemde hangisini kullanacağınızı bilmelisiniz

---

## 📖 DFS — Depth-First Search (Derinlik Öncelikli Arama)

### Temel Fikir
> "Bir yoldan git, çıkmaz sokağa ulaşana kadar devam et. Çıkmaz sokakta geri dön, başka yol dene."

### Stack (Yığın) Mantığı

DFS bir **stack** kullanır (ya da özyineleme ile çağrı yığını):

```
Stack: LIFO — Last In, First Out
Son giren ilk çıkar → en derin node işlenir
```

```
Başla: Stack = [A]
A'yı al → komşularını ekle: Stack = [B, C]
C'yi al (son giren) → Stack = [B, D]
D'yi al → Stack = [B, E]
E çıkmaz sokak → geri dön: Stack = [B]
B'yi al → ...
```

### Recursive DFS

```python
# SADECE MANTIK — Kod yazmayın henüz!
def dfs(node, visited):
    visited.add(node)
    for neighbour in node.get_neighbours():
        if neighbour not in visited:
            dfs(neighbour, visited)  # Recursive çağrı
```

### Iterative DFS

```python
# SADECE MANTIK — Kod yazmayın henüz!
def dfs_iterative(start):
    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()      # Son gireni al (LIFO)
        if node not in visited:
            visited.add(node)
            for neighbour in node.get_neighbours():
                if neighbour not in visited:
                    stack.append(neighbour)
```

### DFS Özellikleri

| Özellik | DFS |
|---|---|
| Veri yapısı | Stack (LIFO) |
| Bellek | Az (yalnızca mevcut path) |
| En kısa yol? | ❌ Garanti değil |
| Labirent üretimi | ✅ Çok uygun |
| Complete? | ✅ (tüm node'ları bulur) |

---

## 📖 BFS — Breadth-First Search (Genişlik Öncelikli Arama)

### Temel Fikir
> "Önce tüm komşuları işle, sonra onların komşularına geç. Dalgalar halinde yayıl."

### Queue (Kuyruk) Mantığı

BFS bir **queue** kullanır:

```
Queue: FIFO — First In, First Out
İlk giren ilk çıkar → en yakın node işlenir
```

```
Başla: Queue = [A]
A'yı al → komşularını ekle: Queue = [B, C]
B'yi al (ilk giren) → komşularını ekle: Queue = [C, D, E]
C'yi al → Queue = [D, E, F]
...
```

### BFS Mantığı

```python
# SADECE MANTIK — Kod yazmayın henüz!
from collections import deque

def bfs(start, goal):
    queue = deque([start])
    visited = {start: None}   # node → parent
    while queue:
        node = queue.popleft()   # İlk gireni al (FIFO)
        if node == goal:
            return reconstruct_path(visited, goal)
        for neighbour in node.get_neighbours():
            if neighbour not in visited:
                visited[neighbour] = node
                queue.append(neighbour)
```

### BFS Özellikleri

| Özellik | BFS |
|---|---|
| Veri yapısı | Queue (FIFO) |
| Bellek | Fazla (tüm seviye) |
| En kısa yol? | ✅ Garanti (unweighted) |
| Labirent üretimi | ⚠️ Kullanılabilir ama nadir |
| Labirent çözümü | ✅ En uygun |

---

## ⚖️ DFS vs BFS Karşılaştırma

| | DFS | BFS |
|---|---|---|
| Veri yapısı | Stack | Queue |
| Yön | Derine gider | Yatay yayılır |
| En kısa yol | ❌ | ✅ |
| Bellek kullanımı | Az | Fazla |
| Maze üretimi | ✅ | ❌ |
| Maze çözümü | ❌ (kısa yol için) | ✅ |
| Zaman karmaşıklığı | O(V + E) | O(V + E) |

---

## ✏️ Mini Görev

### Görev 1 — Kağıtta DFS Yürütmek

```
Graf:
    A
   / \
  B   C
 / \   \
D   E   F
```

1. DFS'i A'dan başlatın
2. Her adımda stack içeriğini yazın
3. Hangi sırayla node'lar işlendi?

### Görev 2 — BFS Karşılaştırması

Aynı grafta BFS yapın:
1. Her adımda queue içeriğini yazın
2. DFS'den hangi sıralama farkı var?

### Görev 3 — Maze'de BFS

```
Labirent (. = yol, # = duvar, S = start, E = end):
S . . # .
# # . # .
. . . . E
```

BFS ile entry'den exit'e olan en kısa yolu bulun.

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| DFS — Stack mantığı, recursive & iterative | BFS — Queue mantığı, en kısa yol |
| Mini Görev 1 ve 3'ü birlikte yapın | |
| Birbirinize öğretin | |

---

## ❓ Anlama Soruları

1. Neden DFS ile en kısa yol garantisi yoktur?
2. BFS neden en kısa yolu garanti eder? (unweighted graph)
3. `stack.pop()` ile `queue.popleft()` arasındaki fark nedir?
4. DFS özyinelemeli versiyonda "geri dönme" nasıl gerçekleşir?
5. Labirent üretiminde neden DFS tercih edilir?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 04 — DFS ve BFS
Topics: DFS, Stack (LIFO), Recursive DFS, Iterative DFS,
        BFS, Queue (FIFO), Shortest Path.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 04 Tamamlandı → Faz 05'e Geçmeye Hazır
