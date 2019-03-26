from .. import api_qwant

class model(object):
    def __call__(self, x):
        resp = api_qwant.send_query(x)
        return resp["result"]