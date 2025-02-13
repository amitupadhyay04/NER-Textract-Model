import spacy
import logging
from api.model.ml_model import detectText  # Importing detectText from ml_model.py

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InitiateNER:
    def __init__(self):
        # Load a pre-trained SpaCy model for Named Entity Recognition
        logging.info("Loading SpaCy model 'en_core_web_sm'...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logging.info("SpaCy model loaded successfully.")
        except OSError as e:
            logging.error("Error loading SpaCy model. Ensure 'en_core_web_sm' is installed.")
            raise e

    def train_model(self, training_data):
        # Placeholder for training logic
        logging.debug("train_model called, but no logic implemented yet.")
        pass
    
    def predict(self, text):
        # Log the input text length to avoid logging large text
        logging.debug(f"Received input text with length: {len(text)} characters")

        if not text.strip():
            logging.warning("Empty input text received.")
            raise ValueError("Input text cannot be empty.")

        # Process the input text
        doc = self.nlp(text)
        logging.info("Text processed with SpaCy NER model.")

        # Extract named entities
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = [(ent.text, (ent.start_char, ent.end_char))]
            else:
                entities[ent.label_].append((ent.text, (ent.start_char, ent.end_char)))

        # Log the number of entities extracted instead of full content
        logging.info(f"Extracted {len(entities)} entity types.")
        return entities

# Debugging Example
# if __name__ == "__main__":
#     ner_model = InitiateNER()

#     # Example of using detectText from ml_model to extract text from an image
#     image_path = r'C:\Users\amitu\scanPlus-main\scanPlus-main\api\images\p2.png'
#     extracted_text = detectText(image_path)  # Extract text from the image

#     logging.info(f"Extracted text from image: {extracted_text[:100]}...")  # Log only the first 100 chars for brevity

#     # Perform NER on the extracted text
#     predictions = ner_model.predict(extracted_text)

#     # Log the final predictions (number of entities) instead of full details
#     logging.info(f"Final predictions returned to API: {len(predictions)} entity types extracted.")
