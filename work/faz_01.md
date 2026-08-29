# FAZ 01 — Maze ve Graph Temelleri

> **Süre:** 2-3 Gün  
> **Amaç:** Labirent ve graf teorisinin temel kavramlarını anlamak.  
> **Bu fazın sonunda şunları açıklayabilmelisiniz.**

---

## 🎯 Hedef Kavramlar

Bu fazın sonunda aşağıdaki kavramları **kendi cümlelerinizle** açıklayabilmelisiniz:

### Maze (Labirent) Kavramları

| Kavram | Açıklama |
|---|---|
| **Maze** | Belirli kurallara göre oluşturulmuş duvarlar ve yollar bütünü |
| **Cell** | Labirentin en küçük birimi, bir kare/hücre |
| **Wall** | İki komşu hücre arasındaki bariyer |
| **Grid** | Hücrelerin dizildiği 2D ızgara yapısı |
| **Neighbour** | Bir hücreye doğrudan bitişik olan hücreler (N/S/E/W) |
| **Perfect Maze** | Her hücreye giden tam 1 yol olan labirent (cycle yok, connected) |

### Graph (Graf) Kavramları

| Kavram | Açıklama |
|---|---|
| **Graph** | Node (düğüm) ve Edge (kenar) kümesinden oluşan yapı |
| **Node** | Grafın her bir noktası → labirentte bir hücre |
| **Edge** | İki node arasındaki bağlantı → iki hücre arasında duvar YOK |
| **Path** | Bir node'dan diğerine ulaşan node dizisi |
| **Cycle** | Başladığı node'a dönen bir path |
| **Connected Graph** | Her node'dan diğerine en az 1 yol olan graf |

### Ağaç (Tree) Kavramları

| Kavram | Açıklama |
|---|---|
| **Tree** | Cycle içermeyen, connected bir graf |
| **Spanning Tree** | Bir grafın tüm node'larını kapsayan tree |
| **Unique Path** | İki node arasında tam olarak 1 yol → perfect maze'in tanımı |

---

## 💡 Kritik Bağlantı

```
Perfect Maze  =  Spanning Tree
```

> Bir perfect maze, hücrelerin (node) oluşturduğu tam bağlantılı bir grafın **spanning tree**'sidir.  
> Yani: cycle yok + her hücreye ulaşılabilir = perfect maze

---

## 📖 Öğrenme Adımları

### Adım 1 — Graph Theory Temelleri
- [ ] Graph nedir? Directed vs Undirected farkı
- [ ] Node ve Edge kavramları
- [ ] Adjacency: komşuluk matrisi vs komşuluk listesi
- [ ] Connected graph nedir, nasıl kontrol edilir?
- [ ] Cycle nedir, nasıl tespit edilir?

### Adım 2 — Tree ve Spanning Tree
- [ ] Tree nedir? (cycle yok + connected)
- [ ] Spanning tree nedir?
- [ ] Neden perfect maze = spanning tree?
- [ ] Kaç farklı spanning tree olabilir? (Her birini düşün)

### Adım 3 — Maze Theory
- [ ] Cell ve Wall modeli
- [ ] Grid yapısı: (row, col) koordinat sistemi
- [ ] Komşuluk: 4 yön (N/S/E/W)
- [ ] Perfect maze tanımı ve özellikleri
- [ ] Perfect maze ↔ Graph bağlantısı

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| Graph Theory araştırır | Maze Theory araştırır |
| Node, Edge, Path, Cycle, Connected | Cell, Wall, Grid, Neighbour, Perfect Maze |
| Birbirinize anlatırsınız (Feynman Tekniği) | |

---

## ✏️ Mini Görev

> **Kağıt üzerinde 4×4 maze çizin ve graph'a dönüştürün.**

### Adımlar:
1. 4×4 ızgara çiz (16 hücre)
2. Bazı duvarları sil (ama perfect maze olsun!)
3. Her hücreyi bir node olarak numaralandır (1-16)
4. Duvarı olmayan komşu hücreler arasına edge çiz
5. Sonuç: Bir graph elde ettin!
6. Bu graph bir tree mi? Spanning tree mi? Kontrol et.

```
Örnek 4x4 grid:
+--+--+--+--+
|  |     |  |
+  +--+  +  +
|     |  |  |
+--+  +  +--+
|  |  |     |
+  +  +--+  +
|        |  |
+--+--+--+--+
```

---

## ❓ Anlama Soruları

Bu soruları cevaplayabiliyorsan faz tamamdır:

1. Bir labirentin "perfect" olup olmadığını nasıl anlarsın?
2. 4×4 bir mazede kaç node ve maksimum kaç edge olabilir?
3. Cycle ile perfect maze neden çelişir?
4. Spanning tree ile perfect maze arasındaki fark nedir?
5. Komşu hücre sayısı köşe, kenar ve iç hücrelerde kaçtır?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 01 — Maze ve Graph Temelleri
Topics: Graph, Node, Edge, Path, Cycle, Connected Graph,
        Perfect Maze, Tree, Spanning Tree, Unique Path.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 01 Tamamlandı → Faz 02'ye Geçmeye Hazır
