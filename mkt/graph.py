import abc

class Edge(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def v1(self):
        pass
    
    @abc.abstractmethod
    def v2(self):
        pass
    
    @abc.abstractmethod
    def isdirected(self):
        pass
    
    @abc.abstractmethod
    def isweighted(self):
        pass
    
    @abc.abstractmethod
    def weight(self):
        pass

class Graph(object):
    
    class __Edge(Edge):
        
        def __init__(self, v1, v2, directed=False, weight=None):
            assert v1 is not None
            assert v2 is not None
            assert isinstance(directed, bool)
            assert not isinstance(weight, bool)
            assert isinstance(weight, (int, float)) or weight is None
            self.__v1 = v1
            self.__v2 = v2
            self.__directed = directed
            if weight is None:
                self.__weight = None
            else:
                self.__weight = float(weight)
        
        def v1(self):
            return self.__v1
        
        def v2(self):
            return self.__v2
        
        def isdirected(self):
            return self.__directed
        
        def isweighted(self):
            return self.__weight is not None
        
        def weight(self):
            return self.__weight
        
        def __repr__(self):
            s1 = repr(self.__v1)
            s2 = repr(self.__v2)
            s3 = str(self.__directed)
            s4 = str(self.__weight)
            return 'Edge{{({0},{1}),d={2},w={3}}}'.format(s1, s2, s3, s4)
    
    def __init__(self):
        self.__vertices = set()
        self.__edges = set()
    
    def add(self, v):
        if v is None:
            raise TypeError('Object to be added must not be None.')
        if not v in self.__vertices:
            self.__vertices.add(v)
    
    def remove(self, v):
        if v is None:
            raise TypeError('Object to be removed must not be None.')
        if v in self.__vertices:
            edges = set()
            for x in self.__edges:
                if x.v1() == v or x.v2() == v:
                    edges.add(x)
            for x in edges:
                self.__edges.remove(x)
            self.__vertices.remove(v)
    
    def has_vertex(self, v):
        if v is None:
            raise TypeError('Argument must not be None.')
        return v in self.__vertices
    
    def vertices(self):
        return self.__vertices.copy()
    
    def connect(self, v1, v2, directed=False, weight=None):
        if v1 is None or v2 is None:
            raise TypeError('Objects to be connected must not be None.')
        if not isinstance(directed, bool):
            raise TypeError('\'directed\' must be either True or False.')
        if isinstance(weight, bool):
            raise TypeError('\'weight\' must be either a number or None.')
        if not isinstance(weight, (int, float)) and weight is not None:
            raise TypeError('\'weight\' must be either a number or None.')
        self.add(v1)
        self.add(v2)
        e = Graph.__Edge(v1, v2, directed, weight)
        self.__edges.add(e)
        return e
    
    def disconnect(self, e):
        if e is None or not isinstance(e, Edge):
            raise TypeError('Argument must be an Edge object.')
        if e in self.__edges:
            self.__edges.remove(e)
    
    def has_edge(self, e):
        if e is None or not isinstance(e, Edge):
            raise TypeError('Argument must be an Edge object.')
        return e in self.__edges
    
    def edges(self):
        return self.__edges.copy()
    
    def clear(self):
        self.__edges.clear()
        self.__vertices.clear()

