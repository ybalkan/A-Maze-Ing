# A-Maze-Ing — Proje Yapısı (Subject PDF + Evaluation Sheet'e göre)
#
# [Z]  = Zorunlu — eksikse grade = 0
# [EV] = Evaluation'da bizzat test edilecek
# [B]  = Bonus (opsiyonel, +puan)
# [▶]  = Kodlama sırası
# ──────────────────────────────────────────────────────

a-maze-ing/
├── README.md                           # [Z][EV] 42 formatı zorunlu — aşağıdaki tüm bölümler eksikse grade=0:
│                                       #   • İlk satır italik: "This project has been created as part of the 42 curriculum by <login>."
│                                       #   • "Description" bölümü
│                                       #   • "Instructions" bölümü (kurulum/çalıştırma)
│                                       #   • "Resources" bölümü (referanslar + AI kullanımı açıklaması)
│                                       #   • Config dosyası formatının tam açıklaması
│                                       #   • Seçilen algoritma ve neden seçildiği
│                                       #   • Reusable modülün kısa dokümantasyonu
│                                       #   • Takım yönetimi: roller, planlama, iyi/kötü giden şeyler, kullanılan araçlar
├── LICENSE.md                          # [Z][EV] Reusable package yeniden kullanım/dağıtıma izin veren lisans
├── .gitignore                          # Python artifact'larını dışlar (__pycache__, .mypy_cache, .venv vb.)
├── Makefile                            # [Z][EV] Kurallar: install / run / debug / clean / lint (flake8 + mypy)
├── pyproject.toml                      # [Z] Paket build için gerekli — "pip install" ve "pip wheel" çalışmalı
├── requirements.txt                    # Bağımlılıklar (pyproject.toml ile çakışmasın)
├── a_maze_ing.py                       # [Z][EV] Bu isim zorunlu: python3 a_maze_ing.py config.txt
├── maze_analyzer.py                    # [Z][EV] Subject tarafından veriliyor, root'ta olmalı
│                                       #   EV: "python3 maze_analyzer.py <output_file>" çalışması zorunlu
├── mazegen-0.1.0-py3-none-any.whl      # [Z][EV] Root'ta olmalı — evaluation'da yeniden build + install test edilecek
├── mazegen-0.1.0.tar.gz                # [Z] Alternatif format (ikisinden biri yeterli ama ikisi de olabilir)
├── output_maze.txt                     # [EV] OUTPUT_FILE config'e bağlı — evaluation'da içeriği kontrol edilecek
│
├── configs/                            # [Z][EV] Default config repoda zorunlu
│   ├── default.txt                     # [Z][EV] Evaluation bu dosyayla çalıştırır
│   │                                   #   Zorunlu keyler: WIDTH / HEIGHT / ENTRY / EXIT / OUTPUT_FILE / PERFECT
│   │                                   #   Opsiyonel: SEED, ALGORITHM, ...
│   └── examples/                       # Hata yönetimi testleri için (EV'de config editlenecek)
│       ├── valid/
│       │   ├── basic.txt               # Küçük boyutlu, PERFECT=True
│       │   ├── medium.txt              # Orta boyut, PERFECT=False
│       │   └── seed_42.txt             # Aynı seed ile tekrarlanabilirlik testi
│       └── invalid/                    # [EV] Hata yönetimi — evaluator bu dosyaları kullanır
│           ├── missing_key.txt         # Zorunlu key eksik
│           ├── bad_format.txt          # KEY=VALUE formatı bozuk (= işareti yok)
│           ├── letters_for_numbers.txt # WIDTH=abc gibi
│           ├── bad_perfect.txt         # PERFECT=maybe gibi geçersiz boolean
│           └── bad_entry_format.txt    # ENTRY=0;0 gibi yanlış tuple formatı
│
├── src/
│   └── mazegen/                        # [Z][EV] Reusable paket — pip install edilebilir olmalı
│       ├── __init__.py                 # Public API export
│       ├── __main__.py                 # python -m mazegen desteği
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── maze_generator.py       # [Z][EV] MazeGenerator class — dışa açık tek API
│       │                               #   Dokümantasyon: nasıl instantiate edilir, parametreler, maze/solution erişimi
│       │
│       ├── models/                     # ▶ BURADAN BAŞLA
│       │   ├── __init__.py
│       │   ├── cell.py                 # [▶ 1] Hücre: N/E/S/W duvar bitleri, hex encoding (bit 0=N,1=E,2=S,3=W)
│       │   ├── maze.py                 # [▶ 2] Grid: WIDTH x HEIGHT hücre matrisi + border wall kontrolü
│       │   ├── direction.py            # [▶ 3] Yön enumları (N=0, E=1, S=2, W=3) + karşı yön
│       │   └── solution.py             # Çözüm yolu (koordinat + yön listesi → N/E/S/W string)
│       │
│       ├── parser/                     # [▶ 4]
│       │   ├── __init__.py
│       │   ├── config_parser.py        # [Z][EV] KEY=VALUE okuma, # yorum satırlarını atla
│       │   ├── hex_decoder.py          # [Z][EV] int ↔ duvar biti; output dosyası hex formatı
│       │   └── validator.py            # [Z][EV] Zorunlu key, sınır, tuple format, boolean kontrolü
│       │                               #   EV: 5 farklı hata senaryosu test edilecek
│       │
│       ├── generation/                 # [▶ 5]
│       │   ├── __init__.py
│       │   ├── generator_base.py       # Soyut temel — seed, boyut, entry/exit alır
│       │   ├── recursive_backtracker.py # [▶ 5a] [Z][EV] Ana algoritma
│       │   │                           #   EV: aynı seed → aynı labirent (tekrarlanabilirlik)
│       │   │                           #   EV: 42 pattern mevcut (çok küçük grid hariç)
│       │   │                           #   EV: 3x3'ten büyük açık alan yok
│       │   │                           #   EV: PERFECT=True → tek yol, PERFECT=False → Pac-Man usable
│       │   │                           #   EV: 4 köşe + merkez açık koridor (PERFECT=False)
│       │   │                           #   EV: en az 2 bağımsız rota (PERFECT=False)
│       │   ├── prim.py                 # [B] Bonus: çoklu algoritma
│       │   ├── kruskal.py              # [B] Bonus: çoklu algoritma
│       │   └── braided.py              # [B] Bonus: hiç dead-end yok (maze_analyzer --max-dead-ends 0)
│       │
│       ├── solving/                    # [▶ 6]
│       │   ├── __init__.py
│       │   ├── solver_base.py          # Soyut temel
│       │   ├── bfs_solver.py           # [▶ 6a] [Z][EV] Garantili en kısa yol
│       │   │                           #   EV: output dosyasındaki N/E/S/W yolu görsel ile eşleşmeli
│       │   ├── dijkstra_solver.py      # [B] Bonus
│       │   └── astar_solver.py         # [B] Bonus
│       │
│       ├── rendering/                  # [▶ 7]
│       │   ├── __init__.py
│       │   ├── ascii_renderer.py       # [▶ 7a] [Z][EV] Terminal render
│       │   │                           #   EV: duvarlar, giriş, çıkış, en kısa yol görünür olmalı
│       │   │                           #   EV: re-generate (yeni labirent), toggle path, renk değiştirme
│       │   ├── mlx_renderer.py         # [B] Bonus: MLX grafik pencere
│       │   ├── animation.py            # [B] Bonus: adım adım üretim animasyonu
│       │   └── color_palette.py        # [Z][EV] Renk değiştirme — zorunlu etkileşim
│       │
│       └── io/                         # [▶ 8]
│           ├── __init__.py
│           └── output_writer.py        # [Z][EV] Hex output formatı:
│                                       #   • HEIGHT satır, her satır WIDTH hex karakter
│                                       #   • Boş satır
│                                       #   • ENTRY tuple
│                                       #   • EXIT tuple
│                                       #   • Yol: N/E/S/W yönleri
│                                       #   • Her satır \n ile biter
│
└── tests/                              # Graded değil ama evaluation sırasında crash olmak yasak
    ├── unit/
    │   ├── test_parser.py              # 5 hata senaryosu için
    │   ├── test_generation.py          # seed tekrarlanabilirlik, 42 pattern, 3x3 kontrolü
    │   └── test_solving.py             # BFS doğruluğu
    └── fixtures/
        ├── valid_maze.txt
        ├── expected_output.txt
        └── sample_solution.txt         # N/E/S/W yol doğrulama için


