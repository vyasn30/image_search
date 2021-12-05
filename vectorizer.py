from facenet_pytorch import MTCNN, InceptionResnetV1
from tqdm import tqdm
import os
from PIL import Image
import json

class Vectorizer:
    def __init__(self) -> None:
        self.mtcnn = MTCNN(image_size=512)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

    def vectorize_lfw(self, lfw_path):
        representations = dict()
        total_count = 0
        img_count = 0
        for root, dirs, files in os.walk(lfw_path):
            if dirs:
                for dir in tqdm(dirs):
                    embeddings = {}
                        

                    for img in os.listdir(os.path.join(root, dir)):
                        try:
                            img_path = root+"/"+dir+"/"+img
                            img_file = Image.open(img_path)
                            img_cropped = self.mtcnn(img_file)
                            img_embedding = self.resnet(img_cropped.unsqueeze(0)).tolist()
                            if len(img_embedding) == 0:
                                raise Exception("Face not detected")
                            

                                

                            representations[str(img_count)] = {dir: img_embedding}
                            img_count+=1

                        except Exception as e:
                            print(e)
                            continue

                    
                    total_count+=1

        return representations
                
                

    def vectorize_single(self, img_file):
        img = img_file
        img_cropped = self.mtcnn(img)
        img_embedding = self.resnet(img_cropped.unsqueeze(0))
        # embedding_dict = dict()

        # embedding_dict["embeddings"] = img_embedding
        # json_object = json.dumps(embedding_dict)
        return img_embedding



if __name__ =="__main__":
    path = "data/lfw-deepfunneled/lfw-deepfunneled/"
    vec = Vectorizer()

    representation_dict = vec.vectorize_lfw(path)

    with open("vecdata/representations_final.json", "w") as output_file:
        json.dump(representation_dict, output_file) 