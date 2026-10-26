import os
import sys
from collections import deque
# 。。。。。

class sortedcontainers:
	class SortedList:
		def __init__(self, iterable=None):
			"""初始化：空或从可迭代对象初始化（自动排序）"""
			self._data = []
			if iterable:
				self._data = sorted(iterable)

		def __len__(self):
			"""获取元素个数：len()"""
			return len(self._data)

		def __getitem__(self, idx):
			"""按索引取值：sl[idx]，支持切片"""
			return self._data[idx]

		def __setitem__(self, idx, value):
			"""按索引赋值（会破坏有序性，仅应急用）"""
			# 注意：直接赋值会打破有序，建议优先用add/remove
			self._data[idx] = value
			self._data.sort()  # 强制重排保证有序

		def __delitem__(self, idx):
			"""按索引删除：del sl[idx]"""
			del self._data[idx]

		def __contains__(self, value):
			"""判断元素是否存在：value in sl"""
			idx = self.bisect_left(value)
			return idx < len(self) and self._data[idx] == value

		def __iter__(self):
			"""迭代元素：for x in sl"""
			return iter(self._data)

		def __repr__(self):
			"""打印友好的字符串"""
			return f"SortedList({self._data})"

		def add(self, value):
			"""添加元素并保持有序（核心方法）"""
			idx = self.bisect_left(value)
			self._data.insert(idx, value)

		def remove(self, value):
			"""删除第一个匹配的元素（不存在抛ValueError）"""
			idx = self.bisect_left(value)
			if idx < len(self) and self._data[idx] == value:
				del self._data[idx]
			else:
				raise ValueError(f"{value} not in SortedList")

		def discard(self, value):
			"""删除第一个匹配的元素（不存在不报错）"""
			idx = self.bisect_left(value)
			if idx < len(self) and self._data[idx] == value:
				del self._data[idx]

		def bisect_left(self, value):
			"""找value的左插入位置：第一个≥value的索引"""
			left, right = 0, len(self._data)
			while left < right:
				mid = (left + right) // 2
				if self._data[mid] < value:
					left = mid + 1
				else:
					right = mid
			return left

		def bisect_right(self, value):
			"""找value的右插入位置：第一个>value的索引"""
			left, right = 0, len(self._data)
			while left < right:
				mid = (left + right) // 2
				if self._data[mid] <= value:
					left = mid + 1
				else:
					right = mid
			return left

		def index(self, value):
			"""找第一个匹配元素的索引（不存在抛ValueError）"""
			idx = self.bisect_left(value)
			if idx < len(self) and self._data[idx] == value:
				return idx
			raise ValueError(f"{value} is not in SortedList")

		def count(self, value):
			"""统计value出现的次数"""
			left = self.bisect_left(value)
			right = self.bisect_right(value)
			return right - left

		def peek_min(self):
			"""返回最小值（空抛IndexError）"""
			if not self._data:
				raise IndexError("peek_min on empty SortedList")
			return self._data[0]

		def peek_max(self):
			"""返回最大值（空抛IndexError）"""
			if not self._data:
				raise IndexError("peek_max on empty SortedList")
			return self._data[-1]

		def pop(self, idx=-1):
			"""删除并返回指定索引元素（默认最后一个，空抛IndexError）"""
			if not self._data:
				raise IndexError("pop from empty SortedList")
			return self._data.pop(idx)

		def pop_min(self):
			"""删除并返回最小值（空抛IndexError）"""
			return self.pop(0)

		def pop_max(self):
			"""删除并返回最大值（空抛IndexError）"""
			return self.pop()

		def clear(self):
			"""清空所有元素"""
			self._data.clear()

		def extend(self, iterable):
			"""批量添加元素并保持有序（比多次add高效）"""
			self._data.extend(iterable)
			self._data.sort()
	class SortedDict:
		def __init__(self, data=None):
			"""初始化：空或从字典/可迭代对象初始化"""
			self._keys = []    # 始终保持升序的键列表
			self._values = {}  # 键值映射
			if data:
				if isinstance(data, dict):
					data = data.items()
				# 批量插入并排序（避免多次二分）
				items = sorted(data, key=lambda x: x[0])
				for k, v in items:
					self._keys.append(k)
					self._values[k] = v

		def __setitem__(self, key, value):
			"""设置键值对：存在则更新，不存在则插入并保持有序"""
			if key in self._values:
				self._values[key] = value
				return
			# 二分找插入位置
			left, right = 0, len(self._keys)
			while left < right:
				mid = (left + right) // 2
				if self._keys[mid] < key:
					left = mid + 1
				else:
					right = mid
			self._keys.insert(left, key)
			self._values[key] = value

		def __getitem__(self, key):
			"""获取值：key不存在抛KeyError（同原生dict）"""
			return self._values[key]

		def __delitem__(self, key):
			"""删除键值对：key不存在抛KeyError"""
			if key not in self._values:
				raise KeyError(key)
			# 二分找位置并删除
			left, right = 0, len(self._keys)
			while left < right:
				mid = (left + right) // 2
				if self._keys[mid] == key:
					del self._keys[mid]
					del self._values[key]
					return
				elif self._keys[mid] < key:
					left = mid + 1
				else:
					right = mid
			raise KeyError(key)

		def __contains__(self, key):
			"""判断键是否存在：in操作"""
			return key in self._values

		def __len__(self):
			"""获取元素个数：len()"""
			return len(self._keys)

		def __iter__(self):
			"""迭代升序的键：for k in sdict"""
			return iter(self._keys)

		def keys(self):
			"""返回升序的键列表"""
			return list(self._keys)

		def values(self):
			"""返回按键升序排列的值列表"""
			return [self._values[k] for k in self._keys]

		def items(self):
			"""返回按键升序排列的(键,值)列表"""
			return [(k, self._values[k]) for k in self._keys]

		def clear(self):
			"""清空所有元素"""
			self._keys.clear()
			self._values.clear()

		def pop(self, key, default=None):
			"""删除并返回值：key不存在返回default（无default则抛KeyError）"""
			if key not in self._values:
				if default is None:
					raise KeyError(key)
				return default
			# 先删key再删value（复用__delitem__逻辑）
			val = self._values[key]
			del self[key]
			return val

		def get(self, key, default=None):
			"""获取值：key不存在返回default"""
			return self._values.get(key, default)

		def bisect_left(self, key):
			"""找key的插入位置（左边界），返回索引"""
			left, right = 0, len(self._keys)
			while left < right:
				mid = (left + right) // 2
				if self._keys[mid] < key:
					left = mid + 1
				else:
					right = mid
			return left

		def bisect_right(self, key):
			"""找key的插入位置（右边界），返回索引"""
			left, right = 0, len(self._keys)
			while left < right:
				mid = (left + right) // 2
				if self._keys[mid] <= key:
					left = mid + 1
				else:
					right = mid
			return left

		def peek_min(self):
			"""返回最小键值对（空则抛IndexError）"""
			if not self._keys:
				raise IndexError("peek_min on empty SortedDict")
			k = self._keys[0]
			return (k, self._values[k])

		def peek_max(self):
			"""返回最大键值对（空则抛IndexError）"""
			if not self._keys:
				raise IndexError("peek_max on empty SortedDict")
			k = self._keys[-1]
			return (k, self._values[k])

		def pop_min(self):
			"""删除并返回最小键值对（空则抛IndexError）"""
			if not self._keys:
				raise IndexError("pop_min on empty SortedDict")
			k = self._keys.pop(0)
			v = self._values.pop(k)
			return (k, v)

		def pop_max(self):
			"""删除并返回最大键值对（空则抛IndexError）"""
			if not self._keys:
				raise IndexError("pop_max on empty SortedDict")
			k = self._keys.pop()
			v = self._values.pop(k)
			return (k, v)

		def __repr__(self):
			"""打印友好的字符串"""
			items = ", ".join([f"{k}: {v}" for k, v in self.items()])
			return f"SortedDict({{{items}}})"


