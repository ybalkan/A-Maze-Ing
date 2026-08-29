# FAZ 10 — ASCII Renderer

> **Süre:** 1 Gün  
> **Amaç:** Labirenti terminalde ASCII karakterlerle görselleştirmek.  
> **MLX'ten önce yapılır — algoritmanın doğru çalıştığını gözle doğrulamak için.**

---

## 🎯 Neden ASCII Renderer Önce?

```
MLX (grafik) karmaşıktır.
ASCII ile labirenti terminalde görürseniz:
✅ Algoritmanın doğru çalıştığını anlarsınız
✅ Bug'ları erkenden bulursunuz
✅ MLX hazır olmadan test edebilirsiniz
```

---

## 📖 ASCII Maze Temsili

### Basit Yöntem — Karakter Haritası

```
┌──┬──┬──┬──┐
│  │     │  │
├──┘  ┌──┤  │
│     │  │  │
│  ┌──┘  └──┤
│  │        │
└──┴──┴──┴──┘
```

Kullanılan karakterler:

| Karakter | Anlamı |
|---|---|
| `─` veya `-` | Yatay duvar |
| `│` veya `\|` | Dikey duvar |
| `┼`, `+` | Köşe nokta |
| ` ` (boşluk) | Açık geçit |
| `S` | Entry (Start) |
| `E` | Exit |
| `·` veya `*` | Çözüm yolu |

---

## 📖 Render Algoritması

### Yöntem 1 — Her Hücre İçin Duvar Çiz

Her hücre 2×2 karakter alanı kaplar:

```
Hücre (0,0) için:
  Üst sol → köşe: +
  Üst sağ → NORTH duvarı varsa: -
  Sol alt → WEST  duvarı varsa: |
  İç alan → boşluk: ' '
```

### Yöntem 2 — Satır Satır Render

```
Her grid satırı için iki ekran satırı:
  Satır 1 (üst duvar): ┌──┬──┬──┐
  Satır 2 (yan duvar): │  │  │  │
Son satır (alt duvar): └──┴──┴──┘
```

### Temel Render Mantığı

```python
# SADECE MANTIK
def render(grid, width, height):
    output = ""
    for y in range(height):
        # Üst duvar satırı
        top_row = ""
        for x in range(width):
            cell = grid[y][x]
            top_row += "+"
            top_row += "--" if cell has NORTH wall else "  "
        top_row += "+"
        output += top_row + "\n"

        # Yan duvar satırı
        mid_row = ""
        for x in range(width):
            cell = grid[y][x]
            mid_row += "|" if cell has WEST wall else " "
            mid_row += "  "  # hücre içi
        mid_row += "|"  # sağ kenarlık
        output += mid_row + "\n"

    # Son satır (alt duvarlar)
    ...
    return output
```

---

## 📖 Çözüm Yolu Gösterimi

Çözüm yolu hücreleri `·` veya `*` ile işaretlenir:

```
┌──┬──┬──┐
│S ·  ·  │
├──┘  ├──┤
│     ·  │
│  ┌──·  │
│        E
└──┴──┴──┘
```

---

## 📖 Kullanıcı Etkileşimi Menüsü (PDF'den)

PDF'de terminalde şu etkileşim isteniyor:

```
[1] Yeni labirent oluştur ve göster
[2] En kısa yolu göster / gizle
[3] Duvar renklerini değiştir
[4] Çık
```

### Menü Mantığı

```python
# SADECE MANTIK
while True:
    print_menu()
    choice = input("> ")
    if choice == "1":
        maze = generate_new_maze()
        render(maze)
    elif choice == "2":
        toggle_solution()
        render(maze)
    elif choice == "3":
        change_wall_color()
    elif choice == "4":
        break
```

---

## 📖 Renk Desteği (ANSI Escape Codes)

Terminalde renk için ANSI kodları:

```python
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
RESET  = "\033[0m"

print(f"{RED}─{RESET}")   # Kırmızı çizgi
print(f"{GREEN}·{RESET}") # Yeşil nokta (çözüm yolu)
```

---

## ✏️ Mini Görev

### Görev — 3×3 ASCII Render

Aşağıdaki 3×3 perfect maze'i kağıtta ASCII olarak çizin:

```
Labirent (x,y) → duvarlar:
(0,0): NORTH, WEST kapalı (sol üst köşe)
(1,0): NORTH kapalı
(2,0): NORTH, EAST kapalı
...
```

Beklenen çıktı formatı:
```
+--+--+--+
|     |  |
+  +--+  +
|  |     |
+  +  +--+
|        |
+--+--+--+
```

---

## ❓ Anlama Soruları

1. Neden her hücre için 2 ekran satırı gerekiyor?
2. En son satır (alt duvarlar) neden ayrıca işlenmeli?
3. Çözüm yolu hücrelerini nasıl takip edersiniz? (Hangi veri yapısı?)
4. ANSI escape kodu nedir? Her terminalde çalışır mı?
5. Entry ve Exit hücrelerini özel olarak nasıl gösterirsiniz?

---

## 🤖 Agent Prompt (Bu Faz İçin)

```
Act as a senior Python mentor.
Do not write code.
We are working on the 42 A-Maze-ing project.
We are currently studying: Faz 10 — ASCII Renderer
Topics: ASCII maze rendering, character mapping, solution path display,
        ANSI colors, terminal user interaction menu.
Explain only the concepts we need for this phase.
Ask us questions to verify understanding.
Do not provide implementation unless we explicitly ask for it.
```

---

## ✔️ Faz 10 Tamamlandı → Faz 11'e Geçmeye Hazır
