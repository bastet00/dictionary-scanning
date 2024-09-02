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

    def parse(self):
        length = len(self.page)
        i = 0
        while i < length:
            if self.page[i] == "[":
                egy_start = i
                egy_end = self.search("]", i)
                trans_start = self.search("]", egy_end)
                trans_end = self.search("{", trans_start)

                if egy_end == -1 or trans_start == -1 or trans_end == -1:
                    break

                self.object_append(
                    self.page[egy_start + 1 : egy_end],
                    self.page[trans_start + 1 : trans_end],
                    self.page[trans_end + 1 : self.page.find("}", trans_end + 1)],
                )

                i = trans_end + 1
            else:
                i += 1

    def object_append(self, *args):
        self.dto.append(
            {
                "Egyptian": args[0],
                "Translation": self.ignore_new_lines(args[1]).split(", "),
                "Symbol": self.ignore_new_lines(args[2]).split(" "),
            }
        )
