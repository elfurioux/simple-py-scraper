import requests
from html import parser as html
from urllib import parse as urlt

class URL:
    def __init__(self, url: str) -> None:
        self._url = url
    
    def parse(self) -> None:
        p = urlt.urlparse(url=self._url)
        print(p)

    def ishttp(self) -> bool:
        return self._url.startswith("http")
    
    def isrelative(self) -> bool:
        return self._url.startswith("/")
    
    def isvalid(self):
        return self.ishttp() or self.isrelative()

    def __repr__(self) -> str:
        l: str = ''
        if self.isrelative(): l = 'R'
        if self.ishttp(): l = 'H'
        if l=='': l = '?'
        return f"URL({l}'{self._url}')"

class HTMLScraper(html.HTMLParser):

    def __init__(self, *, convert_charrefs = True):
        self.urllist: list[URL] = []
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_starttag(self, tag, attrs):
        if tag!='a': return

        for attr in attrs:
            if attr[0]=="href":
                u = URL(attr[1])
                self.urllist.append(u)

    def printurls(self):
        for url in self.urllist:
            print(url)

def htmlparse(srchtml: str):
    scraper = HTMLScraper()

    scraper.feed(srchtml)
    scraper.printurls()


def main(argv: list[str]) -> int:
    if (len(argv) < 1):
        print("ERROR: please provide request url as argument: python sps.py <url>")
        return 1

    _url = argv[0]
    r = requests.get(url=_url)

    if r.status_code != requests.codes.ok:
        print(f"ERROR: Request to address \"{r.url}\" responded error code {r.status_code}")
        return 1

    htmlparse(r.text)

    return 0

if __name__=="__main__":
    from sys import argv
    assert type(argv)==list
    exit(main(argv[1:]))
