*This project has been created as part of the 42 curriculum by ybalkan, iuslu.*

---

# A-Maze-Ing 🧩

Python ile yazılmış bir labirent üreteci. Bir yapılandırma dosyasını okur, labirenti üretir (mükemmel veya Pac-Man oynanabilir), terminalde görüntüler ve sonucu onaltılık (hex) kodlanmış bir çıktı dosyasına yazar. Labirent üretim mantığı, pip ile kurulabilen yeniden kullanılabilir bir Python paketi (`mazegen`) olarak paketlenmiştir.

---

## Description

A-Maze-Ing iki tür labirent üretir:

- **Mükemmel labirent** (`PERFECT=True`): herhangi iki hücre arasında tam olarak bir yol vardır — döngü yok, açık alan yok. Klasik bir yayılan ağaç (spanning-tree) labirenti.
- **Pac-Man labirenti** (`PERFECT=False`): Pac-Man benzeri bir oyunda doğrudan kullanılabilecek bir tahta — tamamen bağlı, en az iki bağımsız rota, dört köşe ve merkez açık, çıkmaz sokaklar minimumda tutulmuş.

Her iki mod da (ızgara boyutu yeterliyse) tamamen kapalı hücrelerden oluşan görünür bir **"42" deseni** içerir ve giriş ile çıkış arasındaki **en kısa yol** kardinal yönler (`N E S W`) kullanılarak çözülüp kaydedilir.

Program düz metin bir yapılandırma dosyasıyla çalışır ve şunları üretir:
1. Terminalde ASCII görsel çıktı.
2. Tüm labirent yapısını ve en kısa yolu içeren onaltılık (hex) çıktı dosyası.
3. Başka projelere kurulup içe aktarılabilen yeniden kullanılabilir bir `mazegen` paketi.

---

## Instructions

### Gereksinimler

- Python 3.10+
- Kod kalitesi için `flake8` ve `mypy` (bkz. `Makefile`)

### Kurulum

```bash
# Depoyu klonla
git clone <repo-url>
cd a-maze-ing

# Bağımlılıkları yükle
make install
```

### Çalıştırma

```bash
# Kök dizindeki config.txt ile çalıştır (varsayılan)
make run

# Ya da doğrudan
python3 a_maze_ing.py config.txt

# Farklı config dosyasıyla
python3 a_maze_ing.py configs/config.txt
```

### Hata ayıklama modu

```bash
make debug
# karşılığı: python3 -m pdb a_maze_ing.py configs/default.txt
```

### Kod kalitesi kontrolü

```bash
make lint
# çalıştırır: flake8 . && mypy . --warn-return-any --warn-unused-ignores \
#               --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Sıkı mod (opsiyonel)
make lint-strict
# çalıştırır: flake8 . && mypy . --strict --ignore-missing-imports
```

### Testler

```bash
make test
# ya da doğrudan
PYTHONPATH=src python -m pytest tests/ -v
```

### Paketi derleme

```bash
# Sanal ortamda:
python3 -m pip install build
python3 -m build
# Çıktı: proje kökünde mazegen-*.whl
```

---

## Yapılandırma Dosyası

Program, her satırda bir `ANAHTAR=DEĞER` çifti içeren düz metin bir yapılandırma dosyasını kabul eder.
`#` ile başlayan satırlar yorum olarak kabul edilir ve atlanır. Boş satırlar da atlanır.

### Zorunlu anahtarlar

| Anahtar | Tür | Açıklama | Örnek |
|---------|-----|----------|-------|
| `WIDTH` | int | Labirent genişliği (hücre sayısı) | `WIDTH=20` |
| `HEIGHT` | int | Labirent yüksekliği (hücre sayısı) | `HEIGHT=15` |
| `ENTRY` | tuple | Giriş hücresinin koordinatları | `ENTRY=0,0` |
| `EXIT` | tuple | Çıkış hücresinin koordinatları | `EXIT=19,14` |
| `OUTPUT_FILE` | str | Çıktı dosyasının yolu | `OUTPUT_FILE=output_maze.txt` |
| `PERFECT` | bool | Mükemmel labirent modu | `PERFECT=False` |

### İsteğe bağlı anahtarlar

| Anahtar | Tür | Açıklama | Varsayılan | Örnek |
|---------|-----|----------|------------|-------|
| `SEED` | int \| None | Tekrarlanabilirlik için rastgele tohum | `None` (rastgele) | `SEED=42` |
| `ALGORITHM` | str | Üretim algoritması | `recursive_backtracker` | `ALGORITHM=prim` |
| `ANIMATION` | bool | Çözüm animasyonu açık/kapalı | `false` | `ANIMATION=true` |
| `ANIMATION_SPEED` | float | Animasyon adım süresi (saniye) | `0.05` | `ANIMATION_SPEED=0.1` |

**`ALGORITHM` seçenekleri:** `recursive_backtracker` · `prim` · `braided`

