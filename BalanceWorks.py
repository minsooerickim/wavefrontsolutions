"""
Node class, Search class
Ship grids are stored as a 2D array, but are flipped vertically, and rotated 90 degrees cw
(It seemed easier to work with, but I could be wrong)
"""

class Node:
    def __init__(self, grid, mins=0, f=0, parent=None, operation=None):
        self.grid = grid
        self.mins = mins
        self.f = f
        self.parent = parent
        self.operation = operation   #tuple of (i,j, time), moving from col i to col j

    """returns a list of children Nodes from current Node by selecting a column's container and moving it to any other spot"""
    def branch_balance(self):
        valid_cols = self.get_valid_cols(self.grid)
        children = []
        for i in valid_cols:
            for j in range(len(self.grid)):
                temp = self.copy(self.grid)
                move_operation = self.move_container(temp, i, j)
                if(move_operation != None):
                    child = Node(move_operation[0], self.mins+self.manhattan_distance(move_operation[0], move_operation[1], move_operation[2])-3, 0, self, (i,j))
                    children.append(child)
        return children

    def branch_loadoffload(self, dock):
        if all(all(cell != 0 for cell in row) for row in self.grid):
            print("Warning: The ship is fully loaded, cannot load more containers.")
            return
        children = []

        dock_index = 0  # Start from the first container in the dock list
        col = 0  # Start loading containers from column 0

        # Loop until all containers in the dock list have been attempted to load
        while dock_index < len(dock):
            container = dock[dock_index]
            temp_grid = self.copy(self.grid)
            pos = self.get_first_empty(temp_grid, col)

            if pos is not None:  # If there is an empty spot in the current column
                temp_grid[pos[0]][pos[1]] = container
                child = Node(temp_grid, self.mins+self.manhattan_distance(self.grid, pos, pos), 0, self)
                children.append(child)
                print(f"Loaded Container {container} to Col {col}. Time spent: {self.manhattan_distance(self.grid, pos, pos)} minutes\n")
                self.grid = temp_grid  # Update the grid state of the current node
                self.print_grid()
                dock_index += 1  # Move to the next container in the dock list
            else:  # The current column is full, try the next column
                col += 1
                if col >= len(self.grid[0]):  # If all columns are full
                    print("The ship is full, cannot load more containers.")
                    break  # Exit the loop

        if dock_index == len(dock):
            print("All containers have been successfully loaded.")

        return children
        
    def manhattan_distance(self, grid, pos1, pos2):
        return abs(pos1[0]+1) + abs(pos2[1]) + 3
    
    #load container into col on grid
    def load_container(self, grid, col, container):
        pos = self.get_first_empty(grid, col)
        if pos:
            grid[pos[0]][pos[1]] = container
            return grid
        return
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
    def move_container(self,grid,col1,col2):
        """pos = x,y coordinates"""
        if(col1 is col2):
            return
        pos1 = self.get_top_container(grid,col1)
        pos2 = self.get_first_empty(grid,col2)
        if pos1 and pos2:
            """swaps positions"""
            grid[pos2[0]][pos2[1]] = grid[pos1[0]][pos1[1]]
            grid[pos1[0]][pos1[1]] = 0
            return grid, pos1, pos2
        return

    def SIFT(self, grid):
        flat_grid = [item for sublist in grid for item in sublist if (item > 0)]
        #sort all containers by desc order in a 1D array
        sort_desc = sorted(flat_grid, reverse = True)
        #empty the ship (replace all non -1 values with 0)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != -1:
                    grid[i][j] = 0
        next_cols = self.SIFTcols(grid)
        for item in sort_desc:
            next_col = next_cols.pop()
            self.load_container(grid, next_col, item)
        print("State after SIFT: ")
        self.print_grid()
        
    #returns a list of columns to SIFT into
    #assumes input is an empty grid
    def SIFTcols(self, grid):
        cols = [] 
        cur_pos = int(len(grid)/2)-1, len(grid[0])-1
        while(cur_pos[1] >= 0):
            if(grid[cur_pos[0]][cur_pos[1]] != -1 and cur_pos[0] >= 0):
                #append left then right side
                cols.append(cur_pos[0])
                cols.append(len(grid)- 1 -cur_pos[0])
                cur_pos = cur_pos[0]-1, cur_pos[1]
            else:
                cur_pos = int(len(grid)/2)-1, cur_pos[1]-1
        return [item for item in reversed(cols)]

    """return coordinates of the top container in col, None if NAN(-1) or column is full"""
    def get_top_container(self,temp_grid,col):
        for y in range(len(temp_grid[col])):
            if temp_grid[col][y] != 0 and temp_grid[col][y] != -1:
                """x,y"""
                return (col, y)
        return None
    """return coordinates of first empty spot in col"""
    def get_first_empty(self, temp_grid, col):
        try:
            pos = (col, next(i for i in reversed(range(len(temp_grid[col]))) if temp_grid[col][i] == 0))
            return pos
        except:
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
        new_grid = []
        for x in range(len(self.grid[0])):
            new_grid.append([row[x] for row in self.grid])
        for row in new_grid:
            print("     ".join("{:2}".format(value) for value in row))
        return

    def unload_containers(self, unload_positions):
        if all(all(cell == 0 for cell in row) for row in self.grid):
            print("Warning: The ship is empty, no unloading necessary.")
            return
        print("Starting the unloading process")
        print("State before unloading:")
        self.print_grid()
        exit_position = (0, len(self.grid[0]) - 1)
        for position in unload_positions:
            i, j = position
            if self.grid[i][j] == 0:
                print(f"Unloading container at position ({i}, {j})\n")
                print("There is no container to unload at this location\n\n")
            elif i < len(self.grid) and j < len(self.grid[0]):
                print(f"Unloading container at position ({i}, {j})")
                time_spent = self.manhattan_distance(self.grid, (i, j), exit_position)
                print(f"Time spent: {time_spent} minutes")
                self.grid[i][j] = 0  
                self.print_grid()  
            else:
                print(f"Warning: Position ({i}, {j}) is out of the ship's grid bounds.")

        print("Unloading process completed")
        print("State after unloading:")
        self.print_grid() 



