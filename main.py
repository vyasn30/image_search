from datastore import Datastore
import utils
import numpy as np

if __name__ == "__main__":
    store = Datastore()

    mappings = utils.get_mappings()
    representations = utils.get_representations()

    names, vectors = utils.get_vectors()

    print(len(names))
    print(len(vectors))

    idx = 0
    for name, vector in zip(names, vectors):
        name = np.array(name)
        vector = np.array(vector)
        print(vector.shape)
        
        store.add(vector, idx, name)

    emb = vectors[6942]

    ans = store.search(emb)
    print(ans)


