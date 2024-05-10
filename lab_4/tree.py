from graphviz import Digraph

class Tree:

    def __init__(self, root_node):
        self.root_node = root_node
        self.tree = Digraph()
        self.__add_node(root_node)

    def __add_node(self, node, parent_id = "-1", node_id = "root"):

        node_name = "node_name: " + root_node.name
        node_content = "node_content: "

        for _ in node.content:
            node_content += str(_)

        self.tree.node(node_id, 
            node_name + "\n" +
            node_content + )

        if parent_id != "-1":
            tree.edge(parent_id, node_id)

    def render(self):
        self.__get_all_tree()
        self.tree.render("parse_tree", format="png", view=True)

    def __get_all_tree(self):
        for _, child in enumerate(self.root_node.children):
            tmp_node_id = str(node_id + "." + str(_))
            self.__add_node(child, parent_id = node_id, node_id = tmp_node_id)
