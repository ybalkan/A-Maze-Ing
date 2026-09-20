import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from a_maze_ing import main  # noqa: E402

sys.exit(main())
