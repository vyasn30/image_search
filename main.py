from re import I
from PIL import Image
import cv2
import faiss
from datastore import Datastore
import utils
import numpy as np
from vectorizer_deepface import Vectorizer

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
        # print(vector.shape)
        
        store.add(vector, idx, name)
        idx+=1
    
    faiss.write_index(store.index, "vecdata/vector.index")


    image = Image.open("test_data/laura.jpg")
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    vec = Vectorizer() 

    emb_2 = vec.vectorize_single(opencvImage) 
    emb_2 = np.array(emb_2, dtype=np.float32)
    emb_2 = emb_2.reshape(1, 128)
    print(emb_2.shape)
    



    ans = store.search(emb_2)
    print(ans)
    for id in ans[0]:
        print(id)
        print(names[id])


