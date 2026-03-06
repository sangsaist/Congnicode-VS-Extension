from flask import Blueprint, request, jsonify
from analyzers.ast_parser import get_code_features
from analyzers.complexity_analyzer import estimate_complexity, detect_inefficiencies
from analyzers.pattern_detector import detect_dsa_patterns
from history.history_manager import HistoryManager
from llm.llm_service import call_llm
from prompts.feedback_prompt import generate_prompt

analyze_bp = Blueprint('analyze', __name__)
history_manager = HistoryManager()

@analyze_bp.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({"error": "No code provided"}), 400
        
    code = data.get('code')
    user_id = data.get('user_id', 'anonymous')
    
    # Stage 1: Static Code Analysis
    features = get_code_features(code)
    
    # Stage 2: Complexity and Inefficiencies
    complexity = estimate_complexity(features)
    patterns = detect_dsa_patterns(code)
    
    # Stage 3: User History
    history = history_manager.get_user_history(user_id)
    
    # Stage 4: LLM Reasoning
    prompt = generate_prompt(code, patterns, complexity, history)
    analysis_result = call_llm(prompt)
    
    # Stage 5: Update History (Save the detected pattern)
    pattern_name = analysis_result.get("algorithm_detected", "Unknown")
    history_manager.add_to_history(user_id, pattern_name, complexity)
    
    # Ensure strict adherence to response format
    final_response = {
        "algorithm_detected": analysis_result.get("algorithm_detected", ""),
        "best_time_complexity": analysis_result.get("best_time_complexity", ""),
        "worst_time_complexity": analysis_result.get("worst_time_complexity", complexity),
        "space_complexity": analysis_result.get("space_complexity", ""),
        "problem": analysis_result.get("problem", ""),
        "explanation": analysis_result.get("explanation", ""),
        "suggested_algorithm": analysis_result.get("suggested_algorithm", ""),
        "improved_complexity": analysis_result.get("improved_complexity", ""),
        "improved_code": analysis_result.get("improved_code", ""),
        "speedup_score": analysis_result.get("speedup_score", 1),
        "optimization_impact": analysis_result.get("optimization_impact", "None"),
        "theoretical_speedup": analysis_result.get("theoretical_speedup", "")
    }
    
    return jsonify(final_response)
