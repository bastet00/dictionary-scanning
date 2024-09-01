from pypdf import PdfReader


class Cases:
    @staticmethod
    def ignore_new_lines(str: str):
        return str.rstrip("\n").replace("\n", "")


"""
[
    {Egyptian:[], Translation:[], Symbol:[]},
    {Egyptian:[], Translation:[], Symbol:[]},
    {Egyptian:[], Translation:[], Symbol:[]},
    {Egyptian:[], Translation:[], Symbol:[]},
    {Egyptian:[], Translation:[], Symbol:[]},
    {Egyptian:[], Translation:[], Symbol:[]},
]
"""
# TODO: the values needs to be looped over again to be ordered efficiently
# TODO: generator functions might be the solving key


class Read(Cases):

    def __init__(self, file):
        self.page = PdfReader(file).pages[0].extract_text()
        self.dto = []

        self.egyptian()
        # self.trans()

    def search(self, char, start):
        return self.page.find(char, start)

    def egyptian(self):
        line_start = 0
        for i in range(len(self.page)):
            start, end = self.search("[", line_start), self.search("]", line_start + 1)
            start2, end2 = self.search("]", line_start), self.search(
                "{", line_start + 1
            )
            if start == -1:
                break
            line_start = end
            self.parse("Egyptian", self.page[start + 1 : end])
            self.parse(
                "Translation",
                self.ignore_new_lines(self.page[start2 + 1 : end2]).split(","),
            )

    # def trans(self):
    #     line_start = 0
    #     for i in range(len(self.page)):
    #         start, end = self.search("]", line_start), self.search("{", line_start + 1)
    #         if start == -1:
    #             break
    #         line_start = end
    #         self.parse(
    #             "Translation",
    #             self.ignore_new_lines(self.page[start + 1 : end]).split(","),
    #         )

    def parse(self, key, value):
        self.dto.append({key: value})


read = Read("DictionaryOfMiddleEgyptian-12-13.pdf")
print(read.dto)
# eg = 0
# trans = 0
# for i in read.dto:
#     if "Egyptian" in i.keys():
#         eg += 1
#     else:
#         trans += 1
#
# print(eg, trans)