**`ANIMATION_SPEED`:** `0.0` verilirse animasyon anlık (delay yok); `0.5` verilirse yavaş adım adım ilerleme.

### Örnek yapılandırma (`config.txt`)

```
# A-Maze-Ing varsayılan yapılandırma

# ── Zorunlu parametreler ──────────────────────────────────────────────────
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=False

# ── İsteğe bağlı parametreler ─────────────────────────────────────────────
SEED=42
ALGORITHM=recursive_backtracker

# Çözüm animasyonu: true/false
ANIMATION=false
# Her animasyon adımı arasındaki bekleme süresi (saniye)
ANIMATION_SPEED=0.05
```

### Hata yönetimi

Program tüm yapılandırma hatalarını çökmeden yakalar:
- Zorunlu anahtar eksik
- `=` işareti olmayan satır
- Sayısal anahtarda sayı yerine harf (`WIDTH=abc`)
- `PERFECT` için geçersiz boolean değer (`PERFECT=maybe`)
- `ENTRY` / `EXIT` için yanlış tuple formatı (`ENTRY=0;0`)

---

## Parser Modülü (`src/mazegen/parser/`)

Yapılandırma dosyasını okuma ve doğrulama işlemlerini yürüten modüller.

### `config_parser.py` — Yapılandırma okuyucu

Config dosyasını satır satır okur, yorumları atlar, anahtar-değer çiftlerini doğru tiplere dönüştürür.

```python
from mazegen.parser import parse_config

cfg = parse_config("configs/config.txt")
# {'WIDTH': 20, 'HEIGHT': 15, 'ENTRY': (0, 0),
#  'EXIT': (19, 14), 'OUTPUT_FILE': 'output_maze.txt',
#  'PERFECT': False, 'SEED': 42}
```

| Anahtar | Python tipi |
|---|---|
| `WIDTH`, `HEIGHT` | `int` |
| `ENTRY`, `EXIT` | `tuple[int, int]` — `(col, row)` |
| `PERFECT` | `bool` |
| `SEED` | `int \| None` |
| `OUTPUT_FILE` | `str` |

### `validator.py` — Doğrulayıcı

`parse_config()` çıktısını alır, hatalı değerlerde `ValueError` fırlatır.

```python
from mazegen.parser import validate_config

validate_config(cfg)  # Hata yoksa sessizce geçer
```

Kontrol edilen kurallar:
- Zorunlu anahtarların tümü mevcut mu?
- `WIDTH` ve `HEIGHT` en az 1 mi?
- `ENTRY` ve `EXIT` grid sınırları içinde mi (`0 <= col < WIDTH`, `0 <= row < HEIGHT`)?
- `ENTRY` ve `EXIT` "42" deseni hücreleriyle çakışıyor mu?

---

## Çıktı Dosyası Formatı


Çıktı dosyası `OUTPUT_FILE` anahtarıyla belirtilen yola yazılır.

```
<HEIGHT satır, her satırda WIDTH hex karakter>\n
\n
<ENTRY x,y>\n
<EXIT x,y>\n
<boşluksuz N/E/S/W yönleri — örn: ESEENEEESSSEENEE>\n
```

Her hex karakter, bir hücrenin dört duvarını bit olarak kodlar:

| Bit | Yön |
|-----|-----|
| 0 (LSB) | Kuzey (North) |
| 1 | Doğu (East) |
| 2 | Güney (South) |
| 3 | Batı (West) |

`1` = duvar kapalı, `0` = duvar açık.

**Örnek:** `A` = ikili `1010` → Doğu ve Batı duvarları kapalı.

Verilen analiz betiğiyle doğrulama:
```bash
python3 maze_analyzer.py output_maze.txt
python3 maze_analyzer.py output_maze.txt --max-dead-ends 0  # braided kontrolü
```

---

## Seçilen Algoritma

**Recursive Backtracker (Derinlik Öncelikli Arama — DFS)**

### Neden bu algoritma?

- Uzun, kıvrımlı koridorlar üretir — `PERFECT=True` modu için idealdir
- Yığın (stack) tabanlı, basit bir uygulama — doğal tohum (seed) tekrarlanabilirliği
- Kolay genişletilebilir: `PERFECT=False` modunda üretim sonrası ek duvar kaldırılarak döngüler oluşturulur
- İyi belgelenmiş, yaygın bilinir — değerlendirme sırasında açıklaması kolay
- Hızlı: O(n), n = hücre sayısı

### Uygulanan bonus algoritmalar

| Algoritma | Türü | Gerekçe |
|-----------|------|---------|
| `braided` | Üretme | Tüm çıkmaz sokakları kaldırır; `--max-dead-ends 0` ile doğrulanır |
| `prim` | Üretme | Daha geniş açık alanlar üretir, DFS'ten görsel olarak farklı |
| `animation` | Görselleştirme | Labirent oluşumunun adım adım görseli |

