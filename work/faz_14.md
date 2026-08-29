# FAZ 14 — Python Package (pip Paketi)

> **Süre:** 2 Gün  
> **Amaç:** Labirent üretici modülünü pip ile kurulabilir paket haline getirmek.  
> **PDF'in en özel şartlarından biri — zorunlu!**

---

## 🎯 Hedef

Bu fazın sonunda:
- Python paket yapısını anlayabilmelisiniz
- `pyproject.toml` veya `setup.py` yazabilmelisiniz
- `.whl` ve `.tar.gz` dosyası üretebilmelisiniz
- Paketi `pip install` ile kurabilmelisiniz

---

## 📖 1. Python Paket Yapısı

### Klasör Yapısı

```
mazegen/                    ← Paket kök dizini
├── mazegen/                ← Python modülü
│   ├── __init__.py         ← Paketi tanımlar
│   ├── generator.py        ← MazeGenerator sınıfı
│   ├── solver.py           ← Çözücü
│   └── models.py           ← Cell, Wall, Coordinate
├── tests/                  ← Testler (paket dışı)
│   └── test_generator.py
├── pyproject.toml          ← Modern paket konfigürasyonu
├── LICENSE.md              ← Zorunlu! (PDF şartı)
└── README.md               ← Kısa dokümantasyon
```

---

## 📖 2. `__init__.py`

Dışarıdan erişilecek sınıfları export et:

```python
# mazegen/__init__.py
from .generator import MazeGenerator
from .solver import MazeSolver
from .models import Cell, Wall, Coordinate

__version__ = "1.0.0"
__all__ = ["MazeGenerator", "MazeSolver"]
```

Kullanıcı şöyle import edebilir:
```python
from mazegen import MazeGenerator
```

---

## 📖 3. `pyproject.toml` (Modern Yaklaşım)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "mazegen-yourlogin"
version = "1.0.0"
description = "A-Maze-ing: Perfect maze generator and solver"
authors = [
    {name = "Your Name", email = "your@email.com"}
]
readme = "README.md"
license = {file = "LICENSE.md"}
requires-python = ">=3.8"
dependencies = []   # Harici bağımlılık yok!

[project.urls]
Repository = "https://github.com/yourlogin/a-maze-ing"
```

---

## 📖 4. Paket İsimlendirme (PDF Şartı)

```
Paket adı: mazegen-*
Örnek:     mazegen-1.0.0-py3-none-any.whl
           mazegen-1.0.0.tar.gz
```

> ⚠️ PDF: Paket adı `mazegen-` ile başlamalı, repo kök dizininde olmalı!

---

## 📖 5. Build Süreci

```bash
# Araçları kur
pip install build

# Paket oluştur (wheel + tar.gz üretir)
python -m build

# Çıktı:
# dist/mazegen-1.0.0-py3-none-any.whl
# dist/mazegen-1.0.0.tar.gz
```

---

## 📖 6. Test Kurulumu

Virtualenv içinde test:

```bash
# Yeni sanal ortam oluştur
python3 -m venv test_env
source test_env/bin/activate

# Paketi kur
pip install dist/mazegen-1.0.0-py3-none-any.whl

# Test et
python3 -c "from mazegen import MazeGenerator; print('OK')"
```

---

## 📖 7. Dokümantasyon (README içinde)

PDF'in istediği kısa kullanım kılavuzu:

```markdown
## Usage

### Installation
pip install mazegen-1.0.0-py3-none-any.whl

### Basic Example
from mazegen import MazeGenerator

gen = MazeGenerator(size=10, seed=42)
maze = gen.generate()
solution = gen.solve(entry=(0,0), exit=(9,9))
print(solution)  # "ESEENEE..."

### Parameters
- size (int): Maze width and height
- seed (int): Random seed for reproducibility
- algorithm (str): "backtracker" | "prim" | "kruskal"
```

---

## 📖 8. LICENSE.md (Zorunlu!)

PDF özellikle istiyor. Seçenekler:

| Lisans | Açıklama | Seçim Kriteri |
|---|---|---|
| **MIT** | En özgür, kullanıcı dostu | Başkası değiştirip kapatabilir |
| **GPL v3** | Türevler de açık kaynak olmalı | Kodu açık tutmak istiyorsanız |
| **Apache 2.0** | Patent koruması var | Kurumsal projeler |

**Öneri:** MIT — basit, anlaşılır, 42 projeleri için uygun.

```markdown
# LICENSE.md
MIT License

Copyright (c) 2024 <login1>, <login2>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...
```

---

## ✏️ Mini Görev

### Görev — Paket Yapısını Tasarlayın

Kağıtta şu soruları yanıtlayın:

1. `MazeGenerator` sınıfı hangi dosyada olmalı?
2. `__init__.py` hangi sınıfları export etmeli?
3. Kullanıcı `from mazegen import MazeGenerator` yazınca ne olur?
4. Paket adınız ne olacak? (`mazegen-yourlogin`)
5. Hangi lisansı seçersiniz? Neden?

---

## ❓ Anlama Soruları

1. `__init__.py` neden gereklidir?
2. `.whl` ve `.tar.gz` arasındaki fark nedir?
3. Neden `requires = []` (bağımlılık yok) hedeflenmelidir?
4. Değerlendirmede `pip install` sonrası kaynak koddan tekrar build istenirse ne yapılır?
5. Paket versiyon numaralandırması (`1.0.0`) ne anlama gelir? (SemVer)

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 14 — Python Package
Topics: package structure, __init__.py, pyproject.toml,
        wheel (.whl), tar.gz, pip install, LICENSE.md, virtualenv testing.
The package must be named mazegen-* and installable via pip.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 14 Tamamlandı → Faz 15'e Geçmeye Hazır
