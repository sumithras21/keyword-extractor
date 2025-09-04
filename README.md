# Keyword Extractor Tool

A Python-based Keyword Extractor Tool that uses Natural Language Processing (NLP) techniques to identify important keywords from any text input.  
Built with Flask, NLTK, and Scikit-learn, it removes stopwords, calculates TF-IDF scores, and provides a simple web interface for easy interaction.


##  Features
- Extracts keywords automatically from text
- Removes common stopwords using NLTK
- Uses TF-IDF for keyword ranking
- Simple Flask web interface
- Easy installation with `requirements.txt`


##  Installation & Setup

### 1. Clone the Repository

git clone https://github.com/your-username/keyword-extractor.git
cd keyword-extractor


### 2. Install Dependencies

pip install -r requirements.txt


### 3. Download NLTK Stopwords

python -m nltk.downloader stopwords


## 4. Run the Application

Start the Flask server: python app.py

Then open your browser and go to: http://127.0.0.1:5000


##  Project Structure


keyword-extractor/
│-- app.py                 # Main Flask application
│-- requirements.txt       # Project dependencies
│-- templates/             # HTML templates
│-- static/                # CSS, JS files
│-- README.md              # Project documentation

## Example Usage

Input Text: Python is a popular programming language widely used in AI and data science.

Extracted Keywords: python, programming, language, ai, data, science


##  Contributing

Pull requests are welcome!


##  License

This project is licensed under the MIT License.
