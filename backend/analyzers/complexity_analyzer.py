def estimate_complexity(features):
    """
    Smarter heuristic estimation using AST features.
    """
    if "error" in features:
        return "Unknown"

    depth = features.get("max_loop_depth", 0)
    has_recursion = features.get("has_recursion", False)
    has_memo = features.get("has_memoization", False)
    loop_steps = features.get("loop_steps", [])
    
    # 1. Check for O(log n) patterns
    if any(step == "log" for loop_type, step in loop_steps):
        if depth == 1:
            return "O(log n)"
        elif depth == 2:
            return "O(n log n)"
            
    # 2. Check for recursion with memoization (usually O(n) or O(V+E))
    if has_recursion:
        if has_memo:
            return "O(n) [Memoized]"
        return "O(2^n) [Exponential Risk]"
    
    # 3. Standard Polynomial Complexity
    if depth == 0:
        return "O(1)"
    elif depth == 1:
        return "O(n)"
    elif depth == 2:
        return "O(n^2)"
    elif depth == 3:
        return "O(n^3)"
    else:
        return f"O(n^{depth})"

def detect_inefficiencies(features):
    """
    Detects common inefficient search or brute force patterns.
    """
    inefficiencies = []
    if features.get("max_loop_depth", 0) >= 2:
        inefficiencies.append("Nested loops detected (Potential O(n^2) brute force)")
    
    if features.get("has_recursion", False):
        inefficiencies.append("Recursion detected (Risk of stack overflow or TLE if not memoized)")

    return inefficiencies
