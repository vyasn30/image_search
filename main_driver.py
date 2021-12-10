from re import S
from local_search import Searcher
from Downloader import Downloader
from Scrapper import Scrapper
import os


downloader = Downloader()


dir_name = input("Enter the dir name to store results  ==> ")
os.mkdir("Downloads/"+dir_name)
download_dir = "Downloads/"+dir_name
downloader.download(dir_name)
query_image_path = "test_data/muk.jpg"
searcher = Searcher(download_dir)
searcher.input_query_image(query_image_path)
searcher.initialize_data_store()
searcher.search()

