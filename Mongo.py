# mongo_db/Mongo.py
from pymongo import MongoClient
import logging as log
import os,json,sys
from bson import ObjectId, json_util
from datetime import datetime

class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        # self.client = MongoClient("mongodb://localhost:27017/")  # When only Mongo DB is running on Docker.
        self.client = MongoClient(os.getenv('DATABASE_URI'))     # When both Mongo and This application is running on
                                                                    # Docker and we are using Docker Compose       
        database = "fyers"
        collection = data
        self.cursor = self.client[database]
        self.collection = self.cursor[collection]
        print("<---------------------------------->")
        print("|      ",  'DB initialized' ,"            |")
        print("<---------------------------------->")
        self.data = data

    def switch_collection(self,collection_name):
        self.cursor = self.cursor
        self.collection = self.cursor[collection_name]
        print('Collection switch')

    def read(self,data='',sortVal='_id'):
        log.info('Reading All Data')
        filt = {}
        #projection ={}
        if 'Filter' in data:
            filt = data['Filter']
        if 'Projection' in data:
            projection = data['Projection']
            documents = self.collection.find(filt,projection).sort(sortVal,-1)
        else:
            documents = self.collection.find(filt).sort(sortVal,-1)
        output = [{item: str(data[item]) if item == '_id' else data[item] for item in data} for data in documents]
        return output
    
    def paginated(self,data='',pagination={"page_number":1,"per_page":10},sortVal='_id'):
        log.info('Reading All Data')
        # Calculate the number of documents to skip
        skip_count = (pagination['page_number'] - 1) * pagination['per_page']
        filt = {}
        #projection ={}
        if 'Filter' in data:
            filt = data['Filter']
        if 'Projection' in data:
            projection = data['Projection']
            # Use find() with skip() and limit() for pagination
            documents = self.collection.find(filt,projection).sort(sortVal,-1).skip(skip_count).limit(pagination['per_page'])
        else:
            # Use find() with skip() and limit() for pagination
            documents = self.collection.find(filt).sort(sortVal,-1).skip(skip_count).limit(pagination['per_page'])
        output = [{item: str(data[item]) if item == '_id' else data[item] for item in data} for data in documents]
        # Retrieve the total count without skip and limit
        total_count = self.collection.count_documents(filt)
        pagedata={};
        pagedata["total"] = total_count
        pagedata["limit"] = pagination['per_page']
        pagedata["offset"] = skip_count
        pagedata["items"] = output
        return pagedata

    def readAggregatePaginated(self,pipeline={},pagination={"page_number":1,"per_page":10},sortVal='_id'):
        log.info('Reading All Data')
        # Calculate the number of documents to skip
        skip_count = (pagination['page_number'] - 1) * pagination['per_page']
        filt = {}
        pipeline[4]["$facet"]["results"].append({"$limit": skip_count + pagination['per_page']})
        pipeline[4]["$facet"]["results"].append({"$skip": skip_count})

        documents = list(self.collection.aggregate(pipeline))
        if len(documents)>0:
            if documents[0]["total_count"]:
                total_count = documents[0]["total_count"][0]["count"]
            else:
                total_count = 0
            if documents[0]["results"]:
                documents = documents[0]["results"]
            else:
                documents = []
        else:
            total_count = 0
            documents = []

        output = [{item: str(data[item]) if item == '_id' else data[item] for item in data} for data in documents]
        pagedata={};
        pagedata["total"] = total_count
        pagedata["limit"] = pagination['per_page']
        pagedata["offset"] = skip_count
        pagedata["items"] = output
        return pagedata

    def read_one(self,data='',sortVal='_id'):
        log.info('Reading All Data')
        filt = {}
        #projection ={}
        if 'Filter' in data:
            filt = data['Filter']
        if 'Projection' in data:
            projection = data['Projection']
            documents = self.collection.find(filt,projection).sort(sortVal,-1).limit(1)
        else:
            documents = self.collection.find(filt).sort(sortVal,-1).limit(1)
        output = [{item: str(data[item]) if item == '_id' else data[item] for item in data} for data in documents]
        if len(output):
            return output[0]
        else:
            return output

    def readAggregate(self,pipeline={}):
        log.info('Reading Aggregate Data')
        filt = {}
        documents = self.collection.aggregate(pipeline)
        # if len(documents)>0:
        #     print('hiiiiiiiiiiiiiiii')
        #projection ={}
        # if 'Filter' in data:
        #     filt = data['Filter']
        # if 'Projection' in data:
        #     projection = data['Projection']
        #     documents = self.collection.find(filt,projection).sort(sortVal,-1)
        # else:
        #     documents = self.collection.find(filt).sort(sortVal,-1)
        # output = [{item: str(data[item]) if item == '_id' else data[item] for item in data} for data in documents]
        return documents

    def escape_keys(self,json_data):
        if isinstance(json_data, dict):
            return {f'\"{key}\"' if key.startswith('$') else key: self.escape_keys(value) for key, value in json_data.items()}
        elif isinstance(json_data, list):
            return [self.escape_keys(item) for item in json_data]
        else:
            return json_data

    def write(self, data):
        log.info('Writing Data')
        data["db_created"]=datetime.now()
        new_document = data

        response = self.collection.insert(new_document,check_keys=False)
        output = {'status':True,'message': 'Successfully Inserted',
                  'Document_ID': str(response)}
        return output

    def update(self, DataToBeUpdated):
        log.info('Updating Data')
        if 'Filter' in DataToBeUpdated:
            filt = DataToBeUpdated['Filter']
            data = DataToBeUpdated['DataToBeUpdated']
            data["db_updated"]=datetime.now()
        else:
            return {'status':False,'message': 'Filter query missing'}
        updated_data = {"$set": data}
        # updated_data = {"$set": data,"$setOnInsert": { 'db_updated': datetime.now() }
        # print('--------------filter-----------')
        # print(filt)
        # print(updated_data)
        response = self.collection.update_many(filt, updated_data)
        output = {'status':True,'message': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        print(output)
        return output

    def converttoString(self,obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if(key=='data'):
                    obj['data']=str(value)
        return obj

    def collectionMove(self,pipeline={},tomove='',from_collection=''):
        log.info('Reading collection to Move')
        documents = list(self.collection.aggregate(pipeline))
        if len(documents)>0:
                insert_count=0
                # Loop through documents and check for existing ones
                for document in documents:
                    print('-----------------------------')
                    self.switch_collection(tomove)
                    # Check if document with the same _id already exists
                    if not self.collection.find_one({'_id': document['_id']}):
                        document = self.converttoString(document)
                        result = self.collection.insert_one(document)
                        insert_count = insert_count + 1
                        if(result):
                            self.switch_collection(from_collection)
                            requestDataToDelete={}
                            requestDataToDelete["Filter"] = { "_id" : ObjectId(document['_id'])}
                            sessionResponse = self.delete(requestDataToDelete)
                status = "Moved "+ str(insert_count)+ " documents to the destination collection"
        else:
            status = " No documents found in collections"
        return status

    def delete(self, data):
        log.info('Deleting Data')
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'status':True,'message': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def delete_all(self, data):
        log.info('Deleting Data')
        filt = data['Filter']
        response = self.collection.delete_many(filt)
        output = {'status':True,'message': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
    
    def total_doc(self):
        log.info('All Data Count')
        documents = self.collection.count_documents()
        output = documents
        return output

    def dateFromObjectId(self,data):    
        return ObjectId('5c51aca67c76124020edbbaf').generation_time;

# for parsing the datetime.now to json format
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)