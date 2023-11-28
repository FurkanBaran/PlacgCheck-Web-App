import streamlit as st
import string

def check_plagiarism(text, db_text, n):
    check_text = []
    plag_count = 0

    for i in range(n - 1):
        check_text.append(text[i])

    text_len = len(text)

    for id in range(text_len - n):
        check_text.append(text[id + n])
        for file_id in range(len(db_text)):
            for j in range(len(db_text[file_id]) - n):
                if check_text == db_text[file_id][j:j + n]:
                    for k in range(n):
                        text[id + k]['isPlagiarism'] = True
                        db_text[file_id][j + k]['isPlagiarism'] = 1
        check_text.pop(0)

    return text

def main():
    st.title("Plagiarism Checker")

    uploaded_file = st.file_uploader("Upload your text file", type=["txt"])

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("Selected Document", content, height=300)

        n = st.slider("Select Level (N)", min_value=3, max_value=7, value=3)
        st.button("Check Plagiarism", on_click=lambda: check_and_display(content, n))

def check_and_display(text_content, n):
    text = preprocess_text(text_content)
    db_text = preprocess_db_text()  # You need to implement the function that loads your database text

    text = check_plagiarism(text, db_text, n)

    st.text_area("Checked Document", display_text(text), height=300)

def preprocess_text(text_content):
    text_lines = text_content.split('\n')
    text = []

    for line in text_lines:
        for word in line.split():
            text.append({'word': word, 'isPlagiarism': False, 'isNewLine': True})
            text[-1]['word'] = word.translate(str.maketrans('', '', string.punctuation)).lower()

    return text

def display_text(text):
    result = ""
    for word_info in text:
        result += word_info['word'] + (" " if not word_info['isNewLine'] else "\n")
    return result

if __name__ == "__main__":
    main()
