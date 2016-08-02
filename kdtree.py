#encoding=utf-8

import math
import numpy as np

data = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]

class KD_node(object):
	def __init__(self, point=None, split=None, LL=None, RR=None):
		"""
		point:数据点
		split:划分域
		LL,RR:结点的左右子节点
		"""
		self.point = point
		self.split = split
		self.left = LL
		self.right = RR

def createKDTree(root, data_list):
	"""
	root:当前数的根节点
	data_list:数据点的集合(无序)
	return:构造的KDTree的树根
	"""
	LEN = len(data_list)
	if LEN == 0:
		return
	#数据点的维度
	dimension = len(data_list[0])
	#方差
	max_var = 0
	#最后选择的划分域
	split = 0
	for i in range(dimension):
		ll = []
		for t in data_list:
			ll.append(t[i])
		var = computeVariance(ll)
		if var > max_var:
			max_var = var
			split = i
	#根据划分域的数据对数据点进行排序
	data.sort(key=lambda x: x[split])
	#选择下标为len/2的点作为分割点
	point = data_list[LEN/2]
	root = KD_node(point, split)
	root.left = createKDTree(root.left, data_list[0:(LEN/2)])
	root.right = createKDTree(root.right, data_list[(LEN/2 + 1):LEN])
	return root

def computeVariance(arrayList):
	"""
	arrayList:存放的数据点
	return:返回数据点的方差
	"""
	for ele in arrayList:
		ele = float(ele)
	LEN = len(arrayList)
	array = np.array(arrayList)
	sum1 = array.sum()
	array2 = array * array
	sum2 = array2.sum()
	mean = sum1 / LEN
	#D[x] = E[x^2] - (E[x])^2
	variance = sum2 / LEN - mean**2
	return variance

def findNN(root, query):
	"""
	root:KDTree的树根
	query:查询点
	return:返回距离data最近的点NN，同时返回最短距离min_dist
	"""
	#初始化为root的节点
	NN = root.point
	min_dist = computeDist(query, NN)
	nodeList = []
	temp_root = root
	##二分查找建立路径
	while temp_root:
		nodeList.append(temp_root)
		dd = computeDist(query, temp_root.point)
		if min_dist > dd:
			NN = temp_root.point
			min_dist = dd
		#当前节点的划分域
		ss = temp_root.split
		if query[ss] <= temp_root.point[ss]:
			temp_root = temp_root.left
		else:
			temp_root = temp_root.right
	##回溯查找
	while nodeList:
		#使用list模拟栈，后进先出
		back_point = nodeList.pop()
		ss = back_point.split
		print 'back.point = ', back_point.point
		##判断是否需要进入父节点的子空间进行搜索
		if abs(query[ss] - back_point.point[ss]) < min_dist:
			temp_root = back_point.right
		else:
			temp_root = back_point.left

		if temp_root:
			nodeList.append(temp_root)
			curDist = computeDist(query, temp_root.point)
			if min_dist > curDist:
				min_dist = curDist
				NN = temp_root.point
	return NN, min_dist

def computeDist(pt1, pt2):
	"""
	计算两个数据点的距离
	return:pt1和pt2之间的距离
	"""
	sum1 = 0.0
	for i in range(len(pt1)):
		sum1 += (pt1[i] - pt2[i])**2
	return math.sqrt(sum1)


def preorder(root):
	"""
	KDTree的前序遍历
	"""
	print root.point
	if root.left:
		preorder(root.left)
	if root.right:
		preorder(root.right)

def KNN(list1, query):
	min_dist = 9999.0
	NN = list1[0]
	for pt in list1:
		dist = computeDist(query, pt)
		if dist < min_dist:
			NN = pt
			min_dist = dist
	return NN, min_dist

root = KD_node()
t = createKDTree(root, data)
print t.point
print findNN(t,[2,4])