class networkx: # 无属性/无权重
	"""极简高性能版：无属性/无权重/匹配NX核心行为"""
	class Graph:
		def __init__(self, g=None):
			if g is not None:
				self._init_from_graph(g)
				return
			# 核心邻接表（无属性）
			self._adj = {}
			# O(1) 缓存（无冗余计算）
			self._node_count = 0
			self._edge_count = 0

			# 视图对象（属性/方法共用，仅初始化一次）
			self._nodes_view = self.NodesView(self)
			self._edges_view = self.EdgesView(self)
		def _init_from_graph(self, g):
			# 复制邻接表
			self._adj = {k: set(v) for k, v in g._adj.items()}
			# 复制计数
			self._node_count = g._node_count
			self._edge_count = g._edge_count
			# 视图对象（属性/方法共用，仅初始化一次）
			self._nodes_view = self.NodesView(self)
			self._edges_view = self.EdgesView(self)
		def __getitem__(self, node):
			return self._adj[node]

		# -------------------------- 核心增删（O(1) 复杂度） --------------------------
		def add_node(self, node):
			if node not in self._adj:
				self._adj[node] = set()
				self._node_count += 1

		def add_nodes_from(self, nodes):
			# 批量添加：一次遍历+批量计数（避免多次自增）
			new_nodes = set(nodes) - set(self._adj.keys())
			for node in new_nodes:
				self._adj[node] = set()
			self._node_count += len(new_nodes)

		def add_edge(self, u, v):
			# 无向边标准化：直接存 (min, max)，避免后续排序/集合转换
			self.add_node(u)
			self.add_node(v)
			if v in self._adj[u]: pass # 存在
			else:
				self._adj[u].add(v)
				self._adj[v].add(u)
				self._edge_count += 1

		def add_edges_from(self, edges):
			for u, v in edges:
				self.add_edge(u, v)

		def remove_node(self, node):
			# 遍历邻接节点（O(deg(node)) 复杂度，而非 O(E)）
			for neighbor in list(self._adj[node]):
				self._adj[neighbor].discard(node)
				self._edge_count -= 1
			del self._adj[node]
			self._node_count -= 1

		def remove_edge(self, u, v):
			self._adj[u].discard(v)
			self._adj[v].discard(u)
			self._edge_count -= 1

		# -------------------------- 视图类（极致轻量） --------------------------
		class NodesView:
			def __init__(self, graph):
				self._graph = graph

			def __len__(self):
				return self._graph._node_count  # O(1)

			def __iter__(self):
				return iter(self._graph._adj.keys())  # O(V) 原生迭代

			def __contains__(self, node):
				return node in self._graph._adj  # O(1)

			def __repr__(self):
				return f"NodesView({list(self)})"

			def __call__(self):
				return self

		class EdgesView:
			def __init__(self, graph):
				self._graph = graph

			def __len__(self):
				return self._graph._edge_count  # O(1)

			def __iter__(self):
				for u, u_adjs in self._graph._adj.items():
					for v in u_adjs:
						if u < v: yield u, v

			def __contains__(self, edge):
				# 标准化后判断（O(1)）
				return self._graph.has_edge(*edge)

			def __repr__(self):
				return f"EdgesView({list(self)})"

			def __call__(self):
				return self

		# -------------------------- 双特性（无性能损耗） --------------------------
		@property
		def nodes(self):
			return self._nodes_view

		@property
		def edges(self):
			return self._edges_view

		# -------------------------- 基础方法（O(1)/O(deg) 复杂度） --------------------------
		def number_of_nodes(self):
			return self._node_count  # O(1)

		def number_of_edges(self):
			return self._edge_count  # O(1)

		def __iter__(self):
			return iter(self._adj.keys())  # O(V) 原生迭代

		def __contains__(self, node):
			return node in self._adj  # O(1)

		def __len__(self):
			return self._node_count  # O(1)
		
		def neighbors(self, node):
			return self._adj[node]  # O(deg(node))

		def degree(self, node):
			return len(self._adj[node])  # O(1)

		def has_node(self, node):
			return node in self._adj  # O(1)

		def has_edge(self, u, v):
			if u not in self._adj: return False
			return v in self._adj[u]  # O(1)

		def clear(self):
			self._adj = {}
			self._node_count = 0
			self._edge_count = 0
			self._edges_cache = set()  # O(1) 重置

		def is_empty(self):
			return self._node_count == 0  # O(1)

		def copy(self):
			# 深拷贝：O(V+E)（原生NX也是O(V+E)）
			new_G = networkx.Graph()
			new_G._adj = {n: set(neighbors) for n, neighbors in self._adj.items()}
			new_G._node_count = self._node_count
			new_G._edge_count = self._edge_count
			new_G._edges_cache = set(self._edges_cache)
			return new_G

		def subgraph(self, nodes):
			# 性能优化：仅遍历子图节点的邻接边（O(V_sub + E_sub) 而非 O(E)）
			sub_G = networkx.Graph()
			valid_nodes = set(nodes) & set(self._adj.keys())
			if not valid_nodes:
				return sub_G
			# 批量添加子图节点
			sub_G.add_nodes_from(valid_nodes)
			# 仅遍历子图节点的邻接边（避免遍历所有边）
			for u in valid_nodes:
				for v in self._adj[u]:
					if v in valid_nodes and u <= v:  # 避免重复添加
						sub_G.add_edge(u, v)
			return sub_G

	# -------------------------- 连通分量（BFS 最优复杂度） --------------------------
	@staticmethod
	def connected_components(G):
		# BFS 复杂度 O(V+E)（原生NX也是此复杂度）
		visited = set()
		components = []
		for node in G:
			if node not in visited:
				component = []
				queue = [node]
				visited.add(node)
				while queue:
					current = queue.pop(0)
					component.append(current)
					for neighbor in G.neighbors(current):
						if neighbor not in visited:
							visited.add(neighbor)
							queue.append(neighbor)
				components.append(component)
		return components		
	def shortest_path(G, start_node, end_node): # 最短路径，无权, 找不到->NetworkXNoPath
		
		"""
		无权无向简单图中，找到两点间的最短路径（允许空路径：起始节点=目标节点）
		BFS实现：天然保证无权图最短路径，时间复杂度O(V+E)
		
		参数:
			G (nx.Graph): 输入的无权无向简单图（支持自环）
			start_node: 起始节点（需存在于图中）
			end_node: 目标节点（需存在于图中）
		
		返回:
			list/None: 最短路径列表；
					- 空路径（起始=目标）：[start_node]
					- 邻接路径：[start_node, end_node]（长度1）
					- 多跳路径：[start_node, n1, ..., end_node]（长度≥2）
					- 无可达路径：None
		"""
		# 2. 空路径场景：起始节点=目标节点，直接返回仅含自身的路径
		if start_node == end_node:
			return [start_node]
		
		# 3. BFS初始化：访问状态 + 父节点映射（回溯路径用）
		visited = set()
		parent = {}
		queue = deque([start_node]) # 准备加入
		visited.add(start_node)
		found = False  # 标记是否找到目标节点
		parent[start_node] = None
		
		# 4. BFS核心：逐层遍历，找到目标节点即终止（保证最短）
		while queue:
			curr_node = queue.popleft()
			# 遍历当前节点的所有邻接节点
			for neighbor in G.neighbors(curr_node):
				if neighbor not in visited:
					visited.add(neighbor)
					parent[neighbor] = curr_node
					queue.append(neighbor)
					# 命中目标节点：立即终止BFS
					if neighbor == end_node:
						# 6. 回溯路径：从目标节点倒推至起始节点，再反转
						path = []
						curr = end_node
						while curr is not None:
							path.append(curr)
							curr = parent[curr]
						return path[::-1]
		
		# 5. 无可达路径
		raise networkx.NetworkXNoPath
		
	class NetworkXNoPath(Exception):
		"""无路径异常"""
		pass
