# ref code:
# https://colab.research.google.com/drive/1ejLc4LkrmjpbcRYC3W2xjfA0C0o1PWTp?usp=sharing#scrollTo=u5ZHJ1oq8Ucm
# https://favtutor.com/blogs/breadth-first-search-python

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
                    if self.matrix[i - 1][j].is_path():
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i - 1][j])
                    if self.matrix[i + 1][j].is_path():
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i + 1][j])
                    if self.matrix[i][j - 1].is_path():
                        self.matrix[i][j].neighbor_node.append(
                            self.matrix[i][j - 1])
                    if self.matrix[i][j + 1].is_path():
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
                cost += node.self_cost
                # back-tracking:
                while node.pre_node:
                    pre = node.pre_node[0]
                    route.append(pre.self_node)
                    cost += pre.self_cost
                    node = pre
            else:
                for n in node.neighbor_node:
                    if n not in visited:
                        visited.append(n)
                        queue.append(n)
                        n.pre_node.append(node)
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
                    direction.append('^')  # ^
                elif route[i][0]-route[i-1][0] < 0:
                    direction.append('v')  # v
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


def main():
    m = Map()
    m.read_file('input2.txt')
    route, cost = m.BFS()
    m.write_file('output2.txt', route, cost)  # test
    m.visualize_maze(route)


main()
