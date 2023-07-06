# MetaScan 🖼️: Image Scanning 📸 and Metadata Management 📚

## Project Overview 🎯

MetaScan is an innovative prototype solution 🔧 crafted to streamline the management of extensive scanned document archives 📂. It resolves the typical issues of document organization and retrieval 🧩 by establishing a robust metadata archival system 🗃️. Beyond just digitising documents, MetaScan intelligently identifies 🔍, extracts, and archives crucial information from each scanned document 📝. This feature significantly simplifies document retrieval, empowering users to find specific documents based on their content, not just their titles 🔖. By enhancing how we archive and retrieve scanned documents, MetaScan aims to drastically boost efficiency and productivity in environments where document scanning is a regular necessity 🏢.

*This project is created as a demo submission 📥 for the upcoming Ubuntu Summit 2023 along with my ongoing [work](https://github.com/michaelrsweet/pappl/pull/249) for PAPPL.*

## Workflow ⚙️

1) **Document Scanning:** 📄 The user initiates the process by scanning a document using the built-in scanner interface in MetaScan, powered by the Python-based SANE library 🐍. In case you do not have the scanner you can still test the application using the test scanning process which takes a random image from the testImages folder 🗂️. The scan currently is configured for a default of 300 dpi.

2) **OCR Processing:** 📖 Once the document is scanned, the Tesseract OCR engine is employed to convert the image into readable-text format. This step allows us extract the necessary text information present in the image and which can be further used for metadata analysis 📊.

3) **Metadata Extraction:** 🔍 The converted text is then analysed using various natural language processing (NLP) techniques. Processes like stop word removal, lemmatisation, and named entity recognition, enable MetaScan to extract valuable metadata from the document 📈.

4) **Archiving:** 🗂️ Following the extraction, the metadata along with the scanned image is stored in an SQLite database. This compact and powerful database ensures efficient storage and quick retrieval of the documents 🗃️.

5) **Data Access via Backend Server:** 💻 The Flask-based backend server exposes the data in the SQLite database , allowing interaction between the backend and the frontend 🔄.

6) **User Interaction via Frontend:** 👥 Users interact with the MetaScan system through a simple user-friendly frontend designed with React. Here, they can view, navigate, and manage their digitised documents 📑.

7) **Document Retrieval:** 🔍 To find a specific document, users utilise the search tool that leverages the metadata to locate documents. This process greatly simplifies document retrieval, as users can search based on the content of the documents rather than relying solely on file names 🔖.

MetaScan ensures a seamless transition from a physical document to a digitised, easily retrievable version stored safely within an integrated metadata archival system 🌐.

## Tech Stack 🏗️:

- **Python** 🐍: Core scripting language
- **SANE Library** 📚: Scanner interfacing
- **Tesseract**: 📖 OCR processing
- **NLP Techniques** 🧠: Lemmatisation , Stop word removal , Named Entity Recognition
- **SQLite** 🗄️: Data storage and retrieval
- **Flask** 🔥: Backend server setup
- **React** ⚛️: Frontend user interface

## Getting Started 🚀

1. **Clone the repository from GitHub** 📋 <br>
    ```bash
   

git clone https://github.com/Kappuccino111/MetaScan.git
    ```
  
2. **Navigate to the project directory** 📁 <br>
    ```bash
    cd MetaScan
    ```
  
3. **Create a virtual environment** 🌐<br>
    ```python
    python3 -m venv your_env_name
    ```

4. **Activate the virtual environment** 💡<br>
     On macOS and Linux:
     ```bash
     source env/bin/activate 
     ```

5. **Install the required Python packages** 📦
  
    ```python
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

6. **Installing Tesseract Binaries** 📖

    - On Linux
    ```python
    sudo apt install tesseract-ocr
    sudo apt install libtesseract-dev
    ```
     
    -  On macOS
    ```python
    brew install tesseract
    ```

7. **Installing SANE binaries** 📚

    - On Linux
    ```bash
    sudo apt get install sane
    sudo apt-get install sane sane-utils libsane-extras xsane
    ```
    
    - On macOS
    ```bash
    brew install sane-backends
    ```

8. **Setup the front-end server** ⚙️

    a) **Node.js and npm Installation** 🟢
    
      - **On macOS**
        
        ```bash
        brew install node
        ```
      
      -  **On Ubuntu/Linux**
          
          ```bash
          sudo apt-get update
          sudo apt-get install nodejs npm
          ```
    
    b) **Setup the React Server** ⚛️
      ```bash
      cd front-end
      npm install 
      ```

9. **Run the Application** 🏃

    The application can be run using 
    ```bash
    ./run.py
    ```
    
    **OR**
    ```python
    python3 run.py
    ```

## Future Packaging 📦

The prototype for MetaScan has been developed in Python 🐍, with the project's design executed to accommodate future expansion and compatibility with other programming languages, such as C or C++. Each component of the code has been designed to be individually extractable, which enables the enhancement of specific functions or components without impacting the entire system.

The future scope includes the creation of a wrapper to facilitate integration with C or C++ code. This will allow us to leverage Scanning libraries being developed in these languages, such as for PAPPL or other open-source scanning software, thereby extending MetaScan's capabilities and enhancing its performance 🚀.

## Current Work 🚧

I am currently working on making a **Sandboxed-Scanner Application Framework for PAPPL**.
The PR for ongoing work can be found [here](https://github.com/michaelrsweet/pappl/pull/249).
