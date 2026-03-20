import networkx as nx
import pandas as pd
import os

def build_graph():
    """Builds a directed graph from skill_graph.csv where edges represent prerequisites."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(script_dir, '..', 'data', 'skill_graph.csv')
    df = pd.read_csv(graph_path)
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row['from'], row['to'])
    return G

# Build graph once when module loads
G = build_graph()

def generate_pathway(current_skills, target_skills):
    """
    Generate a learning pathway based on current skills and target skills.

    Args:
        current_skills (dict): Skills the user already has (skill -> confidence).
        target_skills (dict): Skills required by the job (skill -> confidence).

    Returns:
        list of tuples: (skill, reason) in recommended learning order.
    """
    # Skills needed that are not already possessed
    needed = set(target_skills.keys()) - set(current_skills.keys())
    if not needed:
        return [("All required skills already acquired!", "You're ready!")]

    # Get all prerequisites for the needed skills
    all_prereqs = set()
    for skill in needed:
        if skill in G:
            # ancestors are prerequisites in a directed graph
            ancestors = nx.ancestors(G, skill)
            all_prereqs.update(ancestors)

    # Combine prerequisites and directly needed skills, remove already known
    to_learn = (all_prereqs | needed) - set(current_skills.keys())

    # Try to sort topologically if the graph is a DAG
    try:
        # Filter nodes that exist in the graph
        subgraph_nodes = [n for n in to_learn if n in G]
        order = list(nx.topological_sort(G.subgraph(subgraph_nodes)))
    except (nx.NetworkXUnfeasible, Exception):
        # Fallback: just list unsorted
        order = list(to_learn)

    # Generate reasoning for each step
    pathway = []
    for skill in order:
        if skill in needed:
            reason = "Directly required for the job."
        else:
            # Find which needed skill depends on this prerequisite
            dependent = next((s for s in needed if skill in nx.ancestors(G, s)), "a required skill")
            reason = f"Prerequisite for {dependent}."
        pathway.append((skill, reason))

    return pathway