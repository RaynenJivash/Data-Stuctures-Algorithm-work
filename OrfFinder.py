"""
Assignment 2 by Raynen Jivash Athirathan 32836791
"""


class Node:
    """
    This is a Node class which will be initalized/used in the SuffixTrie class
    """

    def __init__(self):
        """
        This init function initializes a Node. A Node has 2 attributes, one being self.link which is used 
        to refer to the other Nodes (if they exist) and the other being self.ids which 
        contain the starting indexes of suffixes in which this Node could be found in

        Precondition: No precondition
        Postcondition: The node has 2 lists

        Input: Does not take in any input
        Return: Does not return anything

        Time complexity: 
            Best case analysis: O(1), creating self.link and self.ids are constant operations
            Worst case analysis: O(1), creating self.link and self.ids are constant operations
        Space complexity: 
            Input space analysis: O(1), no input
            Aux space analysis: O(1), self.link is a fixed size and self.ids is empty
        """
        # index 0,1,2,3 = A,B,C,D in self.link
        self.link = [None] * 4
        # contains the index of suffixes
        self.ids = []

    def add_id(self, id):
        """
        add_id adds the integer passed in (id) into self.ids

        Precondition: id is a non-negative integer
        Postcondition: id is appended to self.ids

        Input: id to be appended into self.ids
        Return: None

        Time complexity: 
            Best case analysis:O(1), adding to a list is a constant operation
            Worst case analysis:O(1), adding to a list is a constant operation
        Space complexity: 
            Input space analysis:O(1), input is an integer
            Aux space analysis:O(1), does not require auxiliary space
        """
        self.ids.append(id)
    
        
class SuffixTrie:
    """
    This is a SuffixTrie class which contains all suffixes of the input genome starting from a root
    """

    def __init__(self, genome):
        """
        This init function initializes the SuffixTrie class, it takes the input genome and calls insert
        len(genome) number of times with start as an input. start is the starting index of the suffix being
        inserted. If genome was "AABB", start at 0 would represent "AABB". start at 1 would represent "ABB"
        and so on until the last letter of genome.

        Precondition: genome is a non-empty string
        Postcondition: A SuffixTrie has been initialized based on self.root and genome

        Input: genome = The string which the SuffixTrie class will be built on (The class would contain
                        all suffixes of genome)
        Return: None

        Time complexity: 
            Best and worst case analysis: O(N^2), complexity of insert is O(N) and insert is called N number of times
                                          which would mean complexity is O(N)*O(N) = O(N^2)
            
        Space complexity: 
            Input space analysis: O(N), where N is the length of genome
            Aux space analysis: O(N), where N is the length of genome (Complexity is based on aux space of insert)
        """
        # String that the suffix trie will be built on
        self.genome = genome
        # Root of the suffix trie
        self.root = Node()

        # start represents the starting index of the suffix we would like to insert (like a suffix id)
        # it is incremented in every iteration to ensure all suffixes are added
        start = 0
        for i in range(len(genome)):
            self.insert(start)
            start += 1

        

    
    def insert(self, suffix_index):
        """
        The insert function inserts suffixes of self.genome into the trie and adds suffix_index to the self.ids list 
        of each node being inserted or traversed through. It loops from suffix_index to the length of self.genome, 
        adding suffix_index to the self.ids lists of the Nodes being traversed through or the new Nodes being inserted

        Precondition: suffix_index is a non-negative integer
        Postcondition: suffix_index has been added to every Node visited or every new Node created

        Input: start = An integer which is used to determine the beginning index of the suffixes being inserted
        Return: Does not return anything

        Time complexity: 
            Best case analysis: O(N) where N is the length of self.genome
            Worst case analysis: O(N) where N is the length of self.genome
        Space complexity: 
            Input space analysis: O(1), suffix_index is an integer
            Aux space analysis: O(N), where N is the length of self.genome (An integer is added to a Node's list (Different Nodes) N number of times 
                                which would take O(N) space)
        """
        
        # begin from root
        current = self.root
        # go through the key 1 by 1
        for i in range(suffix_index, len(self.genome)):
            # calculate index
            # A = 1, B = 2, C = 3, D = 4 
            index = ord(self.genome[i]) - 65 
            # if path exists, add suffix_index to the Node and set current to current.link[index]
            if current.link[index] is not None:
                current.link[index].add_id(suffix_index)
                current = current.link[index]

            # if path doesn't exist       
            else:
                # create a new node
                current.link[index] = Node()
                current.link[index].add_id(suffix_index)   #Adding starting index id to self.ids
                # Set new current to current.link[index]
                current = current.link[index]
            
           
            

    def search(self, key):
        """
        The search function searches for a Node in the SuffixTrie based on the input (key) and returns
        the self.ids list of the Node that the query (key) points to if the query (key) does exist. If
        it does not however, search would return an empty list.

        Precondition: key is a non-empty string
        Postcondition: returns a list

        Input:
            start: key, the query which we would traverse through
        Return:
            Returns the self.ids list of the final Node traversed through or returns an empty list if
            the path of the query does not exist

        Time complexity: 
            Best case analysis: O(1) where the first letter of the key does not have a link (Does not exist)
            Worst case analysis: O(N) where N is the length of the key
        Space complexity: 
            Input space analysis: O(N), where N is the length of key
            Aux space analysis: O(1), does not need extra space
        """
        # begin from root
        current = self.root
       
        for char in key:
            # calculate index
            index = ord(char) - 65 
            # if path exists
            if current.link[index] is not None:
                # ret_list.append(current.id)
                current = current.link[index]
                # If first iteration hold the node
             
            # if path doesn't exist
            else:
                return []
            
        # Return self.ids of the last node traversed from the query
        return current.ids
        
        
          

