import sys
from pydantic import ValidationError
from prednaska51 import Person


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} file_name')
        sys.exit(1)

    try:

        filename = sys.argv[1]
        with open(filename, 'r') as fp:
            data = fp.read()
        
        print(data)
        person = Person.model_validate_json(data)
        print(person)

    except FileNotFoundError:
        print(f"Soubor {filename} neexistuje")
    except ValidationError:
        print(f"Nepodarilo se naparsovat data: {data}")