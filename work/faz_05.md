# FAZ 05 — Maze Generation Algorithms

> **Süre:** 4 Gün  
> **Amaç:** Perfect maze üreten algoritmaları anlamak ve uygulamak.  
> **PDF'in çekirdeği — bu faz projenin kalbidir.**

---

## 🎯 Hedef

Bu fazın sonunda:
- Recursive Backtracker'ı tam olarak açıklayabilmelisiniz
- Prim ve Kruskal'ı kavramsal düzeyde anlayabilmelisiniz
- Aralarındaki farkı (hız, görsellik, karmaşıklık) karşılaştırabilmelisiniz

---

## 📖 1. Recursive Backtracker (DFS Maze Generation)

> **İlk öğrenilecek algoritma. En yaygın, en sezgisel.**

### Algoritma Adımları

```
1. Rastgele bir hücreyi seç → başlangıç noktası
2. Bu hücreyi "ziyaret edildi" olarak işaretle
3. Ziyaret edilmemiş komşuları listele
4. Varsa → rastgele birini seç, aradaki duvarı kaldır, o hücreye git (recursive)
5. Yoksa → geri dön (backtrack) → bir önceki hücreye dön
6. Tüm hücreler ziyaret edilene kadar devam et
```

### Görselleştirme (4×4)

```
Başlangıç: tüm duvarlar kapalı
[■][■][■][■]
[■][■][■][■]
[■][■][■][■]
[■][■][■][■]

Adım 1: (0,0)'dan başla, EAST gider
[  ─ ][■][■]
[■][■][■][■]
...

Son: Perfect maze oluştu (spanning tree)
```

### Özellikler

| Özellik | Değer |
|---|---|
| Zaman Karmaşıklığı | O(N) — N = hücre sayısı |
| Bellek | O(N) — stack derinliği |
| Tünel uzunluğu | Uzun, derin tüneller (biased) |
| Görünüm | "River-like", uzun koridorlar |
| Uygulaması | Kolay |

---

## 📖 2. Prim's Algorithm

> **Minimum Spanning Tree algoritmasının randomize versiyonu.**

### Algoritma Adımları

```
1. Rastgele bir hücreyi seç → "maze" içine al
2. Bu hücrenin komşularını "frontier" listesine ekle
3. Frontier boşalana kadar:
   a. Frontier'dan rastgele bir hücre seç
   b. Bu hücreye maze içinden komşu olan hücreleri bul
   c. Rastgele birini seç, aradaki duvarı kaldır
   d. Seçilen hücreyi maze'e ekle
   e. Yeni hücrenin maze-dışı komşularını frontier'a ekle
```

### Özellikler

| Özellik | Değer |
|---|---|
| Zaman Karmaşıklığı | O(N log N) |
| Bellek | O(N) — frontier listesi |
| Tünel uzunluğu | Kısa, çok dallanmış |
| Görünüm | "Organic", kısa yollar |
| Uygulaması | Orta |

---

## 📖 3. Kruskal's Algorithm

> **Her iki hücreyi birleştiren kenar (edge) listesini random shuffle eder.**

### Algoritma Adımları

```
1. Tüm olası duvarları (edge) listele
2. Listeyi rastgele karıştır
3. Her duvar için:
   a. İki hücre farklı set'te mi? (Union-Find ile kontrol)
   b. Evet → duvarı kaldır, iki seti birleştir
   c. Hayır → atla (cycle oluşturur)
4. Tüm hücreler aynı set'te → bitti
```

### Union-Find Yapısı

```
Başlangıç: Her hücre kendi seti
{A} {B} {C} {D} {E} ...

A-B duvarı kaldırılır → {A,B} {C} {D} {E}
C-D duvarı kaldırılır → {A,B} {C,D} {E}
B-C duvarı kaldırılır → {A,B,C,D} {E}
...
Hepsi birleşince → perfect maze!
```

### Özellikler

| Özellik | Değer |
|---|---|
| Zaman Karmaşıklığı | O(N log N) |
| Bellek | O(N) — union-find |
| Tünel uzunluğu | Dengeli |
| Görünüm | "Uniform", düzenli |
| Uygulaması | Zor (Union-Find gerekir) |

---

## ⚖️ Karşılaştırma Tablosu

| Özellik | Recursive Backtracker | Prim | Kruskal |
|---|---|---|---|
| Hız | Hızlı | Orta | Orta |
| Bellek | Orta | Orta | Az |
| Görünüm | Uzun tüneller | Organik | Dengeli |
| Uygulama Zorluğu | Kolay | Orta | Zor |
| Dead-end sayısı | Az | Çok | Orta |
| Perfect maze? | ✅ | ✅ | ✅ |

---

## ⭐ BONUS: Braided Maze

PDF'de bonus olarak istenen **braided maze** (dead-end olmayan labirent):

```
Perfect Maze:    Braided Maze:
Her yerde        Bazı cycle'lar var,
tek yol          dead-end yok
```

Braided maze üretmek için:
1. Perfect maze oluştur
2. Dead-end hücreleri bul (yalnızca 1 açık duvar)
3. O hücrenin kapalı bir duvarını kaldır (cycle oluşur)
4. `--max-dead-ends 0` ile doğrula

---

## ✏️ Mini Görev

### Görev 1 — Kağıtta Recursive Backtracker

4×4 grid çizin ve Recursive Backtracker'ı elle yürütün:
1. (0,0)'dan başlayın
2. Her adımda hangi komşuyu seçtiğinizi yazın
3. Geri dönme (backtrack) anlarını işaretleyin
4. Sonuçta tüm hücreler ziyaret edildi mi?

### Görev 2 — Karşılaştırma

Aynı 4×4 grid üzerinde Prim'i yürütün. Fark nedir?

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| Recursive Backtracker | Prim's Algorithm |
| Kruskal'ı beraber yapın | |
| Sonra karşılaştırın | |

---

## ❓ Anlama Soruları

1. Recursive Backtracker neden her zaman perfect maze üretir?
2. Prim ve Backtracker'ın ürettiği maze'ler görünüşte nasıl farklıdır?
3. Kruskal'da neden Union-Find gerekir? Sadece set() kullansak olmaz mı?
4. "Braided maze" nasıl doğrulanır? Hangi koşul sağlanmalıdır?
5. Hangi algoritmayı projenizde ana algoritma olarak seçerdiniz? Neden?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 05 — Maze Generation Algorithms
Topics: Recursive Backtracker, Prim's Algorithm, Kruskal's Algorithm,
        Braided Maze, spanning tree, dead-ends.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 05 Tamamlandı → Faz 06'ya Geçmeye Hazır
