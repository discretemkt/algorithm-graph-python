import heapq

class Edge(object):
    
    def __init__(self, vertex1, vertex2, weight=None, directed=False):
        assert vertex1 is not None
        assert vertex2 is not None
        assert not isinstance(weight, bool)
        assert isinstance(weight, (int, float)) or weight is None
        assert isinstance(directed, bool)
        self.__vertices = (vertex1, vertex2)
        self.__directed = directed
        if weight is None:
            self.__weight = None
        else:
            self.__weight = float(weight)
    
    def vertices(self):
        return self.__vertices
    
    def weight(self):
        return self.__weight
    
    def isdirected(self):
        return self.__directed
    
    def __repr__(self):
        st = 'Edge {{vertices={0}, weight={1}, isdirected={2}}}'
        s0 = repr(self.__vertices)
        s1 = repr(self.__weight)
        s2 = repr(self.__directed)
        return st.format(s0, s1, s2)

class Graph(object):
    
    def __init__(self, weighted=False):
        if not isinstance(weighted, bool):
            raise TypeError('\'weighted\' must be either True or False.')
        self.__vertices = set()
        self.__edges = set()
        self.__weighted = weighted
    
    def add(self, vertex):
        if vertex is None:
            raise TypeError('Object to be added must not be None.')
        if not vertex in self.__vertices:
            self.__vertices.add(vertex)
    
    def remove(self, vertex):
        if vertex is None:
            raise TypeError('Object to be removed must not be None.')
        if vertex in self.__vertices:
            s = set()
            for e in self.__edges:
                if vertex in e.vertices():
                    s.add(e)
            self.__edges -= t
            self.__vertices.remove(vertex)
    
    def contains(self, vertex):
        if vertex is None:
            raise TypeError('Argument must not be None.')
        return vertex in self.__vertices
    
    def vertices(self):
        return iter(self.__vertices)
    
    def connect(self, vertex1, vertex2, weight=None, directed=False):
        if vertex1 is None or vertex2 is None:
            raise TypeError('Objects to be connected must not be None.')
        if self.__weighted and weight is None:
            raise ValueError('Edges must be weighted in this graph.')
        if not self.__weighted and weight is not None:
            raise ValueError('Edges must not be weighted in this graph.')
        if self.__weighted and not isinstance(weight, (int, float)):
            raise TypeError('\'weight\' must be given by a number.')
        if not isinstance(directed, bool):
            raise TypeError('\'directed\' must be either True or False.')
        self.add(vertex1)
        self.add(vertex2)
        e = Edge(vertex1, vertex2, weight, directed)
        self.__edges.add(e)
        return e
    
    def disconnect(self, edge):
        if edge is None or not isinstance(edge, Edge):
            raise TypeError('Argument must be an Edge object.')
        if edge in self.__edges:
            self.__edges.remove(edge)
    
    def edges(self):
        return iter(self.__edges)
    
    def isweighted(self):
        return self.__weighted
    
    def clear(self):
        self.__edges.clear()
        self.__vertices.clear()

class Dijkstra(object):
    
    def find_shortest_path(graph, source, destination):
        if graph is None or source is None or destination is None:
            raise TypeError('Arguments must not be null.')
        if not isinstance(graph, Graph):
            raise TypeError('First argument must be a Graph object.')
        if not graph.contains(source) or not graph.contains(destination):
            return []
        if source == destination:
            return [source]
        adj_list_table = {}
        for e in graph.edges():
            (v1, v2) = e.vertices()
            w = e.weight()
            if w is None:
                w = 1.0
            if not v1 in adj_list_table:
                adj_list_table[v1] = []
            adj_list_table[v1].append((v2, w))
            if not e.isdirected():
                if not v2 in adj_list_table:
                    adj_list_table[v2] = []
                adj_list_table[v2].append((v1, w))
        dist_pred_table = {}
        queue = []
        for v in graph.vertices():
            if v == source:
                dist_pred_table[v] = (0.0, None)
                heapq.heappush(queue, (0.0, v))
            else:
                dist_pred_table[v] = (float('inf'), None)
                heapq.heappush(queue, (float('inf'), v))
        while 0 < len(queue):
            (d, v) = heapq.heappop(queue)
            if d == float('inf'):
                break
            if not v in adj_list_table:
                continue
            for x in adj_list_table[v]:
                old_d = dist_pred_table[x[0]][0]
                new_d = d + x[1]
                if new_d < old_d:
                    queue.remove((old_d, x[0]))
                    dist_pred_table[x[0]] = (new_d, v)
                    heapq.heappush(queue, (new_d, x[0]))
        p = []
        v = destination
        while v is not None:
            p.insert(0, v)
            v = dist_pred_table[v][1]
        if p[0] == source:
            return p
        else:
            return []

g=Graph(weighted=True)
g.connect('S', 'A', 1.0, True)
g.connect('S', 'B', 4.0, True)
g.connect('A', 'B', 4.5, True)
g.connect('A', 'C', 2.0, True)
g.connect('A', 'D', 5.0, True)
g.connect('B', 'C', 2.5, True)
g.connect('B', 'D', 1.5, True)
g.connect('C', 'Z', 3.5, True)
g.connect('C', 'B', 0.5, True)
g.connect('C', 'D', 2.5, True)
g.connect('D', 'A', 1.0, True)
g.connect('D', 'C', 2.0, True)
g.connect('D', 'Z', 1.0, True)
print(Dijkstra.find_shortest_path(g, 'S', 'Z')) # --> ['S', 'A', 'C', 'B', 'D', 'Z']

g.add('X')
print(Dijkstra.find_shortest_path(g, 'S', 'X')) # --> []