class Search:
    def __init__(self):
        self.open=[]
        self.closed=[]

    """replace f to represent as total # of mins"""
    def f(self, node):
        return node.mins + self.h_balance(node.grid)


    """heuristic function for balance"""
    def h_balance(self, grid):
        if(sum(1 for row in grid for value in row if (value != -1 and value != 0)) == 1):
            return 0
        num_left_col = int(len(grid)/2)
        left_sum = sum(grid[i][j] for i in range(num_left_col) for j in range(len(grid[0]))if grid[i][j] != -1)
        right_sum = sum(grid[i][j] for i in range(num_left_col, len(grid)) for j in range(len(grid[0]))if grid[i][j] != -1)
        if(left_sum == 0 and right_sum==0):
            return 0
        curr_balance_score = min(left_sum, right_sum)/max(left_sum,right_sum)
        balance_mass = (left_sum + right_sum)/2
        deficit = 0
        if(min(left_sum,right_sum == left_sum)):
            #left_sum is smaller, need to add from right side
            deficit = balance_mass - left_sum
            #get a list of right half's values sorted in descending order
            right_half = [((i,j), grid[i][j])for i in range(len(grid) // 2) for j in range(len(grid[0]))]
            right_sorted = sorted(right_half, key=lambda x: x[1], reverse=True)
            for i in right_sorted:
                if min(left_sum+i[1],right_sum-i[1])/max(left_sum+i[1],right_sum-i[1]) == 0:
                    return 0
                if min(left_sum+i[1],right_sum-i[1])/max(left_sum+i[1],right_sum-i[1]) >= curr_balance_score:
                    return self.dist_first_open(grid, i[0][0])
            #have to SIFT at this point
            return -1
        else:
            #right_sum is smaller, need to add from left side
            deficit = balance_mass - right_sum
            #get a list of left half's values sorted in descending order
            left_half = [((i,j), grid[i][j]) for i in range(len(grid) // 2, len(grid)) for j in range(len(grid[0]))]
            left_sorted = sorted(left_half, key = lambda x: x[1], reverse=True)
            for i in left_sorted:
                if min(left_sum-i[1],right_sum+i[1])/max(left_sum-i[1],right_sum+i[1]) == 0:
                    return 0
                if min(left_sum-i[1],right_sum+i[1])/max(left_sum-i[1],right_sum+i[1]) >= curr_balance_score:
                    return self.dist_first_open(grid, i[0][0])
            #have to SIFT at this point
            return -1
    
    """heuristic function for load/unloading"""
    def h_loadoffload(self,begin,end):
        dif = 0
        for i in range(len(begin.grid)):
            for j in range(len(begin.grid[0])):
                if begin.grid[i][j] != end.grid[i][j]:
                    dif += 1
        return dif

    def dist_first_open(self, grid, col):
        if(col > len(grid)/2):
            #left side
            for i in range(int(len(grid)/2)):
                if grid[i][0] == 0:
                    return abs(col-i)
            #doesn't account for case where it's impossible to move
            return None
        else:
            #right side
            for i in range((int(len(grid)/2))+1,len(grid)):
                if grid[i][0] == 0:
                    return abs(col-i)
            return None

    """
    returns weight difference between left/right side as a %
    for legal balance, should be >= 0.90
    """
    def balance_score(self, grid):
        if(sum(1 for row in grid for value in row if (value != -1 and value != 0)) == 1):
            return 1
        num_left_col = int(len(grid)/2)
        left_sum = sum(grid[i][j] for i in range(num_left_col) for j in range(len(grid[0])) if grid[i][j] != -1)
        right_sum = sum(grid[i][j] for i in range(num_left_col, len(grid)) for j in range(len(grid[0])) if grid[i][j] != -1)
        if(left_sum == 0 and right_sum == 0):
            return 1
        return (min(left_sum, right_sum)/max(left_sum,right_sum))


    """just do text input for now"""
    """takes 2D array input"""
    """this is the search function"""


    def process(self, start):
        self.open.append(start)
        while self.open:
            cur = self.open.pop(0)
            self.closed.append(cur)
            h_cur = self.h_balance(cur.grid)
            if self.balance_score(cur.grid) >= 0.9:
                print("Found a Balanced Configuration with a balance score of : ", self.balance_score(cur.grid))
                cur.print_grid()
                return cur 
            elif h_cur == -1:
                cur.grid = self.SIFT(cur.grid)
                cur.print_grid()
                return cur
            for child in cur.branch_balance():
                if child in self.closed:
                    continue
                child.f = self.f(child)
                if child not in self.open:
                    self.open.append(child)
            self.open.sort(key=lambda x: x.f)
        return None

    def print_path(self,final_node):
        cur = final_node
        stack = []
        while(cur.parent!= None):
            stack.append(cur)
            cur = cur.parent
        num_steps = len(stack)
        for i in range(num_steps):
            cur = stack.pop()
            print("Step ", i + 1, " of ", num_steps, ".")
            print("Move Ship Container from Column ", cur.operation[0]+1, " to Column ", cur.operation[1]+1, ".")
            print("Estimated time: ", cur.mins, " minutes.\n")
            cur.print_grid()
            next = input("Enter \"Next\" when finished with this step.\n")
            while(next != "Next"):
                next = input()
        return


arr_ship = [
    [0, 0, 0, 0, 3, 2, -1, -1],
    [0, 0, 0, 0, 0, 0, 5, -1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 4, 1, 1, 2, 2, 3, 2],
    [0, 0, 0, 0, 0, 0, 9, -1],
    [0, 0, 0, 0, 3, 2, -1, -1]
]

ShipCase3 = [
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,6,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,2,1,1,1,1,1,1],
    [1,2,1,1,1,1,1,1],
    [1,1,3,1,1,1,1,1],
    [1,1,1,4,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,5,1,1,1,1]
]
initial_node = Node(ShipCase3)

# Display the initial state of the ship and the dock
print("Initial State:")
initial_node.print_grid()

puz = Search()
goal = puz.process(initial_node)
puz.print_path(goal)