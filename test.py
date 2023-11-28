import streamlit as st
import pandas as pd
import string

def check_plagiarism(main_text, data_text, n):
    check_text = []
    plag_count = 0

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

def main():
    st.title("Plagiarism Checker")

    main_text = st.file_uploader("Upload Main Text File", type=["txt"])
    data_text_files = st.file_uploader("Upload Data Text Files", type=["txt"], accept_multiple_files=True)

    if main_text is not None and data_text_files is not None:
        main_text_content = main_text.read().decode("utf-8")
        st.text_area("Main Text", main_text_content, height=300)

        n = st.slider("Select Level (N)", min_value=3, max_value=7, value=3)
        st.button("Check Plagiarism", on_click=lambda: check_and_display(main_text_content, data_text_files, n))

def check_and_display(main_text_content, data_text_files, n):
    main_text = preprocess_text(main_text_content)
    data_text = preprocess_data_text(data_text_files)

    main_text, data_text = check_plagiarism(main_text, data_text, n)

    st.markdown("### Checked Main Text")
    display_text(main_text)

    selected_file = st.selectbox("Select Data Text File", [f"File {i + 1}" for i in range(len(data_text))])
    st.markdown(f"### Checked Data Text ({selected_file})")
    display_text(data_text[int(selected_file.split()[-1]) - 1])

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
    for word_info in text:
        if word_info['isPlagiarism']:
            st.markdown(f"<font color='red'>{word_info['word']}</font> ", unsafe_allow_html=True)
        else:
            st.text(word_info['word'] + (" " if not word_info['isNewLine'] else "\n"))

if __name__ == "__main__":
    main()
