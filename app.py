from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

main_text = []      # main text list [word]
main_gui = []       # main text gui list [word, isPlagiarism?, isNewLine?]
source_texts = []   # source text list [file] [word]
source_gui = []     # source text gui list [file] [word, isPlagiarism?, isNewLine?]
plag_ratio=0.0

file_dict = {}      # dictionary that holds file names {file_id: file name}


def read_file(file_content):
    main_text.clear()
    main_gui.clear()
    text_lines = file_content.splitlines()
    word_id = 0
    for line in text_lines:
        for word in line.split():
            main_text.append(word.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~‘’“”""")).lower())
            main_gui.append([word, False, False])
            word_id += 1
        main_gui[word_id - 1][2] = True


def read_files(file_contents):
    source_gui.clear()
    source_texts.clear()
    file_id = 0
    for file_content in file_contents:
        source_texts.append([])
        source_gui.append([])
        text_lines = file_content.splitlines()
        word_id = 0
        for line in text_lines:
            for word in line.split():
                source_gui[file_id].append([word, 0, False])
                source_texts[file_id].append(word.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”""")).lower())
                word_id += 1
            source_gui[file_id][word_id - 1][2] = True
        file_id += 1



def deleteGUI():
    for word in main_gui:    
        word[1]=False
    for file in  (source_gui):
        for word in file:
            word[1]=0

@app.route('/recheck', methods=['GET', 'POST'])
def recheck():
    print(main_text)
    if request.method == 'POST':
        deleteGUI()
        N = int(request.form.get('N'))
        result = check(N)
        return render_template('result.html', result=result, files=file_dict, mainfile=mainfilename, plag_ratio=plag_ratio//1, N=N)


def check(N):
    n = N - 1 # N sayının bir eksiği, eklenecek kelime ilk kelimeden N-1 kelime sonraki kelime olacaktır # one less than N, the added word will be the N-1th word from the first word
    main_N= main_text[:N-1].copy() # we add the first N-1 words to the main_N list, the reason we don't add N words is that the next word will be added in the loop
    main_len = len(main_text) 
    for id in range(main_len - n):
        main_N.append(main_text[id + n])  # we add the next word to the main_N list
        for file_id in range(len(source_texts)): # loop as many times as the number of files
            for j in range(len(source_texts[file_id]) - n): # loop as many times as the number of words in the file -1
                if main_N == source_texts[file_id][j:j + N]: # if the main_N list is equal to the consecutive N words of the source word list
                    for k in range(N): # we mark each word in a loop of N
                        main_gui[id + k][1] = True # in the list containing the unconverted form of main_text for the interface, the 1st index of the word takes the value True (plagiarism) (the 0th index holds the word)     
                        main_gui[id + k][2] = [file_id, j + k] # in the list containing the unconverted form of main_text for the interface, the 2nd index of the word holds the file and word number where the plagiarism occurred. [file_id, word_id]
                        source_gui[file_id][j + k][1] = True  # in the list containing the unconverted form of the source word list for the interface, the 1st index of the word takes the value 1 (plagiarism) (the 0th index holds the word)
        main_N.pop(0) # we remove the first element of the main_N list, so that a new word can be added
    return [ html_format(i) for i in range(-1, len(source_gui))]



def html_format(fileid):
    
    if fileid == -1:
        main_html = []
        text_len = len(main_text)
        main_html.append("<p> ")
        plag_count = 0
        word_count = 0
        global plag_ratio
        for word in range(text_len):
            if main_gui[word][1] == False:
                main_html.append(main_gui[word][0] + " ")
                word_count += 1
            else:
                main_html.append('<a href="#w{}-{}" style="color:red;">{}</a> '.format(main_gui[word][2][0]+1 , main_gui[word][2][1], main_gui[word][0]))
                plag_count += 1
                word_count += 1
            if main_gui[word][2] == True:
                main_html.append("</p><p>")
        plag_ratio = (plag_count / word_count) * 100
        return "".join(main_html) # adds <p> tag to the beginning and end of the text
    else:
        comp_text = []
        lenn = len(source_gui[fileid])
        comp_text.append( "<h2>#{} - {}</h2>  <p> ".format(fileid +1,file_dict[fileid]))
        for word in range(lenn):
            if source_gui[fileid][word][1] == 0:
                comp_text.append(source_gui[fileid][word][0] + " ")
            elif source_gui[fileid][word][1] == 1:
                comp_text.append('<span id="w{}-{}" style="color:red;">{}</span> '.format(fileid+1,word,source_gui[fileid][word][0]))
            if source_gui[fileid][word][2] == 1:
                comp_text.append("</p><p>")
        return "".join(comp_text)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        N = int(request.form.get('N'))
        global mainfilename
        mainfile = request.files.get('mainfile')
        otherfiles = request.files.getlist('otherfiles')

        if not mainfile or not otherfiles:
            return render_template('index.html', error='No files selected.')

        if allowed_file(mainfile.filename):
            file_content = mainfile.read().decode('utf-8')
            file_dict[-1] = mainfile.filename
            mainfilename = mainfile.filename
            read_file(file_content)
        else: 
            return render_template('index.html', error='Invalid file type.')    


        file_contents = []
        for i, file in enumerate(otherfiles):
            if allowed_file(file.filename):
                file_contents.append(file.read().decode('utf-8'))
                file_dict[i] = file.filename
        print(file_dict)
        read_files(file_contents)

        result = check(N)
        return render_template('result.html', result=result, files=file_dict, mainfile=mainfile.filename, plag_ratio=plag_ratio//1, N=N)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)









