import json
from read import Read


class Write:
    def __init__(self, obj):
        self.obj = obj

    def to_json(self):
        print("start proccesing")
        with open("dictinary.json", "w") as f:
            json.dump(self.obj, f)
        self.has_equal_keys()

    def has_equal_keys(self):
        x = False
        obj = None
        for i in self.obj:
            if len(i.keys()) != 3:
                x = False
                obj = i
            else:
                x = True

        print("All keys exists") if x else print(f"{obj} have an issue")


read = Read("DictionaryOfMiddleEgyptian-12-13.pdf")
Write(read.dto).to_json()
