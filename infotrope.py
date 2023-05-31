## Infotrope; a tool for managing local sentence-embedding augemented databases of text data
# Structure:
# sources.py: utilities for finding, fetching, and adding to the corpus new sources
# scrapers.py: scrapers for fetching from web-based sources
# query.py: tools for analyzing and querying the corpus
# config.py: configuration
# reporting.py: tools for storing and displaying the results of analyses
# infotrope.py: this file, high-level interface for operating on your personal knowledgebase

# Right now, the tool only really supports directed queries.  This involves writing a scraper for the
# sources of interest (including the reference component!) then calling
# python infotrope.py <output filename [stored in ./reports]> "<query>" <seed source> <seed sources...> 
# example: `python infotrope.py mck_supply_chain.txt "Supply chain optimization, manufacturing operations and digital engineering improved through artificial intelligence and machine learning" "https://www.mckinsey.com/capabilities"`

import sys
import query as QUERY
import reporting

if __name__=="__main__":
    name = sys.argv[1]
    query = sys.argv[2]
    seeds = sys.argv[3:]
    print(f"Starting {name} from {seeds}, finding {query}")
    scores = QUERY.query(query, seeds)
    print('Generating report')
    reporting.report(query, seeds, scores, name)
