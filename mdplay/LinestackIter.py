__copying__ = """
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

try:
    StopIteration = StopIteration
except NameError:
    StopIteration = IndexError

class LinestackIter(object):
    """Specialised iterator for a list of lines, allowing peeking as well as
    re-running of previously seen lines.
    """
    
    _stack = None
    _n = None
    _c = None
    
    def __init__(self, stack):
        self._stack = list(stack)
        self._n = -1
        self._c = 0 #Number of calls to __next__
    
    def __next__(self):
        self._c += 1
        self._n += 1
        if self._n == len(self._stack):
            return ""
        if self._n >= (len(self._stack) + 1):
            raise StopIteration
        return self._stack[self._n]
    
    def peek_back(self, n=1):
        """Return the previous line, or None if there isn't one."""
        if (self._n - n) < 0:
            return None
        return self._stack[self._n - n]
    
    def peek_ahead(self, n=1):
        """Return the next line, or None if there isn't one."""
        if (self._n + n) >= len(self._stack):
            return None
        return self._stack[self._n + n]
    
    def rtpma(self): #Run that past me again
        """Make the next iteration yield the current line again."""
        self._n -= 1
    
    # Is itself an iterator, so its iterator is itself.
    def __iter__(self):
        return self
    
    # Wrappers for older iterator APIs
    # In particular, next() is needed on Python 2.
    def next(self):
        return self.__next__()
    def __getitem__(self,i):
        if i==self._c:
            return self.__next__()
        else:
            raise TypeError("indexing an iterator")

