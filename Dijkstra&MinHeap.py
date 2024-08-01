# ==========
# Problem to solve: A bear to escape the forest with the shortest possible time
# Solved by implementing Dijkstra with a MinHeap with some extra conditions that came with the assignment question
# Dijkstra implemented within the escape function and the MinHeap implementation could be found at the last section of the code


class TreeMap:
    """
    Class which represents a Forest, containing Trees.
    Each Tree may contain Roads.
    """

    def __init__(self, roads, solulus):
        """
        This initiliazes a TreeMap object

        Precondition: roads and solulus are lists of tuples
        Postcondition: self.adjacency_list contains all of the Trees and Roads based on roads & solulus input

        Input:
            roads: List of Road objects
            solulus: List of tuples representing solulu trees
        Return:
            None

        Time complexity: 
            Best case analysis: O(T+R), for each Road in roads we iterate through all Trees in adjacency_list 
            Worst case analysis: O(T+R), for each Road in roads we iterate through all Trees in adjacency_list 
        Space complexity: 
            Input space analysis: O(T), where T are the number of trees in the adjacency_list
            Aux space analysis: O(T), where T are the number of trees in the adjacency_list
        """

        #Finding the maximum number of trees by finding the highest Tree.id among all roads
        max = 0
        for i in range(len(roads)):
            if roads[i][0] > max:
                max = roads[i][0]
            if roads[i][1] > max:
                max = roads[i][1]
        #Storing so that it could be accessed
        self.max = max
        
        #Creating our adjacency_list with max+1 spaces
        self.adjacency_list = [None] * (max+1)

        for i in range(max+1):  #Creating a tree for each slot in adjacency_list
            if self.adjacency_list[i] == None:
                self.adjacency_list[i] = Tree(i)
        
        #Creating and adding roads to its respective Trees
        for i in range(len(roads)):    
            for j in range(len(self.adjacency_list)):
                if self.adjacency_list[j].id == roads[i][0]:
                    self.adjacency_list[j].add_road(Road(roads[i][0], roads[i][1], roads[i][2]))
                    
        # For each Tree object in seld.adjacency list that is a solulu
        # Set the solulu attributes belonging to the tree
        for i in range(len(solulus)):
            self.adjacency_list[solulus[i][0]].solulu = True
            self.adjacency_list[solulus[i][0]].claw_time = solulus[i][1]
            self.adjacency_list[solulus[i][0]].teleport_to = solulus[i][2]
        
        

           
   
    
    def escape(self, start, exits):
        """
        Finds the shortest time and route for a TreeMap with the given start and exits.
        Uses Dijkstra twice to find the shortest route.

        Precondition: start is a non-negative integer and exits is a list of non-negative integer/integers
        Postcondition: returns None (If no route) or a tuple (min, [return_route])

        Input:
            start: id of starting tree
            exits: id of exit trees
        Return:
            (total_time, route):
            total_time: is the answer
            route: is the answer

        Time complexity: 
            Best case analysis: O(R^2), where R is the number of roads in the TreeMap (Complexity of shortest_time() function)
            Worst case analysis: O(R^2), where R is the number of roads in the TreeMap (Complexity of shortest_time() function)
        Space complexity: 
            Input space analysis: O(T), where T are the number of trees
            Aux space analysis: O(T+R), T & R are the number of Trees and Roads in seld.adjacency_list
        """
      
        final_routes = []
        route = []

        #Initializing MinHeap and inserting
        self.adjacency_list[start].time = 0
        discovered = MinHeap(len(self.adjacency_list))
        for i in range(len(self.adjacency_list)):
            discovered.insert(self.adjacency_list[i].time, self.adjacency_list[i])

        #Updating the start tree with a start time of 0
        discovered.update(self.adjacency_list[start].time, self.adjacency_list[start])

        #Dijkstra
        while discovered.size > 0:
        
            current = discovered.serve() #Serve min item from the heap
            current.visited = True   #Time finalized for current
            current.discovered = True

            #route keeps track of the time and the tree
            route.append([current.time, current.id])

            # Perform edge relaxation on all of the roads connected to the tree
            for road in current.roads:
                v_int = road.v
                v = self.adjacency_list[v_int]

                # If tree has not been discovered
                if v.discovered == False:
                    v.discovered = True
                    v.time = current.time + road.w
                    v.previous = current
                    discovered.update(v.time, v)   #Updating Tree v in heap as v.time has changed

                #If tree time has not been finalized
                elif v.visited == False:
                    if v.time > current.time + road.w:
                        v.time = current.time + road.w
                        v.previous = current
                        discovered.update(v.time, v)   #Updating Tree v in heap as v.time changed

    

        #Adding the initial routes of each Tree into a list so that we can access them even after the reversal of the tree
        # initial_routes is a list containing lists of numbers(Tree Id's)
        initial_routes = []

        for items in route:
            item = self.adjacency_list[items[1]] #Access the Tree object in the adjacency list
            add_route = [item.id]  #Starting point of the route is the Tree's ID
            #Adding the Tree.id's taken in a route 
            while item.previous != None:
                add_route.append(item.previous.id)
                item = self.adjacency_list[item.previous.id]
            initial_routes.append(add_route) #Adds the route for each tree as a list into initial_routes

    

        reversed_route = []

        #Reversing the tree map (Flipping the TreeMap to find the shortest path from exit to solulus)
        reversed_treemap = self.reverse_treemap(self.adjacency_list, exits)

        reversed_treemap[-1].time = 0
        
        #Initializing MinHeap
        discovered2 = MinHeap(len(reversed_treemap))
        #Inserting 
        for i in range(len(reversed_treemap)):
            discovered2.insert(reversed_treemap[i].time, reversed_treemap[i])
        
        #Updating the start tree (The new Tree added when reversing)
        discovered2.update(reversed_treemap[-1].time, reversed_treemap[-1])

        #Dijkstra
        while discovered2.size > 0:
            current = discovered2.serve()   #Serve min item from the heap
            current.visited = True    #Time finalized for current
            current.discovered = True
            
            #Appending time, tree and tree id into reversed_route
            # We do this as reversed_route is used to retrieve the time and the route in our output
            reversed_route.append([current.time, current, current.id])  

            # Perform edge relaxation on all of the roads connected to the tree
            for road in current.roads:
                v_int = road.v
                v = self.adjacency_list[v_int]
              
                #If not discovered, set discovered to true and update the time of the Tree
                if v.discovered == False:                 
                    v.discovered = True    
                    v.time = current.time + road.w
                    v.previous = current
                  
                    discovered2.update(v.time, v)  #Updating Tree v in heap as v.time changed
                #If v.time is not finalized
                elif v.visited == False:
                    #If a shorter route is found, update time
                    if v.time > current.time + road.w:
                        v.time = current.time + road.w
                        v.previous = current
                        discovered2.update(v.time, v)   #Updating Tree v in heap with lesser duration, v.time
        

       #Function shortest_time is called to find the minimum time to exit the forest 
       #and the index of the minimum time among the final_routes
        min, index = self.shortest_time(route, reversed_route, exits, final_routes)

        # If min is float('inf'), it would mean there is no path out of the forest
        # So return None
        if min == float('inf'):
            return None

        # obtaining the route of the reversed treemap
        reverse_tree = final_routes[index][2]
        reverse_trees = [reverse_tree.id]
        #Accessing previous to find the route
        while reverse_tree.previous != None:
            reverse_trees.append(reverse_tree.previous.id)
            reverse_tree = reverse_tree.previous
        #Reverse tree route
        # reverse_trees = reverse_trees[:-1]

        # obtaining the route of the original treemap
        for i in range(len(initial_routes)):
            #Checks if the initial routes and reverse_tree Tree's match, if yes initial route is found
            if self.adjacency_list[initial_routes[i][0]] == reversed_treemap[reverse_trees[0]]:
                initial_path = initial_routes[i]
                initial_path.pop(0)
                initial_path.reverse() #Initial route obtained after reversing
                break

        reverse_trees.pop() #Removes last item from reverse_trees
        #Concatenate the routes to find the entire route
        return_route =  initial_path + reverse_trees
      

        return min, return_route
    


    def shortest_time(self, route, reversed_route, exits, final_routes):
        """
        Function description: 
        Finds the shortest time taken from the start to an exit using the information stored in routes
        and reversed_route
        :Input:
            route: Dijkstra output of original graph
            reversed_route: Dijkstra output of reversed graph
            exits: List of exit trees
            final_routes: The combined routes to exit the forest
        Precondition: All inputs are a list
        Postcondition: min is a non-negative integer or infinity and i is the index of min in the heap
        Return: The minimum time to exit forest and the index of the minimum time among the final_routes
        :Time complexity:
            Best and Worst-case: O(R^2) where R is the number of Roads in route
        :Time complexity analysis: O(R^2), iterating through reversed_route for each item in route

        :Space complexity:
        :Input space: O(T), where T is the length of route/ reversed_route/ exits & final_routes individually
        :Aux space: O(1), No additional space used

        """

        #Combining the two routes together into final_routes (With the following condition)
        #Provided that the id of the tree in the reversed graph is the same as the teleport_to of the tree in the original graph
        for i in range(len(route)):
            #Adds claw_time into the time if the tree is a solulu
            if self.adjacency_list[route[i][1]].solulu == True:
                    route[i][0] += self.adjacency_list[route[i][1]].claw_time
            #The condition for combining
            for j in range(len(reversed_route)):
                if reversed_route[j][1].id == self.adjacency_list[route[i][1]].teleport_to:
                    route[i].append(reversed_route[j][1])
                    final_routes.append(route[i])


        #Adding the time to the exit tree from start for all of the possible paths
        for i in range(len(final_routes)):
            if final_routes[i][2].id in exits:  #If the tree is an exit tree, then no need to add more time
                final_routes[i].append(final_routes[i][0])  #Appending into the third index of final_routes[i]
            else:
                final_routes[i].append(final_routes[i][0] + final_routes[i][2].time) #Appending into the third index of final_routes[i]
        
        #Proceeds to find the minimum time and the index of the minimum time among the final_routes
        min = float('inf')
        index = 0
        for i in range(len(final_routes)):
            if final_routes[i][3] < min:
                min = final_routes[i][3]
                index = i
        # Returns the minimum and the index that it could be found at
        return min, index
        

    
    
    def reverse_treemap(self, treemap, exits):
        """
        Function description: 
        Reverses treemap provided in the input (Reverses the direction of edges) and adds a new vertex
        which has an edge to all exit trees
        (Function also calls the reset method on all Trees to reset certain attributes to their default values)
        :Input:
            treemap: The treemap to be reversed
            exits:  List of exit trees
        Precondition: treemap is the adjacency list of the TreeMap before reversing
        Postcondition: new_adjacency_list is the reversed treemap where each road is reversed and an additional Tree
        Return: The reversed treemap
        :Time complexity:  
            Best & Worst case: O(T+R)
            :Time complexity analysis: Iterating through every road in a Tree for each Trees in adjacency_list
        :Space complexity: 
            Input space: O(T+R), where T & R are the Trees & Roads in adjacency_list
            Aux space: O(R), where R is the number of roads in treemap
        :Space complexity analysis: Adding all roads to a list new_roads
        """
        #List to keep track of the new roads (Reversed roads from the original treemap)
        new_roads = []
        new_adjacency_list = treemap  #Copying the treemap
        
        #Reverses the direction of all roads in each tree and adds them to new_roads
        for tree in new_adjacency_list:
            for i in range(len(tree.roads)):
                new_road = Road(tree.roads[i].v, tree.roads[i].u, tree.roads[i].w)
                new_roads.append(new_road)
    
        #Resets all the trees in the new_adjacency_list
        for tree in new_adjacency_list:
            tree.reset()

       #Adds the reversed roads to the correct tree in new_adjacency_list
        for tree in new_adjacency_list:
            for i in range(len(new_roads)):
                if tree.id == new_roads[i].u:
                    tree.add_road(new_roads[i])

        #Adds a new tree to the adjacency list with roads to all exit trees
        self.adjacency_list.append(Tree(self.max+1))
        for i in range(1, len(self.adjacency_list)):
            if self.adjacency_list[i].id in exits:
                self.adjacency_list[self.max+1].add_road(Road(self.max+1, self.adjacency_list[i].id, 0))

        return new_adjacency_list
    
