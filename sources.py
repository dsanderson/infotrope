from pathlib import Path
import json
import hashlib
import time
from scrapers import SCRAPERS
import ebooklib
from ebooklib import epub
import lxml.html
import unicodedata
from config import MODEL, CORPUS


def find(source):
    """Find and return the folder in the corpus that contains the data for `source`, or `None`"""
    for path in Path(CORPUS).iterdir():
        if path.is_dir():
            with open(path/'metadata.json', 'r') as f:
                data = json.load(f)
            if data['source']==source:
                return path
    return None


def create_source(source, name=None):
    """Create a new folder in the corpus for `source` with optional `name`, generating the appropriate metadata"""
    hash = hashlib.sha256(source.encode('utf-8')).hexdigest()
    folder = CORPUS / hash
    folder.mkdir(parents=True)
    if name == None:
        name = source
    metadata = {'name': name, 'source': source, 'status': 'new', 'create_time': time.time()}
    with open(folder / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    return folder


def find_or_create(source, **kwargs):
    """Find the folder in the corpus that contains the data for `source`, or create a new folder for the source, and return the folder"""
    folder = find(source)
    if not folder:
        folder = create_source(source, **kwargs)
    return folder


def retrieve(source, index):
    folder = find(source)
    with open(folder/'data.jl', 'r') as f:
        for i, l in enumerate(f):
            if i==index:
                return json.loads(l)


def iterate(source):
    folder = find(source)
    with open(folder/'data.jl', 'r') as f:
        for i, l in enumerate(f):
            yield i, json.loads(l)


def iterate_sources():
    for path in Path(CORPUS).iterdir():
        if path.is_dir():
            with open(path/'metadata.json', 'r') as f:
                data = json.load(f)
            yield data['source']


def add_epub(source, folder):
    if not (folder/'cache.txt').is_file():
        fulltext = epub_to_text(source)
        with open(folder/'cache.txt', 'w') as f:
            f.write(fulltext)
    with open(folder/'data.jl', 'w') as out:
        with open(folder/'cache.txt', 'r') as f:
            l = 0
            while line:=f.readline():
                print(f'On line {l}', end='\r')
                l += 1
                text = line.strip()
                if text:
                    data = {'text':text, 'type': 'line', 'refs':[]}
                    data['embedding'] = [float(n) for n in MODEL.encode(text)]
                    out.write(f'{json.dumps(data)}\n')


def epub_to_text(ebook_path):
    book = epub.read_epub(ebook_path)
    docs = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    texts = [lxml.html.fromstring(d.content).text_content() for d in docs]
    texts = [unicodedata.normalize('NFKD', t) for t in texts]
    text = '\n'.join(texts)
    texts = text.split('\n')
    texts = [t.strip() for t in texts]
    text = '\n'.join([t for t in texts if t])
    return text


def fetch_source(source, name=None):
    folder = find_or_create(source, name=name)
    if source.split('.')[-1] == 'epub' and source.is_file():
        add_epub(source, folder)
        return folder
    else:
        for scraper in SCRAPERS:
            if scraper['accepts'](source):
                scraper['scrape'](source, folder)
                return folder
    return None


def find_or_fetch(source, name=None):
    folder = find(source)
    if folder == None or not (folder/'data.jl').is_file():
        fetch_source(source, name=name)