---

## Çözüm Animasyonu

Program, maze çözümünü adım adım canlandırabilir. Bu özellik `ANIMATION=true` ile etkinleştirilir.

### Terminal Animasyonu

Terminalde ANSI escape sequence kullanılarak ekran yerinde güncellenir:

```
+---+---+---+
| S |       |
+   +---+   +
|   |   |   |
+   +   +   +
|       | E |
+---+---+---+

Adım 1/12  [0,0]
Adım 2/12  [1,0]
Adım 3/12  [1,1]
...
Adım 12/12 [2,2]  ✔️ Tamamlandı!
```

- Her adımda çözüm yolu bir hücre büyür
- `\033[2J\033[H` ile ekran temizlenir ve yeniden çizilir
- Animasyon bitince interaktif döngü devam eder
- `[A]` tuşuyla animasyonu istediğiniz zaman yeniden başlatabilirsiniz

### Animasyon Mimarisi

```python
from mazegen.rendering.animation import SolutionAnimator

animator = SolutionAnimator(solution=solution, speed=0.05)

# Adım adım iteration
for step_cells in animator.steps():
    # step_cells: o ana kadar ziyaret edilen hücre kümesi
    render_with_visited(step_cells)
```

`SolutionAnimator` UI'dan bağımsızdır — rendering bilgisi taşımaz, `mazegen` paketi içinde de kullanılabilir.

### Config Örneği

```
ANIMATION=true
ANIMATION_SPEED=0.08
```

`ANIMATION_SPEED=0.0` verilirse animasyon anlık tamamlanır (test/debug için).

---

## Yeniden Kullanılabilir Modül (`mazegen`)

Labirent üretim mantığı bağımsız, pip ile kurulabilir bir modül olarak paketlenmiştir.

### Kurulum

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

### Temel kullanım

```python
from mazegen import MazeGenerator

# Labirent oluştur ve üret
mg = MazeGenerator(width=20, height=15, seed=42, perfect=False)
mg.generate()

# Çöz (en kısa yolu bul)
solution = mg.solve()
print(solution.to_string())  # "NEESSW..."

# Labirent yapısına eriş
maze = mg.get_maze()
cell = maze.get_cell(0, 0)
print(cell.has_wall(Direction.NORTH))  # True/False

# Dosyaya aktar
mg.export("output_maze.txt")
```

### Parametreler

| Parametre | Tür | Varsayılan | Açıklama |
|-----------|-----|-----------|---------| 
| `width` | int | — | Labirent genişliği (hücre sayısı) |
| `height` | int | — | Labirent yüksekliği (hücre sayısı) |
| `seed` | int \| None | `None` | Rastgele tohum (None = rastgele) |
| `perfect` | bool | `False` | Mükemmel labirent modu |
| `algorithm` | str | `"recursive_backtracker"` | Üretim algoritması |
| `entry` | tuple | `(0, 0)` | Giriş koordinatları |
| `exit` | tuple | `(width-1, height-1)` | Çıkış koordinatları |

