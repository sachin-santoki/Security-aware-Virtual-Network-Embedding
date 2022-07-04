import random
import copy
import numpy as np

class Parameters:
    def __init__(
        self,
        lower_edge,
        upper_edge,
        lower_node,
        upper_node,
        lower_demand,
        upper_demand,
        lower_level,
        upper_level,
      
    ) -> None:
        self.lower_edge = lower_edge
        self.uppper_edge = upper_edge
        self.lower_node = lower_node
        self.upper_node = upper_node
        self.lower_demand=lower_demand
        self.upper_demand=upper_demand
        self.lower_level=lower_level
        self.upper_level=upper_level


class Graph:
    def __init__(self, nodes, edges, parameters) -> None:
        lower_edge = parameters.lower_edge
        upper_edge = parameters.uppper_edge
        lower_node = parameters.lower_node
        upper_node = parameters.upper_node
        lower_demand=parameters.lower_demand
        upper_demand=parameters.upper_demand
        lower_level=parameters.lower_level
        upper_level=parameters.upper_level
        self.nodes = nodes
        self.edges = list(edges)
        self.neighbours = dict()
        self.node_weights = dict() # CRB
        self.edge_weights = dict() # BandWidth
        self.node_demand = dict()#security_demand
        self.node_level = dict()#security_level
        self.parameters = parameters
        for a, b in edges:
            self.edge_weights[(a, b)] = int(np.random.uniform(lower_edge, upper_edge))
            self.edge_weights[(b, a)] = self.edge_weights[(a, b)]
        for i in range(self.nodes):
            self.node_weights[i] = int(np.random.uniform(lower_node, upper_node))
            self.node_demand[i] = int(np.random.uniform(lower_demand, upper_demand))
            self.node_level[i] = int(np.random.uniform(lower_level, upper_level))
            
        for i in range(self.nodes):
            self.neighbours[i] = set()
            for a, b in self.edges:
                if int(a) == i:
                    self.neighbours[i].add(b)

    def findPaths(self, s, d, visited, path, all_paths, weight):
        
        visited[int(s)] = True
        path.append(int(s))
        if s == d:
            # print("Path = ",path)#added
            all_paths.append(path.copy())
            return#added
        else:
            
            # print(self.neighbours)
            # x=self.neighbours[s]
            x=[(k, self.neighbours[k]) for k in self.neighbours]
            for k,i in x:
                if(k==s):
                  for j in i:
                    j=int(j)
                    if visited[int(j)] == False and self.edge_weights[(str(s),str(j))] >= weight:#changed:[(str(s), i)]
                        self.findPaths((j), (d), visited, path, all_paths, weight)

        path.pop()
        visited[int(s)] = False

   
    def findPathFromSrcToDst(self, s, d, weight):

        all_paths = []
        visited = [False] * (self.nodes)
        path = []
        self.findPaths(s, d, visited, path, all_paths, weight)
        if all_paths == []:
            return []
        else:
            return all_paths[random.randint(0, len(all_paths) - 1)]

    def BFS(self, src, dest, v, pred, dist, weight):
        queue = []
        visited = [False for i in range(v)]
        for i in range(v):
            dist[i] = 1000000
            pred[i] = -1
        visited[int(src)] = True
        dist[int(src)] = 0
        queue.append(src)
        while len(queue) != 0:
            u = queue[0]
            queue.pop(0)
            for i in self.neighbours[int(u)]:
                if visited[int(i)] == False and self.edge_weights[(u, i)] >= weight:
                    visited[int(i)] = True
                    dist[int(i)] = dist[int(u)] + 1
                    pred[int(i)] = u
                    queue.append(i)
                    if i == dest:
                        return True

        return False

    def findShortestPath(self, s, dest, weight):
        v = self.nodes
        pred = [0 for i in range(v)]
        dist = [0 for i in range(v)]
        ls = []
        if self.BFS(s, dest, v, pred, dist, weight) == False:
            return ls
        path = []
        crawl = dest
        crawl = dest
        path.append(crawl)

        while pred[int(crawl)] != -1:
            path.append(pred[int(crawl)])
            crawl = pred[int(crawl)]

        for i in range(len(path) - 1, -1, -1):
            ls.append(path[i])

        return ls

   
    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''
    def printAllPathsUtil(self, u, d, visited, weight, path, all_path):
        # Mark the current node as visited and store in path
        visited[int(u)]= True
        path.append(u)
        # print(f"{u} {d}")
        # print(path)
        # If current vertex is same as destination, then print
        # current path[]
        
        if u==d:
            all_path.append(copy.deepcopy(path))
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.neighbours[int(u)]:
                if visited[int(i)] == False and self.edge_weights[(u, i)] >= weight:
                # if visited[int(i)]== False:
                    self.printAllPathsUtil(i, d, visited, weight, path, all_path)
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[int(u)]= False
       
  
  
    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d, weight):
        visited =[False]*(self.nodes) # Mark all the vertices as not visited 
        path = []   # Create an array to store a path
        all_path = []   # array to store all the paths
        self.printAllPathsUtil(s, d, visited, weight, path, all_path)  # Call the recursive helper function to print all paths
        return all_path
  
if __name__ == '__main__':
    nodes = 4
    para = Parameters(50, 100, 50,100,50,100,50,100) # 0, 100, 0, 100, 1, 1)
    edges = [('0','1'), ('1','0'), ('0','2'), ('2','0'), ('0','3'),('3','0')]
    graph = Graph(nodes, edges, para)
    res = graph.printAllPaths('1', '2', 0)
    print(f"res {res}")