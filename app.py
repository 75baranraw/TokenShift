import re
import streamlit as st
import tiktoken

st.set_page_config(page_title="TokenShift", page_icon="🔐", layout="centered")

# Tokenizer sözlüğü (cl100k_base: GPT-4, GPT-3.5)
@st.cache_resource
def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

enc = get_encoder()

st.title("⚡ TokenShift")

# --- ARAYÜZ ---
islem = st.radio(
    "İşlem Türü",
    ["Hayallerini Şifrele (Encode)", "Başkasının Hayallerini Öğren (Decode)"]
)

girdi = st.text_area(
    "Hayal (Metin veya [123, 456...] Sayı Dizisi)",
    height=120,
    placeholder="Metin yazın veya sayı dizisi yapıştırın..."
)

shift = st.number_input("Gizli Kod (Shift Key)", value=75, step=1)

btn = st.button("İşlemi Uygula")

# --- MANTIK ---
if btn:
    if not girdi.strip():
        st.warning("Lütfen bir metin veya sayı dizisi girin.")
    else:
        if islem == "Hayallerini Şifrele (Encode)":
            try:
                # Metni token ID listesine dönüştür
                tokens = enc.encode(girdi)
                # Shift ekle (+75)
                sifreli_tokens = [t + shift for t in tokens]

                st.subheader("Sonuç (Token ID Listesi):")
                st.code(str(sifreli_tokens), language="json")
            except Exception as e:
                st.error(f"Şifreleme hatası: {e}")

        else:  # Decode
            # Girdideki tüm sayıları ayıkla
            sayilar = re.findall(r"\d+", girdi)

            if not sayilar:
                st.error("Girdiğiniz metinde geçerli sayı dizisi bulunamadı!")
            else:
                try:
                    # Sayıları integer listesi yap
                    token_ids = [int(s) for s in sayilar]
                    # Shift değerini çıkar (-75)
                    orijinal_tokens = [t - shift for t in token_ids]
                    # Token ID'lerini doğrudan Türkçe/düz metne çevir
                    cozulmus_metin = enc.decode(orijinal_tokens)

                    st.subheader("Sonuç (Metin):")
                    st.code(cozulmus_metin, language="text")

                    st.subheader("Sonuç (Orijinal Token ID Listesi):")
                    st.code(str(orijinal_tokens), language="json")
                except Exception as e:
                    st.error(f"Çözme hatası: Token sözlüğü eşleşmedi. ({e})")
