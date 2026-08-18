import ast
import streamlit as st
import tiktoken

st.set_page_config(page_title="TokenShift", page_icon="🔐", layout="centered")

st.title("🔐 TokenShift 75baran.raw")
st.caption("Tiktoken tabanlı token kaydırma şifreleyicisi")

@st.cache_resource
def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

enc = get_encoder()
# cl100k_base için güvenli maksimum token sınırı (özel token boşluklarını engeller)
MAX_SAFE_VOCAB = enc.max_token_value + 1

mode = st.radio("İşlem Türü", ["Metin Şifrele (Encode)", "Şifreli Metni / Token Listesini Çöz (Decode)"], horizontal=True)
text_input = st.text_area("Girdi (Metin veya [123, 456...] Token Listesi)", placeholder="Buraya metin veya token listesi girin...", height=130)
shift = st.number_input("Kaydırma Anahtarı (Shift Key)", value=15, step=1)

if st.button("Çalıştır", type="primary"):
    val = text_input.strip()
    if val:
        try:
            actual_shift = int(shift) if "Şifrele" in mode else -int(shift)
            
            # Girdi doğrudan bir liste [1, 2, 3] mü yoksa düz metin mi kontrol et
            if val.startswith("[") and val.endswith("]"):
                tokens = ast.literal_eval(val)
                if not isinstance(tokens, list):
                    tokens = enc.encode(val)
            else:
                tokens = enc.encode(val)
            
            # Güvenli modüler kaydırma
            shifted_tokens = [(t + actual_shift) % MAX_SAFE_VOCAB for t in tokens]
            
            # Çözümleme (Bilinmeyen tokenları güvenle atla)
            valid_bytes = []
            for t in shifted_tokens:
                try:
                    valid_bytes.append(enc.decode_single_token_bytes(t))
                except KeyError:
                    # Karşılığı olmayan özel token ID'lerini atla
                    continue
            
            result = b"".join(valid_bytes).decode("utf-8", errors="replace")
            
            st.subheader("Sonuç (Metin):")
            st.code(result if result else "[Metin karşılığı üretilemedi]", language="text")
            
            st.subheader("Sonuç (Token ID Listesi):")
            st.code(str(shifted_tokens), language="python")
            
        except Exception as e:
            st.error(f"İşlem sırasında bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir metin veya token listesi girin.")
