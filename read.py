from pypdf import PdfReader


class Read:

    def __init__(self, file):
        self.page = PdfReader(file).pages[0].extract_text()
        self.dto = []

        self.parse()

    @staticmethod
    def ignore_new_lines(str: str):
        return str.rstrip("\n").replace("\n", "").strip()

    def search(self, char, start):
        return self.page.find(char, start)

    def get_egyptian(self, start):
        start, end = self.search("[", start), self.search("]", start + 1)
        return (start, end)

    def get_translation(self, start):
        start, end = self.search("]", start), self.search("{", start + 1)
        return (start, end)

    def get_symbol(self, start):
        start, end = self.search("{", start), self.search("}", start + 1)
        return (start, end)

    def parse(self):
        line_start = 0
        for i in range(5):
            egy = self.get_egyptian(line_start)
            trans = self.get_translation(line_start)
            symbol = self.get_symbol(line_start)

            if symbol[1] < trans[1]:
                symbol = self.get_symbol(symbol[0])

            if egy[0] == -1:
                break
            line_start = max(egy + trans + symbol)

            self.object_append(
                self.page[egy[0] + 1 : egy[1]],
                self.page[trans[0] + 1 : trans[1]],
                self.page[symbol[0] + 1 : symbol[1]],
            )

    def object_append(self, *args):
        self.dto.append(
            {
                "Egyptian": args[0],
                "Translation": self.ignore_new_lines(args[1]).split(", "),
                "Symbol": self.ignore_new_lines(args[2]).split(" "),
            }
        )


read = Read("DictionaryOfMiddleEgyptian-12-13.pdf")
print(read.dto)