class OrfFinder:
    """
    The OrfFinder class is initialized to obtain all substrings that start with a particular sequence and 
    end with a particular sequence on a string genome (genome would be the input to the __init__)
    """

    def __init__(self, genome):
        """
        This init function initializes the OrfFinder class with a given input (genome). The __init__ instantiates
        2 suffix tries, one built with genome (self.genome) and one built with the reverse of genome (self.genome_reverse)

        Precondition: genome is a non-empty string
        Postcondition: Two SuffixTrie's are instantiated (Using self.genome and self.genome_reverse)

        Input:
            genome: A non-empty string containing only uppercase [A-D], genome is the string which
                    we obtain our substrings from
        Return: None (Does not return anything)

        Time complexity: 
            Best case analysis: O(N^2), where N is the length of the genome
            Worst case analysis: O(N^2), where N is the length of the genome
        Space complexity: 
            Input space analysis: O(N), where N is the length of genome
            Aux space analysis: O(N^2), where N is the length of genome (O(N^2) is the space required for each suffix trie)
        """
        self.genome = genome
        # Reversing genome
        self.genome_reverse = ''.join(reversed(genome))
        
        self.suffix_trie = SuffixTrie(self.genome)  # Original SuffixTrie
        self.reverse_suffix_trie = SuffixTrie(self.genome_reverse) # Reversed SuffixTrie


    def find(self, start, end):
        """
        The find function returns all substrings of genome which have start as a prefix and
        end as a suffix. find calls the search function with start on self.suffix_trie and with
        end on self.reverse_suffix_trie to obtain the indexes in which both start and end could
        be found in the string genome. The indexes are then used to obtain the substrings which 
        match start and end.

        Precondition: start and end are non-empty strings
        Postcondition: returns a list

        Input:
            start: The prefix of the strings to be returned
            end: The suffix of the strings to be returned
        Return:
            return_list: A list containing all of the strings which have start as a prefix and 
                         end as a suffix (List may possibly be empty) 

        Time complexity: 
            Best and Worst case analysis: O(T+U+V), where T is the length of the string start, U is the length of the string
                                          end and V being the number of characters in the output list
        Space complexity: 
            Input space analysis: O(T+U), where T is the length of the start and U is the length of the end
            Aux space analysis: O(V), where V is the total number of characters in the return_list (Could be O(N^2)
                                in the worst-case and O(1) in the best-case)
        """
        # List containing strings to be returned
        return_list = [] 
        # Calling the search function to obtain the indexes in which start and end could be found
        starts = self.suffix_trie.search(start)
        ends = self.reverse_suffix_trie.search(''.join(reversed(end)))  # Finding for end in the reversed suffix trie

        # The indexes from ends could not be used directly as they are the indexes from the reversed genome string
        # To ensure that the right indexes are used, the length of the genome is subtracted by each index in ends
        # To obtain the correct index in the original genome string (Not the reversed string)
        final_ends = []
        for number in ends:
            final_ends.append(len(self.genome)-number)
        
        # Nested for loop to iterate through final_ends list for every index in starts
        # Checks if the length of the query is greater than the length of the string
        # If not, then the sliced string on self.genome with indexes and indexes2 is added to return_list
        for indexes in starts:
            for indexes2 in final_ends:
                if not ((len(start)+len(end)) > len(self.genome[indexes:indexes2])): # and not (indexes>ends[i]):
                    return_list.append(self.genome[indexes:indexes2])
        # returns the strings matched by start and end
        return return_list


