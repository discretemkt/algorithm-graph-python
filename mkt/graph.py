import abc
import heapq

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

class Dijkstra(object):
    
    class __Vertex(object):
        
        def __init__(self, distance_table, v):
            assert distance_table is not None
            assert isinstance(distance_table, dict)
            assert v is not None
            self.__distance_table = distance_table
            self.__v = v
        
        def __hash__(self):
            return hash(self.__v)
        
        def __compare(self, another):
            assert another is not None
#            assert isinstance(another, Dijkstra.__Vertex)
            if not another.v() in self.__distance_table:
                if not self.v() in self.__distance_table:
                    return 0
                else:
                    return -1
            else:
                if not self.v() in self.__distance_table:
                    return 1
            d1 = self.__distance_table[self.v()]
            d2 = self.__distance_table[another.v()]
            if d1 < d2:
                return -1
            if d1 > d2:
                return 1
            return 0
        
        def __eq__(self, another):
            return self.__compare(another) == 0
        
        def __ne__(self, another):
            return self.__compare(another) != 0
        
        def __gt__(self, another):
            return self.__compare(another) > 0
        
        def __ge__(self, another):
            return self.__compare(another) >= 0
        
        def __lt__(self, another):
            return self.__compare(another) < 0
        
        def __le__(self, another):
            return self.__compare(another) <= 0
        
        def v(self):
            return self.__v
    
    def find_shortest_path(g, v1, v2):
        if g is None or v1 is None or v2 is None:
            raise TypeError('Arguments must not be null.')
        if not isinstance(g, Graph):
            raise TypeError('First argument must be a Graph object.')
        if not g.has_vertex(v1) or not g.has_vertex(v2):
            return []
        if v1 == v2:
            return [v1]
        adj_table = {}
        weighted = None
        for e in g.edges():
            if weighted is None:
                weighted = e.isweighted()
            if (weighted and not e.isweighted()) or (not weighted and e.isweighted()):
                raise Exception('Both weighted and unweighted edges are found...')
            w = e.weight()
            if not e.v1() in adj_table:
                adj_table[e.v1()] = {}
            adj1 = adj_table[e.v1()]
            if (not e.v2() in adj1) or (weighted and w < adj1[e.v2()]):
                adj1[e.v2()] = w
            if not e.isdirected():
                if not e.v2() in adj_table:
                    adj_table[e.v2()] = {}
                adj2 = adj_table[e.v2()]
                if (not e.v1() in adj2) or (weighted and w < adj2[e.v1()]):
                    adj2[e.v1()] = w
        predecessor_table = {}
        for v in g.vertices():
            predecessor_table[v] = None
        distance_table = {}
        distance_table[v1] = 0.0
        heap = []
        heapq.heapify(heap)
        for v in g.vertices():
            heapq.heappush(heap, Dijkstra.__Vertex(distance_table, v))
        while 0 < len(heap):
            v = heapq.heappop(heap).v()
            if not v in distance_table:
                break
            if not v in adj_table:
                continue
            d1 = distance_table[v]
            adj = adj_table[v]
            for x in adj:
                w = adj[x]
                if (not x in distance_table) or (d1 + w < distance_table[x]):
                    predecessor_table[x] = v
                    distance_table[x] = d1 + w
                    heapq.heapify(heap)
        path = []
        p = v2
        while p is not None:
            path.insert(0, p)
            p = predecessor_table[p]
        return path

g=Graph()
g.connect('S','A',True,1.0)
g.connect('S','B',True,4.0)
g.connect('A','B',True,4.5)
g.connect('A','C',True,2.0)
g.connect('A','D',True,5.0)
g.connect('B','C',True,2.5)
g.connect('B','D',True,1.5)
g.connect('C','Z',True,3.5)
g.connect('C','B',True,0.5)
g.connect('C','D',True,2.5)
g.connect('D','A',True,1.0)
g.connect('D','C',True,2.0)
g.connect('D','Z',True,1.0)
print(Dijkstra.find_shortest_path(g,'S','Z'))

