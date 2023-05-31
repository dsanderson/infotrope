# Infotrope: a personal knowledgebase

This project is inspired by Greg Egan's novels, where the (transhuman) characters often have *infotropes*.  Their infotropes represent and allow them to examine, query, manipulate and extend their *own* knowledge computationally, enabling totally different approaches to learning and problem solving.

Sadly, BCI is not yet ready to make this happen.  However, when I was learning about sentence transformers, I was struck by their ability to solve *half* of the above; given a knowledge base, they enable semantic problems to be transformed into mathematical problems, allowing the knowledge base to be examined, queried and expanded computationally.

That's what this infotrope is; a tool for building, querying and extending a personal, text based knowledgbase, drawn mostly from online sources, using sentence transformers.  In the long term, integrating with tools like Anki may allow the knowledgbase to capture the user's familiarity with each item, moving towards solving the first half, but I'm not there yet.

As an example, understand, say, different types of mathematical optimization problems, or how a major consultancy discusses the intersection of supply chain and AI.  I can transform the question into a vector, using sentence transformers.  We can then run that query against chunks of data in our existing knowledgebase, looking for "good" matches to our query.  Those chunks of data can also include references (think hyperlinks within a paragraph).  We can then repeat the analysis on the references from data that best matched our query, performing a directed, depth-first search for information that *semantically* matches our interests; a targeted web crawl, in the way a human might.

We can then summarize the results of that analysis for the user, showing the most relevant data chunks.  In this way, the *user* avoids skimming hundreds of pages to acquire those choice chunks, a massive time savings.

We can also then perform further analysis.  `analysis.py` has some (probably broken) code that, given a set of knowledgebase chunks, can cluster and extract *exemplar* chunks.  This allows the user to summarize subsets of their own knowledgebase.  This could, in turn, be used to further expand and summarize; push deeper in topics of interest, or gather more data on anemic references.