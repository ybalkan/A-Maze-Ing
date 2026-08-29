# FAZ 09 — Bitwise ve Hex Encoding

> **Süre:** 2 Gün  
> **Amaç:** PDF'deki hex tabanlı labirent formatını anlamak ve uygulamak.  
> **PDF'in en teknik bölümü — config okuma ve output yazma için zorunlu.**

---

## 🎯 Hedef

Bu fazın sonunda:
- Binary ve hexadecimal sayı sistemlerini anlayabilmelisiniz
- 4 duvarı tek bir sayıda bitmask ile saklayabilmelisiniz
- Hex string'i okuyup 2D grid'e, grid'i hex string'e çevirebilmelisiniz

---

## 📖 1. Binary (İkili Sayı Sistemi)

```
Decimal   Binary    Açıklama
0         0000      Tüm duvarlar açık
1         0001      Yalnızca WEST duvarı kapalı
2         0010      Yalnızca EAST duvarı kapalı
4         0100      Yalnızca SOUTH duvarı kapalı
8         1000      Yalnızca NORTH duvarı kapalı
15        1111      Tüm duvarlar kapalı
```

**Her bit bir duvarı temsil eder:**

```
Bit pozisyonu:  3    2    1    0
Duvar:         NORTH SOUTH EAST WEST
```

---

## 📖 2. Bitmask İşlemleri

### Duvar Kontrolü (AND)

```python
# Belirli bir duvar var mı?
NORTH = 8   # 1000
walls = 9   # 1001 = NORTH + WEST

has_north = walls & NORTH  # 1000 & 1001 = 1000 → Truthy
has_east  = walls & 2      # 0010 & 1001 = 0000 → Falsy
```

### Duvar Ekleme (OR)

```python
# Duvar ekle
walls = 0           # 0000 - boş
walls |= 8          # 0000 | 1000 = 1000 (NORTH eklendi)
walls |= 1          # 1000 | 0001 = 1001 (WEST eklendi)
```

### Duvar Kaldırma (AND NOT)

```python
# Duvar kaldır
walls = 15          # 1111 - hepsi kapalı
walls &= ~8         # 1111 & 0111 = 0111 (NORTH kaldırıldı)
walls &= ~1         # 0111 & 1110 = 0110 (WEST kaldırıldı)
# walls = 6 = 0110 = SOUTH + EAST kaldı
```

### Duvar Durumlarını Tersine Çevirme (XOR)

```python
walls ^= 8  # NORTH varsa kaldır, yoksa ekle (toggle)
```

---

## 📖 3. Hexadecimal (Onaltılık Sayı Sistemi)

```
Hex  Decimal  Binary
0    0         0000
1    1         0001
2    2         0010
3    3         0011
4    4         0100
5    5         0101
6    6         0110
7    7         0111
8    8         1000
9    9         1001
a    10        1010
b    11        1011
c    12        1100
d    13        1101
e    14        1110
f    15        1111
```

**Neden hex?** 4 bit = 1 hex karakter → Kompakt!

---

## 📖 4. Config Dosyası Okuma

PDF örneği:
```
913955111555515395153
ac2a910282913855692c3a92
...
1,1      # entry
19,14    # exit
```

Her karakter bir hücrenin duvar durumu:

```
'9' → hex 9 → decimal 9 → binary 1001 → NORTH + WEST kapalı
'a' → hex a → decimal 10 → binary 1010 → NORTH + EAST kapalı
'f' → hex f → decimal 15 → binary 1111 → tüm duvarlar kapalı
'0' → hex 0 → decimal 0  → binary 0000 → tüm duvarlar açık
```

### Config Okuma Mantığı

```python
# SADECE MANTIK
def parse_config(filename):
    with open(filename) as f:
        lines = f.readlines()

    grid = []
    for line in lines:
        if line.startswith("entry") or line.startswith("exit"):
            break
        row = []
        for char in line.strip():
            walls = int(char, 16)  # hex karakter → integer
            row.append(walls)
        grid.append(row)
    return grid
```

### Output Yazma Mantığı

```python
# SADECE MANTIK
def write_output(grid, entry, exit_pos, solution):
    with open("output_maze.txt", "w") as f:
        for row in grid:
            f.write("".join(hex(walls)[2:] for walls in row) + "\n")
        f.write(f"{entry[0]},{entry[1]}  # entry (x,y)\n")
        f.write(f"{exit_pos[0]},{exit_pos[1]}  # exit (x,y)\n")
        f.write(solution + "\n")  # "ESEENEE..."
```

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| Binary sayı sistemi | Hexadecimal sayı sistemi |
| `&`, `|`, `~` bitmask işlemleri | Hex ↔ decimal ↔ binary dönüşüm |
| Birlikte: config okuma mantığını tartışın | |

---

## ✏️ Mini Görev

### Görev 1 — Hex'ten Duvarlara

Şu hex karakterlerinin hangi duvarları temsil ettiğini çözün:

| Hex | Binary | NORTH | SOUTH | EAST | WEST |
|---|---|---|---|---|---|
| `9` | `1001` | ✅ | ❌ | ❌ | ✅ |
| `a` | `????` | ? | ? | ? | ? |
| `5` | `????` | ? | ? | ? | ? |
| `c` | `????` | ? | ? | ? | ? |
| `3` | `????` | ? | ? | ? | ? |

### Görev 2 — Duvardan Hex'e

Bu duvar kombinasyonları için hex değerini hesaplayın:

| Açık Duvarlar | Kapalı Duvarlar | Binary | Hex |
|---|---|---|---|
| E, W | N, S | `0110` | `6` |
| Yok | N, S, E, W | `????` | `?` |
| N, S, E, W | Yok | `????` | `?` |
| N, E | S, W | `????` | `?` |

---

## ❓ Anlama Soruları

1. Neden `&` duvar kontrolü için, `|` duvar ekleme için kullanılır?
2. `~8` işleminin sonucu nedir? (Python'da hint: negatif değer!)
3. `int('a', 16)` ne döndürür?
4. `hex(10)` ne döndürür? `hex(10)[2:]` ne döndürür?
5. Config dosyasında `'9'` karakteri hangi hücre durumunu temsil eder?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 09 — Bitwise ve Hex Encoding
Topics: Binary, Bitmask (AND, OR, NOT, XOR), Hexadecimal,
        config file parsing, output file writing.
We need to encode 4 walls (N/S/E/W) as a single hex character.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 09 Tamamlandı → Faz 10'a Geçmeye Hazır
