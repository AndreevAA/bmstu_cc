from typing import Any, Dict, List, Union
import uuid

class NodeVisualizer:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.edges: List['NodeVisualizer'] = []
        self.metadata: Dict[str, Union[int, str]] = {
            'id': str(uuid.uuid4()),
            'start': -1,
            'end': -1
        }

    def connect(self, other: 'NodeVisualizer', start: int = -1, end: int = -1) -> None:
        self.edges.append(other)
        other.metadata['start'] = start
        other.metadata['end'] = end

    def visualize(self, graph: Any = None, parent_id: str = '') -> Any:
        if graph is None:
            from graphviz import Digraph
            graph = Digraph()
            graph.node_attr.update(shape='box')

        node_id = self.metadata['id']
        graph.node(node_id, f'{self.value}\n{self.metadata}')
        if parent_id:
            graph.edge(parent_id, node_id)

        for edge in self.edges:
            edge.visualize(graph, node_id)

        return graph
