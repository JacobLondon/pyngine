from typing import Callable, Any
import heapq
import math

# Use a prio queue instead of normal if node count is greater than this
PRIO_SIZE_THRESHOLD = 500_000

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def clear(self):
        self.queue.clear()
    def __bool__(self):
        return bool(self.queue)
    def push(self, ele: Any):
        heapq.heappush(self.queue, ele)
    def pop(self) -> Any:
        return heapq.heappop(self.queue)
    def front(self):
        return self.queue[0]

class Queue(list):
    def push(self, ele: Any):
        self.append(ele)
    def pop(self):
        return list.pop(self, 0)
    def front(self):
        return list.__getitem__(self, 0)

class Node:
    def __init__(self):
        self.global_goal: float = 0
        self.local_goal: float = 0
        self.x: int = 0
        self.y: int = 0
        self.obstacle: bool = False
        self.visited: bool = False
        self.neighbors: list['Node'] = list()
        self.parent: 'Node' = None

    def distance(self, other) -> float:
        return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )

    def add(self, neighbor):
        self.neighbors.append(neighbor)

    def __lt__(self, other):
        return self.global_goal < other.global_goal

class Astar:
    def __init__(self, width: int, height: int, is_obstacle: Callable[[int, int], bool]):
        self.width = width
        self.height = height
        self.is_obstacle_func = is_obstacle

        self.nodes: list[list[Node]] = [[Node() for _ in range(self.width)] for _ in range(self.height)]
        self.untested_queue: list[Node] = Queue() if self.width*self.height < PRIO_SIZE_THRESHOLD else PriorityQueue()

        # Connect all the nodes to each other as neighbors
        for i in range(height):
            for j in range(width):
                noderef: Node = self.nodes[i][j]
                noderef.y = i
                noderef.x = j

                # Only connect neighbors who are in bounds
                if i > 0:             noderef.add(self.nodes[i - 1][j])
                if i < self.height-1: noderef.add(self.nodes[i + 1][j])
                if j > 0:             noderef.add(self.nodes[i][j - 1])
                if j < self.width-1:  noderef.add(self.nodes[i][j + 1])

    def _reset(self):
        # Reset the queue because we're starting fresh
        self.untested_queue.clear()

        # Reset all the nodes
        for i in range(self.height):
            for j in range(self.width):
                noderef: Node = self.nodes[i][j]
                noderef.obstacle = self.is_obstacle_func(j, i)
                noderef.parent = None
                noderef.visited = False
                noderef.global_goal = math.inf
                noderef.local_goal = math.inf

    def _solve(self, startx: int, starty: int, endx: int, endy: int):
        self._reset()

        # Where we are and where we're going
        start: Node = self.nodes[starty][startx]
        end:   Node = self.nodes[endy][endx]

        current: Node = start
        current.local_goal = 0.0
        current.global_goal = start.distance(end)
        self.untested_queue.push(current)

        # While there are nodes
        while self.untested_queue:

            # Remove visited nodes and exit the loop if we are done
            while self.untested_queue and self.untested_queue.front().visited:
                self.untested_queue.pop()
            if not self.untested_queue:
                break

            # Visit the first unvisited node in the queue
            current = self.untested_queue.pop()
            current.visited = True

            # Check if neighbors need work, if so add them to the queue
            for neighbor in current.neighbors:
                if not neighbor.visited and not neighbor.obstacle:
                    # Calculate goal distances based on the best possible goal
                    possible_goal = current.local_goal + current.distance(neighbor)
                    if possible_goal < neighbor.local_goal:
                        neighbor.parent = current           # Save the path
                        neighbor.local_goal = possible_goal # Save the best goal for this neighbor, will come back to later
                        neighbor.global_goal = neighbor.local_goal + neighbor.distance(end) # Save score to end

                    # Record a reference to the neighbor
                    self.untested_queue.push(neighbor)

        #for line in self.nodes:
        #    for node in line:
        #        assert isinstance(node, Node)
        #        print("%-3.0lf" % node.global_goal, end=' ')
        #    print()

    # Note that this solver does not include the start position in the result
    # @returns >1 on success with xs and ys filled. <= 0 on failure.
    def solve(self, startx: int, starty: int, endx: int, endy: int, xs: list[int], ys: list[int]) -> int:
        # Check for invalid input
        if startx < 0 or startx >= self.width:  return -1
        if starty < 0 or starty >= self.height: return -1
        if endx < 0   or endx   >= self.width:  return -1
        if endy < 0   or endy   >= self.height: return -1

        self._solve(startx, starty, endx, endy)

        # The generated solution creates a linked list from end->start.
        # We traverse backwards and record the solution for the user.

        count: int = 0
        noderef: Node = self.nodes[endy][endx]
        while noderef.parent is not None:
            xs.insert(0, noderef.x)
            ys.insert(0, noderef.y)
            count += 1
            noderef = noderef.parent

        return count

def _main():
    region = [
        "########",
        "#      #",
        "###### #",
        "#      #",
        "#  #####",
        "##     #",
        "#    ###",
        "########",
    ]
    region = [[char for char in line] for line in region]

    x1 = 1
    y1 = 1
    x2 = 1
    y2 = 6
    pathfinder = Astar(len(region[0]), len(region), lambda x, y: region[y][x] == '#')

    xs = []
    ys = []
    size = pathfinder.solve(x1, y1, x2, y2, xs, ys)

    if size <= 0: print("ERROR NO ROUTE")
    for line in region:
        for char in line:
            print(char, end='')
        print()

    print("=" * 8)
    for x, y in zip(xs, ys):
        region[y][x] = '*'

    for line in region:
        for char in line:
            print(char, end='')
        print()

if __name__ == '__main__':
    _main()
    #for _ in range(100000):
    #    _main()
