import abc
import heapq

class Edge(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def vertices(self):
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
            self.__vertices = (v1, v2)
            self.__directed = directed
            if weight is None:
                self.__weight = None
            else:
                self.__weight = float(weight)
        
        def vertices(self):
            return self.__vertices
        
        def isdirected(self):
            return self.__directed
        
        def isweighted(self):
            return self.__weight is not None
        
        def weight(self):
            return self.__weight
        
        def __repr__(self):
            s1 = repr(self.__vertices)
            s2 = str(self.__directed)
            s3 = str(self.__weight)
            return 'Edge{{{0},d={1},w={2}}}'.format(s1, s2, s3)
    
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
                if v in x.vertices():
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
    
    def find_shortest_path(g, src, dst):
        if g is None or src is None or dst is None:
            raise TypeError('Arguments must not be null.')
        if not isinstance(g, Graph):
            raise TypeError('First argument must be a Graph object.')
        if not g.has_vertex(src) or not g.has_vertex(dst):
            return []
        if src == dst:
            return [src]
        adj_table = {}
        weighted = None
        for e in g.edges():
            if weighted is None:
                weighted = e.isweighted()
            if (weighted and not e.isweighted()) or (not weighted and e.isweighted()):
                raise Exception('Both weighted and unweighted edges are found...')
            (v1, v2) = e.vertices()
            w = e.weight()
            if not v1 in adj_table:
                adj_table[v1] = {}
            adj1 = adj_table[v1]
            if (not v2 in adj1) or (weighted and w < adj1[v2]):
                adj1[v2] = w
            if not e.isdirected():
                if not v2 in adj_table:
                    adj_table[v2] = {}
                adj2 = adj_table[v2]
                if (not v1 in adj2) or (weighted and w < adj2[v1]):
                    adj2[v1] = w
        predecessor_table = {}
        distance_table = {}
        h = []
        for v in g.vertices():
            predecessor_table[v] = None
            if v == src:
                distance_table[v] = 0.0
                heapq.heappush(h, (0.0, v))
            else:
                distance_table[v] = float('inf')
                heapq.heappush(h, (float('inf'), v))
        while 0 < len(h):
            (d, v) = heapq.heappop(h)
            if d == float('inf'):
                break
            if not v in adj_table:
                continue
            adj = adj_table[v]
            for x in adj:
                old_d = distance_table[x]
                new_d = d + adj[x]
                if new_d < old_d:
                    h.remove((old_d, x))
                    predecessor_table[x] = v
                    distance_table[x] = new_d
                    heapq.heappush(h, (new_d, x))
        path = []
        p = dst
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

