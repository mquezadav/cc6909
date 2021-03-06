import simplejson as json
import urllib2
from model.page import Page
from model.event import Event
from hashlib import md5

F = "[google_news]"

"""
DEPRECATED
"""

class GoogleNews(object):
    #https://ajax.googleapis.com/ajax/services/search/news?v=1.0&topic=s

    @staticmethod
    def get_topnews(results=8):
        URL = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&ned=%s&topic=%s&rsz=%d'
        editions = ('es_cl', 'en_us')
        topics = {'w':'Internacional', 'h':'Titulares'}
        i = 0

        for edition in editions:            
            for topic in topics:
                url = URL % (edition, topic, results)
                print F, url
                response = urllib2.urlopen(url)
                data = response.read()

                news = json.loads(data)
                if news['responseStatus'] == 200:
                    for result in news['responseData']['results']:
                        data = {}

                        data['title'] = result['titleNoFormatting']
                        data['locale'] = edition
                        data['date'] = result['publishedDate']
                        data['url'] = result['url']
                        data['type'] = 'news'
                        data['id'] = md5(data['url']).hexdigest()
                        data['content'] = ''
                        
                        event = {}
                        event['title'] = data['title']
                        event['locale'] = data['locale']
                        event['description'] = result['content']
                        event['date'] = data['date']
                        e_id = event['id'] = md5("%s %s" % (repr(data['title']), data['url'])).hexdigest()

                        print F, repr("Crawled news: %s" % data['title'])
                        e = Event(event)
                        e.save()

                        n = Page(data)
                        n.parent_id = e_id
                        n.save()

                        if result.has_key('relatedStories'):
                            for related in result['relatedStories']:
                                data = {}
                                data['title'] = related['titleNoFormatting']
                                data['locale'] = edition
                                data['date'] = related['publishedDate']
                                data['url'] = related['url']
                                data['id'] = md5(data['url']).hexdigest()
                                data['type'] = 'news'
                                data['content'] = ''

                                print F, repr("Related news: %s" % data['title'])
                                n = Page(data)
                                n.parent_id = e_id
                                n.save()
                                i += 1
                else:
                    print F, news['responseDetails']

        print F, "total news collected: %d" % i

def main():
    GoogleNews.get_topnews()

if __name__ == '__main__':
    main()