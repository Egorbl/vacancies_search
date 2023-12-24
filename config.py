from pathlib import Path
import sys
import os

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = os.path.relpath(root_path)

VACANCY_DF = os.path.join(ROOT, "data/raw/vacancy.csv")
CV_DF = os.path.join(ROOT, "data/raw/cv.csv")

VECTORS_PATH = os.path.join(ROOT, "data/data_vectors")

MODELS_PATH = {
    "rubert": 'cointegrated/rubert-tiny2',
    "distiluse": 'distiluse-base-multilingual-cased-v1',
    "minilm": 'paraphrase-multilingual-MiniLM-L12-v2'
}
