def generate_prompt(code, patterns, complexity, history):
    """
    Constructs a detailed prompt for the LLM based on analysis results.
    """
    history_context = ""
    if history:
        history_context = "User's previous attempts/patterns: " + ", ".join([h['pattern'] for h in history])

    prompt = f"""
    Analyze the following DSA code and provide structured feedback.
    
    User Code:
    {code}
    
    Detected Pattern: {patterns}
    Estimated Complexity: {complexity}
    {history_context}
    
    Return the response in the following JSON format ONLY:
    {{
        "algorithm_detected": "string (e.g., 'QuickSort')",
        "best_time_complexity": "string (The best-case scenario complexity, e.g., 'O(1)', 'O(n)')",
        "worst_time_complexity": "string (The worst-case scenario complexity based on {complexity}, e.g., 'O(n^2)', 'O(n log n)')",
        "space_complexity": "string (The auxiliary space complexity, e.g., 'O(1)', 'O(n)')",
        "problem": "string explaining the issue (If the code is already correct and efficient, return 'No major issue detected')",
        "explanation": "string explaining the logic",
        "suggested_algorithm": "string (If the code is already optimal, return 'No improvement required')",
        "improved_complexity": "string",
        "improved_code": "string with improved python code",
        "speedup_score": "integer (1-10 representing optimization potential, 1 if already optimal)",
        "optimization_impact": "string (High, Medium, Low, or None)",
        "theoretical_speedup": "string (e.g., '10x for N=1000' or an empty string)"
    }}

    CRITICAL RULES:
    1. Use the 'Estimated Complexity' provided above ({complexity}) as a baseline for 'worst_time_complexity'.
    2. Provide accurate 'best_time_complexity', 'worst_time_complexity', and 'space_complexity' strings (e.g., 'O(n)', 'O(1)').
    3. If the code is already optimal for the given task, do not invent problems. Return "No major issue detected" for the 'problem' field.
    4. If the provided code is already optimal, do not suggest a different algorithm. Return "No improvement required" for the 'suggested_algorithm' field.
    5. Ensure the JSON is valid and strictly follows the schema.
    """
    return prompt
