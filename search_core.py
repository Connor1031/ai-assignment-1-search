import collections

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __repr__(self):
        return f"<Node {self.state}>"

def reconstruct_path(node: Node) -> list:
    #reconstruct the path from the goal node back to the start.
    path = []
    while node.parent:
        path.append((node.parent.state, node.action, node.state))
        node = node.parent
    path.reverse()
    return path

def bfs(problem):
    #Breadth-First Search
    nodes_generated = 0
    nodes_expanded = 0
    max_frontier_size = 0
    #search
    start_node = Node(problem.initial_state)
    nodes_generated += 1
    frontier = collections.deque([start_node])
    explored = {start_node.state}

    if problem.is_goal(start_node.state):
        return {
            "path": [],
            "cost": 0,
            "nodes_generated": nodes_generated,
            "nodes_expanded": nodes_expanded,
            "max_frontier_size": max_frontier_size
        }
        
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        node = frontier.popleft()
        nodes_expanded += 1

        for action in problem.get_actions(node.state):
            child_state = problem.get_result(node.state, action)
            
            if child_state not in explored:
                child_node = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    cost=problem.path_cost(node.cost, node.state, action, child_state)
                )
                nodes_generated += 1

                if problem.is_goal(child_node.state):
                    path = reconstruct_path(child_node)
                    return {
                        "path": path,
                        "cost": child_node.cost,
                        "nodes_generated": nodes_generated,
                        "nodes_expanded": nodes_expanded,
                        "max_frontier_size": max_frontier_size
                    }
                frontier.append(child_node)
                explored.add(child_state)
    return None #no solution found

def ids(problem):
    #Iterative-Deepening Search
    total_nodes_generated = 0
    total_nodes_expanded = 0
    
    for depth in range(100): # limit to avoid infinite loops
        result = dls(problem, depth)
        total_nodes_generated += result["nodes_generated"]
        total_nodes_expanded += result["nodes_expanded"]
        
        if result["solution"] is not None:
            path = reconstruct_path(result["solution"])
            return {
                "path": path,
                "cost": result["solution"].cost,
                "nodes_generated": total_nodes_generated,
                "nodes_expanded": total_nodes_expanded,
                "max_frontier_size": depth
            }
    return None # No solution

def dls(problem, limit):
    #Depth-Limited Search for IDS.
    nodes_generated = 0
    nodes_expanded = 0
    
    def recursive_dls(node, limit):
        nonlocal nodes_expanded, nodes_generated
        if problem.is_goal(node.state):
            return {"solution": node}
        if limit == 0:
            return {"cutoff": True}

        nodes_expanded += 1
        cutoff_occurred = False
        
        for action in problem.get_actions(node.state):
            child_state = problem.get_result(node.state, action)
            child_node = Node(
                state=child_state,
                parent=node,
                action=action,
                cost=problem.path_cost(node.cost, node.state, action, child_state)
            )
            nodes_generated += 1
            
            result = recursive_dls(child_node, limit - 1)
            
            if result.get("cutoff"):
                cutoff_occurred = True
            elif result.get("solution") is not None:
                return result
        return {"cutoff": True} if cutoff_occurred else {"solution": None}

    start_node = Node(problem.initial_state)
    nodes_generated += 1
    
    # recursive search
    dls_result = recursive_dls(start_node, limit)

    return {
        "solution": dls_result.get("solution"),
        "nodes_generated": nodes_generated,
        "nodes_expanded": nodes_expanded
    }