class Tree:
    def __init__(self, id):
        """
        This init initializes a Tree object
        Input:
            id: An integer in which a Tree is identified by

        Pre-condition: id is a non-negative integer
        Post-condition: A Tree object with its default attributes
        Time complexity: O(1), all operations are constant
        Space complexity:
            Input Space: O(1), input is an integer
            Aux Space: O(1), all operations are constant (Assignation)

        """
        self.id = id
        self.roads = []
        self.solulu = False   #Indicates if a Tree is a solulu
        self.claw_time = 0    #claw_time if Tree is a solulu
        self.teleport_to = None   #Tree to teleport after clawing
        self.time = float('inf')
        self.visited = False
        self.discovered = False
        self.previous = None
       

    def add_road(self, road):
        """
        Adds a road to the Tree object's self.roads list.
        Input: 
            road: Road object to be added
        Pre-condition:
        Post-condition:
        Complexity(Space and time): O(1)  
        """
        self.roads.append(road)
    

    def reset(self):
        """
        Resets the selected Tree object's attributes to their default values
        Complexity(Space and time): O(1)
        Pre-condition: Existing Tree objects
        Post-condition: Listed attributes are to set to their default values
        Time-Complexity(Best and worst-case): O(1)  
        Space-Complexity(Input and aux): O(1)
        """
        self.time = float('inf')
        self.visited = False
        self.discovered = False
        self.previous = None
        self.roads = []


