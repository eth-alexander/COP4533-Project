import numpy as np
import itertools

# station
class Station:
    def __init__(self, x, y, height):
        self.x= x
        self.y = y
        self.height = height
        
    def __str__(self):
        return f"Station(x={self.x}, y={self.y}, height={self.height})"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
 
# directed edge
class Edge:
    def __init__(self, station1, station2):
        self.station1 = station1
        self.station2 = station2
        self.time = max(-1, 1 + station2.height - station1.height)
        
    # note: station order matters, edges don't have same time going each way
    def __eq__(self, other):
        return (self.station1 == other.station1 and self.station2 == other.station2) and \
               self.time == other.time

    def __hash__(self):
        return hash((self.station1, self.station2, self.time))
 
    def __str__(self):
        return f"Edge(station1={self.station1}, station2={self.station2}, time={self.time})"

    @property
    def station1(self):
        return self._first

    @station1.setter
    def station1(self, value):
        self._first = value

    @property
    def station2(self):
        return self._second

    @station2.setter
    def station2(self, value):
        self._second = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value   

# calculate shortest path from initial_station to final_station
def shortest_path(edges, stations, initial_station, final_station):
    
    # distance from initial_station to all other stations
    distances = {}
    
    # initialize all distances to +infinity
    for  station in stations.values():
        distances[(station.x, station.y)] = np.inf
    
    # set distance from initial_station to itself as 0
    distances[(initial_station.x, initial_station.y)] = 0
    
    # for each station, relax all edges
    for s in range(len(stations) - 1):
        for edge in edges:
            if distances[(edge.station1.x, edge.station1.y)] + edge.time < distances[(edge.station2.x, edge.station2.y)]:
                distances[(edge.station2.x, edge.station2.y)] = distances[(edge.station1.x, edge.station1.y)] + edge.time
    
    # find all negative loops
    for s in range(len(stations) - 1):
        for edge in edges:
            if distances[(edge.station1.x, edge.station1.y)] + edge.time < distances[(edge.station2.x, edge.station2.y)]:
                distances[(edge.station2.x, edge.station2.y)] = -np.inf
    
    return distances[(final_station.x, final_station.y)]
    
# read grid.txt and convert to weighted graph 
def read_grid(filename):
    with open(filename, 'r') as grid:
        num_rows, num_columns = map(int, grid.readline().strip().split(','))
        stations = {}
        
        # stations
        for line in grid:
            height, x, y = map(int, line.strip().split(','))
            station = Station( x, y, height)
            stations[(station.x, station.y)] = station
            
            if len(stations) >= num_rows * num_columns:
                break
            
        # source station (S)
        source_x, source_y = map(int, grid.readline().strip().split(','))
        source = stations[(source_x, source_y)]
        
        # stations that supply water to baths (B)
        water_stations = {}
        for line in grid:
            x, y = map(int, line.strip().split(','))
            water_stations[(x, y)] = stations[(x, y)]
            
        # edges
        edges = set()
        for station in stations.values():
            if (station.x - 1, station.y) in stations:
                edges.add(Edge(station, stations[(station.x - 1, station.y)]))
            if (station.x + 1, station.y) in stations:
                edges.add(Edge(station, stations[(station.x + 1, station.y)]))
            if (station.x, station.y - 1) in stations:
                edges.add(Edge(station, stations[(station.x, station.y - 1)]))
            if (station.x, station.y + 1) in stations:
                edges.add(Edge(station, stations[(station.x, station.y + 1)]))
                
        return stations, source, water_stations, edges
            
# store list of all paths from S to all b_i with respective costs
def find_paths(source, unvisited_ws, edges, stations):
    paths = []
    memo = {}
    
    for order in itertools.permutations(unvisited_ws.keys()):
        paths += find_paths_recursive(source, unvisited_ws, edges, stations, order, source, 0, [source], memo)
    return paths

def find_paths_recursive(source, unvisited_ws, edges, stations, order, current_station, path_length, path, memo):
    # no more water stations to be visited
    if not order:
        return [(path, path_length)]
    
    paths = []
    next_station = unvisited_ws[order[0]]
    
    # check if already calculated path from current_station to next_station
    if (current_station, next_station) in memo:
        path_length += memo[(current_station, next_station)]
    else:
        length = shortest_path(edges, stations, current_station, next_station)
        path_length += length
        memo[(current_station, next_station)] = length
    
    updated_path = path + [next_station]
    paths += find_paths_recursive(source, unvisited_ws, edges, stations, order[1:], next_station, path_length, updated_path, memo)
    
    return paths

# find minimum cost path
def opt(source, unvisited_ws, edges, stations):
    paths = find_paths(source, unvisited_ws, edges, stations)
    return min(path_length for _, path_length in paths)

# read input
stations, source, water_stations, edges = read_grid('grid.txt')

# write output
with open('pathLength.txt', 'w') as file:
    file.write(str(opt(source, water_stations, edges, stations)))
