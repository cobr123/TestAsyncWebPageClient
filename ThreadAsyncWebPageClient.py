import multiprocessing
import traceback
from multiprocessing import Pool
from eventlet.green import urllib2


class AsyncWebPageClient:
    threadCnt = 0

    def __init__(self, cnt=4):
        self.threadCnt = cnt

    def get_pages(self, urls):
        pool = Pool(processes=self.threadCnt)
        for result in pool.imap_unordered(func=get_result, iterable=urls):
            yield result


def get_result(url):
    try:
        o = urllib2.urlopen(url)
        return {'status_code': o.getcode(), 'url': url, 'content': o.read()}
    except Exception, e:
        return {'status_code': -1, 'err': e.__str__(), 'url': url}


def print_result(result):
    print(result['url'])
    if result['status_code'] == -1:
        print(result['err'])
    else:
        print(len(res['content']))


if __name__ == "__main__":
    test_urls = ['http://www.foxnews.com/',
                 'http://some-made-up-domain.com/',
                 'http://www.cnn.com/',
                 'http://europe.wsj.com/',
                 'http://www.bbc.co.uk/']
    client = AsyncWebPageClient()
    for res in client.get_pages(test_urls):
        print_result(res)
