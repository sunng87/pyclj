
import unittest
import clj

class CljLoadTest(unittest.TestCase):
    def setUp(self):
        self.data = {"\"helloworld\"": "helloworld",
                     "23": 23,
                     "23.11": 23.11,
                     "true": True,
                     "false": False,
                     "nil": None,
                     ":hello": "hello"}

    def test_all_data(self):
        for k,v in self.data.items():
            self.assertEqual(clj.loads(k), v)


if __name__ == '__main__':
    unittest.main()            


