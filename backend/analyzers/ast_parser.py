import ast

class CodeFeatureExtractor(ast.NodeVisitor):
    def __init__(self):
        self.features = {
            "max_loop_depth": 0,
            "has_recursion": False,
            "nested_loops": 0,
            "function_calls": set(),
            "data_structures": set(), # dict, set, list, deque, priorityqueue
            "has_memoization": False,
            "loop_steps": [], # list of (type, step_op) e.g., ('for', 'unit'), ('while', 'div')
            "branching_factor": 0,
            "current_function": None,
            "imports": set(),
            "early_exits": 0, # break, return inside loops
            "bit_manipulation": False
        }
        self.loop_depth = 0

    def visit_Import(self, node):
        for alias in node.names:
            self.features["imports"].add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.features["imports"].add(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Detect memoization (decorators like @lru_cache or manual dict)
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and "cache" in decorator.id:
                self.features["has_memoization"] = True
            elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and "cache" in decorator.func.id:
                self.features["has_memoization"] = True

        old_func = self.features["current_function"]
        self.features["current_function"] = node.name
        self.generic_visit(node)
        self.features["current_function"] = old_func

    def _analyze_loop_step(self, node):
        # Detect if loop range is halving (O(log n))
        step_type = "unit"
        for sub in ast.walk(node):
            if isinstance(sub, ast.AugAssign):
                if isinstance(sub.op, (ast.Div, ast.FloorDiv, ast.RShift)):
                    step_type = "log"
                elif isinstance(sub.op, (ast.Mult, ast.LShift)):
                    step_type = "exp"
        return step_type

    def visit_For(self, node):
        self.loop_depth += 1
        self.features["max_loop_depth"] = max(self.features["max_loop_depth"], self.loop_depth)
        if self.loop_depth > 1:
            self.features["nested_loops"] += 1
        
        self.features["loop_steps"].append(("for", self._analyze_loop_step(node)))
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        self.features["max_loop_depth"] = max(self.features["max_loop_depth"], self.loop_depth)
        if self.loop_depth > 1:
            self.features["nested_loops"] += 1
            
        self.features["loop_steps"].append(("while", self._analyze_loop_step(node)))
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            self.features["function_calls"].add(func_name)
            if func_name == self.features["current_function"]:
                self.features["has_recursion"] = True
            
            # Detect data structures
            if func_name in ['dict', 'set', 'list', 'deque', 'PriorityQueue', 'heapq']:
                self.features["data_structures"].add(func_name)
        
        elif isinstance(node.func, ast.Attribute):
            self.features["function_calls"].add(node.func.attr)
            if node.func.attr in ['append', 'pop', 'push', 'heappush', 'heappop']:
                self.features["data_structures"].add('heap' if 'heap' in node.func.attr else 'list/deque')

        self.generic_visit(node)

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift)):
            self.features["bit_manipulation"] = True
        self.generic_visit(node)

    def visit_Break(self, node):
        self.features["early_exits"] += 1
        self.generic_visit(node)

def get_code_features(code):
    try:
        tree = ast.parse(code)
        extractor = CodeFeatureExtractor()
        extractor.visit(tree)
        # Convert sets to lists for JSON serialization
        features = extractor.features
        features["function_calls"] = list(features["function_calls"])
        features["data_structures"] = list(features["data_structures"])
        features["imports"] = list(features["imports"])
        return features
    except Exception as e:
        return {"error": str(e)}
