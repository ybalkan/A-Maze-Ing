# A-Maze-Ing — Proje Yapısı

> **Etiket Sistemi**
> | Etiket | Anlamı |
> |--------|--------|
> | `[Z]` | **Zorunlu** — eksikse grade = 0 |
> | `[EV]` | Evaluation'da **bizzat test** edilecek |
> | `[B]` | **Bonus** — opsiyonel, +puan |
> | `[▶]` | Kodlama sırası numarası |

---

## 📁 Proje Ağacı

```
a-maze-ing/
├── README.md                           [Z][EV]
├── LICENSE.md                          [Z][EV]
├── .gitignore
├── Makefile                            [Z][EV]  install / run / debug / clean / lint
├── pyproject.toml                      [Z]      pip install + pip wheel için
├── requirements.txt
├── a_maze_ing.py                       [Z][EV]  python3 a_maze_ing.py config.txt
├── maze_analyzer.py                    [Z][EV]  subject tarafından veriliyor, root'ta olmalı
├── mazegen-0.1.0-py3-none-any.whl      [Z][EV]  root'ta, eval'da yeniden build edilecek
├── mazegen-0.1.0.tar.gz                [Z]      alternatif format
├── output_maze.txt                        [EV]  OUTPUT_FILE config'e bağlı
│
├── configs/                            [Z][EV]
│   ├── default.txt                     [Z][EV]  WIDTH / HEIGHT / ENTRY / EXIT / OUTPUT_FILE / PERFECT
│   └── examples/
│       ├── valid/
│       │   ├── basic.txt                        küçük boyut, PERFECT=True
│       │   ├── medium.txt                       orta boyut, PERFECT=False
│       │   └── seed_42.txt                      tekrarlanabilirlik testi
│       └── invalid/                       [EV]  evaluator bu dosyaları kullanır
│           ├── missing_key.txt                  zorunlu key eksik
│           ├── bad_format.txt                   = işareti yok
│           ├── letters_for_numbers.txt          WIDTH=abc
│           ├── bad_perfect.txt                  PERFECT=maybe
│           └── bad_entry_format.txt             ENTRY=0;0
│
└── src/
    └── mazegen/                        [Z][EV]  pip install edilebilir paket
        ├── __init__.py
        ├── __main__.py
        │
        ├── api/
        │   ├── __init__.py
        │   └── maze_generator.py       [Z][EV]  MazeGenerator class — dışa açık tek API
        │
        ├── models/                     ◀ BURADAN BAŞLA
        │   ├── __init__.py
        │   ├── direction.py            [▶ 1]    N/E/S/W enum + karşı yön + dx/dy offset
        │   ├── cell.py                 [▶ 2]    4 duvar biti, hex encoding
        │   ├── maze.py                 [▶ 3]    WIDTH×HEIGHT grid, border wall
        │   └── solution.py            [▶ 4]     koordinat + yön listesi → N/E/S/W string
        │
        ├── parser/
        │   ├── __init__.py
        │   ├── config_parser.py        [▶ 5][Z][EV]  KEY=VALUE okuma, # yorum atla
        │   ├── validator.py            [▶ 6][Z][EV]  5 hata senaryosu kontrolü
        │   └── hex_decoder.py          [▶ 7][Z][EV]  int ↔ duvar biti dönüşümü
        │
        ├── generation/
        │   ├── __init__.py
        │   ├── generator_base.py                soyut temel sınıf
        │   ├── recursive_backtracker.py [▶ 8][Z][EV]  ana algoritma
        │   ├── prim.py                    [B]   bonus +1
        │   ├── kruskal.py                 [B]   bonus +1
        │   └── braided.py                 [B]   bonus +1 (dead-end'siz)
        │
        ├── solving/
        │   ├── __init__.py
        │   ├── solver_base.py                   soyut temel sınıf
        │   ├── bfs_solver.py           [▶ 9][Z][EV]  garantili en kısa yol
        │   ├── dijkstra_solver.py         [B]   bonus
        │   └── astar_solver.py            [B]   bonus
        │
        ├── rendering/
        │   ├── __init__.py
        │   ├── color_palette.py       [▶ 10][Z][EV]  renk değiştirme için zorunlu
        │   ├── ascii_renderer.py      [▶ 11][Z][EV]  terminal render + 3 zorunlu etkileşim
        │   ├── mlx_renderer.py            [B]   bonus: grafik pencere
        │   └── animation.py               [B]   bonus: üretim animasyonu
        │
        └── io/
            ├── __init__.py
            └── output_writer.py       [▶ 12][Z][EV]  hex output dosyası yazar

tests/                                           graded değil, crash olmak yasak
    ├── unit/
    │   ├── test_parser.py
    │   ├── test_generation.py
    │   └── test_solving.py
    └── fixtures/
        ├── valid_maze.txt
        ├── expected_output.txt
        └── sample_solution.txt
```