# ════════════════════════════════════════════════════════════════════
# EVALUATION'DA TEST EDİLECEK SENARYOLAR (EV checklist)
# ════════════════════════════════════════════════════════════════════
#
# 1. BASICS
#    □ Tüm zorunlu dosyalar repoda mevcut
#    □ flake8 . → hata yok
#    □ mypy . --warn-return-any --warn-unused-ignores
#         --ignore-missing-imports --disallow-untyped-defs
#         --check-untyped-defs → hata yok
#
# 2. README.md — tüm bölümler eksiksiz
#
# 3. DISPLAY — python3 a_maze_ing.py configs/default.txt
#    □ Labirent ekranda görünüyor
#    □ Re-generate çalışıyor
#    □ Shortest path toggle (göster/gizle) çalışıyor
#    □ Wall rengi değiştirme çalışıyor
#
# 4. CONFIG FORMAT
#    □ # ile başlayan satırlar yorum
#    □ KEY=VALUE formatı (küçük harf de kabul)
#    □ WIDTH/HEIGHT/ENTRY/EXIT/OUTPUT_FILE/PERFECT mevcut
#
# 5. ERROR MANAGEMENT (evaluator config'i editleyecek)
#    □ Zorunlu key silindi → hata mesajı, crash yok
#    □ = işareti olmayan satır → hata mesajı, crash yok
#    □ Sayı yerine harf (WIDTH=abc) → hata mesajı, crash yok
#    □ PERFECT=maybe → hata mesajı, crash yok
#    □ ENTRY=0;0 (yanlış format) → hata mesajı, crash yok
#
# 6. OUTPUT FILE FORMAT
#    □ HEIGHT x WIDTH hex karakterler
#    □ Boş satır
#    □ ENTRY koordinatı
#    □ EXIT koordinatı
#    □ N/E/S/W yol dizisi
#    □ python3 maze_analyzer.py output_maze.txt → PASS
#    □ Yol görsel ile eşleşiyor
#
# 7. MAZE GENERATOR
#    □ Aynı seed → aynı labirent
#    □ Tüm hücreler erişilebilir (42 pattern hariç)
#    □ Dış kenar duvarları var
#    □ 3x3 veya daha büyük açık alan yok
#    □ "42" pattern görünür (yeterli boyut varsa)
#    □ PERFECT=True → maze_analyzer: PERFECT verdict
#    □ PERFECT=False → maze_analyzer: Pac-Man-USABLE verdict
#    □               → 4 köşe + merkez açık
#    □               → en az 2 bağımsız rota
#
# 8. REUSABLE MODULE
#    □ Virtualenv'de package yeniden build edilebiliyor
#    □ Farklı virtualenv'de pip install → a_maze_ing.py çalışıyor
#
# BONUS (her biri +1 puan, maks 5)
#    □ Braided maze (hiç dead-end yok): maze_analyzer --max-dead-ends 0
#    □ Çoklu algoritma (Prim, Kruskal vb.)
#    □ Üretim animasyonu
# ════════════════════════════════════════════════════════════════════
#
# KODLAMA SIRASI (▶)
#  1. models/direction.py      → N/E/S/W enum + karşı yön
#  2. models/cell.py           → 4 duvar, hex bit
#  3. models/maze.py           → WIDTH x HEIGHT grid, border wall
#  4. parser/config_parser.py  → KEY=VALUE okuma
#  5. parser/validator.py      → tüm hata senaryoları
#  6. parser/hex_decoder.py    → hex ↔ duvar biti
#  7. generation/recursive_backtracker.py  (+seed, +42 pattern, +3x3 kontrol)
#  8. solving/bfs_solver.py    → en kısa yol → N/E/S/W dizisi
#  9. io/output_writer.py      → dosyaya yaz
# 10. rendering/ascii_renderer.py  (+ renk, + toggle, + re-generate)
# 11. models/solution.py + api/maze_generator.py
# 12. a_maze_ing.py            → hepsini bağla
# 13. Makefile + pyproject.toml + README.md
# 14. BONUS: braided.py / prim.py / kruskal.py / animation.py

