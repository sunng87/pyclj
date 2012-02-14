# -*- coding: utf-8 -*-
# Copyright (C) 2012 Sun Ning<classicning@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# clojure literals => python types
#
# clojure vector [1 2 3 4] => python list [1 2 3 4] *coll
# clojure list (1 2 3 4) => python list [1 2 3 4] *coll
# clojure set #{1 2 3 4} => python set set(1 2 3 4) *coll
# clojure map {:a 1 :b 2} => python dict dict(a=1,b=2) *coll
# clojure string "a" => python unicode "a"
# clojure character \a => python unicode "a"
# clojure keyword :a => python unicode "a"
# clojure integer 123 => python integer 123
# clojure float 12.3 => python float 12.3
# clojure boolean true => python boolean true
# clojure nil => python None 
#


__all__ = ["dump", "dumps", "load", "loads"]

import os
from cStringIO import StringIO

def number(v):
    if '.' in v:
        return float(v)
    else:
        return int(v)

class CljDecoder(object):
    def __init__(self, fd):
        self.fd = fd
        self.value_stack = []
        self.stop_chars = [" ", ",", "\n", "\r"]
        self.terminator = None ## for collection type

    def decode(self):
        while True:
            v = self.__read_token()
            if len(self.value_stack) == 0:
                return v
        
    def __get_type_from_char(self, c):
        """return a tuple of type information
        * type name
        * a flag to indicate if it's a collection
        """
        if c.isdigit() or c =='-':
            return ("number", False)
        elif c == 't' or c == 'f': ## true/false
            return ("boolean", False)
        elif c == 'n': ## nil
            return ("nil", False)
        elif c == '\\' :
            return ("char", False)
        elif c == ':':
            return ("keyword", False)
        elif c == '"':
            return ("string", False)
        elif c == '#':
            return ("set", True)
        elif c == '{':
            return ("map", True)
        elif c == '(':
            return ("list", True)
        elif c == '[':
            return ('vector', True)
        else:
            return (None, False)

    def __read_token(self):
        fd = self.fd
        
        c = fd.read(1)

        ## skip all stop chars if necessary 
        while c in self.stop_chars:
            c = fd.read(1)

        ## raise exception when unexpected EOF found
        if c == '':
            raise ValueError("Unexpected EOF")

        t, coll = self.__get_type_from_char(c)
        if coll:
            ## move cursor 
            if t == "set":
                ## skip {
                fd.read(1)
                self.terminator = "}"
                self.container = "set"
            elif t == "list":
                self.terminator = ")"
                self.container = "list"
            elif t == "vector":
                self.terminator = "]"
                self.container = "list"
            elif t == "map":
                self.terminator = "}"
                self.container = "dict"
                
            self.value_stack.append(([], self.terminator, self.container))
            return None
        else:
            v = None ## token value
            e = None ## end char
            r = True ## the token contains data or not

            if t == "boolean":
                if c == 't':
                    e = fd.read(4)[-1]
                    v = True
                else:
                    e = fd.read(5)[-1]
                    v = False

            elif t == "char":
                buf = []
                while c is not self.terminator and c is not "" and c not in self.stop_chars:
                    c = fd.read(1)
                    buf.append(c)
                
                e = c
                v = ''.join(buf[:-1])

            elif t == "nil":
                e = fd.read(3)[-1]
                v = None

            elif t == "number":
                buf = []
                while c is not self.terminator and c is not "" and c not in self.stop_chars:
                    buf.append(c)
                    c = fd.read(1)
                e = c
                numstr = ''.join(buf)
                v = number(numstr)

            elif t == "keyword":
                buf = []    ##skip the leading ":"
                while c is not self.terminator and c is not "" and c not in self.stop_chars:
                    c = fd.read(1)
                    buf.append(c)
 
                e = c
                v = ''.join(buf[:-1])

            elif t == "string":
                buf = []
                cp = c = fd.read(1) ## to check escaping character \

                while not(c == '"' and cp != '\\'):
                    buf.append(c)
                    cp = c
                    c = fd.read(1)
                e = c
                #v = u''.join(buf).decode('unicode-escape')
                v = ''.join(buf).decode('string-escape')
            else:
                r = False
                e = c

            if e is self.terminator:
                current_scope, _, self.container = self.value_stack.pop()

                if r:
                    current_scope.append(v)
                    
                if self.container == "set":
                    v = set(current_scope)
                elif self.container == "list":
                    v = current_scope
                elif self.container == "dict":
                    v = {}
                    for i in range(0, len(current_scope), 2):
                        v[current_scope[i]] = current_scope[i+1]

            if len(self.value_stack) > 0:
                self.value_stack[-1][0].append(v)
                self.terminator = self.value_stack[-1][1]

            return v


class CljEncoder(object):
    def __init__(self, data, fd):
        self.data = data
        self.fd = fd

    def encode(self):
        self.__do_encode(self.data)

    def get_type(self,t):
        if t is None:
            return ("None", False)
        elif isinstance(t, str) or isinstance(t, unicode):
            return ("string", False)
        elif isinstance(t, bool):
            return ("boolean", False)
        elif isinstance(t, float) or isinstance(t, int):
            return ("number", False)
        elif isinstance(t, dict):
            return ("dict", True)
        elif isinstance(t, list):
            return ("list", True)
        elif isinstance(t, set):
            return ("set", True)
        else:
            return ("unknown", False)

    def __do_encode(self, d):
        fd = self.fd
        t,coll = self.get_type(d)

        if coll:
            if t == "dict":
                fd.write("{")
                for k,v in d.items():
                    self.__do_encode(k)
                    fd.write(" ")
                    self.__do_encode(v)
                    fd.write(" ")
                fd.seek(-1, os.SEEK_CUR)
                fd.write("}")
            elif t == "list":
                fd.write("[")
                for v in d:
                    self.__do_encode(v)
                    fd.write(" ")
                fd.seek(-1, os.SEEK_CUR)
                fd.write("]")
            elif t == "set":
                fd.write("#{")
                for v in d:
                    self.__do_encode(v)
                    fd.write(" ")
                fd.seek(-1, os.SEEK_CUR)
                fd.write("}")
        else:
            if t == "number":
                fd.write(str(d))
            elif t == "string":
                s = d.encode("unicode-escape").replace('"', '\\"')
                fd.write('"'+s+'"')
            elif t == "boolean":
                if d:
                    fd.write('true')
                else:
                    fd.write('false')
            elif t == 'None':
                fd.write('nil')
            else:
                fd.write('"'+str(d)+'"')
    
def dump(obj, fp):
    return CljEncoder(obj, fp).encode()

def dumps(obj):
    buf = StringIO()
    dump(obj, buf)
    result = buf.getvalue()
    buf.close()
    return result

def load(fp):
    decoder = CljDecoder(fp)
    return decoder.decode()

def loads(s):
    buf = StringIO(s)
    result = load(buf)
    buf.close()
    return result

