from config import MODEL
import sources as SOURCES
import json
from scipy.spatial import distance


def score_sources(query_embedding, sources, scores):
    for source in sources:
        if source not in scores:
            scores[source] = score_source(query_embedding, source)
    return scores


def score_source(query_embedding, source):
    scores = []
    SOURCES.find_or_fetch(source)
    for i, data in SOURCES.iterate(source):
        print(f'Scoring line {i}', end='\r')
        scores.append(
            {
                'line':i,
                'score':distance.cosine(query_embedding, data['embedding'])
            }
        )
    return scores


def query(query, seeds, n_sources = 500):
    query_embedding = [float(t) for t in MODEL.encode(query)]
    sources = set(seeds)
    scores = {}
    explored = set()
    match = True
    while len(sources)<n_sources and match != None:
        scores = score_sources(query_embedding, sources, scores)
        best_score = 3.0
        match = None
        for k, v in scores.items():
            for i, s in enumerate(v):
                if s['score']<best_score:
                    if (k, s['line']) not in explored:
                        match = (k, s['line'])
                        best_score = s['score']
        if match==None:
            break
        data = SOURCES.retrieve(match[0], match[1])
        print(f"From {match[0]}, {match[1]} ({best_score}): {data['text']}")
        print(f"{len(sources)} sources of {n_sources}")
        for r in data['refs']:
            sources.add(r)
        explored.add(match)
    flattened = []
    for source, sc in scores.items():
        for s in sc:
            flattened.append({'source':source, 'line':s['line'], 'score':s['score']})
    flattened.sort(key = lambda x: x['score'])
    return flattened
