from html.parser import HTMLParser
from urllib import parse
from general import *


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url, keywords):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.jobs = set()
        self.keywords = keywords

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.find_job(attrs)

            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    # print('find a link: ' + url)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass

    def find_job(self, attrs):
        url = ''
        title = ''
        for i in range(0, len(attrs)):
            # print(attrs[i])
            if attrs[i][0] == 'href':
                url = attrs[i][1]
            if attrs[i][0] == 'title':
                name = attrs[i][1]
                for keyword in self.keywords:
                    if keyword in name:
                        title = attrs[i][1]
                        break
        if not url == '' and not title == '':
            self.jobs.add('{ "Title" : "' + title + '", "URL" : "' + parse.urljoin(self.base_url, url) + '" },')

    def get_jobs(self):
        return self.jobs