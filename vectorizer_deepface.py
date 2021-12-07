
# from deepface.basemodels import Facenet
import numpy as np
from deepface.basemodels.Facenet import InceptionResNetV2
from deepface.commons import functions
# from facenet_pytorch import MTCNN, InceptionResnetV1
from tqdm import tqdm
import os
from PIL import Image
import json

class Vectorizer:
    def __init__(self) -> None:
        # self.mtcnn = MTCNN(image_size=512)
        # self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
        self.model = InceptionResNetV2()
        self.model.load_weights("models/facenet_weights.h5")

    def vectorize_lfw(self, lfw_path):
        representations = dict()
        total_count = 0
        img_count = 0
        err_count = 0
        for root, dirs, files in os.walk(lfw_path):
            if dirs:
                for dir in tqdm(dirs):
                    embeddings = {}
                        

                    for img in os.listdir(os.path.join(root, dir)):
                        try:
                            img_path = root+"/"+dir+"/"+img
                            img_file = functions.preprocess_face(img=img_path, target_size=(160, 160))
                            img_embedding = self.model.predict(img_file)[0,:].tolist()
                            if len(img_embedding) == 0:
                                raise Exception("Face not detected")
                            

                                

                            representations[str(img_count)] = {dir: img_embedding}
                            img_count+=1

                        except Exception as e:
                            err_count+=1
                            print(err_count)
                            continue

                    
                    total_count+=1

        return representations
                
                

    def vectorize_single(self, img_cv2):
        img_file = functions.preprocess_face(img=img_cv2, target_size=(160, 160))
                            
        img_embedding = self.model.predict(img_file)[0,:].tolist()

        # embedding_dict = dict()

        # embedding_dict["embeddings"] = img_embedding
        # json_object = json.dumps(embedding_dict)
        return np.array(img_embedding, dtype=np.float32)



if __name__ =="__main__":
    path = "data/lfw-deepfunneled/lfw-deepfunneled/"
    vec = Vectorizer()
    emb = vec.vectorize_single("aish.jpg")
    print(emb)
    print(len(emb))
    # representation_dict = vec.vectorize_lfw(path)

    # with open("vecdata/representations_deepface.json", "w") as output_file:
        # json.dump(representation_dict, output_file) 
    