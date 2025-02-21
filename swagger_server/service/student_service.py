import os
import tempfile
import uuid

from bson import ObjectId
from pymongo import MongoClient
from bson.binary import Binary, UUID_SUBTYPE

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "student_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
students_collection = db["students"]

def add(student=None):
    # queries = []
    # query = Query()
    # queries.append(query.first_name == student.first_name)
    # queries.append(query.last_name == student.last_name)
    # query = reduce(lambda a, b: a & b, queries)
    # res = student_db.search(query)
    found_student = students_collection.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })
    if found_student:
        return 'already exists', 409

    student_uuid = str(uuid.uuid4())
    student_dict = student.to_dict()
    student_dict["_id"] = student_uuid
    result = students_collection.insert_one(student_dict)
    return str(result.inserted_id)


def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student["_id"]
    del student["_id"]
    return student


def delete(student_id=None):
    result = students_collection.delete_one({"_id": student_id})
    if result.deleted_count == 0:
        return 'not found', 404

    return student_id