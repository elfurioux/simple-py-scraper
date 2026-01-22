import requests
from html import parser as html
from urllib import parse as urlt

USE_HTTPS = True
__PROTOCOL = "https" if USE_HTTPS else "http"
__URLPREFIX = __PROTOCOL+"://"

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
    
    def reltohttp(self, urlbeginpart: str):
        self._url = urlbeginpart.removesuffix("/")+self._url
        assert self.ishttp()

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

    def resolveurls(self, urlbeginpart: str):
        i = 0
        while i < len(self.urllist):
            if self.urllist[i].isrelative():
                self.urllist[i].reltohttp(urlbeginpart)
            i += 1

    def printurls(self):
        for url in self.urllist:
            print(url)

def main(argv: list[str]) -> int:
    if (len(argv) < 1):
        print("ERROR: please provide request host as argument: python sps.py <host>")
        return 1

    host = argv[0]
    hosturl = __URLPREFIX+host

    if host.startswith("http") or host.find('/')!=-1:
        print("ERROR: please provide just the hostname, not a url (example: 'google.com', 'en.wikipedia.org')")
        return 1

    scraper = HTMLScraper()
    r = requests.get(url=hosturl)

    if r.status_code != requests.codes.ok:
        print(f"ERROR: Request to address \"{r.url}\" responded error code {r.status_code}")
        return 1

    scraper.feed(r.text)
    scraper.printurls()
    scraper.resolveurls(hosturl)
    print("===")
    scraper.printurls()

    return 0

if __name__=="__main__":
    from sys import argv
    assert type(argv)==list
    exit(main(argv[1:]))