### Kaynaktan yeniden derleme

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install build
python3 -m build
```

---

## Resources

### Labirent teorisi
- [Labirent üretim algoritmaları — Jamis Buck](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Mazes for Programmers — kitap](http://www.mazesforprogrammers.com/)
- [Vikipedi: Labirent üretim algoritması](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

### En kısa yol
- [BFS — Vikipedi](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Graf geçiş algoritmaları](https://en.wikipedia.org/wiki/Graph_traversal)

### Python paketleme
- [pyproject.toml referansı](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Python Paketleme Kullanım Kılavuzu](https://packaging.python.org/)

### Yapay zeka kullanımı
> Yapay zeka şu amaçlarla kullanıldı: mimari planlama, diyagram yapılandırma, config hata senaryolarının belirlenmesi ve algoritma seçim gerekçesi. Yapay zeka tarafından üretilen tüm içerik, dahil edilmeden önce incelendi, anlaşıldı ve uyarlandı. Hiçbir yapay zeka kodu tam anlaşılmadan kopyalanmadı.

---

## Takım & Proje Yönetimi

### Takım

| Kullanıcı adı | Rol |
|---------------|-----|
| `ybalkan` | Proje mimarisi, API tasarımı, ASCII renderer, animasyon sistemi, paketleme |
| `iuslu` | Modeller (Cell/Maze/Direction/Solution), config parser, validator, üretim algoritmaları |

### Görev Dağılımı

**ybalkan:**
- `MazeGenerator` API sınıfı
- `AsciiRenderer` interaktif döngü + `SolutionAnimator`
- `pyproject.toml`, `Makefile`, paket yapısı
- Birim testler (solving, generation)

**iuslu:**
- `Cell`, `Maze`, `Direction`, `Solution` modelleri
- `config_parser.py`, `validator.py`
- `RecursiveBacktracker`, `PrimGenerator`, `BraidedGenerator`
- Birim testler (parser)


### Planlama

| Aşama | Hedef Tarih | Durum |
|-------|-------------|-------|
| Gereksinim analizi ve mimari | 2026-08-29 | ✅ Tamamlandı |
| Proje iskeleti (klasör + dosya yapısı) | 2026-08-30 | ✅ Tamamlandı |
| Modeller: direction, cell, maze, solution | 2026-09-05 | ✅ Tamamlandı |
| Parser: config_parser, validator | 2026-09-07 | ✅ Tamamlandı |
| Üretim: recursive_backtracker | 2026-09-07 | ✅ Tamamlandı |
| Bonus üretim: prim, braided | 2026-09-08 | ✅ Tamamlandı |
| Çözüm: bfs_solver | 2026-09-09 | ✅ Tamamlandı |
| Kapsamlı kod denetimi ve bug düzeltmeleri | 2026-09-09 | ✅ Tamamlandı |
| Dosya yazma: output_writer | 2026-09-10 | ✅ Tamamlandı |
| Görselleştirme: ascii_renderer + etkileşimler | 2026-09-10 | ✅ Tamamlandı |
| API: MazeGenerator sınıfı + paketleme | 2026-09-10 | ✅ Tamamlandı |
| Makefile + pyproject.toml tamamlanması | 2026-09-10 | ✅ Tamamlandı |
| Son inceleme + değerlendirme hazırlığı (Unit test & Linting) | 2026-09-10 | ✅ Tamamlandı |

### İyi ve Geliştirilebilecek Yönler (Retrospektif)

**İyi Giden Şeyler:**
- Yapay zeka eşliğinde başlangıçta çok sağlam bir proje iskeleti ve mimari plan oluşturmamız, ileride yaşanacak karmaşayı engelledi.
- Baştan `.gitignore`, `Makefile` ve geçici dosya temizliği (obj/) gibi standartları oturtmak, geliştirme ortamımızı çok temiz tuttu.

**Geliştirilebilecek Yönler (İyileştirmeler):**
- Yapay zekanın doğrudan kod yazması yerine rehber (pair-programmer) olarak kullanılması gerektiği başta net değildi, bu stratejiyi sonradan oturtmamız gerekti.
- Büyük labirent boyutlarında (örneğin 100x100) Python'ın varsayılan rekürsiyon limiti (recursion limit) sorun yaratabilir, optimizasyon gerekecek.

### Yapay Zeka Kullanımı

> Proje boyunca yapay zeka aşağıdaki alanlarda kullanıldı:
>
> - **Mimari planlama:** Modül yapısı (mazegen/api, models, generation, solving, rendering) tasarlandı.
> - **Algoritma araştırması:** BFS karşılaştırması ve üretim algoritmalarının incelenmesi.
> - **Hata ayıklama:** Duvar tutarlılığı (wall consistency), `unsafe_hash`, `came_from` geri izleme.
> - **Dokümentasyon:** README yapısı ve config örnekleri.
> - **Animasyon mimarisi:** `SolutionAnimator` sınıfı tasarlandı; `steps()` generator entegrasyonu.
> - **Kod incelemesi:** mypy ve flake8 uyumluluğu, type hint doğrulaması.
>
> Tüm yapay zeka önerileri incelendi, anlaşıldı ve elle uyarlandı.
> Hiçbir yapay zeka kodu tam anlaşılmadan kopyalanmadı.

### Kullanılan araçlar
- **Antigravity IDE** — Yapay zeka destekli mimari planlama ve diyagram oluşturma
- **Python 3.14** — Ana dil
- **flake8 + mypy** — Kod kalitesi ve tür kontrolü
- **pytest** — Birim testleri
- **git** — Sürüm kontrolü (vogsphere.42kocaeli.com.tr)

---

## Geliştirme Günlüğü

> Bu bölüm projede yapılan her adımı tarih sırasıyla kaydeder.
> Her yeni çalışmadan sonra güncellenir.

---

### 📅 2026-08-29 — Planlama & Analiz Günü

#### ▸ Konu PDF'i okundu (`a-maze-ing.pdf`)

Projenin tüm gereksinimleri ilk kez okundu ve aşağıdaki zorunlu maddeler çıkarıldı:

- Ana program adı `a_maze_ing.py` olmalı — başka isim kabul edilmez
- Config dosyası `KEY=VALUE` formatında, `#` yorum satırları desteklenmeli
- Zorunlu config anahtarları: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`
- Çıktı dosyası hex encoding ile yazılmalı (bit 0=N, 1=E, 2=S, 3=W)
- Çıktı formatı: HEIGHT satır hex → boş satır → ENTRY → EXIT → N/E/S/W yolu
- Görsel: ASCII terminal
- Zorunlu etkileşimler: yeniden üret, yolu göster/gizle, duvar rengi değiştir
- Yeniden kullanılabilir paket: `mazegen-*` adıyla `.whl`, **repo kökünde** olmalı
- `LICENSE.md` zorunlu — yeniden kullanıma izin veren lisans
- Bonus: braided (çıkmaz sokaksız), çoklu algoritma, animasyon

#### ▸ Değerlendirme belgesi okundu (`amazeing_evo_eng.pdf`)

Değerlendirme sırasında test edilecek tüm senaryolar çıkarıldı:

- `maze_analyzer.py` **konu tarafından veriliyor**, repo kökünde bulunmalı
- Değerlendirici config dosyasını düzenleyerek **5 hata senaryosunu** bizzat test edecek:
  1. Zorunlu anahtar eksik
  2. `=` işareti olmayan satır
  3. Sayı yerine harf (`WIDTH=abc`)
  4. Geçersiz boolean (`PERFECT=maybe`)
  5. Yanlış tuple formatı (`ENTRY=0;0`)
- `maze_analyzer.py output_maze.txt` çalışmalı → PERFECT veya Pac-Man-USABLE sonucu
- Yeniden kullanılabilir modül: farklı sanal ortamda derleme → kurulum → çalıştırma zinciri test edilecek
- README'nin **her bölümü tek tek** kontrol edilecek — herhangi biri eksikse not = 0

#### ▸ Algoritmaların rolü netleştirildi

İki algoritma kategorisi birbirinden ayrıldı:

| Tür | Ne Yapar | Zorunlu | Bonus |
|-----|----------|---------|-------|
| **Üretme** | Labirenti inşa eder (duvarları koyar/açar) | Recursive Backtracker | Prim, Braided |
| **Çözme** | Bitmiş labirentte yolu bulur | BFS | — |

#### ▸ Bonus sıralaması belirlendi

| Öncelik | Bonus | Neden Öne Alındı |
|---------|-------|-----------------|
| 1 | **Braided** | `maze_analyzer --max-dead-ends 0` ile kanıtlanır — en somut, en değerli |
| 2 | **Prim** | Basit, hızlı, mülakatlarda çok sorulan |
| 3 | **Animation** | Görsel, değerlendirmede etkileyici |

---

### 📅 2026-08-30 — Yapı Kurulum & README Günü

#### ▸ Tüm klasör ve dosyalar oluşturuldu

Proje yapısı birebir uygulandı. Oluşturulan gruplar:

**Kök dizin:**
`README.md` · `LICENSE.md` · `.gitignore` · `Makefile` · `pyproject.toml` · `requirements.txt` · `a_maze_ing.py` · `maze_analyzer.py` · `output_maze.txt` · `mazegen-0.1.0-py3-none-any.whl`

**`src/mazegen/` — tüm modüller:**

| Alt paket | Dosyalar |
|-----------|---------| 
| `models/` | `direction.py`, `cell.py`, `maze.py`, `solution.py` |
| `parser/` | `config_parser.py`, `validator.py` |
| `generation/` | `generator_base.py`, `recursive_backtracker.py`, `prim.py`, `braided.py` |
| `solving/` | `solver_base.py`, `bfs_solver.py` |
| `rendering/` | `color_palette.py`, `ascii_renderer.py`, `animation.py` |
| `io/` | `output_writer.py` |
| `api/` | `maze_generator.py` |

**`tests/` (6 dosya):**
`test_parser.py` · `test_generation.py` · `test_solving.py` · `valid_maze.txt` · `expected_output.txt` · `sample_solution.txt`

---

### 📅 2026-09-05 — Models Katmanı Kodlama Günü

#### ▸ `direction.py` yazıldı ve doğrulandı

- `Direction` enum'u PDF spec'e göre bit sırasıyla tanımlandı: `NORTH=0b0001`, `EAST=0b0010`, `SOUTH=0b0100`, `WEST=0b1000`
- `.opposite` (karşı yön), `.delta` (koordinat farkı), `.dx` / `.dy` (yatay/dikey kısayollar) property'leri eklendi.
- `maze_analyzer.py` ile uyumlu hex çıktısı için bit sırası doğrulandı: `bit 0 (LSB) = North, bit 1 = East, bit 2 = South, bit 3 = West`
- `flake8` ve `mypy` sıfır hata/uyarı ile geçti.

#### ▸ `cell.py` yazıldı (ve sonrasında `dataclass` olarak güncellendi)

- `Cell` sınıfı okunabilirliği artırmak ve otomatik `__eq__` (eşitlik) metodundan faydalanmak için `dataclass` yapısına geçirildi.
- Her hücre başlangıçta `walls = 0b1111` (4 duvar kapalı) ve `visited = False` ile oluşturuluyor.
- Bitmask tabanlı `has_wall()`, `add_wall()`, `remove_wall()` metodları eklendi.
- `to_hex()` / `from_hex()` metodlarıyla PDF çıktı formatına (`output_maze.txt`) doğrudan uyumlu hex dönüşümü sağlandı.

#### ▸ `maze.py` yazıldı (ve sonrasında `dataclass` olarak güncellendi)

- `Maze` sınıfı `dataclass` yapısına geçirilerek, `grid` alanı `__post_init__` içerisinde başlatıldı.
- `width × height` boyutunda `Cell` matrisi oluşturuluyor: `grid[row][col]`
- `get_cell()`, `in_bounds()`, `get_adjacent_cells()`, `get_accessible_neighbors()` metodları eklendi.
- `remove_wall_between(cell, neighbor, direction)` her iki komşuda da duvarı eş zamanlı kaldırıyor (tutarlılık garantisi).
- `reset_visited_flags()` üretimden çözüme geçiş için eklendi.

#### ▸ `solution.py` yazıldı

- Yol koordinatları (`path_cells`) ve yön listesi (`directions`) ayrı ayrı saklanıyor.
- `to_string()` PDF'te istenen `"NESW..."` formatını üretiyor.

#### ▸ Kritik import sorunu tespit edilip düzeltildi

- Tüm dosyalardaki `from src.mazegen.models...` mutlak importlar `from .direction import Direction` gibi **göreli import**'lara çevrildi.
- Neden önemli: `pip install mazegen.whl` sonrası paket `mazegen` olarak kurulur; `src.mazegen` yolu geçersiz hale gelir.

---

### 📅 2026-09-08 — Generation Katmanı Kodlama Günü

#### ▸ `generator_base.py` tamamlandı

- `GeneratorBase` soyut sınıfı `GeneratorBase(ABC)` olarak tanımlandı.
- `width`, `height`, `seed` parametreleri zorunlu; `generate() -> Maze` metodu soyut.

#### ▸ `recursive_backtracker.py` tamamlandı

- DFS tabanlı iteratif implementasyon (stack ile, Python recursion limitini aşmaz).
- `random.Random(seed)` ile izole rastgelelik — global `random` state'i kirletmez.
- Seed tekrarlanabilirliği doğrulandı: aynı seed → birebir aynı labirent.

#### ▸ Bonus üretim algoritmaları tamamlandı

- `prim.py` — frontier listesi tabanlı Random Prim; daha kısa koridorlar, fazla dal.
- `braided.py` — DFS perfect maze üretip dead-end hücreleri `braid_ratio` oranında açar.
  - `maze_analyzer --max-dead-ends 0` ile doğrulandı.

---

### 📅 2026-09-09 — Solving Katmanı & Kapsamlı Denetim Günü

#### ▸ `solver_base.py` tamamlandı

- `SolverBase(ABC)` — `GeneratorBase` ile simetrik yapı.
- `maze`, `entry: tuple[int,int]`, `exit_: tuple[int,int]` alır; `solve() -> Solution | None` soyut.

#### ▸ `bfs_solver.py` tamamlandı (zorunlu)

- BFS ile garantili en kısa yol; `came_from` sözlüğüyle yol geri izleme.
- `get_accessible_neighbors()` ile duvar-farkında geçiş.
- `Solution` nesnesi döner — `to_string()` → `"ESEENEE..."` (boşluksuz N/E/S/W).

#### ▸ Kapsamlı kod denetimi yapıldı

| Dosya | Hata | Düzeltme |
|---|---|---|
| `cell.py` | `dataclass(eq=True)` `__hash__`'i siliyor; Cell dict key olamazdı | `unsafe_hash=True` eklendi |
| `maze.py` | `get_adjacent_cell` ve `get_accessible_neighbors` tamamen aynı kod (duplicate) | `get_adjacent_cell` → duvarsız tüm komşular; `get_accessible_neighbors` → açık duvarlar |
| `models/__init__.py` | Tamamen boştu, hiçbir sınıf export edilmiyordu | `Cell, Direction, Maze, Solution` eklendi |
| `validator.py` | `ENTRY==EXIT` kontrolü docstring'de vardı ama kodda yoktu | `entry == exit_` kontrolü eklendi |
| `solution.py` | `to_string()` → `"N E S W"` (boşluklu) üretiyordu | `"".join(...)` → `"NESW"` (boşluksuz, PDF uyumlu) |
| `config_parser.py` | `ENTRY=0;0` formatı `IndexError` fırlatıyordu | `try/except` ile temiz `ValueError` |

#### ▸ 5 EV hata senaryosunun tamamı geçti

```
1. Zorunlu key eksik        → ValueError: Config eksik: 'EXIT' bulunamadı.
2. = işareti olmayan satır  → Satır atlandı, crash yok.
3. WIDTH=abc                → ValueError: invalid literal for int()
4. PERFECT=maybe            → False döndü (crash yok)
5. ENTRY=0;0                → ValueError: Geçersiz koordinat formatı
```

---

### 📅 2026-09-12 — I/O ve Rendering Katmanı Kodlama Günü

#### ▸ `output_writer.py` tamamlandı
- Hex formatlama, `maze_analyzer.py` beklentisine tam uyumlu hale getirildi. Her hücre 1 hex karakterine çevrildi.
- Giriş, çıkış noktaları eklendi ve rota (N/E/S/W formatında boşluksuz) kaydedildi.

#### ▸ `ascii_renderer.py` ve Terminal Arayüzü (UI) yazıldı
- Terminal üzerinde labirentin Unicode karakterleriyle estetik bir şekilde çizilmesi için `AsciiRenderer` sınıfı oluşturuldu.
- `ANIMATION=true` ayarı desteklenerek, DFS üretim sürecinin terminal üzerinde adım adım izlenmesi sağlandı (Bonus puan).
- Tema (Tema 1-5) ve renk değiştirme özellikleri için `color_palette.py` yapısı kuruldu.

---

### 📅 2026-09-14 — "42" Deseni ve Algoritma Entegrasyon Günü

#### ▸ "42" Deseni Mantığı İyileştirildi
- Merkezdeki "42" deseni için kapalı duvarlı `X` hücreleri oluşturuldu ve algoritmanın bunları kazmaması için `visited = True` yapıldı.
- Görsel olarak bu "42" deseninin diğer duvarlardan ayrışması için özel Siyan (Cyan) `#` sembolleri ile statik çizim eklendi.

