# utils file with helper functions

def calculate_llm_inference_cost(num_tokens, cost_per_token=0.000001):
    """
    Function to calculate the cost of Large Language Model (LLM) inference based on tokens.
    :param num_tokens: int: Number of tokens in the input text.
    :param cost_per_token: float: Cost per token
    :return: total_cost : float: Total cost of inference
    """
    total_cost = num_tokens * cost_per_token
    return f"${total_cost}"
