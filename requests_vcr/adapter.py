from requests.adapters import BaseAdapter, HTTPAdapter
from requests_vcr.cassette import Cassette


class VCRAdapter(BaseAdapter):

    """This object is an implementation detail of the library.

    It is not meant to be a public API and is not exported as such.

    """

    def __init__(self, **kwargs):
        super(VCRAdapter, self).__init__()
        self.cassette = None
        self.cassette_name = None
        self.http_adapter = HTTPAdapter(**kwargs)
        self.serialize = None
        self.options = {}

    def close(self):
        self.http_adapter.close()

    def send(self, request, stream=False, timeout=None, verify=True,
             cert=None, proxies=None):
        if self.cassette:
            # load cassette
            return self.cassette.as_response()
        else:
            # store the response because if they're using us we should
            # probably be storing the cassette
            response = self.http_adapter.send(
                request, stream=stream, timeout=timeout, verify=verify,
                cert=cert, proxies=proxies
            )
            if self.cassette_name:
                Cassette.from_response(response).save(self.cassette_name)
            return response

    def load_cassette(self, cassette_name, serialize, options):
        self.cassette_name = cassette_name
        self.serialize = serialize
        self.options.update(options)
        # load cassette into memory
        self.cassette = Cassette(cassette_name, serialize, )