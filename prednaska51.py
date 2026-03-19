from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)


if __name__ == '__main__':
    person = Person(name="Alice", age='18')
    print(person)

    json_data = person.model_dump_json()
    with open('person.json', 'w') as fp:
        fp.write(json_data)
    

