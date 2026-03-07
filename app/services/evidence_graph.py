import networkx as nx


def build_skill_graph(skill_map):

    graph = nx.Graph()

    for skill, repos in skill_map.items():

        graph.add_node(skill, type="skill")

        for index, repo in enumerate(repos):

            repo_node = f"{skill}_repo_{index}"

            graph.add_node(repo_node, type="repo")

            graph.add_edge(skill, repo_node)

    return graph