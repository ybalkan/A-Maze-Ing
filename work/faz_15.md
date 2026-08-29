# FAZ 15 — Testing ve Review

> **Süre:** 2 Gün  
> **Amaç:** Kodu test etmek, edge case'leri bulmak, kodu temizlemek.  
> **Son kontrol — değerlendirmeden önce bu faz tamamlanmalı!**

---

## 🎯 Hedef

Bu fazın sonunda:
- `pytest` ile unit test yazabilmelisiniz
- Edge case'leri listeleyip test edebilmelisiniz
- `flake8` ve `mypy` ile kod kalitesini kontrol edebilmelisiniz
- Değerlendirme senaryolarını simüle edebilmelisiniz

---

## 📖 1. pytest

### Temel Kullanım

```bash
# Kurulum
pip install pytest

# Çalıştırma
pytest tests/           # Tüm testleri çalıştır
pytest tests/ -v        # Verbose (detaylı)
pytest tests/ -k "maze" # İsimde "maze" geçen testler
```

### Test Yazma Mantığı

```python
# tests/test_generator.py

def test_maze_is_connected():
    gen = MazeGenerator(size=5, seed=42)
    maze = gen.generate()
    assert is_connected(maze), "Maze must be fully connected"

def test_maze_is_perfect():
    gen = MazeGenerator(size=5, seed=42)
    maze = gen.generate()
    edges = count_passages(maze)
    nodes = 5 * 5
    assert edges == nodes - 1, "Perfect maze: edges = nodes - 1"

def test_same_seed_same_maze():
    maze1 = MazeGenerator(size=10, seed=99).generate()
    maze2 = MazeGenerator(size=10, seed=99).generate()
    assert maze1 == maze2, "Same seed must produce same maze"

def test_solution_exists():
    gen = MazeGenerator(size=10, seed=42)
    maze = gen.generate()
    sol = gen.solve(entry=(0,0), exit=(9,9))
    assert sol is not None, "Solution must exist"

def test_solution_is_valid():
    gen = MazeGenerator(size=5, seed=1)
    maze = gen.generate()
    sol = gen.solve(entry=(0,0), exit=(4,4))
    assert all(c in "NSEW" for c in sol), "Solution must be N/S/E/W only"
```

---

## 📖 2. Edge Cases (Sınır Durumları)

| Edge Case | Beklenen Davranış |
|---|---|
| 1×1 maze | Entry = Exit, boş çözüm |
| 1×N maze | Tek koridor, doğrusal çözüm |
| N×1 maze | Tek koridor, dikey |
| Entry = Exit | Boş çözüm yolu: `""` |
| Geçersiz seed (None) | Rastgele seed kullan |
| Boyut 0 | ValueError fırlat |
| Çok büyük maze (1000×1000) | Performans testi |
| Entry grid dışında | ValueError fırlat |

---

## 📖 3. flake8 (Kod Stili)

```bash
pip install flake8

# Kontrol
flake8 mazegen/

# Yaygın hatalar:
# E501  line too long (>79 chars)
# E302  expected 2 blank lines
# F401  imported but unused
# W291  trailing whitespace
```

---

## 📖 4. mypy (Statik Tip Kontrolü)

```bash
pip install mypy

# Kontrol
mypy mazegen/

# Yaygın hatalar:
# error: Argument 1 to "generate" has incompatible type "str"; expected "int"
# error: Function is missing a return type annotation
```

---

## 📖 5. Değerlendirme Simülasyonu

Değerlendirmede yapılacakların listesi — önce kendiniz deneyin:

### Kontrol 1 — Program Çalışıyor mu?

```bash
python3 ./a_maze_ing.py test_config.txt
# output_maze.txt üretilmeli
```

### Kontrol 2 — Output Formatı Doğru mu?

```bash
# output_maze.txt içeriği:
# Hex satırları → entry koordinatı → exit koordinatı → çözüm string
cat output_maze.txt
```

### Kontrol 3 — pip Paketi Kurulabiliyor mu?

```bash
python3 -m venv test_env
source test_env/bin/activate
pip install mazegen-1.0.0-py3-none-any.whl
python3 -c "from mazegen import MazeGenerator; gen = MazeGenerator(5, 42); print(gen.generate())"
```

### Kontrol 4 — Source'dan Build Edilebiliyor mu?

```bash
python -m build
pip install dist/mazegen-*.whl
```

### Kontrol 5 — Görsel Render Çalışıyor mu?

```bash
python3 ./a_maze_ing.py config.txt
# Terminal veya MLX penceresi açılmalı
```

---

## 📖 6. Son Kontrol Listesi

### Zorunlular

- [ ] `python3 ./a_maze_ing.py config.txt` çalışıyor
- [ ] `output_maze.txt` doğru formatta üretiliyor
- [ ] Çözüm yolu (N/S/E/W) doğru
- [ ] Görsel render çalışıyor (terminal ASCII veya MLX)
- [ ] `mazegen-*.whl` repo kök dizininde mevcut
- [ ] `LICENSE.md` mevcut
- [ ] `README.md` tüm zorunlu bölümleri içeriyor

### Bonuslar

- [ ] Braided maze çalışıyor
- [ ] Çoklu algoritma desteği var
- [ ] Üretim animasyonu çalışıyor
- [ ] MLX grafik render çalışıyor

### Kod Kalitesi

- [ ] `flake8 mazegen/` → 0 hata
- [ ] `mypy mazegen/` → 0 hata
- [ ] `pytest tests/` → tüm testler geçiyor
- [ ] Tüm edge case'ler test edildi

---

## ✏️ Mini Görev

### Görev — Test Listesi Hazırlayın

Kağıtta şu test kategorilerini doldurun:

```
1. MazeGenerator testleri:
   - test_1x1_maze
   - test_same_seed_reproducibility
   - ...

2. Solver testleri:
   - test_solution_reaches_exit
   - test_solution_is_shortest
   - ...

3. Config Parser testleri:
   - test_parse_valid_config
   - test_invalid_hex_character
   - ...

4. Output Writer testleri:
   - test_output_format
   - test_entry_exit_in_output
   - ...
```

---

## ❓ Anlama Soruları

1. `pytest` testleri neden `test_` prefix'i ile başlamalı?
2. `assert maze1 == maze2` çalışması için `Maze` sınıfında ne gerekir?
3. `flake8` ve `mypy` arasındaki fark nedir?
4. Bir test "edge case" mi "happy path" mi olduğu nasıl anlaşılır?
5. Değerlendirmede `pip install` başarısız olursa ne olur?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 15 — Testing ve Review
Topics: pytest, unit testing, edge cases, flake8, mypy,
        evaluation simulation, final checklist.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## 🏁 TÜM FAZLAR TAMAMLANDI!

```
faz_00 → Proje Analizi
faz_01 → Maze ve Graph Temelleri
faz_02 → Python OOP ve Veri Modelleme
faz_03 → Maze Representation
faz_04 → DFS ve BFS
faz_05 → Maze Generation Algorithms
faz_06 → Solver
faz_07 → Randomness ve Seed
faz_08 → Validation
faz_09 → Bitwise ve Hex Encoding
faz_10 → ASCII Renderer
faz_11 → MLX Temelleri
faz_12 → MLX Maze Renderer
faz_13 → Bonus Features
faz_14 → Python Package
faz_15 → Testing ve Review
```

**İyi çalışmalar! 🚀**
