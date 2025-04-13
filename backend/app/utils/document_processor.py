import os
import pypdf
import docx
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#downloading nltk data 
nltk.download('punkt',quiet=True)
nltk.download('stopwords', quiet=True)

#loading in spaCy model
#installing small english model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    #direct download if there is an error
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            #initialize pdf reader object
            pdf_reader = pypdf.PdfReader(file)
            #iterating through every page in the pdf
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        #different encoding if UTF-8 encoding fails
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from TXT: {e}")
        return ""

def extract_text(file_path):
    file_extension = os.path.splittext(file_path)[1].lower()
    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)
    elif file_extension == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def preprocess_text(text):
    #remove leading and trailing white space
    text = text.strip()
    #remove whitespace
    #regular expressions model
    import re
    #replaces all white space characters with a single space
    text = re.sub(r'\s+',' ', text)
    return text

def advanced_preprocess(text):
    doc = nlp(text)
    #remove all stopwords and punctuation
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    #only return lemmatized tokens for specific use cases
    #lemmatize texts 
    lemmatized_text = " ".join(lemmatized_tokens)
    cleaned_text = " ".join(tokens)
    return {
        "full_text": text,
        "cleaned_text": cleaned_text,
        "lemmatized_text": lemmatized_text,
        "sentences": [sent.text for sent in doc.sents ]
    }