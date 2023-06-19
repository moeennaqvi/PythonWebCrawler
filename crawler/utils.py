import gevent
import requests

class WorkerGreenlet(gevent.Greenlet):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def _run(self):
        # Make an HTTP request to the URL and return the response
        response = requests.get(self.url)
        #self.value = response
        return response
