import numpy as np
import json
import sklearn.decomposition
import os
import copy
from sklearn.cluster import AffinityPropagation, OPTICS
from sklearn.metrics.pairwise import paired_cosine_distances
import sources as SOURCES

def extract_cluster_exemplars(items):
    # Apply incremental PCA to reduce the dimensionality of the space
    # items is an array of dictionaries {source:, item:}
    batch_size = 500
    dims = 50
    ipca = sklearn.decomposition.IncrementalPCA(n_components = dims)
    
    positions = []

    count = 0
    embeddings = []
    for i, datum in enumerate(items):
        print(f'On line {i}', end='\r')
        count += 1
        data = SOURCES.retrieve(datum['source'], datum['line'])
        embeddings.append(copy.deepcopy(data['embedding']))
        positions.append({'index':i, 'length':len(data['text'])})

        if count==batch_size:
            count = 0
            embs = np.array(embeddings)
            ipca.partial_fit(embs)
            embs = []
    if embeddings:
        embs = np.array(embeddings)
        ipca.partial_fit(embs)
        embs = []
    print('\n')
    
    embeddings = np.zeros((len(positions), dims))
    for i, datum in enumerate(items):
        print(f'On line {i} of {len(positions)}', end='\r')
        data = SOURCES.retrieve(datum['source'], datum['line'])
        emb = np.array(data['embedding'])
        embeddings[i,:] = ipca.transform(emb.reshape(1, -1))
    print('\n')
    print(embeddings.shape)

    # Apply clustering
    #clustering = AffinityPropagation(random_state=5, verbose=True).fit(embeddings)
    clustering = OPTICS(min_samples=3).fit(embeddings)
    exemplars = get_exemplar_indicies(embeddings, clustering)
    print(f'Summary reduced from {len(positions)} to {len(exemplars)}')
    return exemplars


def get_exemplar_indicies(data, clustering):
    n_clusters = np.amax(clustering.labels_)
    exemplars = []
    for i in range(0, n_clusters+1):
        print(f'On cluster {i} of {n_clusters}', end='\r')
        sub_data = data[clustering.labels_==i,:]
        dists = paired_cosine_distances(sub_data, sub_data)
        avg_dists =  np.average(dists, axis=0)
        ind = np.argmin(avg_dists)
        exemplars.append((np.argwhere(clustering.labels_==i)[ind][0], sub_data.shape[0]))
    return exemplars

