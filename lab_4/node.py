import typing

class Node:
	name = ""
	children: list[typing.Type["Node"]]
	parent_id = -1
	child_id = -1
	content = None

	def __init__(self, name = None, state_proxy = False) -> None:
		self.state_proxy = state_proxy
		self.name = name
		self.children = []
		self.content = []
		pass

	def __is_chilren_exist(self):
		if self.children == None:
			return False
		elif len(self.children) == 0:
			return False
		return True

	def __update_connections(self, node):
		if not len(self.children):
			self.parent_id = node.parent_id
		self.child_id = node.child_id

	def __add_child_proxy(self, node):
		for _ in node.children:
			self.add_child_node(_)

	def __add_child_narrow(self, node):
		self.children.append(node)

	def __update_children(self, node):
		if node.name in ['<proxy>']:
			self.__add_child_proxy(node)
		else:
			self.__add_child_narrow(node)

	def add_child_node(self, node:typing.Type["Node"]):
		self.__update_connections(node)
		self.__update_children(node)


