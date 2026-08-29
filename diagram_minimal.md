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
