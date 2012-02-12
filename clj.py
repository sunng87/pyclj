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


import re
from cStringIO import StringIO

def number(v):
    r = None
    try:
        r = int(v)
    except ValueError:
        r = float(v)
    return r

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
        if c.isdigit():
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
            
        t, coll = self.__get_type_from_char(c)
        if coll:
            self.value_stack.append(list())
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
        else:
            v = None ## token value
            e = None ## end char

            if t == "boolean":
                if c == 't':
                    e = fd.read(4)[-1]
                    v = True
                else:
                    e = fd.read(5)[-1]
                    v = False

            elif t == "char":
                v = fd.read(1)
                e = fd.read(1)

            elif t == "nil":
                e = fd.read(3)[-1]
                v = None

            elif t == "number":
                buf = [c]
                while c is not self.terminator and c is not "" and c not in self.stop_chars:
                    c = fd.read(1)
                    buf.append(c)
                e = c
                numstr = ''.join(buf[:-1])
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
                buf.append(c)
                while not(c == '"' and cp != '\\'):
                    cp = c
                    c = fd.read(1)
                    buf.append(c)
                e = c
                v = ''.join(buf[:-1])
            else:
                e = fd.read(1)

            if e is self.terminator:
                current_scope = self.value_stack.pop()

                if self.container == "set":
                    v = set(current_scope)
                elif self.container == "list":
                    v = current_scope
                elif self.container == "dict":
                    v = {}
                    for i in range(0, len(current_scope), 2):
                        v[current_scope[i]] = current_scope[i+1]

            if len(self.value_stack) > 0:
                self.value_stack[-1].append(v)
            print "debug=== ",v, e
            return v
                
    
def dump(obj, fp):
    pass

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