---

## ✅ Evaluation Checklist

### 1. Basics
- [ ] Tüm zorunlu dosyalar repoda mevcut
- [ ] `flake8 .` → hata yok
- [ ] `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs` → hata yok

### 2. README.md — tüm bölümler eksiksiz
- [ ] İlk satır italik: *This project has been created as part of the 42 curriculum by \<login\>.*
- [ ] `Description` bölümü
- [ ] `Instructions` bölümü (kurulum / çalıştırma)
- [ ] `Resources` bölümü (referanslar + AI kullanımı açıklaması)
- [ ] Config dosyası formatının tam açıklaması
- [ ] Seçilen algoritma ve neden seçildiği
- [ ] Reusable modülün kısa dokümantasyonu
- [ ] Takım yönetimi: roller, planlama, iyi/kötü giden şeyler, kullanılan araçlar

### 3. Display — `python3 a_maze_ing.py configs/default.txt`
- [ ] Labirent ekranda görünüyor
- [ ] **Re-generate** çalışıyor
- [ ] **Toggle path** (en kısa yolu göster/gizle) çalışıyor
- [ ] **Wall rengi değiştirme** çalışıyor

### 4. Config Format
- [ ] `#` ile başlayan satırlar yorum olarak atlanıyor
- [ ] `KEY=VALUE` formatı (küçük harf de kabul)
- [ ] Zorunlu keyler mevcut: `WIDTH` `HEIGHT` `ENTRY` `EXIT` `OUTPUT_FILE` `PERFECT`

### 5. Error Management — evaluator config dosyasını editleyecek
- [ ] Zorunlu key silindi → hata mesajı, **crash yok**
- [ ] `=` işareti olmayan satır → hata mesajı, **crash yok**
- [ ] `WIDTH=abc` (sayı yerine harf) → hata mesajı, **crash yok**
- [ ] `PERFECT=maybe` (geçersiz boolean) → hata mesajı, **crash yok**
- [ ] `ENTRY=0;0` (yanlış tuple formatı) → hata mesajı, **crash yok**

### 6. Output File Format
- [ ] `HEIGHT` satır, her satır `WIDTH` hex karakter
- [ ] Boş satır
- [ ] `ENTRY` koordinatı
- [ ] `EXIT` koordinatı
- [ ] `N E S W ...` yol dizisi
- [ ] `python3 maze_analyzer.py output_maze.txt` → **PASS**
- [ ] Yol görsel ile eşleşiyor

### 7. Maze Generator
- [ ] Aynı seed → aynı labirent (tekrarlanabilirlik)
- [ ] Tüm hücreler erişilebilir (42 pattern hariç)
- [ ] Dış kenar duvarları var
- [ ] 3×3 veya daha büyük açık alan **yok**
- [ ] `"42"` pattern görünür (yeterli boyut varsa)
- [ ] `PERFECT=True` → `maze_analyzer`: **PERFECT** verdict
- [ ] `PERFECT=False` → `maze_analyzer`: **Pac-Man-USABLE** verdict
  - [ ] 4 köşe + merkez açık koridor
  - [ ] En az 2 bağımsız rota

### 8. Reusable Module
- [ ] Virtualenv'de package yeniden build edilebiliyor
- [ ] Farklı virtualenv'de `pip install` → `a_maze_ing.py` çalışıyor

### Bonus (maks 5 puan)
- [ ] Braided maze: `python3 maze_analyzer.py output.txt --max-dead-ends 0`
- [ ] Çoklu algoritma (Prim, Kruskal vb.)
- [ ] Üretim animasyonu

---

## 🗺️ Algoritmalar — Kim Ne Yapıyor?

| Tür | Algoritma | Durum | Ne Yapar |
|-----|-----------|-------|----------|
| **ÜRETME** | Recursive Backtracker | `[Z]` zorunlu | DFS ile labirenti inşa eder |
| **ÜRETME** | Prim | `[B]` bonus | Frontier set ile büyüyen duvar listesi |
| **ÜRETME** | Kruskal | `[B]` bonus | Union-Find ile spanning tree |
| **ÜRETME** | Braided | `[B]` bonus | Dead-end'leri döngüye çevirir |
| **ÜRETME** | Wilson | `[B]` bonus | Random walk (büyük gridde yavaş) |
| **ÇÖZME** | BFS | `[Z]` zorunlu | Garantili en kısa yol |
| **ÇÖZME** | Dijkstra | `[B]` bonus | Ağırlıklı graf |
| **ÇÖZME** | A\* | `[B]` bonus | Buluşsal en kısa yol |

