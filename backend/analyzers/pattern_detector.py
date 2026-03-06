import re

def detect_dsa_patterns(code):
    """
    Advanced detection using combined regex and structural heuristics.
    Covers 15+ common DSA patterns.
    """
    patterns = []
    code_lower = code.lower()

    # 1. Sliding Window
    if any(kw in code_lower for kw in ['window', 'substring', 'subarray']) and 'while' in code_lower:
        patterns.append("Sliding Window")
    
    # 2. Two Pointer
    if ('left' in code_lower and 'right' in code_lower) or ('low' in code_lower and 'high' in code_lower):
        if 'while' in code_lower and ('<' in code or '<=' in code):
            patterns.append("Two Pointer")

    # 3. Fast & Slow Pointer (Cycle Detection)
    if 'slow' in code_lower and 'fast' in code_lower:
        patterns.append("Fast & Slow Pointer (Cycle Detection)")

    # 4. Binary Search
    if 'mid' in code or '// 2' in code or '>> 1' in code:
        if 'while' in code and ('low' in code or 'left' in code):
            patterns.append("Binary Search")

    # 5. Dynamic Programming (Top-Down/Memoization)
    if '@cache' in code or 'memo' in code_lower or ('if' in code_lower and 'in' in code_lower and 'memo' in code_lower):
        patterns.append("Dynamic Programming (Memoization)")

    # 6. Dynamic Programming (Bottom-Up/Tabulation)
    if 'dp = [' in code or 'dp[' in code:
        if 'for' in code:
            patterns.append("Dynamic Programming (Tabulation)")

    # 7. Backtracking
    if ('def' in code and 'path' in code_lower) or 'backtrack' in code_lower:
        if ('append' in code_lower and 'pop' in code_lower) or ('visited' in code_lower):
            patterns.append("Backtracking")

    # 8. Depth First Search (DFS)
    if 'dfs' in code_lower or ('stack' in code_lower and ('pop' in code_lower or 'append' in code_lower)):
        patterns.append("DFS (Depth First Search)")

    # 9. Breadth First Search (BFS)
    if 'bfs' in code_lower or 'deque' in code_lower or ('queue' in code_lower and 'popleft' in code_lower):
        patterns.append("BFS (Breadth First Search)")

    # 10. Heap / Priority Queue
    if 'heapq' in code or 'heappush' in code or 'heappop' in code or 'PriorityQueue' in code:
        patterns.append("Heap / Priority Queue")

    # 11. Prefix Sum
    if 'prefix' in code_lower or 'sum' in code_lower:
        if 'dp[' in code or 'accumulate' in code:
            patterns.append("Prefix Sum")

    # 12. Monotonic Stack/Queue
    if 'stack' in code_lower and ('>' in code or '<' in code) and 'while' in code_lower:
        if 'pop' in code_lower:
            patterns.append("Monotonic Stack")

    # 13. Union Find (Disjoint Set)
    if 'find' in code_lower and 'union' in code_lower and ('parent' in code_lower or 'root' in code_lower):
        patterns.append("Union-Find (Disjoint Set)")

    # 14. Bit Manipulation
    if any(op in code for op in ['<<', '>>', '&', '|', '^', '~']):
        patterns.append("Bit Manipulation")

    # 15. Greedy
    if any(kw in code_lower for kw in ['sort', 'max', 'min']) and patterns == []:
        patterns.append("Greedy / Brute Force")

    # 16. Graph (Adjacency List/Matrix)
    if 'adj' in code_lower or 'graph' in code_lower or 'edges' in code_lower:
        patterns.append("Graph Representation")

    return list(set(patterns)) if patterns else ["Standard Iteration"]