#### ▸ `maze_generator.py` API'si kodlandı
- Kullanıcıya açık tek merkez olan `MazeGenerator` API sınıfı kodlandı.
- Konfigürasyon dosyasına göre (`recursive_backtracker`, `prim`, `braided`) ilgili algoritmayı dinamik seçen yapı kuruldu.
- `PERFECT=False` durumunda `BraidedGenerator` çağrılarak `braid_ratio=1.0` ile tüm çıkmaz sokakların temizlenmesi (Pac-Man board) kurgulandı.

---

### 📅 2026-09-16 — CLI (Ana Döngü) ve Test Günü

#### ▸ `a_maze_ing.py` (CLI) tamamlandı
- `config.txt` dosyasını argüman olarak okuyup, API'yi çağıran ana döngü kuruldu.
- PDF'in istediği zorunlu butonlar (Yeni Üret [R], Çözüm Göster/Gizle [P], Renk Değiştir [C]) eklendi.
- `make run` entegrasyonu ile terminal üzerinden hatasız çalışması sağlandı.

#### ▸ Birim Testler (Unit Tests) ve Linting
- `tests/unit/` altında `test_parser.py`, `test_generation.py`, `test_solving.py` birim testleri yazıldı ve doğrulandı.
- `make lint` (flake8 + mypy) hataları tamamen temizlenerek sıfır hataya ulaşıldı.

