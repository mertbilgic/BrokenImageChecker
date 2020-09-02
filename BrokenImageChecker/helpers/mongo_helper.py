import pymongo

class MongoConnectionHelper:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if MongoConnectionHelper.__instance == None:
            MongoConnectionHelper()
        return MongoConnectionHelper.__instance
        
    def __init__(self):
        """ Virtually private constructor. """
        if MongoConnectionHelper.__instance == None:
            MongoConnectionHelper.__instance = pymongo.MongoClient('mongodb://localhost:27017/')

monglo_client = MongoConnectionHelper.getInstance()

connected_db = monglo_client['BrokenImageChecker']

crawl_links = connected_db["Crawl_Img"]

broken_img = connected_db["Broken_Image"]


    

