import streamlit as st
import tiktoken

st.set_page_config(page_title="TokenShift", page_icon="🔐", layout="centered")

st.title("🔐 TokenShift 75baran.raw")
st.caption("Tiktoken tabanlı token kaydırma şifreleyicisi")

@st.cache_resource
def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

enc = get_encoder()

mode = st.radio("İşlem Türü", ["Metin Şifrele (Encode)", "Şifreli Metni Çöz (Decode)"], horizontal=True)
text = st.text_area("Girdi Metni", placeholder="Buraya metni girin...", height=120)
shift = st.number_input("Kaydırma Anahtarı (Shift Key)", value=15, step=1)

if st.button("Çalıştır", type="primary"):
    if text.strip():
        try:
            tokens = enc.encode(text)
            actual_shift = int(shift) if "Şifrele" in mode else -int(shift)
            
            # Geçerli token sınırlarında modüler kaydırma
            shifted_tokens = [(t + actual_shift) % enc.n_vocab for t in tokens]
            
            # Hatalı UTF-8 baytlarını görmezden gelerek/yerine koyarak güvenli decode et
            raw_bytes = enc.decode_tokens_bytes(shifted_tokens)
            result = b"".join(raw_bytes).decode("utf-8", errors="replace")
            
            st.subheader("Sonuç:")
            st.code(result, language="text")
            
            with st.expander("Token ID Listesini Gör"):
                st.write(shifted_tokens)
                
        except Exception as e:
            st.error(f"İşlem sırasında bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir metin girin.")
