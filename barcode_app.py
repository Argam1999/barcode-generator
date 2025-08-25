import streamlit as st
import barcode
from barcode.writer import ImageWriter
import random
from io import BytesIO

st.title("Генератор штрихкодов для игрушек")

# Имя игрушки
toy_name = st.text_input("Имя игрушки", key="toy_name")

# Инициализация кода
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

# Кнопка случайного кода
if st.button("Случайный код"):
    st.session_state.code_input = ''.join([str(random.randint(0, 9)) for _ in range(13)])

# Поле ввода кода
code_input = st.text_input("Код (13 цифр)", value=st.session_state.code_input, key="code_input")

# Кнопка генерации штрихкода
if st.button("Сгенерировать штрихкод"):
    code_to_use = st.session_state.code_input
    if not toy_name or not code_to_use:
        st.error("Введите имя игрушки и код!")
    elif not code_to_use.isdigit() or len(code_to_use) != 13:
        st.error("Код должен быть 13 цифр!")
    else:
        barcode_class = barcode.get_barcode_class('code128')
        ean = barcode_class(code_to_use, writer=ImageWriter())
        image_buffer = BytesIO()
        ean.write(image_buffer)
        image_buffer.seek(0)
        st.image(image_buffer)
        st.download_button(
            "Скачать PNG",
            data=image_buffer,
            file_name=f"{toy_name}_{code_to_use}.png",
            mime="image/png"
        )