class Road:
    """
    A Road object (u, v, w) which links Tree u to Tree v with a weight of w
    """
    def __init__(self, u, v, w):
       """
       This init function initializes a Road object which is used to determine if there
       is a path from Tree u to Tree v
        Input:
            u: Tree id of origin
            v: Tree id of destination
            w: Weight of road (Time)

        Pre-condition: u, v and w are non-negative integers
        Post-condition: A Road object which links Tree u to Tree v with a weight of w
       Time complexity: O(1)
       Space complexity: O(1)
       """
       self.u = u
       self.v = v
       self.w = w


class MinHeap:
    def __init__(self, max_size):
        """
        This init initializes an instance of this MinHeap class
        Input:
            max_size: an integer representing the length of the MinHeap

        Pre-condition: max_size is a non-negative integer
        Post-condition: heap and index are lists of length (max_size +1)
        
        Time complexity: O(max_size), making a list of size (max_size +1)
        Space complexity: O(max_size), making a list of size (max_size +1)
        """
        self.heap = [None] * (max_size + 1)

         # self.indexes contains the position of Trees in the heap
         # Helps us keep track of the positions of the Trees in self.heap
         # Allows us to access items in the heap in O(1) time
        self.indexes = [None] * (max_size + 1)  
        self.size = 0

    def insert(self, time, tree):
        """
        Inserts the [time, tree] list into the correct position in the heap
    
        Input: 
            time: time taken to tree
            tree: Tree object

        Pre-condition: time is a non-negative integer and tree is a Tree object and self.size < len(self.heap)
        Post-condition: [time, tree] has been inserted in the heap at index self.size

        Time-Complexity: O(log n), where n is the number of items in the heap
        Space-Complexity: 
            Input space: O(1), inputs are constant space
            Aux space: O(1), no extra space required
        """
        if self.size >= len(self.heap):
            raise Exception("Heap is full")
        self.size += 1
        self.heap[self.size] = [time, tree]
        self.indexes[tree.id] = self.size
        self.rise(self.size)

    def size(self):
        """
        Returns the number of items in the heap
        Complexity (Space and Time): O(1)
        """
        return self.size
    
    def rise(self, i):
        """
        Rise element at index i to its correct position
        input:
            i: index of element to rise
        Pre-condition: i is a non-negative integer and 1 <= i <= self.length
        Post-condition: Item at index i in the heap is in its rightful position
        Complexity: 
            Time-Complexity: O(log n), where n is the number of items in the heap
            Space-Complexity:
                Input and Aux: O(1)
        """
        while i > 1 and self.heap[i][1].time < self.heap[i//2][1].time:
            self.swap_elements(i, i//2)
            i = i//2
    
    def swap_elements(self, i, j):
        """
        Swaps the position of elements in the heap and indexes
        input:
            i: index of first item to be swapped
            j: index of second item to be swapped
        Pre-condition: i and j is a non-negative integer
        Post-condition: Item at index i and j in the heap have swapped positions
        Complexity(Space & Time): O(1), assignation are constant operations
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.indexes[self.heap[i][1].id], self.indexes[self.heap[j][1].id] = i, j

    def sink(self, i):
        """
        Sink element at index i to its correct position
        input:
            i: index of item to sink
        Pre-condition: i is a non-negative integer and 1 <= i <= self.length
        Post-condition: Item at index i in the heap is in its rightful position
        Complexity: 
            Time-complexity: O(log n)
            Space-complexity:
                Input: O(1), input is a integer
                Space: O(1), no extra space needed
        """
        while 2*i <= self.size:
            j = 2*i
            if j < self.size and self.heap[j][1].time > self.heap[j+1][1].time:
                j += 1
            if not (j <= self.size and self.heap[j][1].time < self.heap[i][1].time):
                break
            self.swap_elements(i, j)
            i = j


    def serve(self):
        """
        Remove and return the minimum elemment from the heap
        Complexity: 
            Time-complexity: O(log n), where n is the number of items in the heap
            Space-Complexity: O(1), No extra space 
        """
        if self.size == 0:
            return None
        ret_obj = self.heap[1]
        self.swap_elements(1, self.size)
        self.size -= 1
        self.sink(1)
        return ret_obj[1]
    
    def update(self, time, tree):
        """
        Updates the values at the specified index of the heap and calls rise and sink on it
        Input: 
            time: time taken to go to tree
            tree: Tree object
        Pre-condition: time is a non-negative integer
        Post-condition: [time, tree] is in its right position in the heap
        Complexity:
            Time-complexity: O(log n), where n is the number of items in the heap
            Space-complexity:
                Input: O(1), Inputs are an integer and a Tree object
                Aux: O(1), No extra space needed

        """
        self.heap[self.indexes[tree.id]] = [time, tree]
        self.rise(self.indexes[tree.id])
        self.sink(self.indexes[tree.id])