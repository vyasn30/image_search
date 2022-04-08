from tkinter.tix import Tree
from PIL import Image
import cv2
import numpy as np
from deepface import DeepFace
from deepface.basemodels import Facenet
from deepface.commons import functions
from tqdm import tqdm
import os
import json
import utils

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = 3

class Vectorizer:
    def __init__(self) -> None:
        """
        Initializing the models, as the name suggest we'll be using Inceptionresnetv2

        You can download the weights at : https://github.com/serengil/deepface_models/releases/download/v1.0/facenet_weights.h5

        """


        self.model = Facenet.loadModel()
        

    def to_vectorize_lfw(self):
        return False if (   os.path.exists("vecdata/file_name_mappings_lfw.json") and
                                    os.path.exists("vecdata/mappings_deepface_lfw.json") and
                                    os.path.exists("vecdata/representations_deepface_lfw.json")) else True
                        

    def vectorize_lfw(self, lfw_path):
        """
        Vectorize the Labeled faces in the wild dataset, and returns dict.

        Format of the dict:
            {
                "identifiers" : {"Name of the person" : embedding}

            }

        """
        if self.to_vectorize_lfw():
            representations = dict()
            total_count = 0
            img_count = 0
            err_count = 0               
            file_name_mappings = dict()
            for root, dirs, files in os.walk(lfw_path):
                if dirs:
                    for dir in tqdm(dirs):
                                                

                        for img in os.listdir(os.path.join(root, dir)):
                            # try:
                            img_path = root+"/"+dir+"/"+img
                            try:
                                img = functions.preprocess_face(img=img_path, target_size=(160, 160))
                                img_embedding = self.model.predict(img)[0,:].tolist()
                        
                            except Exception as e:
                                err_count+=1
                                print(e)
                                print(err_count)
                                continue
                            

                                
                            file_name_mappings[str(img_count)] = img_path
                            representations[str(img_count)] = {dir: img_embedding}
                            img_count+=1
                            
            print("total =", img_count)                
            print("errors = ",err_count)
            with open("vecdata/representations_deepface.json", "w") as outputFile:
                json.dump(representations, outputFile)
                
            with open("vecdata/file_name_mappings.json", "w") as outputFile:
                json.dump(file_name_mappings, outputFile)
            
            utils.make_mappings()
            return representations, file_name_mappings
                    
        else:
            print("Embeddings already generated")        

    def vectorize_single(self, img_cv2):
        """
            Vectorizes a single image, expects an opencv2 image object.

            Returns an np.arry of embeddings


        """


        img_file = functions.preprocess_face(img=img_cv2, target_size=(160, 160))
                            
        img_embedding = self.model.predict(img_file)[0,:].tolist()

        # embedding_dict = dict()

        # embedding_dict["embeddings"] = img_embedding
        # json_object = json.dumps(embedding_dict)
        return img_embedding



if __name__ =="__main__":
    path = "data/lfw-deepfunneled/lfw-deepfunneled"
    vec = Vectorizer()
    image = Image.open("test_data/test.jpeg")
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    embs = vec.vectorize_single(opencvImage)
    print(embs)

    representation_dict = vec.vectorize_lfw(path)
