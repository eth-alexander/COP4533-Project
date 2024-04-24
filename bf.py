import numpy as np

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
        self.weight = max(-1, 1 + station2.height - station1.height)
        
    # note: station order matters! this is because edges don't have same weight going each way
    def __eq__(self, other):
        return (self.station1 == other.station1 and self.station2 == other.station2) and \
               self.weight == other.weight

    def __hash__(self):
        return hash((self.station1, self.station2, self.weight))
 
    def __str__(self):
        return f"Edge(station1={self.station1}, station2={self.station2}, weight={self.weight})"

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
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value   

# calculate shortest path from initial station to final station
def bellman_ford(edges, stations, initial_station, final_station):
    
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
            if distances[(edge.station1.x, edge.station1.y)] + edge.weight < distances[(edge.station2.x, edge.station2.y)]:
                distances[(edge.station2.x, edge.station2.y)] = distances[(edge.station1.x, edge.station1.y)] + edge.weight
    
    # find all negative loops
    for s in range(len(stations) - 1):
        for edge in edges:
            if distances[(edge.station1.x, edge.station1.y)] + edge.weight < distances[(edge.station2.x, edge.station2.y)]:
                distances[(edge.station2.x, edge.station2.y)] = -np.inf
    
    return distances[(final_station.x, final_station.y)]
    
# read grid.txt and convert to weighted graph 
def read_grid(filename):
    with open(filename, 'r') as grid:
        
        # read number of rows and number of columns
        num_rows, num_columns = map(int, grid.readline().strip().split(','))
        stations = {}
        
        # read stations
        for line in grid:
            height, x, y = map(int, line.strip().split(','))
            station = Station( x, y, height)
            stations[(station.x, station.y)] = station
            
            if len(stations) >= num_rows * num_columns:
                break
            
        # read source station (S)
        source_x, source_y = map(int, grid.readline().strip().split(','))
        source = stations[(source_x, source_y)]
        
        # read stations that supply water to baths (B)
        water_stations = {}
        for line in grid:
            x, y = map(int, line.strip().split(','))
            water_stations[(x, y)] = stations[(x, y)]
            
     
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

stations, source, water_stations, edges = read_grid('Simple_Example/grid.txt')

print(bellman_ford(edges, stations, stations[source.x, source.y], stations[0, 2]))

# for station in stations.values():
#             print(station)
# print("Source Station: ", source)
# for station in water_stations.values():
#     print("Water Station: ", station)
# for edge in edges:
#     print(edge)
# print(len(edges))