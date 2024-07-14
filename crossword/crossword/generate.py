import sys
import queue

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        variables = set(self.domains.keys())
        for variable in variables:
            length = variable.length
            words = set(self.domains[variable])
            for word in words:
                if len(word) != length:
                    self.domains[variable].remove(word)


    def constraint(self,X,Y,i,j):
        if X[i] == Y[j]:
            return True
        else:
            return False

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        #if self.crossword.overlaps[x,y] :
        i, j = self.crossword.overlaps[x,y]
        old_domains = set(self.domains[x])
        y_domains = self.domains[y]
        for X in old_domains :
            if not any(self.constraint(X,Y,i,j) for Y in y_domains):
                self.domains[x].remove(X)
                revised = True
        return revised


    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == []:
            return True
        if  arcs == None:
            arcs = []
            for variable in self.domains.keys():
                for neighbor in self.crossword.neighbors(variable):
                    arcs.append((variable,neighbor))
        q = queue.Queue()
        for arc in arcs:
            q.put(arc)
        while not q.empty():
            x, y = q.get()
            if self.revise(x,y):
                if not self.domains[x] :
                    return False
                for Z in self.crossword.neighbors(x):
                    #个人认为  z != y这个条件不应该加，
                    # 因为（y,x)需要再次判断，因为（y,x)和 (x,y)不是一回事，并不对称
                    if Z != y:
                        q.put((Z,x))
        return True




    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.domains.keys())

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # if self.assignment_complete(assignment):
        #     words = list(assignment.values())
        #     return len(words) == len(set(words))
        # else:
        #     return False
        for variable, word in assignment.items():
            if variable.length != len(word):
                return False
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False
        for x in assignment.keys():
            for y in assignment.keys()  :
                if y in self.crossword.neighbors(x):
                    i, j = self.crossword.overlaps[x,y]
                    if assignment[x][i] != assignment[y][j]:
                        return False
        return True

                
        
        


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #计算出var的每个value 所rule out 别的var的value的个数，然后按照这个去排序就可以了
        def count_constraining(value):
            count = 0
            # 遍历与 `var` 有重叠的所有变量
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    # 查找具体的重叠位置
                    (i, j) = self.crossword.overlaps[var, neighbor]
                    # 计算在邻接变量的值域中与当前值不兼容的值的数量
                    # incompatible_values = sum(
                    #     1 for neighbor_val in self.crossword.domains[neighbor]
                    #     if neighbor_val[j] != value[i]
                    # )
                    incompatible_values = 0
                    for neighbor_value in self.domains[neighbor]:
                        if neighbor_value[j] != value[i]:
                            incompatible_values += 1
                    count += incompatible_values
            return count
        # 获取 `var` 的所有值域值，根据它们对邻居排除的选项数量进行排序
        return sorted(self.domains[var], key=count_constraining)
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = [var for var in self.crossword.variables if var not in assignment.keys()]
        unassigned_variables.sort(key=lambda var : len(self.domains[var]))
        min_domain_size = len(self.domains[unassigned_variables[0]])
        min_domain_vars = [var for var in unassigned_variables if len(self.domains[var]) == min_domain_size]
        if len(min_domain_vars) > 1:
            min_domain_vars.sort(key=lambda var: len(self.crossword.neighbors(var)),reverse=True)

        return min_domain_vars[0]
    

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable,assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                #添加了 inference 部分
                old_domains = {value : list(self.domains[value]) for value in self.domains}
                self.domains[variable] = [value]
                arc = []
                for neighbor in self.crossword.neighbors(variable):
                    arc.append((neighbor,variable))
                if self.ac3(arcs=arc):
                    result = self.backtrack(assignment)
                    if result != None:
                        return result
                self.domains = old_domains
            del assignment[value]
        return None
            


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
