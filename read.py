from pypdf import PdfReader


class Read:
    def __init__(self, file):
        self.pages = PdfReader(file).pages
        self.dto = []

        self.parse_all_pages()

    @staticmethod
    def ignore_new_lines(s: str):
        return s.rstrip("\n").replace("\n", "").strip()

    def parse(self, page_content):
        length = len(page_content)
        i = 0
        while i < length:
            if page_content[i] == "[":
                egy_start = i
                egy_end = page_content.find("]", i)
                trans_start = page_content.find("]", egy_end)
                trans_end = page_content.find("{", trans_start)

                if egy_end == -1 or trans_start == -1 or trans_end == -1:
                    break

                self.object_append(
                    page_content[egy_start + 1 : egy_end],
                    page_content[trans_start + 1 : trans_end],
                    page_content[trans_end + 1 : page_content.find("}", trans_end + 1)],
                )

                i = trans_end + 1
            else:
                i += 1

    def parse_all_pages(self):
        for page in self.pages:
            page_content = page.extract_text()
            if page_content:
                self.parse(page_content)

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
