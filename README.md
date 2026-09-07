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
1. Terminalde ASCII görsel çıktı veya grafik pencere (MLX).
2. Tüm labirent yapısını ve en kısa yolu içeren onaltılık (hex) çıktı dosyası.
3. Başka projelere kurulup içe aktarılabilen yeniden kullanılabilir bir `mazegen` paketi.

---

## Instructions

### Gereksinimler

- Python 3.10+
- Kod kalitesi için `flake8` ve `mypy` (bkz. `Makefile`)
- Grafik pencere için MLX kütüphanesi (`mlx-2.2.tgz`) — isteğe bağlı

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
# Varsayılan yapılandırmayla çalıştır
make run

# Ya da doğrudan
python3 a_maze_ing.py configs/default.txt
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
```

### Paketi derleme

```bash
# Sanal ortamda:
python3 -m pip install build
python3 -m build
# Çıktı: proje kökünde mazegen-*.whl ve mazegen-*.tar.gz
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

| Anahtar | Tür | Açıklama | Örnek |
|---------|-----|----------|-------|
| `SEED` | int | Tekrarlanabilirlik için rastgele tohum | `SEED=42` |
| `ALGORITHM` | str | Üretim algoritması | `ALGORITHM=recursive_backtracker` |

### Örnek yapılandırma (`configs/default.txt`)

```
# A-Maze-Ing varsayılan yapılandırma
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=False
SEED=42
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

Yapılandırma dosyasını okuma, doğrulama ve hex dönüşümü işlemlerini yürüten modüller.

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

### `hex_decoder.py` — Hex ↔️ Maze dönüştürücü

Hex string satırlarını `Maze` nesnesine uygular; `Maze` nesnesini hex satırlarına çevirir.

```python
from mazegen.parser import maze_to_hex_lines, apply_hex_lines_to_maze

# Maze → hex satırları (output dosyası için)
lines = maze_to_hex_lines(maze)  # ['9135', 'ac2a', ...]

# Hex satırları → Maze (config dosyası okunduğunda)
apply_hex_lines_to_maze(maze, lines)
```

Hex encoding kuralı:

| Bit | Yön | Değer |
|---|---|---|
| bit 0 | North | `0x1` |
| bit 1 | East | `0x2` |
| bit 2 | South | `0x4` |
| bit 3 | West | `0x8` |

`1` = duvar var (kapalı), `0` = duvar yok (açık).

`hex_string_to_row()` fonksiyonu tek bir hex string satırını integer listesine çevirir:

```python
from mazegen.parser import hex_string_to_row

hex_string_to_row('9a5f')  # [9, 10, 5, 15]
```

### Public API özeti

```python
from mazegen.parser import (
    parse_config,           # config.txt → dict
    validate_config,        # dict doğrulama, ValueError fırlatır
    hex_string_to_row,      # '9a5f' → [9, 10, 5, 15]
    maze_to_hex_lines,      # Maze → ['9135', 'ac2a', ...]
    apply_hex_lines_to_maze # ['9135', ...] → Maze (yerinde günceller)
)
```

---

## Çıktı Dosyası Formatı


Çıktı dosyası `OUTPUT_FILE` anahtarıyla belirtilen yola yazılır.

```
<HEIGHT satır, her satırda WIDTH hex karakter>\n
\n
<ENTRY x,y>\n
<EXIT x,y>\n
<boşlukla ayrılmış N/E/S/W yönleri>\n
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
| `kruskal` | Üretme | Union-Find kullanır — faydalı bir veri yapısı öğretir |
| `animation` | Görselleştirme | Labirent oluşumunun adım adım görseli |

---

## Yeniden Kullanılabilir Modül (`mazegen`)

Labirent üretim mantığı bağımsız, pip ile kurulabilir bir modül olarak paketlenmiştir.

### Kurulum

```bash
pip install mazegen-0.1.0-py3-none-any.whl
# ya da
pip install mazegen-0.1.0.tar.gz
```

### Temel kullanım