nx = networkx
Graph = nx.Graph

if "lib":
	class list_ext:
		def find_min_index(lst, key=None):
			"""
			查找列表中第一个最小值的索引
			
			参数：
				lst (iterable): 输入的可迭代对象（需包含数值型元素）
			
			返回：
				int: 第一个最小值的索引
			
			异常：
				TypeError: 输入非可迭代对象 / 元素非数值型
				ValueError: 输入为空列表
			"""
			# 处理空列表
			if len(lst) == 0:
				raise ValueError("输入列表不能为空")
			if key is None:
				
				# 查找最小值和第一个索引（一次遍历，效率最优）
				min_val = None
				min_idx = 0
				for idx, val in enumerate(lst):
					# 首次遍历初始化最小值
					if min_val is None:
						min_val = val
						min_idx = idx
					# 找到更小值则更新
					elif val < min_val:
						min_val = val
						min_idx = idx
			else:

				# 查找最小值和第一个索引（一次遍历，效率最优）
				min_val = None
				min_idx = 0
				for idx, val in enumerate(lst):
					# 首次遍历初始化最小值
					if min_val is None:
						min_val = key(val)
						min_idx = idx
					# 找到更小值则更新
					elif key(val) < min_val:
						min_val = key(val)
						min_idx = idx
			return min_idx
		def find_max_index(lst, key=None):
			"""
			查找列表中第一个最大值的索引

			参数：
				lst (iterable): 输入的可迭代对象（需包含数值型元素）

			返回：
				int: 第一个最大值的索引

			异常：
				TypeError: 输入非可迭代对象 / 元素非数值型
				ValueError: 输入为空列表
			"""
			# 处理空列表
			if len(lst) == 0:
				raise ValueError("输入列表不能为空")
			if key is None:

				# 查找最大值和第一个索引（一次遍历，效率最优）
				max_val = None
				max_idx = 0
				for idx, val in enumerate(lst):
					# 首次遍历初始化最大值
					if max_val is None:
						max_val = val
						max_idx = idx
					# 找到更大值则更新
					elif val > max_val:
						max_val = val
						max_idx = idx
			else:
				# 查找最大值和第一个索引（一次遍历，效率最优）
				max_val = None
				max_idx = 0
				for idx, val in enumerate(lst):
					# 首次遍历初始化最大值
					if max_val is None:
						max_val = key(val)
						max_idx = idx
					# 找到更大值则更新
					elif key(val) > max_val:
						max_val = key(val)
						max_idx = idx
			return max_idx

	def path_to_edges(path):
		"""
		将路径转换为边列表

		参数：
			path (list): 输入的路径，包含节点

		返回：
			list: 边列表，包含节点对
		"""
		return [(path[i], path[i+1]) for i in range(len(path)-1)]
	def paste_path(path1, path2):
		"""
		将两个路径拼接，返回拼接后的路径

		参数：
			path1 (list): 第一个路径，包含节点
			path2 (list): 第二个路径，包含节点

		返回：
			list: 拼接后的路径，包含节点
		"""
		return path1 + path2[1:]

	def edge_to_std(edge): # 排序
		u, v = edge
		if u < v: return edge
		else: return (v, u)
	def ring_to_edges(ring):
		if len(ring) <= 1: return []
		rt = []
		for i in range(len(ring)-1):
			rt.append((ring[i], ring[i+1]))
		rt.append((ring[-1], ring[0]))
		return rt
	def ring_to_key(ring:list): # -> tuple(std)
		return tuple(ring_to_std(ring))

	def ring_to_std(ring:list):
		"""说明
			以最小元开始，第二元素尽量小
			"""
		le = len(ring)
		start = list_ext.find_min_index(ring)
		left = ring[(start-1)%le]
		right = ring[(start+1)%le]
		if left < right:
			return list(reversed(ring[:start+1])) + list(reversed(ring[start+1:]))
		else:
			return ring[start:] + ring[:start]
		
	def get_2edge_connected_components_and_bridges(G):
		"""
		高效迭代版Tarjan：无向图2边连通分量+桥（桥不排序，极致性能）
		:param G: networkx无向图对象
		:return: (2边连通分量列表, 桥列表)
			- 2边连通分量列表：每个元素是节点集合（set）
			- 桥列表：边元组（u, v），u < v（无排序，按算法发现顺序）
		"""
		# 边界处理：空图/单节点图（极简逻辑）
		n_nodes = len(G)
		if n_nodes == 0:
			return [], []
		if n_nodes == 1:
			return [set(G.nodes())], []
		
		# 初始化核心变量（仅保留必要项，减少内存占用）
		index = 0
		node_index = {node: -1 for node in G.nodes()}
		node_low = {node: -1 for node in G.nodes()}
		parent = {node: None for node in G.nodes()}
		bridges = set()          # 用set去重，避免重复桥
		edge_stack = []          # 存储树边（标准化）
		edge_stack_set = set()   # 快速判断边是否在栈中（O(1)查询）
		components = []

		# 迭代版Tarjan核心逻辑（无冗余、高性能）
		for start_node in G.nodes():
			if node_index[start_node] != -1:
				continue
			
			# 栈元素：(当前节点u, 邻接节点迭代器, 是否开始处理邻接节点)
			stack = [(start_node, iter(G.neighbors(start_node)), False)]
			node_index[start_node] = index
			node_low[start_node] = index
			index += 1

			while stack:
				u, neighbors_iter, processed = stack[-1]
				
				if not processed:
					# 首次入栈：标记为已开始处理
					stack[-1] = (u, neighbors_iter, True)
				else:
					# 分步处理邻接节点（迭代器减少重复遍历）
					try:
						v = next(neighbors_iter)
						if v == parent[u]:
							continue  # 跳过父节点，避免回边误判
						
						if node_index[v] == -1:
							# 未访问的子节点：初始化+入栈
							parent[v] = u
							node_index[v] = index
							node_low[v] = index
							index += 1
							# 边标准化（仅一次）+ 入栈（双结构同步）
							edge = (u, v) if u < v else (v, u)
							edge_stack.append(edge)
							edge_stack_set.add(edge)
							stack.append((v, iter(G.neighbors(v)), False))
						elif node_index[v] < node_index[u]:
							# 回边：更新low值（O(1)查询是否在栈中）
							edge = (u, v) if u < v else (v, u)
							if edge not in edge_stack_set:
								edge_stack.append(edge)
								edge_stack_set.add(edge)
							if node_index[v] < node_low[u]:
								node_low[u] = node_index[v]
					except StopIteration:
						# 所有邻接节点处理完毕，回溯逻辑
						stack.pop()
						if stack:  # 非根节点：更新父节点low值+判定桥
							parent_u = stack[-1][0]
							# 仅当子节点low值更小，才更新父节点（减少min计算）
							if node_low[u] < node_low[parent_u]:
								node_low[parent_u] = node_low[u]
							# 判定桥：子节点无法到达父节点祖先（核心逻辑）
							if node_low[u] > node_index[parent_u]:
								bridge = (parent_u, u) if parent_u < u else (u, parent_u)
								bridges.add(bridge)
								# 弹出边栈直到桥边（生成2边连通分量）
								component = set()
								while edge_stack:
									top_edge = edge_stack.pop()
									edge_stack_set.remove(top_edge)
									if top_edge == bridge:
										break
									component.add(top_edge[0])
									component.add(top_edge[1])
								if component:
									components.append(component)
						else:
							# 根节点处理完毕：弹出剩余边栈生成最后一个分量
							if edge_stack:
								component = set()
								while edge_stack:
									top_edge = edge_stack.pop()
									edge_stack_set.remove(top_edge)
									component.add(top_edge[0])
									component.add(top_edge[1])
								if component:
									components.append(component)

		# 补充孤立节点（极简逻辑，减少循环）
		all_nodes = set(G.nodes())
		component_nodes = set().union(*components) if components else set()
		for node in all_nodes - component_nodes:
			components.append({node})

		# 桥直接转列表（不排序，保留发现顺序）
		bridge_list = list(bridges)
		
		return components, bridge_list

	def get_2edge_connected_components(G): # 2边连通分量和桥
		"""
		【对外暴露函数】仅返回无向图G的所有2边连通分量（简化调用）
		参数：
			G: nx.Graph，输入的无向图（可非连通）
		返回：
			components: 列表，每个元素是集合，代表一个2边连通分量的节点集合
		"""
		components, _ = get_2edge_connected_components_and_bridges(G)
		return components

	def basis_to_total_len(basis):
		rt = 0
		for ring in basis:
			rt += len(ring)
		return rt
	def find_shortest_path(G, u, v): # 找不到返回None
		try:
			return nx.shortest_path(G, u, v)
		except nx.NetworkXNoPath:
			return None
	def find_shortest_path_node_to_set_w(G, node, node_set):
		"""
		无权无向简单图中，找到单个节点到目标节点集的最短非空路径（路径长度≥1）
		支持自环场景：起始节点的自环（node-node）算作合法非空路径（长度1）
		BFS实现：优先匹配最短路径（自环 < 邻接节点 < 多跳节点）
		
		参数:
			G (nx.Graph): 输入的无权无向简单图（支持自环）
			node: 起始节点（需存在于图中）
			node_set (iterable): 目标节点集（如list/tuple/set）
		
		返回:
			list/None: 最短非空路径列表（长度≥1）；
					- 自环场景：[node, node]（长度1）
					- 邻接场景：[node, neighbor]（长度1）
					- 多跳场景：[node, n1, ..., target]（长度≥2）
					- 无有效非空路径时返回None
		"""
		if node in node_set: return [node]
		# 4. BFS初始化：访问状态 + 父节点映射（回溯路径用）
		visited = set()
		parent = {}
		to_add = deque([node])
		found_target = None

		parent[node] = None

		# 树中加入node
		visited.add(node)
		for neighbor in G.neighbors(node):
			parent[neighbor] = node
			to_add.append(neighbor)
		
		# 5. BFS核心：逐层遍历，找到第一个目标节点即终止（保证最短）
		while len(to_add) != 0:
			curr = to_add.popleft()
			# 遍历当前节点的所有邻接节点（含自环，但自环已提前处理）
			for neighbor in G.neighbors(curr):
				if neighbor in node_set:
					# 排除 0 -> 1 -> 0这样的2环
					if neighbor == node and parent[curr] == node: continue 
					found_target = neighbor
					break
				if neighbor not in visited:
					visited.add(neighbor)
					parent[neighbor] = curr
					to_add.append(neighbor)
			else: continue
			break
		
		# 6. 无可达目标节点（无有效非空路径）
		if found_target is None:
			return None
		
		# 7. 回溯路径：从目标节点倒推至起始节点，再反转（路径长度≥1）
		path = []
		while curr is not None:
			path.append(curr)
			curr = parent[curr]
		return path[::-1] + [found_target]

	def get_shortest_paths(G, u, v):
		"""
		求解nx.Graph类型的无权无向图中从u到v的所有最短路径（不依赖nx路径相关函数）
		优化点：移除全节点初始化，按需动态记录距离和前驱，大幅减少u/v距离近时的开销
		复杂度：时间O(V'+E')，空间O(V'+E')（V'=u/v最短路径涉及节点数，E'=相关边数）
		
		参数：
			G (nx.Graph): NetworkX无向无权简单图
			u: 起始节点（需存在于G中）
			v: 目标节点（需存在于G中）
		
		返回：
			list: 所有最短路径的列表，每个路径是节点组成的列表
				- u==v：返回 [[u]]
				- 无可达路径：返回空列表
				- 有最短路径：返回所有最短路径（如 [[u,1,3,v], [u,2,3,v]]）
		"""
		# 边界条件1：起始节点=目标节点
		if u == v:
			return [[u]]
		
		# ------------------- 第一步：BFS计算最短距离 + 前驱节点列表（优化版） -------------------
		# 初始化：仅记录已访问节点的距离和前驱（不再遍历所有节点）
		distance = {u: 0}  # 仅起点有初始距离
		predecessors = {}   # 空字典，按需添加
		queue = deque([u])
		
		found_v = False  # 标记是否找到目标节点v
		while queue and not found_v:
			curr_node = queue.popleft()
			
			# 遍历当前节点的所有邻接节点（适配nx.Graph的neighbors接口）
			for neighbor in G.neighbors(curr_node):
				# 情况1：邻接节点未访问过（首次发现，动态记录距离+前驱）
				if neighbor not in distance:
					distance[neighbor] = distance[curr_node] + 1
					predecessors[neighbor] = [curr_node]  # 动态添加前驱
					queue.append(neighbor)
					# 找到目标节点，标记后无需再处理更远节点
					if neighbor == v:
						found_v = True
				# 情况2：邻接节点已访问，且当前路径是最短路径（补充前驱）
				elif distance[neighbor] == distance[curr_node] + 1:
					predecessors[neighbor].append(curr_node)
		
		# 边界条件3：目标节点不可达（未被记录距离）
		if v not in distance:
			return []
		
		# ------------------- 第二步：回溯前驱节点生成所有最短路径 -------------------
		# 递归回溯函数（仅遍历最短路径涉及的节点）
		def backtrack(current_node):
			# 递归终止：回到起点，返回仅含起点的路径
			if current_node == u:
				return [[u]]
			# 遍历当前节点的所有前驱，递归生成路径
			paths = []
			for pred in predecessors.get(current_node, []):  # 兼容极端情况（理论不会触发）
				# 递归获取前驱到起点的所有最短路径
				pred_paths = backtrack(pred)
				# 将当前节点追加到每条路径末尾
				for path in pred_paths:
					paths.append(path + [current_node])
			return paths
		
		# 从目标节点v开始回溯，生成所有最短路径
		all_shortest_paths = backtrack(v)
		return all_shortest_paths

		# 1. 构建超大稀疏图（10000节点，20000边）
		large_G = nx.random_regular_graph(4, 10000)  # 4-正则稀疏图
		u, v = 0, 5  # u/v距离很近（仅几步）
		
		# 2. 测试优化后函数的耗时
		import time
		start = time.perf_counter()
		paths = get_shortest_paths(large_G, u, v)
		end = time.perf_counter()
		
		print(f"超大图（10000节点）u={u}到v={v}的最短路径：{paths}")
		print(f"优化后耗时：{end - start:.6f}s")  # 耗时极短，无全节点初始化开销
		
		# 3. 验证逻辑正确性（小图测试）
		small_G = nx.Graph()
		small_G.add_edges_from([(0,1), (0,2), (1,3), (2,3), (3,4), (1,4)])
		print("\n小图测试 - 多条最短路径：", get_shortest_paths(small_G, 0, 3))  # 输出 [[0,1,3], [0,2,3]]

