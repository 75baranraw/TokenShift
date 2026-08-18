# TokenShift
import tiktoken

def shift_tokens(text: str, shift: int = 42, encoding_name: str = "cl100k_base") -> str:
    enc = tiktoken.get_encoding(encoding_name)
    tokens = enc.encode(text)
    shifted_tokens = [(t + shift) % enc.n_vocab for t in tokens]
    return enc.decode(shifted_tokens)

if __name__ == "__main__":
    original = "Hello World!"
    encrypted = shift_tokens(original, shift=15)
    decrypted = shift_tokens(encrypted, shift=-15)
    
    print(f"Orijinal: {original}")
    print(f"Sifreli:  {encrypted}")
    print(f"Cozulmus: {decrypted}")
