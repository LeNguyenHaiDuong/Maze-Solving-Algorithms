import math


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
        self.matrix = []  # ma tran
        self.start_node = None  # node bat dau 'S'
        self.end_node = None  # node ket thuc 'E'
        self.bonus_node = []  # node co diem thuong '+'

    def set_map(self):
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                if self.matrix[i][j].element == ' ' and (i % (len(self.matrix)-1) == 0 or j % (len(self.matrix[0])-1) == 0):
                    self.end_node = self.matrix[i][j]
                elif self.matrix[i][j].element == 'S':
                    self.start_node = self.matrix[i][j]
                    self.matrix[i][j].total_cost = 0
                # Chi phi cua node nay
                if self.matrix[i][j].element == 'S':
                    self.matrix[i][j].self_cost = 0

                # Danh sach lien ket
                # luu cac dinh lan can co the di den
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
        fin = open(file_path, "r")
        data = fin.read()
        p = []
        row = 0
        column = 0
        for i in data:
            if i != '\n':
                p.append(Node(i, [row, column]))
                column += 1
            else:
                self.matrix.append(p)
                p = []
                column = 0
                row += 1
        self.set_map()
        return self

    def read_file2(self, file_path):
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

# import stack_data
stack = []
m = Map()


def DFS(goal, close):
    if len(stack) != 0:
        cur_node = stack.pop()
        close.append(cur_node)

        if cur_node is goal:
            return

        for node in cur_node.neighbor_node:
            if node not in close:
                node.pre_node.append(cur_node.self_node)
                stack.append(node)
                DFS(goal, close)


def GreedySearch(start, goal):
    open = [(start, 0)]
    close = []

    while goal not in close:
        if open:
            mini = min(open, key = lambda node: node[1])
            open.remove(mini) 
            cur_node = mini[0]
            close.append(mini[0])  

            for node in cur_node.neighbor_node:
                cost = heuristic_3(node, goal)
                if node not in close:
                    open.append((node, cost))
                    node.pre_node.append(cur_node.self_node)

        else:
            print('Can not find any way!')
            break

def UCS(start, goal, explore):
    mini = explore[0]
    for i in explore:
        if i.total_cost < mini.total_cost:
            mini = i
    for i in mini.neighbor_node:
        if mini.total_cost + i.self_cost < i.total_cost:
            i.total_cost = mini.total_cost + i.self_cost
            i.pre_node.append(mini.self_node)
            if i.self_cost < 0:
                i.self_cost = 1
            if i not in explore:
                explore.append(i)
    if mini != goal:
        explore.remove(mini)
        UCS(start, goal, explore)
    else:
        return


def heuristic_1(goal, now):  # khoang cach theo toa do
    return abs(goal.self_node[0] - now.self_node[0]) + abs(goal.self_node[1] - now.self_node[1]) + now.self_cost


def heuristic_3(goal, now):
    return math.dist(now.self_node, goal.self_node)


def heuristic_2(mat, now, next_node):  # giai thuat bam tuong ben phai
    if now.self_node[0] == next_node.self_node[0]:  # 2 node nam cung hang
        if now.self_node[1] > next_node.self_node[1]:  # now nam ben phai cua next_node
            if mat[next_node.self_node[0] - 1][next_node.self_node[1]].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] - 1][next_node.self_node[1] + 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
        else:  # now nam ben trai cua next_node
            if mat[next_node.self_node[0] + 1][next_node.self_node[1]].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] + 1][next_node.self_node[1] - 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
    else:  # 2 node nam cung cot
        if now.self_node[0] > next_node.self_node[0]:  # now nam tren next_node
            if mat[next_node.self_node[0]][next_node.self_node[1] - 1].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] - 1][next_node.self_node[1] - 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
        else:  # now nam duoi next_node
            if mat[next_node.self_node[0]][next_node.self_node[1] + 1].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] + 1][next_node.self_node[1] + 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)


# - Astar
def Astar(start, goal, now):
    mini = now.neighbor_node[0]
    for i in now.neighbor_node:
        if heuristic_1(goal, i) < heuristic_1(goal, mini):
            mini = i

    if mini != goal:
        explore.remove(mini)
        UCS(start, goal, explore)
    else:
        return


def output_result(now, map):
    if now == map.start_node:
        now.element = 'o'
        return
    now.element = 'o'
    td = now.pre_node.pop()
    output_result(map.matrix[td[0]][td[1]], map)


explore = []

def main():
    # - In ra ket qua
    m.read_file2('input.txt')
    m.print_matrix()

    # explore.append(m.start_node)
    # UCS(m.start_node, m.end_node, explore)
    # output_result(m.end_node, m)

    print()
    # TEST THUAT TOAN DFS
    # stack.append(m.start_node)
    # close = []
    # close.append(m.start_node)
    # DFS(m.end_node, close)
    # output_result(m.end_node, m)

    # TEST THUAT TOAN GREEDY BEST FIRST SEARCH
    GreedySearch(m.start_node, m.end_node)
    output_result(m.end_node, m)

    m.print_matrix()


main()