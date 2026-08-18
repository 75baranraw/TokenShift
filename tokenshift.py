import tiktoken

def shift_tokens(text: str, shift: int, encoding_name: str = "cl100k_base") -> str:
    enc = tiktoken.get_encoding(encoding_name)
    tokens = enc.encode(text)
    shifted_tokens = [(t + shift) % enc.n_vocab for t in tokens]
    return enc.decode(shifted_tokens)

def main():
    print("=" * 40)
    print("        TOKENSHIFT - LLM OBFUSCATOR    ")
    print("=" * 40)
    
    print("\n1. Metin Şifrele")
    print("2. Şifreli Metni Çöz")
    
    choice = input("\nİşlem seçin (1/2): ").strip()
    
    if choice not in ["1", "2"]:
        print("Geçersiz seçim!")
        return

    text = input("\nMetni girin: ")
    
    try:
        key = int(input("Gizli anahtarı / Kaydırma sayısını girin (Örn: 23): "))
    except ValueError:
        print("Hata: Anahtar bir tam sayı olmalıdır!")
        return

    if choice == "1":
        result = shift_tokens(text, shift=key)
        print("\n🔒 Şifreli Çıktı:")
        print("-" * 30)
        print(result)
        print("-" * 30)
    else:
        result = shift_tokens(text, shift=-key)
        print("\n🔓 Çözülmüş Orijinal Metin:")
        print("-" * 30)
        print(result)
        print("-" * 30)

if __name__ == "__main__":
    main()