---

### 📅 2026-09-17 — Temizlik ve PDF Uyumluluk / Analyzer Test Günü

#### ▸ Proje Mimarisi Sadeleştirildi ve Hatalar Giderildi
- MLX grafik kütüphanesine ihtiyaç duyulmadığı ve terminal arayüzünün (AsciiRenderer) PDF şartlarını tek başına %100 karşıladığı teyit edilerek `mlx_renderer.py` tamamen kaldırıldı.
- Aşırı karmaşıklık yaratan ancak zorunlu olmayan `astar_solver.py`, `dijkstra_solver.py` ve `kruskal.py` modülleri temizlendi.
- Tüm yorum satırları ve docstring'ler kaynak koddan kaldırıldı.
- `Makefile` güncellenerek yalnızca `.whl` çıktısı alınacak şekilde optimize edildi ve root dizini kirliliği önlendi.

#### ▸ Resmi 42 `maze_analyzer.py` Doğrulaması (Kusursuz Sonuçlar)
- **PERFECT=True (Mükemmel Labirent):** Algoritma test edildi. `Verdict: PERFECT maze: a single path, no loop` sonucu alındı (0 Döngü).
- **PERFECT=False (Pac-Man Modu):** Test edildi. `Verdict: Pac-Man-USABLE: fully connected, corners and centre reachable... no real dead-end -> bonus-grade (perfectly braided)` sonucuyla %100 başarı ve Bonus puan kazanıldı.
- "42" deseni çevresindeki tutarsız duvar hataları giderilerek "Wall coherence: OK" raporuna ulaşıldı.

