import cv2
import string
import re
import os
from datetime import datetime
from PIL import Image
import pytesseract
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk, pos_tag
import spacy
import numpy as np
import os
import logging 

logging.getLogger('nltk').setLevel(logging.CRITICAL)

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('stopwords')

# Load Spacy's English Model
nlp = spacy.load('en_core_web_sm')

# Instantiate the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# OCR

class OCRProcessor:
    def __init__(self):
        self.image_path = None

    def preprocess_image(self, image_path):
        """
        This function will preprocess the image to improve OCR read quality.
        """
        # Check if the file exists
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"The file {image_path} does not exist.")
            
        # Read the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding for handling different light conditions
        thresholded_image = cv2.adaptiveThreshold(grayscale_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                  cv2.THRESH_BINARY, 11, 2)

        # No need to save the preprocessed image
        # Return the thresholded image directly
        return thresholded_image

    def ocr_core(self, filename):
        """
        This function will handle the core OCR processing of images.
        """
        try:
            # Preprocess the image
            preprocessed_image = self.preprocess_image(filename)

            # Perform OCR on the preprocessed image
            img = Image.fromarray(preprocessed_image)
            text = pytesseract.image_to_string(img)
        except Exception as e:
            print(f"Error processing image: {filename}")
            print(f"Error: {str(e)}")
            text = ""

        return text

class MetadataExtractor(OCRProcessor):
    
    def filter_text(self, text):
        # Filter out non-text characters and punctuation
        filtered_text = ''.join(filter(lambda x: x in string.printable and x not in string.punctuation, text))
        return filtered_text

    def preprocess_text(self, text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [lemmatizer.lemmatize(w) for w in word_tokens if not w in stop_words]
        return " ".join(filtered_text)
    
    def extract_keywords(self,text):
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        keywords = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in stop_words and word.isalpha()]
        return keywords

    def extract_entities(self, text):
        doc = nlp(text)
        entity_dict = {}
        for ent in doc.ents:
            entity_dict.setdefault(ent.label_, []).append(ent.text)
        return entity_dict

    def extract_file_metadata(self, filename):
        file_stats = os.stat(filename)
        metadata = {
            "filename": filename,
            "created": datetime.fromtimestamp(file_stats.st_ctime).strftime("%d/%m/%y, %H:%M:%S"),
            "size": file_stats.st_size
        }
        return metadata

    def extract_metadata(self, filename):
        text = self.ocr_core(filename)
        text = self.filter_text(text)
        text = self.preprocess_text(text)

        entities = self.extract_entities(text)
        extra_text = str(self.extract_keywords(text))  # Extract extra entities
        file_metadata = self.extract_file_metadata(filename)
        
        for key in entities:
            file_metadata[key] = entities[key]
            
        file_metadata['extra_entities'] = extra_text  # Add extra entities to file metadata

        return file_metadata


if __name__ == "__main__":
    extractor = MetadataExtractor()
    metadata = extractor.extract_metadata("ocr2.png")
    output_text = "\n".join([f"{key}: {metadata[key]}" for key in metadata])
    print(output_text)
