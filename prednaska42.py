import json
import pickle
from user_pb2 import User

if __name__ == "__main__":
    data = {"name": "Alice", "age": 18}
    json_data = json.dumps(data)
    print(len(json_data))
    print(json_data)

    pickle_data = pickle.dumps(data)
    print(len(pickle_data))
    print(pickle_data)

    u = User(name="Alice", age=18)
    proto_data = u.SerializeToString()
    print(len(proto_data))
    print(proto_data)