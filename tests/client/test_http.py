import unittest
import client.http
import os


class TestHttpClient(unittest.TestCase):
    # def test_get_exist(self):
    #     c = client.http.Client()
    #     r = c.get('abc', '123', 'a')
    #     print(r)

    def test_parse(self):
        filepath = os.path.join(os.path.dirname(__file__), 'abc123.html')
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        c = client.http.Client()
        r = c.parse(html)
        print(r)


if __name__ == "__main__":
    unittest.main()
