from datastore import Datastore
from vectorizer import Vectorizer 
# from datastore import Datastore
import utils
import numpy as np
import faiss

# def search(emb, k=5):
#     D,I = index.search(emb, k)
#     return list


# store = Datastore()
mappings = utils.get_mappings()
vectors = []
names = []
identifiers = list(mappings.keys())
identifiers = np.array(identifiers, dtype=np.float32)

print(identifiers) 

for index in mappings:
    name, vector = utils.yield_pairs(index)
    vector = np.array(vector, dtype=np.float32)
    vectors.append(vector)
    names.append(name)

vectors = np.array(vectors)
print(vectors.shape)

# for vector, identifier, name in zip(vectors, identifiers, names):
    # print(vector.shape, identifier, name)

d = 512
xb = np.array([val.flatten() for val in vectors])

# print(xb.shape)
# print(xb[0].shape)
# print(xb[0].flatten().shape)

print(mappings["6942"])

index = faiss.IndexFlatIP(d)

for val in xb:
    to_add = []
    to_add.append(val)
    to_add = np.array(to_add)
    # print(to_add.shape)
    index.add(to_add)

emb = vectors[6942]

D, I =  index.search(emb, 5)
print(I[0])

for val in I[0]:
    print(mappings[str(val)])