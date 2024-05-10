class Node:

    def __init__(self, name = None, state_proxy = False):
        self.name = name
        self.children = list()
        self.content = list()
       	self.parent_id = -1
       	self.child_id = -1

    def __is_chilren_exist(self):
    	if self.children == None:
    		return False
    	elif len(self.children) == 0:
    		return False
    	return True

    def __update_connections(self, node):
		if not self.__is_chilren_exist():
            self.parent_id = node.parent_id
        self.child_id = node.child_id

    def __add_child_proxy(self, node):
    	for _ in node.children:
			self.add_child_node(_)

	def __add_child_narrow(self, node):
		if node != None:
			self.children.append(node)

    def __update_children(self, node):
    	if self.state_proxy:
    		self.__add_child_proxy(node)
    	else:
    		self.__add_child_narrow(node)

    def add_child_node(self, node):
        self.__update_connections(node)
        self.__update_children(node)

