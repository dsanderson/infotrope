from sentence_transformers import SentenceTransformer
from pathlib import Path

MODEL = SentenceTransformer('all-mpnet-base-v2')
#CORPUS = Path(__file__).parent / 'corpus'
CORPUS = Path('/mnt/d/infotrope/corpus')
REPORTS = Path(__file__).parent / 'reports'