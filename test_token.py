import os
import cohere

# Replace this with your actual Cohere API key
COHERE_API_KEY = "A1Fi5KBBNoekwBPIa833CBScs6Z2mHEtOXxr52KO"

def tokenize_text(text: str):
    # Initialize the Cohere client
    co = cohere.Client(COHERE_API_KEY)
    
    # Tokenize the text
    result = co.detokenize(tokens=text, model="command-r")
    
    # Print the tokens and their count
    print(f"Input text: {text}")
    print(f"Tokenized: {result.tokens}")
    print(f"Token count: {len(result.tokens)}")

    # Optionally, you can also detokenize to verify
    detokenized = co.detokenize(tokens=result.tokens, model="command-r")
    print(f"Detokenized text: {detokenized.text}")

if __name__ == "__main__":
    # Example usage
    sample_text = [1]
    tokenize_text(sample_text)
    #user_input = "Hello\nHello\n\n\n My Name\nis Teo"
    # You can add more examples or prompt the user for input
    #user_input = input("\nEnter your own text to tokenize (or press Enter to exit): ")
    #if user_input:
     #   tokenize_text(user_input)