# ════════════════════════════════════════════════════════════════════
# ALGORİTMALAR — KİM NE YAPIYOR?
# ════════════════════════════════════════════════════════════════════
#
# ÜRETME algoritmaları          →  labirenti inşa eder (duvarları koyar/açar)
# ─────────────────────────────────────────────────────────────────
#   Recursive Backtracker  [Z]  →  zorunlu, bunu yaz
#   Prim                   [B]  →  bonus +1
#   Kruskal                [B]  →  bonus +1
#   Wilson                 [B]  →  bonus +1
#   Braided                [B]  →  bonus +1  (dead-end'siz üretim)
#
# ÇÖZME algoritmaları           →  bitmiş labirentte yolu bulur
# ─────────────────────────────────────────────────────────────────
#   BFS                    [Z]  →  zorunlu, bunu yaz
#   Dijkstra               [B]  →  bonus
#   A*                     [B]  →  bonus
#
# → Wilson da bir ÜRETME algoritması (BFS gibi görünür ama labirenti inşa eder)
# → Bonus için birden fazla ÜRETME algoritması ekliyorsun
#
# ════════════════════════════════════════════════════════════════════
# KODLAMA SIRASI — DETAYLI
# ════════════════════════════════════════════════════════════════════
#
#  Şehir kuruyorsun. Önce arsa, sonra bina planı, sonra inşaat,
#  sonra yol, sonra harita, sonra rehber kitapçık.
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 1 — TEMEL VERİ YAPILARI  (arsayı çiz)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 1. models/direction.py
#        Ne yapar : Yön kavramını tanımlar.
#        İçerik   : N=0, E=1, S=2, W=3 enum + her yönün karşısı (N↔S, E↔W)
#                   + (dx, dy) offset tablosu (N→y-1, E→x+1, S→y+1, W→x-1)
#        Neden önce: cell.py ve generation buraya bağımlı, temel taş bu.
#        Çıktı    : Direction enum, opposite(d), delta(d)
#
#  ▶ 2. models/cell.py
#        Ne yapar : Tek bir labirent karesini temsil eder.
#        İçerik   : 4 duvar (N/E/S/W) → boolean veya bit mask
#                   has_wall(direction) / remove_wall(direction) metodları
#                   to_hex() → tek hex karakter (bit 0=N, 1=E, 2=S, 3=W)
#                   from_hex(char) → Cell oluşturur
#        Neden önce: maze.py Cell nesnelerinden oluşur.
#        Çıktı    : Cell sınıfı
#
#  ▶ 3. models/maze.py
#        Ne yapar : Tüm ızgarayı tutar.
#        İçerik   : WIDTH x HEIGHT Cell matrisi (list of list)
#                   get_cell(x, y) / in_bounds(x, y)
#                   get_neighbors(x, y) → geçerli komşu listesi
#                   initialize_walls() → tüm duvarları kapat (başlangıç durumu)
#                   remove_wall_between(a, b) → iki komşu hücre arasındaki duvarı
#                   her iki hücrede de açar (tutarlılık zorunlu!)
#        Önemli   : Dış kenarlardaki duvarlar HİÇBİR ZAMAN açılmaz.
#        Çıktı    : Maze sınıfı
#
#  ▶ 4. models/solution.py
#        Ne yapar : Çözüm yolunu tutar.
#        İçerik   : Koordinat + yön listesi [(x,y,Direction), ...]
#                   to_string() → "N E E S W ..." formatında string
#        Çıktı    : Solution sınıfı
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 2 — CONFIG OKUMA  (inşaat ruhsatı)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 5. parser/config_parser.py
#        Ne yapar : .txt config dosyasını okur.
#        İçerik   : Satır satır oku
#                   # ile başlayanları atla (yorum)
#                   = içerenleri KEY/VALUE'ya böl
#                   Boş satırları atla
#                   Sonuç: dict[str, str]
#        EV test  : = işareti olmayan satır → ValueError, crash yok
#        Çıktı    : parse_config(path) → dict
#
#  ▶ 6. parser/validator.py
#        Ne yapar : Config dict'ini doğrular.
#        İçerik   : Zorunlu keyler: WIDTH HEIGHT ENTRY EXIT OUTPUT_FILE PERFECT
#                   WIDTH/HEIGHT → pozitif int
#                   ENTRY/EXIT   → "x,y" formatı, bounds içinde, birbirinden farklı
#                   PERFECT      → "true"/"false" (case insensitive)
#                   SEED         → opsiyonel, int
#        EV test  : 5 hata senaryosu (eksik key, harf yerine sayı, bad boolean, bad tuple)
#        Çıktı    : validate(config_dict) → MazeConfig dataclass veya exception
#
#  ▶ 7. parser/hex_decoder.py
#        Ne yapar : Hex ↔ duvar biti dönüşümü.
#        İçerik   : int_to_walls(n) → {N: bool, E: bool, S: bool, W: bool}
#                   walls_to_hex(cell) → "0"–"F" tek karakter
#                   decode_row(row_str) → Cell listesi
#        EV test  : maze_analyzer output dosyasındaki hex'i parse eder
#        Çıktı    : encode/decode fonksiyonları
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 3 — ÜRETME  (inşaatı yap)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 8. generation/generator_base.py
#        Ne yapar : Tüm algoritmalar için soyut temel.
#        İçerik   : __init__(maze, seed, entry, exit)
#                   generate() → abstract method
#                   _seed_random(seed) → random.seed() ile tekrarlanabilirlik
#        Çıktı    : GeneratorBase abstract class
#
#  ▶ 9. generation/recursive_backtracker.py   ← ANA ALGORİTMA
#        Ne yapar : DFS ile labirenti üretir.
#        Nasıl    : Başlangıç hücresinden DFS stack ile ilerle
#                   Ziyaret edilmemiş komşu varsa → duvarı aç, stack'e ekle
#                   Yoksa → geri dön (backtrack)
#                   Ta ki tüm hücreler ziyaret edilene kadar
#        EV test  : PERFECT=True  → tek yol (maze_analyzer: PERFECT verdict)
#                   PERFECT=False → Pac-Man usable (en az 2 bağımsız rota,
#                                   4 köşe + merkez açık, dead-end az)
#                   Aynı seed   → aynı labirent
#                   "42" pattern → belirli hücreler tamamen kapalı
#                   3x3 açık alan → asla oluşmamalı
#        Çıktı    : generate() → doldurulmuş Maze nesnesi
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 4 — ÇÖZME  (navigasyon)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 10. solving/solver_base.py
#         Ne yapar : Tüm çözücüler için soyut temel.
#         İçerik   : __init__(maze, entry, exit)
#                    solve() → abstract, Solution döner
#         Çıktı    : SolverBase abstract class
#
#  ▶ 11. solving/bfs_solver.py   ← ZORUNLU ÇÖZÜCÜ
#         Ne yapar : BFS ile garantili en kısa yolu bulur.
#         Nasıl    : Queue ile entry'den başla
#                    Her adımda açık duvarlardan komşuya geç
#                    exit'e ulaşınca parent listesinden yolu geri sar
#                    Yön dizisi oluştur: N E E S W ...
#         EV test  : Output dosyasındaki yol görsel ile eşleşmeli
#                    maze_analyzer da bu yolu doğrular
#         Çıktı    : solve() → Solution
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 5 — DOSYA YAZMA  (haritayı kağıda bas)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 12. io/output_writer.py
#         Ne yapar : Labirenti + çözümü output dosyasına yazar.
#         Format   :
#                    [HEIGHT satır] her satır WIDTH hex karakter \n
#                    [boş satır]    \n
#                    [ENTRY]        "x,y\n"
#                    [EXIT]         "x,y\n"
#                    [YOL]          "N E E S W ...\n"
#         EV test  : maze_analyzer bu dosyayı parse eder — format sapması = fail
#         Çıktı    : write(maze, solution, path)
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 6 — GÖRSEL  (fotoğrafını çek)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 13. rendering/color_palette.py
#         Ne yapar : Renk tanımlarını merkezi tutar.
#         İçerik   : DEFAULT_WALL / SOLUTION_PATH / ENTRY / EXIT renkleri
#                    ANSI escape kodları (terminal) veya RGB tuple (MLX)
#         Neden önce: ascii_renderer buraya bağımlı, ayrı tutmak renk
#                    değiştirme özelliğini kolaylaştırır (EV'de test edilecek)
#         Çıktı    : ColorPalette dataclass veya sabitler
#
#  ▶ 14. rendering/ascii_renderer.py   ← ZORUNLU RENDERER
#         Ne yapar : Labirenti terminale çizer.
#         İçerik   : render(maze, solution=None) → string
#                    Her hücre için duvar karakteri seç: █ ║ ═ boşluk vb.
#                    Giriş/çıkış noktaları işaretli
#                    Çözüm yolu işaretli (toggle ile göster/gizle)
#         EV test  : 3 zorunlu etkileşim:
#                    • Re-generate → yeni labirent üret ve göster
#                    • Toggle path → çözüm yolunu göster/gizle
#                    • Change color → duvar rengi değiştir
#         Çıktı    : render() + event loop (keyboard input)
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 7 — API PAKETI  (şehir şirketini kur)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 15. api/maze_generator.py
#         Ne yapar : Tüm sistemi saran tek public sınıf.
#         İçerik   : class MazeGenerator:
#                      __init__(width, height, seed=None, perfect=False, ...)
#                      generate() → self
#                      solve()    → Solution
#                      get_maze() → Maze
#                      export(path) → output dosyası yazar
#         Önemli   : Bu sınıf pip ile kurulup import edilebilmeli
#                    Dokümantasyon zorunlu (docstring, örnek kullanım)
#         EV test  : Farklı venv'de "from mazegen import MazeGenerator" çalışmalı
#         Çıktı    : MazeGenerator sınıfı
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 8 — ANA PROGRAM  (belediye başkanı emri verir)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 16. a_maze_ing.py
#         Ne yapar : Tüm sistemi birbirine bağlar.
#         Akış     : sys.argv[1] → config path
#                    parse_config() → validate() → MazeConfig
#                    MazeGenerator(config) → generate() → solve()
#                    output_writer.write(...)
#                    ascii_renderer.run() → event loop başlat
#         EV test  : python3 a_maze_ing.py configs/default.txt → çalışmalı
#                    Program crash olmadan tüm hataları yakalamalı
#         Çıktı    : Çalışan program
#
# ────────────────────────────────────────────────────────────────────
#  AŞAMA 9 — PAKET & DOKÜMANTASYON  (yönetmelik + rehber)
# ────────────────────────────────────────────────────────────────────
#
#  ▶ 17. pyproject.toml + Makefile
#         pyproject.toml : [project] name="mazegen", version, dependencies
#                          [build-system] hatchling veya setuptools
#         Makefile       : install / run / debug / clean / lint hedefleri
#                          lint = flake8 . && mypy . --warn-return-any ...
#
#  ▶ 18. README.md
#         Zorunlu bölümler (eksikse grade=0):
#         • İlk satır italik: This project has been created as part of...
#         • Description / Instructions / Resources
#         • Config formatı tam açıklaması
#         • Seçilen algoritma + neden
#         • Reusable module dokümantasyonu
#         • Takım yönetimi
#
# ────────────────────────────────────────────────────────────────────
#  BONUS SIRALAMA (önerilen sıra)
# ────────────────────────────────────────────────────────────────────
#
#  [B1] braided.py     ← EN DEĞERLİ: maze_analyzer --max-dead-ends 0 ile kanıtlanır
#                         Nasıl: üretimden sonra dead-end hücreleri tespit et,
#                         komşu duvarları rastgele aç → döngü oluştur
#
#  [B2] prim.py        ← Basit, hızlı, interview'larda çok sorulan
#                         Nasıl: frontier set ile büyüyen duvar listesi,
#                         rastgele duvar seç → komşu ziyaret edilmemişse aç
#
#  [B3] kruskal.py     ← Union-Find öğretir, değerli veri yapısı
#                         Nasıl: tüm duvarları karıştır, union-find ile
#                         farklı bileşenler arasındaki duvarları aç
#
#  [B4] animation.py   ← Gösterişli, değerlendirmede etkileyici
#                         Nasıl: generate() her adımda yield eder,
#                         renderer her frame'i çizer
#
#  [B5] wilson / astar / dijkstra ← Sonraya bırak
#         Wilson: uniform random spanning tree ama büyük gridde çok yavaş
#         A*/Dijkstra: BFS yeterli olduğu için bonus değeri düşük
#
# ════════════════════════════════════════════════════════════════════