---

### ✅ Tüm Görevler Tamamlandı! (Final Durumu)

```
[x] src/mazegen/models/direction.py
[x] src/mazegen/models/cell.py
[x] src/mazegen/models/maze.py
[x] src/mazegen/models/solution.py
[x] src/mazegen/models/__init__.py
[x] src/mazegen/parser/config_parser.py
[x] src/mazegen/parser/validator.py
[x] src/mazegen/generation/generator_base.py
[x] src/mazegen/generation/recursive_backtracker.py
[x] src/mazegen/generation/prim.py          (Bonus)
[x] src/mazegen/generation/braided.py       (Bonus)
[x] src/mazegen/solving/solver_base.py
[x] src/mazegen/solving/bfs_solver.py
[x] src/mazegen/io/output_writer.py
[x] src/mazegen/rendering/color_palette.py
[x] src/mazegen/rendering/ascii_renderer.py
[x] src/mazegen/rendering/animation.py      (Bonus)
[x] src/mazegen/api/maze_generator.py
[x] src/mazegen/__init__.py                 (API export)
[x] a_maze_ing.py                           (CLI / Main)
[x] configs/ ve tests/ klasörlerinin tamamlanması
[x] Kullanılmayan dosyaların (MLX, kruskal, dijkstra, astar) temizliği
[x] Tüm yorum satırları ve docstring'lerin temizlenmesi
[x] mypy ve flake8 (make lint) pürüzsüz geçişi
[x] Makefile build komutunun .whl üretecek şekilde güncellenmesi
[x] maze_analyzer.py ile Final PDF uygunluk testlerinin başarıyla geçilmesi
```

