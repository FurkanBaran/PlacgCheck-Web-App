
# Plagiarism Checker Web App

This Flask application provides a web-based interface for plagiarism detection. It was developed upon request as a simple project to address specific needs. Users can upload a primary text file along with multiple source files. The application will compare the primary text against the sources to identify any potential plagiarism, highlighting suspected portions in red. This tool aims to offer a direct and effective way to spot similarities in textual content, tailored to educational and preliminary research contexts.
**Live demo**: https://plgtest.vercel.app/

## Features

- File upload for a primary text file and multiple source files.
- Plagiarism detection based on customizable N-gram comparison.
- Highlighting of plagiarized text in the user interface.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/FurkanBaran/PlagCheck-Web-App.git
   cd PlagCheck-Web-App
2.  **Set Up a Virtual Environment** (optional, but recommended)
     
    ``python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate` `` 
    
3.  **Install Requirements**
 
    
    `pip install -r requirements.txt` 
    
 

## Usage

To start the server:

`flask run` 

Open a web browser and navigate to `http://127.0.0.1:5000/` to access the application.

### Uploading Files

-   Navigate to the main page.
-   Use the file input fields to select one main file and multiple source files.
-   Set the N value for N-gram comparison.
-   Submit the form to see the plagiarism detection results.



## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Furkan Baran - furkanbaran021@gmail.com
##
Project Link: [https://github.com/FurkanBaran/PlagCheck-Web-App]
Live demo: https://plgtest.vercel.app/