> **Not:** Wilson da bir **üretme** algoritmasıdır. BFS'e benzer görünür ama labirenti inşa eder, çözmez.
> Bonus için birden fazla **üretme** algoritması ekliyorsun.

---

## 🏗️ Kodlama Sırası — Detaylı

> *Şehir kuruyorsun. Önce arsa, sonra bina planı, sonra inşaat, sonra yol, sonra harita, sonra rehber kitapçık.*

### Aşama 1 — Temel Veri Yapıları *(arsayı çiz)*

#### `[▶ 1]` `models/direction.py`
| | |
|---|---|
| **Ne yapar** | Yön kavramını tanımlar |
| **İçerik** | `N=0, E=1, S=2, W=3` enum · karşı yön `N↔S, E↔W` · `(dx, dy)` offset tablosu |
| **Neden önce** | `cell.py` ve `generation/` buraya bağımlı |
| **Çıktı** | `Direction` enum, `opposite(d)`, `delta(d)` |

#### `[▶ 2]` `models/cell.py`
| | |
|---|---|
| **Ne yapar** | Tek bir labirent karesini temsil eder |
| **İçerik** | 4 duvar (N/E/S/W) → bit mask · `has_wall()` / `remove_wall()` · `to_hex()` · `from_hex()` |
| **Neden önce** | `maze.py` Cell nesnelerinden oluşur |
| **Çıktı** | `Cell` sınıfı |

#### `[▶ 3]` `models/maze.py`
| | |
|---|---|
| **Ne yapar** | Tüm ızgarayı tutar |
| **İçerik** | `WIDTH × HEIGHT` Cell matrisi · `get_cell(x,y)` · `in_bounds(x,y)` · `get_neighbors(x,y)` · `remove_wall_between(a, b)` — iki tarafta da açar |
| **⚠️ Kritik** | Dış kenar duvarları **hiçbir zaman** açılmaz |
| **Çıktı** | `Maze` sınıfı |

#### `[▶ 4]` `models/solution.py`
| | |
|---|---|
| **Ne yapar** | Çözüm yolunu tutar |
| **İçerik** | `[(x, y, Direction), ...]` listesi · `to_string()` → `"N E E S W ..."` |
| **Çıktı** | `Solution` sınıfı |

---

### Aşama 2 — Config Okuma *(inşaat ruhsatı)*

#### `[▶ 5]` `parser/config_parser.py`
| | |
|---|---|
| **Ne yapar** | `.txt` config dosyasını okur |
| **İçerik** | Satır satır · `#` yorum atla · `KEY=VALUE` böl · boş satır atla |
| **EV test** | `=` işareti olmayan satır → `ValueError`, crash yok |
| **Çıktı** | `parse_config(path) → dict[str, str]` |

#### `[▶ 6]` `parser/validator.py`
| | |
|---|---|
| **Ne yapar** | Config dict'ini doğrular |
| **İçerik** | Zorunlu keyler · `WIDTH/HEIGHT` → pozitif int · `ENTRY/EXIT` → `"x,y"` formatı, bounds içinde · `PERFECT` → `true/false` · `SEED` → opsiyonel int |
| **EV test** | 5 farklı hata senaryosu test edilecek |
| **Çıktı** | `validate(config) → MazeConfig` dataclass veya exception |

#### `[▶ 7]` `parser/hex_decoder.py`
| | |
|---|---|
| **Ne yapar** | Hex ↔ duvar biti dönüşümü |
| **İçerik** | `int_to_walls(n)` · `walls_to_hex(cell) → "0"–"F"` · `decode_row(row_str) → [Cell]` |
| **EV test** | `maze_analyzer` output dosyasındaki hex'i parse eder |
| **Çıktı** | encode/decode fonksiyonları |

---

### Aşama 3 — Üretme *(inşaatı yap)*

#### `[▶ 8]` `generation/recursive_backtracker.py` — Ana Algoritma
| | |
|---|---|
| **Ne yapar** | DFS ile labirenti üretir |
| **Nasıl** | Stack · ziyaret edilmemiş komşu varsa duvarı aç, stack'e ekle · yoksa backtrack · tüm hücreler bitene kadar |
| **EV test** | `PERFECT=True` → PERFECT verdict · `PERFECT=False` → Pac-Man-USABLE · aynı seed = aynı labirent · "42" pattern · 3×3 açık alan yok · 4 köşe + merkez açık |
| **Çıktı** | `generate() → Maze` |

---

### Aşama 4 — Çözme *(navigasyon)*

