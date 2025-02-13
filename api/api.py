import sys
import os
import json
from flask import Flask, request, jsonify
import logging  # For logging debug messages

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.model.ner_spacy import *  # Import from the 'model' package
from api.model.ml_model import detectText  # Importing detectText from ml_model.py
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow all origins

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
ner_model = InitiateNER()
@app.route("/scan", methods=["POST"])
def scan():
    try:
        logging.debug("Received a request at '/scan' endpoint.")
        
        # Retrieve the file path from the request form data
        file_path = request.form["path"]
        logging.debug(f"File path received: {file_path}")

        # Extract text from the image using detectText (from ml_model.py)
        extracted_text = detectText(file_path)
        logging.debug(f"Extracted text: {extracted_text}")

        # Perform NER on the extracted text
        ner_result = ner_model.predict(extracted_text)
        logging.debug(f"NER result: {json.dumps(ner_result, indent=4)}")

        # Prepare a clean response for the frontend
        formatted_result = {}
        for label, entities in ner_result.items():
            formatted_result[label] = [entity[0] for entity in entities]

        # Log the formatted result
        logging.debug(f"Formatted NER result: {json.dumps(formatted_result, indent=4)}")
        print(formatted_result)
        return jsonify(formatted_result)
    
    except Exception as e:
        logging.error("An error occurred in the '/scan' endpoint", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        # Initialize and load the NER model
        logging.debug("Initializing NER model.")
        ner_model = InitiateNER()
        logging.debug("NER model initialized successfully.")
        
        # Start the Flask application
        logging.debug("Starting the Flask app.")
        app.run(debug=True, port=6000)
    except Exception as e:
        logging.critical("Failed to start the Flask application", exc_info=True)
