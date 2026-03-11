import user_pb2
import pickle
import json

data = {"name": "Jan", "age": 30}

pickled_data = pickle.dumps(data)
print(pickled_data)
print(len(pickled_data))

json_data = json.dumps(data)
print(json_data)
print(len(json_data))

user = user_pb2.User()
user.name = data["name"]
user.age = data["age"]

data = user.SerializeToString()

print(data)
print(len(data))

# deserializace
u2 = user_pb2.User()
u2.ParseFromString(data)

print(u2.name, u2.age)