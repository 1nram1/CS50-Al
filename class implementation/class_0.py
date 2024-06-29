class Node:
    def __init__(self,state,parent,action) -> None:
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self) -> None:
        self.Frontier = []
    def add(self,node):
        self.Frontier.append(node)
    def contains_state(self,state):
        return any(node.state == state for node in self.Frontier)
    def empty(self):
        return len(self.Frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.Frontier[-1]
            self.Frontier = self.Frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.Frontier[0]
            self.Frontier = self.Frontier[1:]
            return node

class Maze:
    def solve(self):
        self.number_explored = 0
        start = Node(state = self.start,parent = None,action = None)
        frontier = StackFrontier()
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")
            node = frontier.remove()
            self.number_explored += 1


            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
            self.explored.add(node.state)

            for action,state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state = state,parent = node,action = action)
                    frontier.add(child)
        

