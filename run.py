import argparse
from domains.wgc import WGCProblem
from search_core import bfs, ids

def format_state(state):
    return str(tuple('L' if pos == 0 else 'R' for pos in state))

def print_results(results, domain_name, algo_name):
    if results is None:
        print(f"Domain: {domain_name.upper()} | Algorithm: {algo_name.upper()}")
        print("No solution found.")
        return

    # Header
    print(f"Domain: {domain_name.upper()} | Algorithm: {algo_name.upper()}")
    
    # Metrics
    cost = results['cost']
    depth = len(results['path'])
    generated = results['nodes_generated']
    expanded = results['nodes_expanded']
    frontier_max = results['max_frontier_size']

    print(f"Solution cost: {cost} | Depth: {depth}")
    print(f"Nodes generated: {generated} | Nodes expanded: {expanded} | Max frontier: {frontier_max}")
    
    # Path 
    print("Path:")
    if not results['path']:
        print("  (Already at goal state)")
    else:
        for i, (from_state, action, to_state) in enumerate(results['path']):
            from_str = format_state(from_state)
            to_str = format_state(to_state)
            print(f"  {i+1}) {action:<14} {from_str} -> {to_str}")

def main():
    parser = argparse.ArgumentParser(description="Run uninformed search algorithms on problem domains.")
    parser.add_argument(
        '--domain', 
        type=str, 
        required=True,
        choices=['wgc', 'wgc-sheep'], 
        help="The problem domain to solve."
    )
    parser.add_argument(
        '--algo', 
        type=str, 
        required=True, 
        choices=['bfs', 'ids'], 
        help="The search algorithm to use."
    )
    args = parser.parse_args()

    problem = None
    if args.domain == 'wgc':
        problem = WGCProblem(instance='classic')
    
    elif args.domain == 'wgc-sheep':
        problem = WGCProblem(instance='sheep')

    search_algorithm = None
    if args.algo == 'bfs':
        search_algorithm = bfs
    elif args.algo == 'ids':
        search_algorithm = ids

    if problem and search_algorithm:
        print("-" * 70) 
        results = search_algorithm(problem)
        print_results(results, args.domain, args.algo)
        print("-" * 70)

if __name__ == "__main__":
    main()

