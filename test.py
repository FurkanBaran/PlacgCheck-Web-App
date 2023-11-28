import streamlit as st
import string

def check_plagiarism(main_text, data_text, n):
    check_text = []

    for i in range(n - 1):
        check_text.append(main_text[i])

    main_text_len = len(main_text)

    for id in range(main_text_len - n):
        check_text.append(main_text[id + n])
        for file_id in range(len(data_text)):
            for j in range(len(data_text[file_id]) - n):
                if check_text == data_text[file_id][j:j + n]:
                    for k in range(n):
                        main_text[id + k]['isPlagiarism'] = True
                        data_text[file_id][j + k]['isPlagiarism'] = True
        check_text.pop(0)

    return main_text, data_text

def preprocess_text(text_content):
    text_lines = text_content.split('\n')
    main_text = []

    for line in text_lines:
        for word in line.split():
            main_text.append({'word': word, 'isPlagiarism': False, 'isNewLine': True})
            main_text[-1]['word'] = word.translate(str.maketrans('', '', string.punctuation)).lower()

    return main_text

def preprocess_data_text(data_text_files):
    data_text = []

    for file_id, file in enumerate(data_text_files):
        content = file.read().decode("utf-8")
        file_text = preprocess_text(content)
        data_text.append(file_text)

    return data_text

def display_text(text):
    text_to_display = ""
    for word_info in text:
        if word_info['isPlagiarism']:
            text_to_display += f"<font color='red'>{word_info['word']}</font> "
        else:
            text_to_display += word_info['word'] + (" " if not word_info['isNewLine'] else "\n")

    st.markdown(text_to_display, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")

    st.title("Plagiarism Checker")

    n = st.slider("Select Level (N)", min_value=3, max_value=7, value=3)
    main_text = st.file_uploader("Upload Main Text File", type=["txt"])
    data_text_files = st.file_uploader("Upload Data Text Files", type=["txt"], accept_multiple_files=True)

    # Dosyaların içeriğini bu değişkenlerde tutalım
    main_text_data = None
    data_text_data = None

    # Dosya seçildiyse içeriği al
    if main_text is not None:
        main_text_content = main_text.read().decode("utf-8")
        main_text_data = preprocess_text(main_text_content)

    # Dosyalar seçildiyse içerikleri al
    if data_text_files is not None:
        data_text_data = preprocess_data_text(data_text_files)

        # Kontrol işlemini optimize et
        if main_text_data is not None:
            main_text_data, data_text_data = check_plagiarism(main_text_data, data_text_data, n)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Main Text")
        if main_text_data:
            display_text(main_text_data)

    with col2:
        st.markdown("### Data Text")
        if data_text_data:
            selected_file = st.selectbox("Select Data Text File", [f"File {i + 1}" for i in range(len(data_text_data))])
            display_text(data_text_data[int(selected_file.split()[-1]) - 1])

if __name__ == "__main__":
    main()
