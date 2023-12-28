import tiktoken

map_model_to_cost_per_1k_tokens = {
    "gpt-4": 0.075,  # ($0.03 Input Tokens + $0.06 Output Tokens) / 2
    "gpt-4-1106-preview": 0.02,  # ($0.01 Input Tokens + $0.03 Output Tokens) / 2
    "gpt-4-1106-vision-preview": 0.02,  # ($0.01 Input Tokens + $0.03 Output Tokens) / 2
    "gpt-3.5-turbo-1106": 0.0015,  # ($0.001 Input Tokens + $0.002 Output Tokens) / 2
}


def count_tokens(text: str):
    """
    Count the number of tokens in a string.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def estimate_price_and_tokens(text, model="gpt-4"):
    """
    Conservative estimate the price and tokens for a given text.
    """
    # round up to the output tokens
    COST_PER_1k_TOKENS = map_model_to_cost_per_1k_tokens[model]

    tokens = count_tokens(text)

    estimated_cost = (tokens / 1000) * COST_PER_1k_TOKENS

    # round
    estimated_cost = round(estimated_cost, 2)

    return estimated_cost, tokens
