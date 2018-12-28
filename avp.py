'''
with open('/work/avp_tree/graf.txt','r') as f:
    arr=f.readlines()
    gr = {}
    for i in arr:
        i = i.split('\n')[0].split(' ')
        gr[i[0]]=i[1:]
print(gr)
'''
#is it avp tree?
def is_it_avp_tree(tree):
	avp_tree = {}
	for key in tree.keys():
		left, right = tree[key][0], tree[key][1]
		razn = height_of_tree(tree, right) - height_of_tree(tree, left)
		avp_tree[key] = razn
	#print(avp_tree)
	for val in avp_tree.values():
		if abs(val) > 1:
			return False
	return True


#height of tree
def height_of_tree(tree, start):
	result = 1
	if start == None:
		return 0
	n_versh = tree[start]
	while True:
		nexxt = []
		for versh in n_versh:
			if versh != None:
				for i in tree[versh]:
					nexxt.append(i)
		if len(nexxt) != 0:
			result += 1
			n_versh = nexxt
		else:
			break
		#print(n_versh, result)
	return result

def find_node(tree, koren, key):
	while True:
		if koren == None:
			#print('no key in tree')
			return False
		elif int(key) == int(koren):
			#print('key is in tree')
			return True
		elif int(key) < int(koren):
			koren = tree[koren][0]
		elif int(key) > int(koren):
			koren = tree[koren][1]


def add_vertex(tree, koren, vertex):
	if find_node(tree, koren, vertex):
		print('vertex is already in tree')
		return False
	else:
		tree[vertex] = [None, None]
		while True:
			if int(vertex) < int(koren):
				if tree[koren][0] != None:
					koren = tree[koren][0]
				else:
					tree[koren][0] = vertex
					break
			elif int(vertex) > int(koren):
				if tree[koren][1] != None:
					koren = tree[koren][1]
				else:
					tree[koren][1] = vertex
					break
		return tree

def del_vertex(tree, koren, vertex):
	vertex_ierarhy = []
	for key in tree.keys():
		vertex_ierarhy.append(int(key))
	vertex_ierarhy.sort()
	next_vertex = str(vertex_ierarhy[vertex_ierarhy.index(int(vertex)) + 1])
	#print(next_vertex)

	if tree[vertex][0] == None:
		for key, val in tree.items():
			for index in range(len(val)):
				if val[index] == vertex:
					tree[key][index] = tree[vertex][1]
		tree.pop(vertex)
	elif tree[vertex][1] == None:
		for key, val in tree.items():
			for index in range(len(val)):
				if val[index] == vertex:
					tree[key][index] = tree[vertex][0]
		tree.pop(vertex)
	else:
		if tree[vertex][1] == next_vertex:
			tree[next_vertex][0] = tree[vertex][0]
			for key, val in tree.items():
				for index in range(len(val)):
					if val[index] == vertex:
						tree[key][index] = next_vertex
			tree.pop(vertex)
		else:
			for key, val in tree.items():
				for index in range(len(val)):
					if val[index] == next_vertex:
						tree[key][0] = tree[next_vertex][1]

			tree[next_vertex] = tree[vertex]
			tree.pop(vertex)
	return tree


def update_to_avl_tree(tree, koren):
	if is_it_avp_tree(tree):
		print('this tree is already avl')
		return tree
	else:
		avp_tree, ierarhy = {}, {}
		for key in tree.keys():
			left, right = tree[key][0], tree[key][1]
			razn = height_of_tree(tree, right) - height_of_tree(tree, left)
			avp_tree[key] = razn
		print(avp_tree)

		ierarhy[koren], next_v = 1, tree[koren]
		sch = 2
		while True:
			temp = []
			for i in next_v:
				ierarhy[i] = sch
			sch += 1
			for versh in next_v:
				for j in tree[versh]:
					if j != None:
						temp.append(j)
			next_v = temp
			if len(next_v) == 0:
				break
		print(ierarhy)
		sch = 0
		for key, val in avp_tree.items():
			if abs(val) > 1 and ierarhy[key] > sch:
				change_vert = key
				sch = ierarhy[key]
		print(change_vert)

		if avp_tree[change_vert] < 0:
			change_second_vert = tree[change_vert][0]
			for key, val in tree.items():
				for k in range(0, 2):
					if tree[key][k] == change_vert:
						tree[key][k] = change_second_vert
			tree[change_vert][0] = tree[change_second_vert][1]
			tree[change_second_vert][1] = change_vert
			return tree

		else:
			change_second_vert = tree[change_vert][1]
			for key, val in tree.items():
				for k in range(0, 2):
					if tree[key][k] == change_vert:
						tree[key][k] = change_second_vert
			tree[change_vert][1] = tree[change_second_vert][0]
			tree[change_second_vert][0] = change_vert
			return tree

def make_avl_tree(tree, koren):
	while True:
		if is_it_avp_tree(tree):
			return tree
		else:
			update_to_avl_tree(tree, koren)
#main==========================================


tree = {'10': ['7', '14'], '7': ['4', '9'], '14': ['12', '20'], '4':['2', None], 
'9':[None, None], '12':[None, '13'], '20':['17', '30'], '2':[None, None], '13':[None, None], 
'17':['16', '19'], '30':[None, None], '16':[None, None], '19':[None, None]}


#tree = {'10': ['7', '14'], '7': ['4', '9'], '14': ['12', '20'], '4':['2', None], '9':[None, None], '12':[None, '13'], '20':['17', '30'], '2':[None, None], '13':[None, None], '17':[None, None], '30':['31', '33'], '31': [None, None], '33': ['32', '40'], '32': [None, None], '40': [None, None]}
print(is_it_avp_tree(tree))
koren, key = '10', '13'
#print(find_node(tree, koren, key))
#tr = add_vertex(tree, koren, key)
##add_vertex(tree, koren, key)
#print(tr)
#print(is_it_avp_tree(tr))
print('===================================')
print(del_vertex(tree, koren, key))
print(is_it_avp_tree(tree))
print(update_to_avl_tree(tree, koren))
