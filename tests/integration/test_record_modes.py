import os
from betamax import Betamax
from requests import Session


class TestBetamax(object):
    def setUp(self):
        self.cassette_path = None

    def tearDown(self):
        os.unlink(self.cassette_path)

    def test_record_once(self):
        s = Session()
        with Betamax(s).use_cassette('test_record_once') as betamax:
            assert betamax.current_cassette.is_empty() is True
            r = s.get('http://httpbin.org/get')
            assert r.status_code == 200
            assert betamax.current_cassette.is_empty() is False
            self.cassette_path = betamax.current_cassette.cassette_name