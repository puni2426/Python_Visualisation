try:
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    import os
    import json
    from enum import Enum
    print("Inside try")
except Exception as e:
    raise Exception("Module missing:{}".format(e))


class MongoDB(object):

    def __init__(self, dBName=None, collectionName=None):

        self.dBName = dBName
        self.collectionName = collectionName

        self.client = MongoClient("localhost", 27017, maxPoolSize=50)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]



    def InsertData(self, path=None):
        """
        :param path: Path os csv File
        :return: None
        """

        df = pd.read_csv(path)
        data = df.to_dict('records')

        self.collection.insert_many(data, ordered=False)
        print("All the Data has been Exported to Mongo DB Server .... ")

if __name__ == "__main__":
    mongodb = MongoDB(dBName = 'Dataset', collectionName='EnergyConsumption')
    mongodb.InsertData(path="/home/ee212821/Downloads/test.csv")
