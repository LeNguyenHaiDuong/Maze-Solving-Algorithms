#!/usr/bin/env python
# coding: utf-8

# - Class nodeel

# In[8]:


class node():
  def __init__(self, ele, pos):
    self.pre_node = [] #node truoc
    self.self_node = pos #toa do cua node
    self.element = ele #thuoc tinh node ('x', ' ', '+', 'S', 'E')
    self.total_cost = 1000000 #tong chi phi tu start den node nay
    self.self_cost = 1 #chi phi khi di chuyen den node nay
    self.neighbor_node = [] #node lan can co the di chuyen toi
  def is_path(self):
    if self.element == 'x':
        return False
    else:
        return True


# - Class Ma tran

# In[2]:


class matrix():
  def __init__(self):
    self.m = [] #ma tran
    self.start_node = None #node bat dau 'S'
    self.end_node = None #node ket thuc 'E'
    self.bonus_node = [] #node co diem thuong '+'
  def check_mat(self):
    for i in range(0, len(self.m)):
        for j in range(0, len(self.m[i])):
            if self.m[i][j].element == 'E':
                self.end_node = self.m[i][j]
            elif self.m[i][j].element == 'S':
                self.start_node = self.m[i][j]
                self.m[i][j].total_cost = 0
            #Chi phi cua node nay
            if self.m[i][j].element == 'S':
                self.m[i][j].self_cost = 0
            
            #Danh sach lien ket
            if self.m[i][j].is_path() and self.m[i][j].element != 'E': #luu cac dinh lan can co the di den
                if self.m[i - 1][j].is_path():
                    self.m[i][j].neighbor_node.append(self.m[i - 1][j])
                if self.m[i + 1][j].is_path():
                    self.m[i][j].neighbor_node.append(self.m[i + 1][j])
                if self.m[i][j - 1].is_path():
                    self.m[i][j].neighbor_node.append(self.m[i][j - 1])
                if self.m[i][j + 1].is_path():
                    self.m[i][j].neighbor_node.append(self.m[i][j + 1])
    
                    
  def read_file(self, file_path):
    fin = open(file_path, "r")
    data = fin.read()
    p = []
    row = 0
    column = 0
    for i in data:
        if i != '\n':
            p.append(node(i, [row, column]))
            column += 1
        else:
            self.m.append(p)
            p = []
            column = 0
            row += 1
    self.check_mat()
    return self
  
  def print_mat(self):
    for i in mat.m:
        for j in i:
            print(j.element, end = '')
        print()
  


# - Thuat toan UCS

# In[ ]:


def read_file(self, file_path = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text=f.read()
  matrix = [list(i) for i in text.splitlines()]
  for i in range(len(matrix)):
    row = []
    for j in range(len(matrix[0]):
        row.append(node(matrix[i][j], (i, j))
    self.m.append(row)
  f.close()
  self.bonus_node = bonus_points


# In[3]:


def UniformCostSearch(start, goal, explore):
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
        UniformCostSearch(start, goal, explore)
    else:
        return


# - Heuristic

# In[4]:


def heuristic_1(goal, now): #khoang cach theo toa do
    return abs(goal.self_node[0] - now.self_node[0]) + abs(goal.self_node[1] - now.self_node[1]) + now.self_cost

def heuristic_2(mat, now, next_node): #giai thuat bam tuong ben phai
    if now.self_node[0] == next_node.self_node[0]: # 2 node nam cung hang
        if now.self_node[1] > next_node.self_node[1]: #now nam ben phai cua next_node
            if mat[next_node.self_node[0] - 1][next_node.self_node[1]].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] - 1][next_node.self_node[1] + 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
        else: #now nam ben trai cua next_node
            if mat[next_node.self_node[0] + 1][next_node.self_node[1]].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] + 1][next_node.self_node[1] - 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
    else: #2 node nam cung cot
        if now.self_node[0] > next_node.self_node[0]: #now nam tren next_node
            if mat[next_node.self_node[0]][next_node.self_node[1] - 1].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] - 1][next_node.self_node[1] - 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)
        else: #now nam duoi next_node
            if mat[next_node.self_node[0]][next_node.self_node[1] + 1].element == 'x':
                return 0 + len(next_node.pre_node)
            elif mat[next_node.self_node[0] + 1][next_node.self_node[1] + 1].element == 'x':
                return 1 + len(next_node.pre_node)
            else:
                return 2 + len(next_node.pre_node)


# - Astar

# In[5]:


def Astar(start, goal, now):
    mini = now.neighbor_node[0]
    for i in now.neighbor_node:
        if heuristic_1(goal, i) < heuristic(goal, mini):
            mini = i
    
    if mini != goal:
        explore.remove(mini)
        UniformCostSearch(start, goal, explore)
    else:
        return


# - In ra ket qua

# In[6]:


def output_matrix(now, mat):
    if now == mat.start_node:
        now.element = 'o'
        return
    now.element = 'o'
    td = now.pre_node.pop(0)
    output_matrix(mat.m[td[0]][td[1]], mat)


# - Doc ma tran tu file

# In[7]:


file_path = "/mnt/d/mat1.txt"
mat = matrix().read_file(file_path)
mat.print_mat()

explore = []

explore.append(mat.start_node)

UniformCostSearch(mat.start_node, mat.end_node, explore)

output_matrix(mat.end_node, mat)

print()

mat.print_mat()

