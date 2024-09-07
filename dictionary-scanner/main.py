import json
from datetime import datetime
from read import Read


class Write:
    def __init__(self, obj):
        self.obj = obj

    def to_json(self):
        with open("dictionary.json", "w") as f:
            json.dump(self.obj, f)


if __name__ == "__main__":
    start = datetime.now()
    read = Read("DictionaryOfMiddleEgyptian.pdf")
    Write(read.dto).to_json()
    end = datetime.now()
    print(end - start)