def apply_mcb_T_on_t(get_mcb_T): # 找到所有2边连通分量
	"""
		处理连通性，找到所有2边连通分量
		"""
	def Rt(G):
		rt = []
		components = get_2edge_connected_components(G)
		if len(components) <= 1:
			return get_mcb_T(G)
		else:

			for component in components:
				sub = Graph(G.subgraph(component))
				rt += get_mcb_T(sub)
			return rt
	return Rt

def mcb_approx2_v1_gwT(G):
	"""人类给ai的提词(若原本没有，请作为注释放到函数头部。若原本有，提供了新版本，替换。否则请一字不改动地复制到输出中。)
		这个注释的下面是另一个类似格式的注释,题目是"ai给ai的提词"
			若不存在，请添加
			其中内容允许你修改，请精炼出你认为对你下次修改函数时有用的信息
		用tab缩进
		默认输出完整（要import,测试部分）
		当人类说输出核心时，代表（不要import,测试部分）
		弧：任意(>=0)多条边串联的路径
		环r基于图H的段落
			环r中的G-H边和G-H点的连通分量（开集，路径）
		输入nx.Graph 无权无向简单图 2边连通
		输出G的环基rings
		为每个边环r分配唯一标识id_ring, 用于去重
		ring始终保持list类型
		预期B=E-V+1
		B始终构成H的一个环基
		尽量做到线性复杂度
		用一个结构维护所有有效边环的H段数(动态排序)
			在H变化(增加点集，边集）时动态修改(只修改可能影响的,即新增的某个点和边属于边环r)
			用字典记录每个点和边所属的所有边环，动态修改时就不用遍历所有边环
		H变化时动态修改有效性：
			当r完全属于H时(段落数0）无效
		逻辑
			1.对所有边e，找到包含e的所有最小环，称作边环
			2.初始图H=单点 环基B=空集
			循环:
				找到一个与H相连边环r，r的段落数最小(>=1), len(r)尽量小
				若H在r上仅有1段
					H'=H+r B'=B+r
				若H在r上有多段
					对每一段弧pi, 找到一个环ri，ri=pi拼接qi, 其中qi全部位于H，ri是满足条件的环中最小的
					H'=H+r
					B'=B+r+{ri}-rmax (rmax是ri中最大的一个)
				直到B数量达到预期
		术语
			ering:边环
			ring<list>: 环,用点集表示，符合环中的顺序，(首尾不要重复)
		数学原理保证了B在达到预期时, 边环不会用完
		"""
	"""可能存在的问题
		非锐化，导致边环多余
		"""
	def get_min_rings_containing_edge(G, e):
		"""找包含边e的最小环（点序列，首尾不重复），返回list类型"""
		u, v = e
		# 暂时移除边e
		G.remove_edge(u, v)
		rt = []
		if 0:
			path = nx.shortest_path(G, u, v)
			rt.append(path)
		for path in get_shortest_paths(G, u, v):
			rt.append(path)
		assert len(rt) > 0
		# 恢复边e
		G.add_edge(u, v)
		return rt  # 保持list类型

	def get_segments(H, ring): # 与H无交返回False
		"""说明
			ring<list>: 首尾不重复
			环r基于图H的段落
				环r中的G-H边和G-H点的所有连通分量（开集，非环路径）
			"""
		"""逻辑
			依次遍历r中的元素（点或边）a
			若a在H中
				若a的一个已遍历相邻元素b也在H中
					将a归为b所在段落
				否则：
					为a创建一个新段落
			否则：继续

			在回到初始点时
				若初始点两端是2个不同段落
					合并段落
			合法的中间点代表相邻的边也合法
				
			"""

		"""实现
			遍历ring中的边
				合并相邻的合法边（中间点合法）
			"""
		
		segs = []
		growing_seg = None # 上一条边所属的seg, 若不存在为None, 暂未加入segs
		for u, v in ring_to_edges(ring):
			if growing_seg is None: # u 不合法 或 是环开头第一边
				if H.has_edge(u,v): # e不合法
					pass
				else: # e合法
					growing_seg = [u,v]
			else:
				if H.has_node(u): # v不合法
					# 断开
					segs.append(growing_seg)
					growing_seg = None
					if H.has_edge(u,v): # e不合法
						pass
					else: # e合法
						growing_seg = [u,v]
				else: # u合法且(u,v)合法，继续生长
					growing_seg.append(v)
		# 末尾边处理, v是起始/末尾点
		if growing_seg is not None:
			if H.has_node(v): # v不合法
				# 断开
				segs.append(growing_seg)
			else: # v合法,(v,v+)合法，需要拼接
				if len(segs) == 0: # 1个段落首尾相接覆盖整个环，游离态
					return False
				else:
					# 拼接
					segs[0] = paste_path(growing_seg, segs[0])
		return segs

	def main(G):
		"""变量
			erings: 所有边环，list类型
			node_to_eringids: {节点: [所属边环ID集合]} （冻结）
			edge_to_eringids: {标准化边: [所属边环ID集合]} （冻结）
			H: 动态维护的子图
			B: 最终输出的环基，所有元素都是list类型
			eid_segs_map: {边环ID: 当前段数} （全部）(游离为False, 失效为空)
			segnumLen_eids_map: [(段数,长度)] -> [边环ID集合] （动态维护，仅相邻且不包含边环，段数>0）（失效边环段数为0）
			
			"""
		V = len(G.nodes)
		E = len(G.edges)
		expected_B_size = E - V + 1
		SortedDict = sortedcontainers.SortedDict
		
		# -------------------------- 预处理：生成边环 + 分配唯一ID + 构建映射字典 --------------------------
		# 1. 生成所有边环（保持list类型，用元组临时去重）
		erings = []  # 存储list类型的边环
		keys = set()  # 用元组作为临时键去重
		edges = list(G.edges)
		for e in edges:
			e = edge_to_std(e)
			for ring in get_min_rings_containing_edge(G, e):
				# 生成临时键（元组）用于去重，环本身保持list
				key = ring_to_key(ring)
				if key not in keys:
					keys.add(key)
					erings.append(ring)  # 始终保持list类型
	
		# 3. 构建点/边到边环ID的映射（H更新时快速定位相关边环）
		node_to_eringids = {}  # {节点: [所属边环ID集合]} (冻结，失效的也不会影响效率）
		edge_to_eringids = {}  # {标准化边: [所属边环ID集合]} (冻结)
		for eid, ring in enumerate(erings):
			# 节点映射
			for node in ring:
				if node not in node_to_eringids:
					node_to_eringids[node] = set()
				node_to_eringids[node].add(eid)
			# 边映射（标准化为(u,v)且u<v，避免重复）
			ring_edges = ring_to_edges(ring)
			for e in ring_edges:
				e_std = edge_to_std(e)
				if e_std not in edge_to_eringids:
					edge_to_eringids[e_std] = set()
				edge_to_eringids[e_std].add(eid)
		
		# -------------------------- 初始化动态维护结构（线性复杂度核心） --------------------------
		H = nx.Graph()
		init_node = next(iter(G.nodes))
		H.add_node(init_node)
		B = []  # 最终输出的环基，所有元素都是list类型
		
		# 段数字典：缓存边环当前段数（键为边环ID）（活跃边环）
		eid_segs_map = {}
		# 各段数的边环
		segnumLen_eids_map = SortedDict() # [segnum,length] -> eids 相邻边环
		
		# 初始化堆和缓存字典
		for eid, ring in enumerate(erings):
			ring = erings[eid]
			segs = get_segments(H, ring)
			eid_segs_map[eid] = segs
			if segs is False: # 游离边环
				pass
			else: # 相邻边环（包括失效）
				seg_num = len(segs)
				if seg_num == 0: pass
				else: # 相邻且不被包含
					key = seg_num, len(ring)
					if key not in segnumLen_eids_map:
						segnumLen_eids_map[key] = set()
					segnumLen_eids_map[key].add(eid)

		# -------------------------- 循环构建环基 --------------------------
		while len(B) < expected_B_size:
			# 找到最优的边环(段数>0且最小)
			for key in segnumLen_eids_map.keys():
				segnum_r, len_r = key
				eids = segnumLen_eids_map[key]
				eid = next(iter(eids)) # 当前处理的环
				break
			
			r = erings[eid]
			segs = eid_segs_map[eid]

			if segnum_r == 1:
				# 情况1：H在r上仅1段 → 直接扩展H并添加r到B
				new_edges = ring_to_edges(r)
				B.append(r) # 复制避免后续修改影响B
				

			else:
				# 情况2：H在r上有多段 → 拼接弧生成ri，更新H和B
				ris = []  # 存储list类型的ri环
				new_edges = []
				for pi in segs:
					u = pi[0]
					v = pi[-1]
					qi = nx.shortest_path(H, v, u)  # qi完全在H内，list类型
					ri = pi[1:] + qi[1:]  # 拼接pi和qi（去重首尾），保持list类型
					ris.append(ri)
					new_edges.extend(path_to_edges(pi))
				max_index = list_ext.find_max_index(ris, key=len)
				ris.pop(max_index)

				B.append(r)
				B.extend(ris)

			# 向H添加新的边，计算新加入的点和边
			new_edges = [ edge_to_std(e) for e in new_edges]
			new_nodes = set()
			for u, v in new_edges:
				for node in u, v:
					if not H.has_node(node):
						new_nodes.add(node)
			H.add_edges_from(new_edges)

			# 更新相关数据 segnum
			related_eringids = set()
			for node in new_nodes:
				related_eringids.update(node_to_eringids[node])
			for e_std in new_edges:
				related_eringids.update(edge_to_eringids[e_std])
			for eid in related_eringids:
				ring = erings[eid]
				old_segs = eid_segs_map[eid]
				segs = get_segments(H, ring)
				# 清除原来的信息 (当ring原本是活跃中间环）
				if old_segs is False: pass
				elif len(old_segs) == 0: pass
				else: # 原本活跃
					old_key = len(old_segs), len(ring)
					segnumLen_eids_map[old_key].remove(eid)
					if len(segnumLen_eids_map[old_key]) == 0:
						del segnumLen_eids_map[old_key]
				# 添加新的信息
				eid_segs_map[eid] = segs
				if segs is False: pass # 游离
				elif len(segs) == 0: pass
				else: # 非游离
					key = len(segs), len(ring)
					if key not in segnumLen_eids_map:
						segnumLen_eids_map[key] = set()
					segnumLen_eids_map[key].add(eid)

		
		assert len(B) == expected_B_size, (len(B), expected_B_size)
		return B
	
	return main(G)
get_mcb_T = mcb_approx2_v1_gwT
def get_mcb_t(G):
	return apply_mcb_T_on_t(get_mcb_T)(G)

def main(input_file, output_file):
	G = Graph()
	with open(input_file, 'r') as f:
		lines = [line.strip() for line in f if line.strip()] # 已经处理空行
		for line in lines[1:]:
			str1, str2 = line.split()
			v1, v2 = int(str1), int(str2)
			G.add_edge(v1, v2)
	# 选手实现核心算法
	result = get_mcb_t(G)
	for ring in result:
		ring.append( ring[0] ) # 首尾重复

	# 输出
	with open(output_file, 'w') as f:
		f.write(f"{len(result)}\n")
		for cyc in result:
			k = len(cyc)
			f.write(f"{k} {' '.join(map(str, cyc))}\n")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python solution.py <input_file> <output_file>")
		sys.exit(1)
	output_dir = "./output"
	os.makedirs(output_dir, exist_ok=True)
	main(sys.argv[1], sys.argv[2])