
"""
Node class, Search class
Ship grids are stored as a 2D array, but are flipped vertically, and rotated 90 degrees cw
(It seemed easier to work with, but I could be wrong)
"""
class Node:
    """replace depth with num_mins"""
    def __init__(self,grid,depth,f,parent):
        self.grid=grid
        self.depth=depth
        self.f=f
        self.parent=parent

    """returns a list of children Nodes from current Node by selecting a column's container and moving it to any other spot"""
    """want branching factor = # columns"""
    def branch(self):
        valid_cols = self.get_valid_cols(self.grid)
        children = []
        for i in valid_cols:
            for j in range(len(self.grid)):
                temp = self.copy(self.grid)
                if(self.move_container(temp, i, j) != None):
                    child = Node(temp,self.depth+1, 0,self)
                    children.append(child)
                    
                    #print("after moving column ", i, " to column ", j, "\n")
                    #child.print_grid()
        return children

    """
    operators
    chooses valid columns to move, returns a list 
    """
    def get_valid_cols(self, temp_grid):
        valid_cols = []
        for x in range(len(temp_grid)):
            if(self.get_top_container(temp_grid,x) != None):
                valid_cols.append(x)
        return valid_cols

    """
    moves the container from the top of col1 -> top of col2
    returns None if there's nothing to move/column is full
    """
    def move_container(self,temp_grid,col1,col2):
        """pos = x,y coordinates"""
        pos1 = self.get_top_container(temp_grid,col1)
        if col1 == col2 or not pos1:
            return None
        try:
            pos2 = (col2, next(i for i in reversed(range(len(temp_grid[col2]))) if temp_grid[col2][i] == 0))
        except StopIteration:
            return
        if(col1 == col2 or not pos1 or not pos2):
            return
        else:
            """swaps positions"""
            temp_grid[pos2[0]][pos2[1]] = temp_grid[pos1[0]][pos1[1]]
            temp_grid[pos1[0]][pos1[1]] = 0
            return temp_grid

    """HELPER FUNCTIONS"""

    """    
    O(n)
    helper function to return coordinates of top container
    """
    def get_top_container(self,temp_grid,col):
        for y in range(len(temp_grid[col])):
            if temp_grid[col][y] != 0:
                """x,y"""
                return (col, y)
        return None

    """returns a copy of a grid"""
    def copy(self,root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp
    
    """
    print the grid in the correct viewing orientation
    """
    def print_grid(self):
        for x in range(len(self.grid)):
            print([row[x] for row in self.grid])
        print("\n")
        return



class Search:
    def __init__(self, size):
        self.size = size
        self.open=[]
        self.closed=[]

    """replace f to represent as total # of mins"""
    def f(self, node):
        return node.depth + self.h_balance(node)

        
    """heuristic function for balance"""
    def h_balance(self, node):
        return self.balance_score(node.grid)


    """heuristic function for load/unloading"""
    def h_loadoffload(self,begin,end):
        dif = 0
        for i in range(len(begin.grid)):
            for j in range(len(begin.grid[0])):
                if begin.grid[i][j] != end.grid[i][j]:
                    dif += 1
        return dif


    """
    returns weight difference between left/right side as a %
    for legal balance, should be >= 0.90
    """
    def balance_score(self, grid):
        num_left_col = int(len(grid)/2)
        left_sum = sum(grid[i][j] for i in range(num_left_col) for j in range(len(grid[0])))
        right_sum = sum(grid[i][j] for i in range(num_left_col, len(grid)) for j in range(len(grid[0])))
        
        #print(left_sum, right_sum)
        
        return min(left_sum, right_sum)/max(left_sum,right_sum)


    """just do text input for now"""
    """takes 2D array input"""
    """this is the search function"""


    def process(self, start, balance):
        begin = Node(start, 0, 0, None)
        self.open.append(begin)

        while self.open:
            cur = self.open.pop(0)
            self.closed.append(cur)
            if self.balance_score(cur.grid) >= balance:
                return cur 
            for child in cur.branch():
                if child in self.closed:
                    continue
                child.f = self.f(child)  
                if child not in self.open:
                    self.open.append(child)
            self.open.sort(key=lambda x: x.f)
        return None  