---

### 📅 2026-09-20 — Global Compatibility & Final Code Review

#### ▸ Full English translation completed

All Turkish strings remaining in the codebase were identified and replaced with English equivalents:

- Source comments and step-marker comments removed from `__init__.py`, `__main__.py`, `tests/__init__.py`, `tests/unit/__init__.py`
- All error messages in `config_parser.py` and `validator.py` translated to English
- All UI strings in `ascii_renderer.py` (menu labels, status lines, controls) translated
- Log/status strings in `animation.py` translated
- Theme names `"Klasik"`, `"Zindan"`, `"Tam Blok"` → `"Classic"`, `"Dungeon"`, `"Full Block"`
- All test `assert` messages and `pytest.raises(match=...)` strings updated to match the new English error messages
- Config example file comments translated
- Entry point usage string `<config_dosyası>` → `<config_file>`
- Verified with `grep` for Turkish Unicode characters — **zero matches** in all project files

#### ▸ Critical bugs fixed during final review

| File | Bug | Fix |
|---|---|---|
| `models/maze.py` | `@dataclass` missing `width: int` and `height: int` fields — `Maze(5, 5)` raised `TypeError` at runtime | Added `width` and `height` as proper dataclass fields |
| `mazegen/__init__.py` | File was empty — `import mazegen; mazegen.MazeGenerator` failed; `test_reusable_module_import` failed | Exported full public API: `MazeGenerator`, `Maze`, `Cell`, `Direction`, `Solution`, renderers, generators, solver |
| `ascii_renderer.py` | `"".join(lines)` — entire maze rendered as a single line with no newlines | Fixed to `"\n".join(lines)` |
| `tests/unit/test_parser.py` | `match="Config eksik"` and `match="negatif"` — stale Turkish regex strings that no longer matched the English error messages, causing silent test failures | Updated to `"Config is missing required key"` and `"cannot be negative"` |
| `a_maze_ing.py` | `for arg in sys.argv[1:]: config_path = arg` — silently discarded all arguments except the last | Replaced with `config_path = sys.argv[1]` |
| `animation.py` | `yield frozenset(visited)` — mypy type mismatch against `Set[Tuple[int,int]]` | Changed to `yield set(visited)` |
| `ascii_renderer.py` | `maze_generator: object` type hint caused 9 mypy `attr-defined` errors | Changed to `maze_generator: Any` |
| `a_maze_ing.py` | `renderer._regenerate = _regenerate_and_export` — mypy `method-assign` error | Added `# type: ignore[method-assign]` |
| `.gitignore` | `output_maze.txt` (generated file) was not listed | Added `output_maze.txt` |
| `__main__.py` | Completely empty — `python3 -m mazegen` did nothing | Wired to `a_maze_ing.main()` |
| `__main__.py`, `tests/__init__.py` | Blank-only files triggered flake8 `W391` | Truncated to truly empty files |
| `a_maze_ing.py` imports | Post-`sys.path.insert` imports triggered flake8 `E402` | Added `# noqa: E402` to each import |

#### ▸ Final verification results

```
pytest  : 32 / 32 PASSED
flake8  : 0 errors
mypy    : 0 errors  (32 source files)
Turkish : 0 characters found
```

#### ▸ End-to-end run confirmed

```bash
python3 a_maze_ing.py configs/config.txt   # exit 0 — maze rendered, output written
python3 -m mazegen configs/config.txt      # exit 0 — identical behaviour
python3 a_maze_ing.py                      # exit 1 — usage message
python3 a_maze_ing.py nonexistent.txt      # exit 1 — file not found message
python3 a_maze_ing.py configs/examples/invalid/missing_key.txt  # exit 1 — validation error
```

```
maze_analyzer.py output_maze.txt
→ PERFECT maze / Pac-Man-USABLE  ✅
→ Wall coherence: OK              ✅
```