#### `[▶ 9]` `solving/bfs_solver.py` — Zorunlu Çözücü
| | |
|---|---|
| **Ne yapar** | BFS ile garantili en kısa yolu bulur |
| **Nasıl** | Queue ile entry'den başla · açık duvarlardan komşuya geç · exit'e ulaşınca parent'tan geri sar · `N E E S W ...` dizisi üret |
| **EV test** | Output dosyasındaki yol görsel ile eşleşmeli · `maze_analyzer` doğrular |
| **Çıktı** | `solve() → Solution` |

---

### Aşama 5 — Dosya Yazma *(haritayı kağıda bas)*

#### `[▶ 10]` `io/output_writer.py`
| | |
|---|---|
| **Ne yapar** | Labirenti + çözümü output dosyasına yazar |
| **Format** | `HEIGHT` satır × `WIDTH` hex karakter · boş satır · `ENTRY` · `EXIT` · `N E S W ...` · her satır `\n` |
| **EV test** | `maze_analyzer` bu dosyayı parse eder — format sapması = fail |
| **Çıktı** | `write(maze, solution, path)` |

---

### Aşama 6 — Görsel *(fotoğrafını çek)*

#### `[▶ 11]` `rendering/color_palette.py`
| | |
|---|---|
| **Ne yapar** | Renk tanımlarını merkezi tutar |
| **İçerik** | `WALL / PATH / ENTRY / EXIT` renkleri · ANSI escape kodları |
| **Neden önce** | `ascii_renderer` buraya bağımlı · renk değiştirme özelliği (EV'de test edilir) buradan yönetilir |

#### `[▶ 12]` `rendering/ascii_renderer.py` — Zorunlu Renderer
| | |
|---|---|
| **Ne yapar** | Labirenti terminale çizer |
| **İçerik** | `render(maze, solution=None)` · duvar karakterleri (`█ ║ ═`) · giriş/çıkış işaretli |
| **EV test** | **3 zorunlu etkileşim:** Re-generate · Toggle path · Change wall color |
| **Çıktı** | `render()` + event loop |

---

### Aşama 7 — API Paketi *(şehir şirketini kur)*

#### `[▶ 13]` `api/maze_generator.py`
| | |
|---|---|
| **Ne yapar** | Tüm sistemi saran tek public sınıf |
| **İçerik** | `MazeGenerator(width, height, seed=None, perfect=False)` · `generate()` · `solve()` · `get_maze()` · `export(path)` |
| **Önemli** | Docstring + örnek kullanım zorunlu · pip ile kurulup import edilebilmeli |
| **EV test** | Farklı venv'de `from mazegen import MazeGenerator` çalışmalı |

---

### Aşama 8 — Ana Program *(belediye başkanı)*

#### `[▶ 14]` `a_maze_ing.py`
| | |
|---|---|
| **Ne yapar** | Tüm sistemi birbirine bağlar |
| **Akış** | `sys.argv[1]` → `parse_config()` → `validate()` → `MazeGenerator.generate()` → `solve()` → `output_writer.write()` → `ascii_renderer.run()` |
| **EV test** | `python3 a_maze_ing.py configs/default.txt` çalışmalı · hiçbir hata crash'e yol açmamalı |

---

### Aşama 9 — Paket & Dokümantasyon *(yönetmelik + rehber)*

#### `[▶ 15]` `pyproject.toml` + `Makefile`
- `pyproject.toml`: `[project]` name/version/dependencies + `[build-system]` (hatchling veya setuptools)
- `Makefile`: `install` / `run` / `debug` / `clean` / `lint`
  - `lint` = `flake8 .` + `mypy . --warn-return-any --warn-unused-ignores ...`

#### `[▶ 16]` `README.md`
Zorunlu bölümler (herhangi biri eksikse **grade = 0**):
- İlk satır italik · Description · Instructions · Resources
- Config formatı tam açıklaması · Seçilen algoritma + neden
- Reusable module dokümantasyonu · Takım yönetimi

---

## 🎯 Bonus Sıralaması

| Öncelik | Dosya | Neden |
|---------|-------|-------|
| **1. Braided** | `generation/braided.py` | `maze_analyzer --max-dead-ends 0` ile kanıtlanır — en somut bonus |
| **2. Prim** | `generation/prim.py` | Basit, hızlı, interview'larda çok sorulan |
| **3. Kruskal** | `generation/kruskal.py` | Union-Find öğretir, değerli veri yapısı |
| **4. Animation** | `rendering/animation.py` | Gösterişli, değerlendirmede etkileyici |
| **5. Wilson** | `generation/wilson.py` | Büyük gridde çok yavaş, anlatması zor — en sona bırak |

> `A*` ve `Dijkstra`: BFS zaten yeterli olduğu için çözüm tarafındaki bonusların değeri düşük.
