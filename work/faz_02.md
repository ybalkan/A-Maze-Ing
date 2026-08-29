# FAZ 02 — Python OOP ve Veri Modelleme

> **Süre:** 2 Gün  
> **Amaç:** Maze, Cell, Coordinate ve Wall yapılarını Python OOP ile tasarlamak.  
> **Kod yazmadan önce tasarımı netleştirmek.**

---

## 🎯 Hedef

Bu fazın sonunda şu sınıfları **tasarlayabilmelisiniz** (kod yazmadan, UML olarak):

- `Cell` — Bir labirent hücresi
- `Wall` — Bir hücrenin duvarları
- `Coordinate` — (x, y) konumu
- `Maze` — Tüm labirent yapısı

---

## 📖 Öğrenilecek Python Kavramları

### 1. `@dataclass`

```python
from dataclasses import dataclass

@dataclass
class Coordinate:
    x: int
    y: int
```

| Özellik | Açıklama |
|---|---|
| `@dataclass` | `__init__`, `__repr__`, `__eq__` otomatik üretir |
| `field()` | Varsayılan değer, factory tanımlamak için |
| `frozen=True` | Immutable (değiştirilemez) dataclass |
| `post_init` | `__post_init__` ile doğrulama |

Öğrenme soruları:
- [ ] Normal class ile dataclass farkı nedir?
- [ ] `frozen=True` ne işe yarar? Neden kullanırsın?
- [ ] `field(default_factory=list)` neden gerekir?

---

### 2. `Enum`

```python
from enum import Enum, IntFlag

class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST  = "E"
    WEST  = "W"
```

| Tür | Açıklama |
|---|---|
| `Enum` | Basit sabit değerler kümesi |
| `IntEnum` | Integer değerli enum |
| `IntFlag` | Bit flag işlemleri için (duvarlar!) |
| `auto()` | Otomatik değer atama |

Öğrenme soruları:
- [ ] Enum neden `if direction == "N"` yerine daha iyidir?
- [ ] `IntFlag` ile 4 duvarı tek sayıda nasıl saklarsın?
- [ ] `Direction.NORTH.value` ne döner?

---

### 3. Bit Flag (Duvar Temsili)

PDF'de duvarlar 4 bit ile temsil edilir:

```
bit 3 (8) = NORTH
bit 2 (4) = SOUTH
bit 1 (2) = EAST
bit 0 (1) = WEST
```

```python
from enum import IntFlag

class Wall(IntFlag):
    NONE  = 0
    WEST  = 1   # 0001
    EAST  = 2   # 0010
    SOUTH = 4   # 0100
    NORTH = 8   # 1000
    ALL   = 15  # 1111

# Kullanım:
walls = Wall.NORTH | Wall.WEST   # = 9 = 0x9
has_north = bool(walls & Wall.NORTH)  # True
```

Öğrenme soruları:
- [ ] `|` (OR) operatörü duvarları birleştirmek için nasıl çalışır?
- [ ] `&` (AND) operatörü belirli duvarı kontrol etmek için nasıl kullanılır?
- [ ] Hex `9` değeri hangi duvarları temsil eder?

---

### 4. Composition (Bileşim)

```python
@dataclass
class Cell:
    coord: Coordinate    # Composition: Cell bir Coordinate "içerir"
    walls: Wall          # Composition: Cell bir Wall "içerir"
    visited: bool = False
```

> **Composition** = "has-a" ilişkisi → Cell bir Coordinate'e **sahiptir**  
> **Inheritance** = "is-a" ilişkisi → her zaman daha uygun değil

---

### 5. Type Hints

```python
from typing import Optional, List, Tuple

def get_neighbours(self, coord: Coordinate) -> List[Cell]:
    ...

def find_path(self, start: Coordinate, end: Coordinate) -> Optional[List[Coordinate]]:
    ...
```

| Syntax | Açıklama |
|---|---|
| `int`, `str`, `bool` | Basit tipler |
| `List[Cell]` | Cell listesi |
| `Optional[Cell]` | Cell veya None |
| `Tuple[int, int]` | (x, y) demeti |
| `Dict[Coordinate, Cell]` | Sözlük |

---

## ✏️ Mini Görev — UML Tasarımı

> **Kod yazmadan** aşağıdaki sınıfları kağıt üzerinde tasarlayın:

```
┌─────────────────┐       ┌──────────────┐
│   Coordinate    │       │     Wall     │
├─────────────────┤       ├──────────────┤
│ x: int          │       │ NORTH: int   │
│ y: int          │       │ SOUTH: int   │
├─────────────────┤       │ EAST:  int   │
│ __eq__()        │       │ WEST:  int   │
│ __hash__()      │       └──────────────┘
└─────────────────┘              │
         │                       │
         └──────────┐ ┌──────────┘
                    ▼ ▼
               ┌──────────┐
               │   Cell   │
               ├──────────┤
               │ coord    │
               │ walls    │
               │ visited  │
               └──────────┘
                    │
                    ▼
               ┌──────────┐
               │   Maze   │
               ├──────────┤
               │ width    │
               │ height   │
               │ cells[]  │
               │ entry    │
               │ exit     │
               └──────────┘
```

---

## 👥 Ekip Dağılımı

| Kişi A | Kişi B |
|---|---|
| `@dataclass` araştırır | `Enum` ve bit flag araştırır |
| `Coordinate`, `Maze` tasarlar | `Wall` (IntFlag), `Direction` tasarlar |
| Birleştirerek `Cell` tasarını tartışırsınız | |

---

## ❓ Anlama Soruları

1. `@dataclass` ile `class` arasındaki en büyük fark nedir?
2. `Wall.NORTH | Wall.EAST` işleminin sonucu nedir? (bit düzeyinde)
3. `frozen=True` bir dataclass'ta neden hashable olur?
4. Composition ne zaman Inheritance'tan daha iyi bir seçimdir?
5. Config'deki `9` (hex) değeri hangi duvarları açık bırakır?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 02 — Python OOP ve Veri Modelleme
Topics: dataclass, Enum, IntFlag, composition, type hints.
We need to model: Cell, Wall, Coordinate, Maze.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 02 Tamamlandı → Faz 03'e Geçmeye Hazır
