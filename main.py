"""References:
https://colab.research.google.com/drive/1ejLc4LkrmjpbcRYC3W2xjfA0C0o1PWTp?usp=sharing#scrollTo=u5ZHJ1oq8Ucm
https://favtutor.com/blogs/breadth-first-search-python
"""
from heuristic import *
import matplotlib.pyplot as plt


class Node():
    def __init__(self, ele, pos):
        self.pre_node = []  # node truoc
        self.self_node = pos  # toa do cua node
        self.element = ele  # thuoc tinh node ('x', ' ', '+', 'S', 'E')
        self.total_cost = 1000000  # tong chi phi tu start den node nay
        self.self_cost = 1  # chi phi khi di chuyen den node nay
        self.neighbor_node = []  # node lan can co the di chuyen toi

    def is_path(self):
        if self.element == 'x':
            return False
        else:
            return True


class Map():
    def __init__(self):
        self.matrix = []
        self.start_node = None
        self.end_node = None  # lối ra
        self.bonus_node = []

    def set_map(self):
        counter = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                # end node:
                if self.matrix[i][j].element == ' ':
                    if i == 0 or j == 0 or i == len(self.matrix)-1 or j == len(self.matrix[0])-1:
                        self.end_node = self.matrix[i][j]
                # start node:
                elif self.matrix[i][j].element == 'S':
                    self.start_node = self.matrix[i][j]
                    self.matrix[i][j].total_cost = 0
                    self.matrix[i][j].self_cost = 0
                # bonus node:
                if counter < len(self.bonus_node):
                    for bn in self.bonus_node:
                        if bn[0] == i and bn[1] == j:
                            self.matrix[i][j].self_cost = bn[2]
                            counter += 1
                # check neighbor node:
                if self.matrix[i][j].is_path() and self.matrix[i][j] != self.end_node:
                    if self.matrix[i - 1][j].is_path():  # up
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i - 1][j])
                    if self.matrix[i + 1][j].is_path():  # down
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i + 1][j])
                    if self.matrix[i][j - 1].is_path():  # left
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i][j - 1])
                    if self.matrix[i][j + 1].is_path():  # right
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i][j + 1])

    def read_file(self, file_path):
        f = open(file_path, 'r')
        n_bonus_points = int(next(f)[:-1])
        bonus_points = []
        for i in range(n_bonus_points):
            x, y, reward = map(int, next(f)[:-1].split(' '))
            bonus_points.append((x, y, reward))

        text = f.read()
        matrix = [list(i) for i in text.splitlines()]
        for i in range(len(matrix)):
            row = []
            for j in range(len(matrix[0])):
                row.append(Node(matrix[i][j], (i, j)))
            self.matrix.append(row)
        f.close()
        self.bonus_node = bonus_points
        self.set_map()
        print()

    def print_matrix(self):
        for i in self.matrix:
            for j in i:
                print(j.element, end='')
            print()

    def back_tracking_route(self, route, node, total_cost=None):
        if total_cost:
            cost = total_cost
        else:
            cost = node.self_cost
        while node.pre_node:
            pre = node.pre_node.pop()
            route.append(pre.self_node)
            if total_cost is None:
                cost += pre.self_cost
            node = pre
        return cost

    def DFS_Util(self, stack, goal, close):
        if len(stack) != 0:
            cur_node = stack.pop()
            close.append(cur_node)

            if cur_node is goal:
                return

            for node in cur_node.neighbor_node:
                if node not in close:
                    node.pre_node.append(cur_node)
                    stack.append(node)
                    self.DFS_Util(stack, goal, close)

    def DFS(self):
        stack = []
        close = []
        stack.append(self.start_node)
        close.append(self.start_node)
        self.DFS_Util(stack, self.end_node, close)
        route = [self.end_node.self_node]
        cost = self.back_tracking_route(route, self.end_node)
        return route, cost

    def BFS(self):
        queue = []
        route = []
        visited = []
        visited.append(self.start_node)
        queue.append(self.start_node)
        cost = 0

        while queue:
            node = queue.pop(0)
            if node == self.end_node:
                route.append(node.self_node)
                cost = self.back_tracking_route(route, node)
            else:
                for n in node.neighbor_node:
                    if n not in visited:
                        visited.append(n)
                        queue.append(n)
                        n.pre_node.append(node)
        return route, cost

    def UCS_Util(self, goal, explore, close):
        if not explore:
            return
        mini = explore[0]
        for i in explore:
            if i.total_cost < mini.total_cost:
                mini = i
        for i in mini.neighbor_node:
            if i not in close and mini.total_cost + i.self_cost < i.total_cost:
                i.total_cost = mini.total_cost + i.self_cost
                i.pre_node.append(mini)
                if i not in explore:
                    explore.append(i)
        if mini != goal:
            close.append(mini)
            explore.remove(mini)
            self.UCS_Util(goal, explore, close)
        else:
            return

    def UCS(self):
        explore = []
        explore.append(self.start_node)
        self.UCS_Util(self.end_node, explore, [])
        route = [self.end_node.self_node]
        cost = self.back_tracking_route(
            route, self.end_node, self.end_node.total_cost)
        return route, cost

    def GBFS(self):
        open = [(self.start_node, 0)]
        close = []

        while self.end_node not in close:
            if open:
                # get the mini node which having min cost
                mini = min(open, key=lambda node: node[1])
                open.remove(mini)
                cur_node = mini[0]
                close.append(mini[0])

                for node in cur_node.neighbor_node:
                    if node not in close:
                        cost = heuristic_1(self.end_node, node)
                        open.append((node, cost))
                        node.pre_node.append(cur_node)
            else:
                break

        route = [self.end_node.self_node]
        cost = self.back_tracking_route(route, self.end_node)
        return route, cost

    def Astar_Util(self, goal, explore, close):
        if not explore:
            return
        mini = explore[0]
        for i in explore:
            if i.total_cost + heuristic_1(goal, i) < mini.total_cost + heuristic_1(goal, mini):
                mini = i
        for i in mini.neighbor_node:
            if i not in close and mini.total_cost + i.self_cost < i.total_cost:
                i.total_cost = mini.total_cost + i.self_cost
                i.pre_node.append(mini)
                if i not in explore:
                    explore.append(i)
        if mini != goal:
            close.append(mini)
            explore.remove(mini)
            self.Astar_Util(goal, explore, close)
        else:
            return

    def Astar(self):
        explore = []
        explore.append(self.start_node)
        self.Astar_Util(self.end_node, explore, [])
        route = [self.end_node.self_node]
        cost = self.back_tracking_route(
            route, self.end_node, self.end_node.total_cost)
        return route, cost

    def visualize_maze(self, route):
        bonus = [bn for bn in self.bonus_node]
        start = self.start_node.self_node
        end = self.end_node.self_node

        # 1. Define walls and array of direction:
        walls = [(i, j) for i in range(len(self.matrix))
                 for j in range(len(self.matrix[0])) if self.matrix[i][j].element == 'x']

        if route:
            direction = []
            for i in range(1, len(route)):
                if route[i][0]-route[i-1][0] > 0:
                    direction.append('^')
                elif route[i][0]-route[i-1][0] < 0:
                    direction.append('v')
                elif route[i][1]-route[i-1][1] > 0:
                    direction.append('<')
                else:
                    direction.append('>')

            direction.pop(0)

        # 2. Drawing the map
        ax = plt.figure(dpi=100).add_subplot(111)

        for i in ['top', 'bottom', 'right', 'left']:
            ax.spines[i].set_visible(False)

        plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                    marker='X', s=100, color='black')

        plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                    marker='P', s=100, color='green')

        plt.scatter(start[1], -start[0], marker='*',
                    s=100, color='gold')

        if route:
            for i in range(len(route)-2):
                plt.scatter(route[i+1][1], -route[i+1][0],
                            marker=direction[i], color='silver')

        plt.text(end[1], -end[0], 'EXIT', color='red',
                 horizontalalignment='center',
                 verticalalignment='center')
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def write_file(self, file_path, route, cost):
        with open(file_path, 'w') as f:
            f.write(str(cost)) if route else f.write('NO')

    def reset_map(self):
        for row in self.matrix:
            for j in row:
                if j is self.start_node:
                    continue
                j.pre_node = []
                j.total_cost = 1000000


def main():
    m = Map()
    m.read_file('input.txt')
    route, cost = m.Astar()
    m.write_file('output1.txt', route, cost)  # 8
    m.reset_map()
    route, cost = m.UCS()
    m.write_file('output2.txt', route, cost)  # 8
    m.visualize_maze(route)


if __name__ == "__main__":
    main()
