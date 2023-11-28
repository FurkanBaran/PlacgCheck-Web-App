import streamlit as st
import string

N=3 
text=[]         # main text list, [word]
text_gui=[]     # main text list for gui, [word, isPlagiarism, newLine ]
db_text=[]      # database text list    [File] [Word] 
db_gui=[]       # db text list for gui, [File] [word, isPlagiarism, newLine ]
file_dict={}    # file list dictionary, keys=file name, values=file id

def open_file():
    filepath = st.file_uploader("Upload a text file", type=["txt"])
    text.clear()                                                          # clear the main text list
    text_gui.clear()                                                      # clear main text_gui list 
    text_file=open(filepath,'r',encoding="utf-8")                         # open selected file as reading mode
    text_lines=text_file.readlines()                                      # read lines
    word_id=0                                                             # words count variable

    if filepath is not None:
        text = read_file(filepath)
        return text
    return None

def open_files():
    filepaths = st.file_uploader("Upload data files", type=["txt"], accept_multiple_files=True)
    if filepaths:
        return [read_file(file) for file in filepaths]
    return None

def read_file(file):
    text_file=open(filepath,'r',encoding="utf-8")                         # open selected file as reading mode
    text_lines=text_file.readlines()                                      # read lines    
    for line in text_lines:                                               # for each line 
        for word in  line.split():                                                              # for each word
                text.append( )   # append the word's simple and lowercase version (without punctuation) to text list
                text_gui.append([word,False, False])                                                # append the word and its plagiarism values (false initially) to text_gui list
                word_id+=1                                                                          # increase the word id (index) by 1
        text_gui[word_id-1][2]=True                                                             # set newline for this word as True


def main():
    st.title("Plagiarism Check with Streamlit")

    text = open_file()
    if text is None:
        st.warning("Please upload a text file.")
        return

    db_text = open_files()
    if db_text is None:
        st.warning("Please upload data files.")
        return

    N = st.slider("Select Level (N)", min_value=3, max_value=7, value=3)
    
    if st.button("Check"):
        check(text, db_text, N)

    if st.button("Search"):
        search()

if __name__ == "__main__":
    main()
