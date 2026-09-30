import io
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw

# --- 1. Konfigurasi Halaman & Tema Web ---
st.set_page_config(
    page_title="KriptoKraf - Vigenère Batik Craft",
    page_icon="🎨",
    layout="wide",
)

# Custom CSS untuk Latar Belakang & Tampilan Menarik (Gradient + Card UI)
st.markdown(
    """
    <style>
    /* Latar Belakang Seluruh Aplikasi */
    .stApp {
        background: linear-gradient(135deg, #FDFBF7 0%, #EFE6D5 100%);
    }
    
    /* Judul Utama */
    .main-title {
        color: #7B1113;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #555555;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Kartu Informasi Panduan */
    .guide-box {
        background-color: #FFFFFF;
        border-left: 5px solid #7B1113;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Desain Tombol */
    .stButton>button {
        background: linear-gradient(90deg, #7B1113 0%, #A31417 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        border: none;
        box-shadow: 0px 4px 10px rgba(123, 17, 19, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #961316 0%, #B8181C 100%);
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- 2. Fungsi Kriptografi (Vigenère Cipher) ---
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    if not key:
        key = "BATIK"

    ciphertext = []
    for i, char in enumerate(plaintext):
        if char.isalpha():
            p_val = ord(char) - ord("A")
            k_val = ord(key[i % len(key)]) - ord("A")
            c_val = (p_val + k_val) % 26
            ciphertext.append(chr(c_val + ord("A")))
        else:
            ciphertext.append(char)
    return "".join(ciphertext)


# --- 3. Fungsi Generator Visual Batik ---
def generate_vigenere_batik(
    ciphertext, bg_color="#F5F2EB", pattern_color="#B85B28", size=700
):
    img = Image.new("RGB", (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)

    center = size // 2
    chars = [c for c in ciphertext if c.isalpha()]
    total_chars = max(len(chars), 1)

    for idx, char in enumerate(chars):
        val = ord(char) - ord("A")
        radius = (idx + 1) * (center // (total_chars + 1))
        num_petals = 4 + (val % 8)
        petal_length = 15 + (val * 2)

        for i in range(num_petals):
            angle = (2 * np.pi / num_petals) * i + (val * 0.1)
            x_end = center + int(radius * np.cos(angle))
            y_end = center + int(radius * np.sin(angle))

            draw.line(
                [(center, center), (x_end, y_end)], fill=pattern_color, width=2
            )
            draw.ellipse(
                [
                    x_end - petal_length / 2,
                    y_end - petal_length / 2,
                    x_end + petal_length / 2,
                    y_end + petal_length / 2,
                ],
                outline=pattern_color,
                width=2,
            )

    return img


# --- Sidebar Informasi & Gambar Inspirasi ---
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Batik_Parang_Rusak.jpg/320px-Batik_Parang_Rusak.jpg",
        caption="Inspirasi Seni Batik Nusantara",
        use_container_width=True,
    )
    st.header("📌 Panduan Pengisian")
    st.write(
        """
    **Langkah-langkah Pembuatan:**
    1. **Pesan Rahasia:** Masukkan kalimat atau nama yang ingin diubah menjadi bentuk batik.
    2. **Kunci Rahasia:** Masukkan kata kunci enkripsi (bebas).
    3. **Pilih Warna:** Kustomisasi warna dasar latar dan warna garis motif batik.
    4. Klik tombol **Hasilkan Batik Sekarang**.
    """
    )
    st.markdown("---")
    st.info("💡 *Setiap kombinasi pesan dan kunci menghasilkan simetri batik yang unik!*")

# --- Header Utama ---
st.markdown(
    "<h1 class='main-title'>🎨 KriptoKraf: Vigenère Batik</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='sub-title'>Inovasi Digitalisasi Batik Berbasis Kriptografi Vigenère Cipher</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- Form Input & Pilihan Warna ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown(
        """
    <div class='guide-box'>
        <b>📝 Form Input Parameter</b><br>
        Silahkan isi pesan rahasia dan kunci di bawah ini untuk membentuk parameter visual batik.
    </div>
    """,
        unsafe_allow_html=True,
    )

    text_input = st.text_input(
        "1. Masukkan Pesan / Teks Rahasia:",
        value="MATEMATIKA UNIMED",
        placeholder="Contoh: UNIMED MEDAN",
        help="Ketik teks/kalimat rahasia yang akan dienkripsi menjadi pola batik.",
    )

    key_input = st.text_input(
        "2. Masukkan Kunci Rahasia:",
        value="MEDAN",
        placeholder="Contoh: SECRET",
        help="Kunci enkripsi Vigenère untuk mengacak sudut dan jumlah kelopak batik.",
    )

    st.subheader("3. Kustomisasi Warna Batik")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        bg_col = st.color_picker(
            "Warna Latar Belakang",
            "#F5F2EB",
            help="Pilih warna dasar kain batik",
        )
    with col_w2:
        pat_col = st.color_picker(
            "Warna Motif Batik",
            "#8B0000",
            help="Pilih warna garis/pola batik",
        )

    btn_generate = st.button("✨ Hasilkan Batik Sekarang")

# --- Hasil Visualisasi ---
with col_right:
    st.subheader("🖼️ Hasil Visualisasi Batik")

    if btn_generate or text_input:
        cipher = vigenere_encrypt(text_input, key_input)
        st.success(f"🔑 **Ciphertext (Hasil Enkripsi):** `{cipher}`")

        batik_img = generate_vigenere_batik(
            cipher, bg_color=bg_col, pattern_color=pat_col
        )

        # Penampil Gambar (Menggunakan use_container_width=True)
        st.image(
            batik_img,
            caption="Hasil Motif Batik Vigenère Cipher - KriptoKraf",
            use_container_width=True,
        )

        # Tombol Unduh Gambar
        buf = io.BytesIO()
        batik_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="💾 Unduh Motif Batik (PNG)",
            data=byte_im,
            file_name=f"Batik_Vigenere_{cipher}.png",
            mime="image/png",
        )