```python
from mazegen import MazeGenerator

# Labirent oluştur ve üret
mg = MazeGenerator(width=20, height=15, seed=42, perfect=False)
mg.generate()

# Çöz (en kısa yolu bul)
solution = mg.solve()
print(solution.to_string())  # "N E E S S W ..."

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
| `ybalkan` | Takım üyesi |
| `iuslu` | Takım üyesi |

### Planlama

| Aşama | Hedef Tarih | Durum |
|-------|-------------|-------|
| Gereksinim analizi ve mimari | 2026-08-29 | ✅ Tamamlandı |
| Proje iskeleti (klasör + dosya yapısı) | 2026-08-30 | ✅ Tamamlandı |
| Modeller: direction, cell, maze, solution | 2026-09-05 | ✅ Tamamlandı |
| Parser: config_parser, validator, hex_decoder | 2026-09-07 | ✅ Tamamlandı |
| Üretim: recursive_backtracker | 2026-09-07 | ✅ Tamamlandı |
| Çözüm: bfs_solver | — | 🔲 Bekliyor |
| Dosya yazma: output_writer | — | 🔲 Bekliyor |
| Görselleştirme: ascii_renderer + etkileşimler | — | 🔲 Bekliyor |
| API: MazeGenerator sınıfı + paketleme | — | 🔲 Bekliyor |
| Makefile + pyproject.toml | — | 🔲 Bekliyor |
| Bonus: braided, prim, kruskal, animation | — | 🔲 Bekliyor |
| Son inceleme + değerlendirme hazırlığı | — | 🔲 Bekliyor |

### İyi ve Geliştirilebilecek Yönler (Retrospektif)

**İyi Giden Şeyler:**
- Yapay zeka eşliğinde başlangıçta çok sağlam bir proje iskeleti ve mimari plan oluşturmamız, ileride yaşanacak karmaşayı engelledi.
- Baştan `.gitignore`, `Makefile` ve geçici dosya temizliği (obj/) gibi standartları oturtmak, geliştirme ortamımızı çok temiz tuttu.

**Geliştirilebilecek Yönler (İyileştirmeler):**
- Yapay zekanın doğrudan kod yazması yerine rehber (pair-programmer) olarak kullanılması gerektiği başta net değildi, bu stratejiyi sonradan oturtmamız gerekti.
- Büyük labirent boyutlarında (örneğin 100x100) Python'ın varsayılan rekürsiyon limiti (recursion limit) sorun yaratabilir, optimizasyon gerekecek.

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
- Görsel: ASCII terminal veya MLX grafik pencere (en az biri zorunlu)
- Zorunlu etkileşimler: yeniden üret, yolu göster/gizle, duvar rengi değiştir
- Yeniden kullanılabilir paket: `mazegen-*` adıyla `.whl` veya `.tar.gz`, **repo kökünde** olmalı
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

#### ▸ İlk diyagram incelendi ve düzeltildi (`Diagram/diagram.md`)

Başka bir yapay zeka tarafından hazırlanan ilk tam proje ağacı incelendi. Tespit edilen sorunlar:

- `src/mazegen/__init__.py` **iki kez** yazılmıştı → kaldırıldı
- `work/` klasörü 16 faz dosyasını ayrı ayrı listeliyordu → tek satıra indirildi
- `dist/` klasörü gösterilmişti, oysa `.whl` ve `.tar.gz` **kök dizinde** olmalı → düzeltildi
- Hiçbir dosyada açıklama yoktu → her satıra Türkçe açıklama eklendi
- `tmp/` dosyaları `# tmp -> açıklaması` formatıyla etiketlendi
- `maze_analyzer.py` hiç yoktu → eklendi, `[KONU TARAFINDAN VERİLİYOR]` notu ile

#### ▸ Minimal diyagram oluşturuldu (`Diagram/diagram_minimal.md`)

PDF ve değerlendirme belgesine dayanarak yalnızca gerekli dosyaları içeren temiz bir yapı çıkarıldı.

**Diyagramdan silinen fazlalıklar:**

| Silinen | Neden |
|---------|-------|
| `docs/` (8 dosya) | Sadece `README.md` zorunlu |
| `assets/` | PDF'de geçmiyor |
| `examples/` | README yeterli |
| `notebooks/` | PDF'de yok |
| `dist/` klasörü | `.whl` kök dizinde olmalı, `dist/` yanlış |
| `scripts/` betikleri | PDF gerektirmiyor |
| `utils/`, `extras/` | Önceden planlamak yerine gerekince eklenir |
| `setup.cfg` | `pyproject.toml` yeterli |
| `models/coordinate.py` | `tuple` yeterli, ayrı dosya şişirme |

**Diyagrama eklenen eksikler:**

- `maze_analyzer.py` kök dizine taşındı — PDF "konu tarafından veriliyor" diyor
- `configs/examples/invalid/` altına 5 hata dosyası eklendi (değerlendirme testleri için)
- `color_palette.py` bonus değil **zorunlu** olarak yeniden etiketlendi
- Her dosya ve klasöre `[Z]`, `[DEĞ]`, `[B]` etiketi eklendi

