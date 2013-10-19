# -*- coding: utf-8 -*-
import unittest
import clj
import pytz
import decimal
from datetime import datetime
import uuid

class CljLoadTest(unittest.TestCase):
    def setUp(self):
        self.data = {"\"helloworld\"": "helloworld",
                     "23": 23,
                     '23.45M': decimal.Decimal('23.45'),
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
                     "[23[34][32][4]]": [23,[34],[32],[4]],
                     "#inst \"2012-10-19T22:19:03.000-00:00\"": datetime(2012, 10, 19, 22, 19, 3, tzinfo=pytz.utc),
                     '#uuid "6eabd442-6958-484b-825d-aa79c0ad4967"': uuid.UUID("6eabd442-6958-484b-825d-aa79c0ad4967"),
                     '{:a #inst "2012-10-19T22:19:03.000-00:00"}': {"a":datetime(2012, 10, 19, 22, 19, 3, tzinfo=pytz.utc)},
                     '[#inst "2012-10-19T22:19:03.000-00:00"]': [datetime(2012, 10, 19, 22, 19, 3, tzinfo=pytz.utc)]
                     '{:likes #{{:db/id 2} {:db/id 1}}}': {'likes': tuple([{'db/id': 2}, {'db/id': 1}])}
                     }

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
                     '23.45M': decimal.Decimal('23.45'),
                     '12.334': 12.334,
                     'true': True,
                     'false': False,
                     'nil': None,
                     "[1 2 3]":[1,2,3],
                     "[1 2 3 4]": (1,2,3,4),
                     "[]": (),
                     "{}": {},
                     '{"a" 1 "b" 2}':{"a":1, "b":2},
                     '#{1}': set([1]),
                     '["h" nil [1 2 3] {"w" true}]':["h",None,[1,2,3],{"w":True}],
                     '#inst "2012-10-19T14:16:54Z"':datetime(2012,10,19,14,16,54,907),
                     '#uuid "6eabd442-6958-484b-825d-aa79c0ad4967"': uuid.UUID("6eabd442-6958-484b-825d-aa79c0ad4967")
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
