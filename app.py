import ast
import streamlit as st
import tiktoken

st.set_page_config(page_title="TokenShift", page_icon="🔐", layout="centered")

# Metinlerin ve kod bloklarının alt satıra geçmesini (wrap) sağlayan stil
st.markdown("""
<style>
.output-box {
    background-color: #0e1117;
    color: #fafafa;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #30363d;
    font-family: monospace;
    white-space: pre-wrap;       /* Alt satıra geçmesini sağlar */
    word-break: break-word;     /* Kelimelerin taşmasını engeller */
    max-height: 400px;
    overflow-y: auto;           /* Dikey kaydırma */
}
</style>
""", unsafe_allow_html=True)

st.title("🔐 TokenShift 75baran.raw")
st.caption("Hayallerin herkese Açık Olmak Zorunda Değil")

@st.cache_resource
def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

enc = get_encoder()
MAX_SAFE_VOCAB = enc.max_token_value + 1

mode = st.radio("İşlem Türü", ["Hayallerini Şifrele (Encode)", "Başkasının Hayallerini Öğren (Decode)"], horizontal=True)
text_input = st.text_area("Hayal (Metin veya [123, 456...] Token Listesi)", placeholder="Buraya Hayallerini veya Sayı Dizisini girin...", height=130)
shift = st.number_input("Gizli Kod (Shift Key)", value=15, step=1)

if st.button("Tree", type="primary"):
    val = text_input.strip()
    if val:
        try:
            actual_shift = int(shift) if "Şifrele" in mode else -int(shift)
            
            # Girdi token listesi mi yoksa metin mi?
            if val.startswith("[") and val.endswith("]"):
                tokens = ast.literal_eval(val)
                if not isinstance(tokens, list):
                    tokens = enc.encode(val)
            else:
                tokens = enc.encode(val)
            
            # Modüler kaydırma
            shifted_tokens = [(t + actual_shift) % MAX_SAFE_VOCAB for t in tokens]
            
            # Çözümleme
            valid_bytes = []
            for t in shifted_tokens:
                try:
                    valid_bytes.append(enc.decode_single_token_bytes(t))
                except KeyError:
                    continue
            
            result = b"".join(valid_bytes).decode("utf-8", errors="replace")
            
            st.subheader("Sonuç (Metin):")
            st.markdown(f'<div class="output-box">{result if result else "[Metin üretilemedi]"}</div>', unsafe_allow_html=True)
            
            st.subheader("Sonuç (Token ID Listesi):")
            st.markdown(f'<div class="output-box">{str(shifted_tokens)}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"İşlem sırasında bir hata oluştu: {e}")
    else:
        st.warning("Lütfen Hayallerini Benimle Paylaş.")