#### ▸ Algoritmaların rolü netleştirildi

İki algoritma kategorisi birbirinden ayrıldı:

| Tür | Ne Yapar | Zorunlu | Bonus |
|-----|----------|---------|-------|
| **Üretme** | Labirenti inşa eder (duvarları koyar/açar) | Recursive Backtracker | Prim, Kruskal, Braided, Wilson |
| **Çözme** | Bitmiş labirentte yolu bulur | BFS | Dijkstra, A* |

> Wilson da bir **üretme** algoritmasıdır — BFS'e benzer görünür ama labirenti inşa eder, çözmez.
> Bonus için birden fazla **üretme** algoritması ekliyoruz.

#### ▸ Kodlama sırası metaforlaştırıldı

"Şehir kuruyorsun" metaforu geliştirildi ve her adım için ayrıntılandırıldı:

```
1.  direction.py          → pusula yap            (N/E/S/W ne demek?)
2.  cell.py               → tek arsa parseli       (4 kenarında duvar var/yok)
3.  maze.py               → tüm şehir planı        (WIDTH × HEIGHT ızgara)
4.  config_parser.py      → inşaat ruhsatını oku   (belediyeye başvuru)
5.  validator.py          → ruhsat eksikse ret      (hata yönetimi)
6.  hex_decoder.py        → ruhsattaki kodu çöz    (hex → duvar)
7.  recursive_backtracker → şehri inşa et          (duvarları koy/aç)
8.  bfs_solver.py         → en kısa yolu bul       (navigasyon)
9.  output_writer.py      → haritayı dosyaya yaz   (kağıda bas)
10. ascii_renderer.py     → şehri ekranda göster   (fotoğrafını çek)
11. maze_generator.py     → "şehir şirketi" kur    (API paketi)
12. a_maze_ing.py         → belediye başkanı        (hepsine emir verir)
13. Makefile + pyproject  → şehir yönetmeliği
14. README.md             → şehir rehberi           (yabancılar için)
15. BONUS                 → yeni inşaat firmaları   (Prim, Kruskal, Braided)
```

Her adım için `diagram_minimal.md`'de ayrıntılı açıklama yazıldı:
- Ne yapar · İçerik (hangi metodlar) · Neden bu sırada · Değerlendirmede nasıl test edilir · Çıktısı ne

#### ▸ Bonus sıralaması belirlendi

| Öncelik | Bonus | Neden Öne Alındı |
|---------|-------|-----------------|
| 1 | **Braided** | `maze_analyzer --max-dead-ends 0` ile kanıtlanır — en somut, en değerli |
| 2 | **Prim** | Basit, hızlı, mülakatlarda çok sorulan |
| 3 | **Kruskal** | Union-Find veri yapısını öğretir |
| 4 | **Animation** | Görsel, değerlendirmede etkileyici |
| 5 | Wilson | Büyük ızgaralarda yavaş, anlatması zor — en sona |

#### ▸ Diyagram Markdown formatına alındı

`diagram_minimal.md` düz metin (yorum satırı) formatından tam Markdown formatına dönüştürüldü:

- Etiket referans tablosu
- Proje ağacı kod bloğu
- Tıklanabilir değerlendirme kontrol listesi (`- [ ]`)
- Her adım için tablo: `Ne yapar / İçerik / Değerlendirme testi / Çıktı`
- Bonus öncelik tablosu

Eski düz metin versiyon `Diagram/diagram_minimal_ilk.md` olarak yedeklendi.

---

### 📅 2026-08-30 — Yapı Kurulum & README Günü

#### ▸ Tüm klasör ve dosyalar oluşturuldu

`diagram_minimal.md`'deki yapı birebir proje dizinine uygulandı. Oluşturulan gruplar:

**Kök dizin (11 dosya):**
`README.md` · `LICENSE.md` · `.gitignore` · `Makefile` · `pyproject.toml` · `requirements.txt` · `a_maze_ing.py` · `maze_analyzer.py` · `output_maze.txt` · `mazegen-0.1.0-py3-none-any.whl` · `mazegen-0.1.0.tar.gz`

**`configs/` (9 dosya):**
- `default.txt` — çalışan yapılandırma (20×15, SEED=42, PERFECT=False)
- `examples/valid/` — `basic.txt`, `medium.txt`, `seed_42.txt`
- `examples/invalid/` — `missing_key.txt`, `bad_format.txt`, `letters_for_numbers.txt`, `bad_perfect.txt`, `bad_entry_format.txt`

