from tenn_ai.fabric_ai.edrak.databases.tenn_object_db import TENN_Object, TENN_ObjectDB
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
import json
import uuid

utils = TENN_Utils()

obj1 = TENN_Object()
obj1.object_id = "123"
obj1.aid = "456"
obj1.content_type = "TEXT"
obj1.contents = "Hello, world!"
print(obj1.to_json())

json_str = '{"_id": "453", "aid": "789", "content_type": "TEXT", "contents": "Hello, magical world!"\n}'
obj2 = TENN_Object.from_json(json_str)
# obj2 = TENN_Object(passed_data=json.loads(json_str))
print(obj2.to_json())

obj3 = TENN_Object()
obj3.aid = utils.generate_aid()
obj3.content_type = "TEXT"
obj3.contents = "Howdy, AID world! This object has AID " + obj3.aid 
print(obj3.to_json())

db = TENN_ObjectDB(passed_verbose=True)

# test db add
db.add_object(obj1, passed_collection_name="CORE_TEXT")
retrieved_obj = db.get_object(passed_aid=obj1.aid, passed_collection_name="CORE_TEXT")
print(retrieved_obj)

# test db modify
db.add_object(obj2, passed_collection_name="GEN_SUMMARY")
db.add_object(obj3, passed_collection_name="GEN_SUMMARY")

obj2.contents = "Goodbye, world!"
db.modify_object(obj2.aid, obj2, passed_collection_name="GEN_SUMMARY")
retrieved_obj = db.get_object(obj2.aid, passed_collection_name="GEN_SUMMARY")
print(retrieved_obj)

# test db delete
deleted = db.delete_object(obj2.aid, passed_collection_name="GEN_SUMMARY")
print("Deleted? " + str(deleted))
retrieved_obj = db.get_object(obj2.aid, passed_collection_name="GEN_SUMMARY")
if retrieved_obj is None:
    print("Object not found.")


obj4 = TENN_Object()
obj4.aid = utils.generate_aid()
obj4.content_type = "JSON"
obj4.contents = '{"This is": "a text object", "AID" : "' + obj4.aid + '"}'
print(obj4.to_json())

db.add_object_core(obj4)

# test the count function
count1 = db.count_objects({"_id": "123"}, passed_collection_name="CORE_TEXT")
count2 = db.count_objects({}, passed_collection_name="GEN_SUMMARY")

print("Counts: CORE_TEXT " + str(count1) + ", GEN_SUMMARY " + str(count2))