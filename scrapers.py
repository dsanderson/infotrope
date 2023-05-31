import requests
import lxml.html
import unicodedata
import json
import time
from config import MODEL


def metascraper(fetcher, content_iterator, ref_extractor):
    fetcher = fetcher
    content_iterator = content_iterator
    ref_extractor = ref_extractor
    def s(source, folder):
        html = fetcher(source, folder)
        with open(folder/'data.jl', 'w') as out:
            for i, chunk in enumerate(content_iterator(html)):
                print(f'On chunk {i}', end='\r')
                text = chunk.text_content().strip()
                refs = ref_extractor(chunk, html)
                text = unicodedata.normalize('NFKD', text)
                text = ' '.join([t for t in text.split() if t.strip()!=''])
                data = {'text':text, 'type': 'chunk', 'refs':refs}
                data['embedding'] = [float(n) for n in MODEL.encode(text)]
                out.write(f'{json.dumps(data)}\n')
        time.sleep(0.5)
    return s


def generic_cached_fetcher(source, folder):
    if not (folder/'cache.txt').is_file():
        page = requests.get(source)
        with open(folder/'cache.txt', 'w') as f:
            f.write(page.text)
    with open(folder/'cache.txt', 'r') as f:
        text = f.read()
    html = lxml.html.fromstring(text)
    html.make_links_absolute(source, resolve_base_href = True)
    return html


def generic_ref_extractor(chunk, html):
    refs = [e[2] for e in chunk.iterlinks()]
    if len(refs)==0:
        refs = [e[2] for e in html.iterlinks()]
    return refs


def no_extension(url):
    return len(url.split('/')[-1].split('.'))==1


def wikipedia_content_iterator(html):
    for b in html.xpath('//div[@id="mw-content-text"]//*[self::p or self::li]'):
        yield b

def wikipedia_ref_extractor(chunk, html):
    refs = generic_ref_extractor(chunk, html)
    refs = [r for r in refs if 'wikipedia.org' in r and 'index.php' not in r and '#' not in r and 'Special:' not in r]
    return refs


def mckinsey_content_iterator(html):
    for b in html.xpath('//*[self::p or contains(@class, "item")]'):
        yield b

def mckinsey_ref_extractor(chunk, html):
    refs = generic_ref_extractor(chunk, html)
    refs = [r for r in refs if 'www.mckinsey.com' in r and all(p not in r for p in ['signin', '#', '~', '/resources/', '/Scripts/', '/modules/']) and no_extension(r)]
    return refs


def mckinsey_content_iterator(html):
    for b in html.xpath('//*[self::p or contains(@class, "item")]'):
        yield b

def mckinsey_ref_extractor(chunk, html):
    refs = generic_ref_extractor(chunk, html)
    refs = [r for r in refs if 'www.mckinsey.com' in r and all(p not in r for p in ['signin', '#', '~', '/resources/', '/Scripts/', '/modules/']) and no_extension(r)]
    return refs


SCRAPERS = [
    {
        'accepts':lambda s: len(s.split('/'))>2 and 'wikipedia.org' in s.split('/')[2],
        'scrape':metascraper(
            generic_cached_fetcher,
            wikipedia_content_iterator,
            wikipedia_ref_extractor
        )
    },
    {
        'accepts':lambda s: len(s.split('/'))>2 and 'www.mckinsey.com' in s.split('/')[2],
        'scrape':metascraper(
            generic_cached_fetcher,
            mckinsey_content_iterator,
            mckinsey_ref_extractor
        )
    },
    {
        'accepts':lambda s: len(s.split('/'))>2 and 'www.mckinsey.com' in s.split('/')[2],
        'scrape':metascraper(
            generic_cached_fetcher,
            mckinsey_content_iterator,
            mckinsey_ref_extractor
        )
    }
]