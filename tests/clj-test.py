
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
                     ":hello": "hello",
                     '"string\\"ing"': 'string"ing',
                     '"string\\n"': 'string\n',
                     "[1 2]": [1,2],
                     "#{true \"hello\" 12}": set([True, "hello", 12]),
                     "(\\a \\b \\c \\d)": ["a","b","c","d"],
                     "{:a 1 :b 2 :c 3 :d 4}": {"a":1, "b":2, "c":3,"d":4},
                     "[1     2 3,4]": [1,2,3,4],
                     "{:a [1 2 3] :b #{23.1 43.1 33.1}}": {"a":[1,2,3], "b":set([23.1,43.1,33.1])}}

    def test_all_data(self):
        for k,v in self.data.items():
            self.assertEqual(clj.loads(k), v)


if __name__ == '__main__':
    unittest.main()            


