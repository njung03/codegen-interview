import ast
import os
import json
import networkx as nx
import matplotlib.pyplot as plt


class ImportLoopDetector:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.dependency_graph = nx.DiGraph()

    def parse_python_files(self):
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        try:
                            tree = ast.parse(f.read(), filename=file)
                            self.extract_imports(tree, filepath)
                        except Exception as e:
                            print(f"Error parsing {filepath}: {e}")

    def extract_imports(self, tree, filepath):
        # Extract just the filename
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Extracting just the module name (filename)
                    module_name = node.module

                    self.dependency_graph.add_edge(filepath, module_name)
            elif isinstance(node, ast.ImportFrom):
                # Extracting just the module name (filename)
                module_name = node.module
                module_path = os.path.join(
                    self.root_dir, module_name.replace(".", os.sep) + ".py"
                )
                if os.path.exists(module_path):
                    self.dependency_graph.add_edge(filepath, module_path)

    def detect_import_loops(self):
        loops = list(nx.simple_cycles(self.dependency_graph))
        return loops

    def output_loop_information(self):
        loops = self.detect_import_loops()
        loop_info = {"loops": loops}
        with open("import_loops.json", "w") as f:
            json.dump(loop_info, f, indent=4)

    def visualize_dependency_graph(self):
        plt.figure(figsize=(10, 8))  # Adjust figure size for better readability

        # Define node and edge colors
        node_color = "skyblue"
        edge_color = "gray"

        # Define node size
        node_size = 300

        # Define edge width
        edge_width = 1.5

        # Use spring layout for better node positioning
        pos = nx.spring_layout(self.dependency_graph)

        # Draw nodes and edges
        nx.draw_networkx_nodes(
            self.dependency_graph, pos, node_color=node_color, node_size=node_size
        )
        nx.draw_networkx_edges(
            self.dependency_graph, pos, edge_color=edge_color, width=edge_width
        )

        # Add node labels
        nx.draw_networkx_labels(
            self.dependency_graph, pos, font_size=10, font_family="sans-serif"
        )

        # Remove axis
        plt.axis("off")

        # Show plot
        plt.show()

    def resolve_import_loops(self):
        # Implement codemod solution here
        pass


if __name__ == "__main__":
    detector = ImportLoopDetector("path/to/your/code/repository")
    detector.parse_python_files()
    detector.output_loop_information()
    detector.visualize_dependency_graph()
    detector.resolve_import_loops()
