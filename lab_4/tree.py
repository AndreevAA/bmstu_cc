from graphviz import Digraph
import html

class Tree:
    """
    Класс дерева.
    """
    def __init__(self, root_node):
        self.root_node = root_node
        self.tree = Digraph()
        self.tree.node_attr["shape"] = "plaintext"
        # self.tree.node_attr["color"] = "white"
        # self.tree.node_attr["style"] = "filled"
        # self.tree.node_attr["fontcolor"] = "black"
        # self.tree.graph_attr["bgcolor"] = "white"
        # self.tree.edge_attr["color"] = "#9370DB"
        # self.tree.edge_attr["style"] = "dashed"
        # self.tree.body = [
        #     'rankdir=LR',
        #     'label="\N{sparkles} Welcome to the Magical Graph \N{sparkles}"',
        #     'fontsize=20']
        self._add_node(root_node, parent_id="-1", node_id="root")

    def _create_parent_edge(self, parent_id, node_id):
        """
        Создает ребро между родительским и дочерним узлами в графе.
        """
        if parent_id != "-1":
            self.tree.edge(parent_id, node_id)

    def _add_child_nodes(self, node, parent_id, node_id):
        """
        Рекурсивно добавляет дочерние узлы к текущему узлу в графе.
        """
        for index, child in enumerate(node.children):
            child_node_id = f"{node_id}.{index}"
            self._add_node(child, parent_id=node_id, node_id=child_node_id)

    def _add_node_table(self, node_id, node_name, node_content_str):
        self.tree.node(node_id, f"""<
        <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
          <tr>
            <td colspan="3">{html.escape(node_name)}</td>
          </tr>
          <tr>
            <td colspan="3">{html.escape(node_content_str)}</td>
          </tr>
        </table>>""")


    def _add_node_name(self, node_id, node_name):
        self.tree.node(node_id, 
            f'''<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
              <TR>
                <TD COLSPAN="3">{html.escape(node_name)}</TD>
              </TR>
            </TABLE>>''')

    def _add_node(self, node, parent_id="-1", node_id="root"):
        """
        Добавляет узел к графу и вызывает методы для создания ребра с родительским узлом
        и добавления дочерних узлов.
        """
        node_name = f"Node: {node.name}"
        node_content = "Content: "
        for item in node.content:
            node_content += str(item)

        node_content_str = f'{node_content}' if node.content else ''

        if node_content_str != '':
            self._add_node_table(node_id, node_name, node_content_str)
        else:
            self._add_node_name(node_id, node_name)
        self._create_parent_edge(parent_id, node_id)
        self._add_child_nodes(node, parent_id, node_id)


    def render(self):
        """
        Отображает дерево в формате PNG.
        """
        self.tree.render("parse_tree", format="png", view=True)