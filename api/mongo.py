import pymongo
import certifi

# Replace these values with your own MongoDB connection details
mongo_uri = "mongodb+srv://el:W6hkUqzTQWcL6IVw@cluster0.9uk8uat.mongodb.net/?retryWrites=true&w=majority"

# Establish a connection to the MongoDB server
client = pymongo.MongoClient(mongo_uri, tlsCAFile=certifi.where())

# Access a specific database (replace 'mydb' with your database name)
db = client.vectors_db
collection = db.vectorizations

def get_history(user_id):
    history = []
    docs = collection.find({'user_id': user_id, 'is_prompt': True})
    for doc in docs:
        answer = collection.find_one({'user_id': user_id, '_id': doc['answer_id']})
        pair = {
            "prompt": doc['prompt'],
            "vectorized_prompt" : doc['vectorized_prompt'],
            "answer": answer['answer'],
        }
        history.append(pair)

    return history

def add_answer(user_id, answer):
    collection.insert_one({
        "user_id": user_id,
        "answer": answer,
        "is_prompt": False,
    })
    return collection.find_one({'user_id': user_id, 'answer': answer})['_id']

def add_prompt(user_id, prompt, vectorized_prompt, answer_id):
    collection.insert_one({
        "user_id": user_id,
        "prompt": prompt,
        "vectorized_prompt": vectorized_prompt,
        "answer_id": answer_id,
        "is_prompt": True,
    })