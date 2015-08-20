try:
    StopIteration=StopIteration
except NameError:
    StopIteration=IndexError
class LinestackIter(object):
    _stack=None
    _n=None
    _c=None
    def __init__(self,stack):
        self._stack=list(stack)
        self._n=-1
        self._c=0 #Number of calls to __next__
    def __next__(self):
        self._c+=1
        self._n+=1
        if self._n==len(self._stack):
            return ""
        if self._n>=(len(self._stack)+1):
            raise StopIteration
        return self._stack[self._n]
    def peek_back(self,n=1):
        if (self._n-n)<0:
            return None
        return self._stack[self._n-n]
    def peek_ahead(self,n=1):
        if (self._n+n)>=len(self._stack):
            return None
        return self._stack[self._n+n]
    def rtpma(self): #Run that past me again
        self._n-=1
    #
    # Tell Python to use iterator __next__/next API
    def __iter__(self):
        return self
    #
    # Wrappers for older iterator APIs
    def next(self):
        return self.__next__()
    def __getitem__(self,i):
        if i==self._c:
            return self.__next__()
        else:
            raise TypeError("indexing an iterator")
