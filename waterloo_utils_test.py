import unittest

from waterloo_utils import waterloo_workaround_get_request


class Test(unittest.TestCase):
    url = "https://www.waterloo.ca/en/things-to-do/arenas-and-outdoor-rinks.aspx"

    def test_waterloo_workaround(self):
        self.response = waterloo_workaround_get_request(self.url)
        self.assertTrue(isinstance(self.response, str))


if __name__ == "__main__":
    unittest.main()
