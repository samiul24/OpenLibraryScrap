import scrapy
from scrapy.exceptions import CloseSpider
import json


class OpenlibrarySpider(scrapy.Spider):

    increment_by = 12
    offset = 0

    name = 'OpenLibrary'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12']

    def parse(self, response):
        if response.status == 500:
            raise CloseSpider('Reached the last page...')

        resps = json.loads(response.body)
        #print(resps)
        #resp = resps.get('works')
        #print(type(resps))
        #print(type(resp))
        #pre_list = []
        for x in resps:
            if x == 'name':
                name = resps[x]
            elif x == 'key':
                key = resps[x]
            elif x == 'subject_type':
                subject_type = resps[x]
            elif x == 'works':
                for y in resps[x]:
                    #print(type(y))
                    for z in y:
                        # print(z)
                        # print(type(z))
                        if z == 'title':
                            title = y[z]
                        elif z == 'edition_count':
                            edition_count = y[z]
                        elif z == 'subject':
                            subject = y[z]
                        elif z == 'authors':
                            #print(type(y[z])) # List
                            authors = ''
                            for a in y[z]:
                                for b in a:
                                    if b =='name':
                                        authors += a[b] + ', '
                            authors = authors.strip()[:-1]
                                #print(y[z])
                                #print(type(a)) # Dict
                            
                    yield{
                            'key': key,
                            'name': name,
                            'subject_type': subject_type,
                            'title': title,
                            'edition_count': edition_count,
                            'subject': subject,
                            'authors': authors,
                        
                        }
            #print(resps[x])
            #print(type(resps[x]))
        self.offset += self.increment_by
        yield scrapy.Request(
            url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}', 
            callback=self.parse
        )


