import streamlit as st
import tiktoken

st.set_page_config(page_title="TokenShift", page_icon="🔐")

st.title("🔐 TokenShift")
st.caption("Tiktoken tabanlı token kaydırma şifreleyicisi")

@st.cache_resource
def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

enc = get_encoder()

mode = st.radio("İşlem Türü", ["Şifrele (Encode)", "Şifre Çöz (Decode)"], horizontal=True)
text = st.text_area("Metin", placeholder="Buraya metni girin...")
shift = st.number_input("Kaydırma Anahtarı (Shift Key)", value=15, step=1)

if st.button("Çalıştır", type="primary"):
    if text.strip():
        tokens = enc.encode(text)
        actual_shift = shift if "Şifrele" in mode else -shift
        shifted_tokens = [(t + actual_shift) % enc.n_vocab for t in tokens]
        result = enc.decode(shifted_tokens)
        
        st.subheader("Sonuç:")
        st.code(result, language="text")
    else:
        st.warning("Lütfen bir metin girin.")
