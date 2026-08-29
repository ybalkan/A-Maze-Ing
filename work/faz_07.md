# FAZ 07 — Randomness ve Seed

> **Süre:** 1 Gün  
> **Amaç:** Tekrar üretilebilir (reproducible) labirent oluşturmayı anlamak.  
> **PDF bunu özellikle istiyor.**

---

## 🎯 Hedef

Bu fazın sonunda:
- Seed'in ne işe yaradığını açıklayabilmelisiniz
- Aynı seed ile aynı labirenti üretebilmelisiniz
- Python'da `random` modülünü doğru kullanabilmelisiniz

---

## 📖 Öğrenilecek Kavramlar

### 1. Randomness (Rastgelelik)

Bilgisayarlar gerçek anlamda rastgele sayı üretemez — **pseudorandom** (sahte rastgele) üretir.

```
Pseudorandom Number Generator (PRNG):
- Bir başlangıç değeri (seed) alır
- Deterministik bir formülle sayı üretir
- Aynı seed → her zaman aynı sayı dizisi
```

---

### 2. `random` Modülü

```python
import random

# Seed set et
random.seed(42)

# Rastgele sayılar
random.randint(0, 10)     # 0-10 arası tam sayı
random.choice([1, 2, 3])  # Listeden rastgele seç
random.shuffle(liste)     # Listeyi karıştır

# Seed olmadan → her çalıştırmada farklı sonuç
# Seed ile → her çalıştırmada aynı sonuç
```

---

### 3. Seed (Tohum)

```
Seed = 42 → Sequence: 7, 3, 9, 1, 5, ...
Seed = 42 → Sequence: 7, 3, 9, 1, 5, ...  (aynı!)
Seed = 99 → Sequence: 2, 8, 4, 6, 0, ...  (farklı!)
```

**Neden önemli?**

| Kullanım Amacı | Açıklama |
|---|---|
| **Debug** | Aynı labirenti tekrar üretip hatayı incelemek |
| **Test** | Belirli bir labirentle test yazmak |
| **Paylaşım** | "Ben 42 seed'li labirenti çözemedim" diyebilmek |
| **PDF şartı** | Paket parametresi: `MazeGenerator(seed=42)` |

---

### 4. Reproducibility (Tekrar Üretilebilirlik)

```python
# SADECE MANTIK

# Kötü yöntem:
gen = MazeGenerator(size=10)  # Her çalışmada farklı labirent

# İyi yöntem:
gen = MazeGenerator(size=10, seed=42)  # Her zaman aynı labirent
```

**Paket arayüzünde seed parametresi zorunludur:**
```python
MazeGenerator(size=20, seed=42)
```

---

### 5. Random State (İleri Düzey)

Bazen seed'i dışarıdan almak yerine kaydedip aktarmak gerekir:

```python
# State kaydet
state = random.getstate()

# Bazı işlemler yap...

# State geri yükle
random.setstate(state)

# Bu noktadan sonra aynı sonuçlar üretilir
```

---

## ✏️ Mini Görev

### Görev 1 — Seed Deneyi

Aşağıdakileri kağıtta planlayın, sonra terminal'de deneyin:

```python
import random

random.seed(42)
print([random.randint(1, 100) for _ in range(5)])

random.seed(42)
print([random.randint(1, 100) for _ in range(5)])

# İki satır aynı çıktı vermeli!
```

### Görev 2 — Aynı Seed Aynı Maze

Recursive Backtracker algoritmanızı düşünün:
- Hangi adımlarda `random.choice()` kullanılır?
- Seed değiştiğinde ne değişir?
- Seed aynı kalırsa ne değişmez?

---

## ❓ Anlama Soruları

1. Neden bilgisayarlar "gerçekten" rastgele sayı üretemez?
2. Aynı seed ile aynı labirentin üretilmesi neden faydalıdır?
3. `random.seed()` çağrısını programın neresine koymalısınız?
4. Seed verilmezse ne olur? Python ne kullanır?
5. İki farklı bilgisayarda aynı Python sürümü + aynı seed → aynı labirent mi?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 07 — Randomness ve Seed
Topics: random module, seed, reproducibility, pseudorandom numbers.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 07 Tamamlandı → Faz 08'e Geçmeye Hazır
