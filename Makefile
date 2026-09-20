.PHONY: all install run debug lint lint-strict test build clean fclean re venv

PYTHON     = python3
VENV_BIN   = .venv/bin
MAIN       = a_maze_ing.py
CONFIG     = configs/config.txt
OBJ_DIR    = obj
SRCS       = $(shell find src -name "*.py")

export PYTHONPYCACHEPREFIX = $(OBJ_DIR)/pycache

all: build

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)


install: $(OBJ_DIR)
	.venv/bin/pip install -e ".[dev]" 2>/dev/null || \
	  $(PYTHON) -m pip install --break-system-packages -e ".[dev]"

run: $(OBJ_DIR)
	$(PYTHON) $(MAIN) $(CONFIG)

debug: $(OBJ_DIR)
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint: $(OBJ_DIR)
	$(VENV_BIN)/flake8 . && \
	$(VENV_BIN)/mypy . \
	  --cache-dir $(OBJ_DIR)/.mypy_cache \
	  --exclude "42" \
	  --exclude "maze_analyzer" \
	  --warn-return-any \
	  --warn-unused-ignores \
	  --ignore-missing-imports \
	  --disallow-untyped-defs \
	  --check-untyped-defs

lint-strict: $(OBJ_DIR)
	$(VENV_BIN)/flake8 . && \
	$(VENV_BIN)/mypy . \
	  --cache-dir $(OBJ_DIR)/.mypy_cache \
	  --exclude "42" \
	  --exclude "maze_analyzer" \
	  --strict \
	  --ignore-missing-imports

test: $(OBJ_DIR)
	PYTHONPATH=src $(VENV_BIN)/pytest tests/ -v \
	  -o cache_dir=$(OBJ_DIR)/.pytest_cache

venv:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"
	@echo ""
	@echo "✅  The virtual environment is ready! To activate it:"
	@echo "    source .venv/bin/activate"
	@echo ""

build: $(OBJ_DIR)/.built

$(OBJ_DIR)/.built: pyproject.toml $(SRCS) | $(OBJ_DIR)
	$(PYTHON) -m build --wheel --outdir $(OBJ_DIR)/dist
	cp $(OBJ_DIR)/dist/mazegen-*.whl . 2>/dev/null || true
	@touch $(OBJ_DIR)/.built
	@echo "The package was copied to the root.."

clean:
	rm -rf $(OBJ_DIR)
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned up — obj/ removed."

fclean: clean
	rm -f output_maze.txt
	rm -f mazegen-*.whl
	@echo "Complete cleanup finished."

re: fclean all

