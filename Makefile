.PHONY: install run debug lint test build clean fclean

PYTHON     = python3
MAIN       = a_maze_ing.py
CONFIG     = configs/default.txt
OBJ_DIR    = obj

# Python bytecode cache'ini obj/ altına yönlendir
export PYTHONPYCACHEPREFIX = $(OBJ_DIR)/pycache

# obj/ klasörü yoksa oluştur
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

# ── Kurulum ───────────────────────────────────────────
install: $(OBJ_DIR)
	$(PYTHON) -m pip install -e ".[dev]"

# ── Çalıştırma ────────────────────────────────────────
run: $(OBJ_DIR)
	$(PYTHON) $(MAIN) $(CONFIG)

# ── Hata ayıklama ─────────────────────────────────────
debug: $(OBJ_DIR)
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# ── Kod kalitesi ──────────────────────────────────────
lint: $(OBJ_DIR)
	flake8 . && \
	mypy . \
	  --cache-dir $(OBJ_DIR)/.mypy_cache \
	  --warn-return-any \
	  --warn-unused-ignores \
	  --ignore-missing-imports \
	  --disallow-untyped-defs \
	  --check-untyped-defs

# ── Testler ───────────────────────────────────────────
test: $(OBJ_DIR)
	$(PYTHON) -m pytest tests/ -v \
	  --cache-dir=$(OBJ_DIR)/.pytest_cache

# ── Paket derleme (whl + tar.gz) ─────────────────────
build: $(OBJ_DIR)
	$(PYTHON) -m build --outdir $(OBJ_DIR)/dist
	cp $(OBJ_DIR)/dist/mazegen-*.whl . 2>/dev/null || true
	cp $(OBJ_DIR)/dist/mazegen-*.tar.gz . 2>/dev/null || true
	@echo "Paket root'a kopyalandı."

# ── Temizlik (obj/ ve egg-info) ───────────────────────
clean:
	rm -rf $(OBJ_DIR)
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned up — obj/ removed."

# ── Tam temizlik (output + whl dahil) ────────────────
fclean: clean
	rm -f output_maze.txt
	rm -f mazegen-*.whl mazegen-*.tar.gz
	@echo "Complete cleanup finished."
