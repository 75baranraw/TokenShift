# TokenShift 🔐

> A lightweight, experimental text obfuscation tool that applies Caesar cipher shift logic directly to LLM token IDs using `tiktoken`.

## 🚀 Usage

```python
from tokenshift import shift_tokens

# Metni şifrele (token kaydırma)
secret = shift_tokens("Hello World!", shift=15)

# Metni çöz
original = shift_tokens(secret, shift=-15)
```
