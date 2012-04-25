# -*- coding: utf-8 -*-
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
                     r'"string\"ing"': 'string"ing',
                     '"string\n"': 'string\n',
                     '[:hello]':["hello"],
                     '-10.4':-10.4,
                     '"你"': '你',
                     "[1 2]": [1,2],
                     "#{true \"hello\" 12}": set([True, "hello", 12]),
                     "(\\a \\b \\c \\d)": ["a","b","c","d"],
                     "{:a 1 :b 2 :c 3 :d 4}": {"a":1, "b":2, "c":3,"d":4},
                     "[1     2 3,4]": [1,2,3,4],
                     "{:a [1 2 3] :b #{23.1 43.1 33.1}}": {"a":[1,2,3], "b":set([23.1,43.1,33.1])},
                     "{:a 1 :b [32 32 43] :c 4}": {"a":1,"b":[32,32,43],"c":4},
                     "\\你": "你",
                     "[23[34][32][4]]": [23,[34],[32],[4]]}

    def test_all_data(self):
        for k,v in self.data.items():
            self.assertEqual(clj.loads(k), v)

            
    def test_misformed_data(self):
        data = ["[1 2 3", "til", "falSe", "nik", "@EE", "[@nil tee]"]
        for d in data:
            self.assertRaises(ValueError, clj.loads, d)



class CljDumpTest(unittest.TestCase):
    def setUp(self):
        self.data = {'"helloworld"': "helloworld",
                     '"hello\\"world"': "hello\"world",
                     '12': 12,
                     '12.334': 12.334,
                     'true': True,
                     'false': False,
                     'nil': None,
                     "[1 2 3]":[1,2,3],
                     "[1 2 3 4]": (1,2,3,4),
                     '{"a" 1 "b" 2}':{"a":1, "b":2},
                     '#{1}': set([1]),
                     '["h" nil [1 2 3] {"w" true}]':["h",None,[1,2,3],{"w":True}]
                     }
        
    def test_all_data(self):
        for k,v in self.data.items():
            self.assertEqual(k, clj.dumps(v))

    def test_circular_ref(self):
        s = [1,2,3]
        d = {"a": [], "b": s}
        s.append(d)
        self.assertRaises(ValueError, clj.dumps, d)

if __name__ == '__main__':
    unittest.main()            


