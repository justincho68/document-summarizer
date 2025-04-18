from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab')
nltk.download('stopwords', quiet=True)

#summarizer class with multiple methods for user to select which type
#of summary they would like
#extractive - consistent with the original text - returns most important parts
#abstractive - model will understand the text and summarize in unique words

class Summarizer:
    def __init__(self):
        #initializer all transformer models to load later
        self.abstractive_model = None
        self.abstractive_tokenizer = None
        #try to default to gpu if the machine has one
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.stop_words = set(stopwords.words('english'))

    def load_abstractive_model(self):
        #only load model if there was not one in use
        if self.abstractive_model is None:
            model_name = "facebook/bart-large-cnn"
            self.abstractive_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.abstractive_model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
            summary = self.summarization_pipeline = pipeline(
                "summarization",
                model = self.abstractive_model,
                tokenizer = self.abstractive_tokenizer,
                device=0 if self.device == "cuda" else -1
            )
    #extractive summary - only include the most important sentences in the original text
    def extractive_summarize(self, text, ratio=0.3):
        #TF-IDF model to summarize text
        #Args text = text to summarize
        #ratio = ratio of sentences to keep in the summary
        #returns summary
        sentences = sent_tokenize(text)
        if len(sentences) <= 3:
            return text
        #using tf-idf model to calculate the sentences that will be the summary
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences)
        #sentence scores to determine what will be included in the summary
        #form [0.1, 0.8, 0.3, 0.6]
        #argsort will put in ascending order -> [0,2,3,1]
        sentence_scores = np.array([tfidf_matrix].sum() for i in range(len(sentences)))
        #number of sentences to be included in the summary
        num_sentences = max(3, int(len(sentences) * ratio))
        top_indices = sentence_scores.argsort()[-num_sentences:]
        top_indices = sorted(top_indices)
        #combine the top sentences that will be the summary
        summary = ' '.join([sentences[i] for i in top_indices])
        return summary

    def abstractive_summarize(self, text, max_length=150, min_length=50):
        #abstractive summarize using pre trained model
        self.load_abstractive_model()

        max_input_length = 1024
        if len(text.split()) > max_input_length:
            #shorten if it is too long 
            text = self.extractive_summarize(text, ratio=0.5)
        summary = self.summarization_pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']
        return summary

    #combination
    def hybrid_summarize(self, text, max_length=150, min_length=50, ratio=0.3):
        extractive_summary = self.extractive_summarize(text, ratio=ratio)
        abstractive_summary = self.abstractive_summarize(
            extractive_summary if len(text.split()) > 1024 else text,
            max_length=max_length,
            min_length=min_length
        )
        return {
            "extractive_summary": extractive_summary,
            "abstractive_summary": abstractive_summary
        }