**`src/mazegen/` (33 dosya) — tüm modüller:**

| Alt paket | Dosyalar |
|-----------|---------|
| `models/` | `direction.py`, `cell.py`, `maze.py`, `solution.py` |
| `parser/` | `config_parser.py`, `validator.py`, `hex_decoder.py` |
| `generation/` | `generator_base.py`, `recursive_backtracker.py`, `prim.py`, `kruskal.py`, `braided.py` |
| `solving/` | `solver_base.py`, `bfs_solver.py`, `dijkstra_solver.py`, `astar_solver.py` |
| `rendering/` | `color_palette.py`, `ascii_renderer.py`, `mlx_renderer.py`, `animation.py` |
| `io/` | `output_writer.py` |
| `api/` | `maze_generator.py` |

**`tests/` (6 dosya):**
`test_parser.py` · `test_generation.py` · `test_solving.py` · `valid_maze.txt` · `expected_output.txt` · `sample_solution.txt`

Tüm dosyalar boş iskelet olarak oluşturuldu — uygulama bekliyor.

#### ▸ README.md yazıldı

42 formatına uygun, tüm zorunlu bölümleri içeren ilk README versiyonu oluşturuldu:
- İtalik ilk satır (`ybalkan, iuslu`)
- Açıklama, Kurulum Talimatları, Yapılandırma Formatı, Çıktı Formatı
- Algoritma seçimi + bonus tablosu
- Yeniden kullanılabilir modül dokümantasyonu
- Kaynaklar + yapay zeka kullanımı açıklaması
- Takım & Planlama tablosu
- Geliştirme Günlüğü (bu bölüm)

#### ▸ Proje İskeleti PDF ve Evaluation Sheet'e Göre Doğrulandı

- `Makefile`, `pyproject.toml` ve `.gitignore` dosyaları 42 standartlarına uygun olarak revize edildi.
- Geçici dosyaların (`__pycache__`, vb.) kök dizini kirletmemesi için hepsi `obj/` klasörüne yönlendirildi ve `make clean` ile entegre edildi.
- Risk oluşturmaması adına yapılandırma dosyalarındaki (`Makefile`, vb.) tüm yorum satırları temizlendi.
- Kodlama sırasını takip edebilmek için 32 boş Python dosyasının en üstüne numaralı yönlendirme notları (`# ADIM X: ...`) eklendi.
- `Diagram/diagram_minimal.md` ile gerçek klasör yapısının `%100` uyumlu olduğu teyit edildi.
- Rehberli kodlama (pair-programming) kararı alınarak, kodun bizzat öğrenci tarafından yazılması aşamasına geçildi.

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
- `to_string()` PDF'te istenen `"N E S W ..."` formatını üretiyor.

#### ▸ `__init__.py` dışa aktarma yapısı kuruldu

- `Direction`, `Cell`, `Maze`, `Solution` tek bir noktadan (`from mazegen.models import ...`) erişilebilir.

#### ▸ Kritik import sorunu tespit edilip düzeltildi

- Tüm dosyalardaki `from src.mazegen.models...` mutlak importlar `from .direction import Direction` gibi **göreli import**'lara çevrildi.
- Neden önemli: `pip install mazegen.whl` sonrası paket `mazegen` olarak kurulur; `src.mazegen` yolu geçersiz hale gelir → değerlendirme fail olurdu.
- Her iki senaryo doğrulandı: root'tan `python3 a_maze_ing.py` ✅ ve `pip install` sonrası `from mazegen.models import ...` ✅ 

---

### 🔲 Sıradaki Adımlar

```
[x] src/mazegen/models/direction.py
[x] src/mazegen/models/cell.py
[x] src/mazegen/models/maze.py
[x] src/mazegen/models/solution.py
[x] src/mazegen/parser/config_parser.py
[x] src/mazegen/parser/validator.py
[x] src/mazegen/parser/hex_decoder.py
[ ] src/mazegen/generation/generator_base.py
[ ] src/mazegen/generation/recursive_backtracker.py
[ ] src/mazegen/solving/bfs_solver.py
[ ] src/mazegen/io/output_writer.py
[ ] src/mazegen/rendering/color_palette.py
[ ] src/mazegen/rendering/ascii_renderer.py
[ ] src/mazegen/api/maze_generator.py
[ ] a_maze_ing.py
[ ] Makefile + pyproject.toml tamamlanması
[ ] BONUS: braided, prim, kruskal, animation
[ ] Tam test kapsamı
[ ] Son değerlendirme hazırlığı
```