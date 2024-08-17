import cohere

# Replace this with your actual Cohere API key
COHERE_API_KEY = "A1Fi5KBBNoekwBPIa833CBScs6Z2mHEtOXxr52KO"

if __name__ == "__main__":
    # Example usage
    co = cohere.Client(COHERE_API_KEY)
    tokens = "This is sentence 3 of the medium document."
    detokenize_result = co.tokenize(text=tokens, model="command-r")
    print("AAA:", detokenize_result)