import sources
import tqdm
from config import REPORTS
import json

def report(query, seeds, scores, name, n_results=5000):
    # with open(REPORTS/'score.json', 'w') as f:
    #     json.dump(scores, f, indent=2)
    with open(REPORTS/name, 'w') as f:
        f.write(f'Searching {query} from {seeds}\n')
        for item in tqdm.tqdm(scores[:min(n_results, len(scores))]):
            data = sources.retrieve(item['source'], item['line'])
            f.write(f"{data['text']} ;;{item['source']};;{item['line']};;{item['score']}\n")