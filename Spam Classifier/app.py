import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import re

# Initialize Porter Stemmer
ps = PorterStemmer()

# Stop words ko set mein convert karna
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()  # Text ko lowercase mein convert karo
    text = re.sub(r'\d+', '', text)  # Digits hatao
    text = re.sub(r'[^\w\s]', '', text)  # Punctuation hatao
    text = re.sub(r'\s+', ' ', text)  # Extra spaces hatao
    text = ' '.join([ps.stem(word) for word in text.split() if word not in stop_words])  # Stopwords hatao aur stemming apply karo
    return text

# Load CountVectorizer and Model
cv = pickle.load(open("CountVectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

# Title of the app
st.title("Email/SMS Spam Classifier")

# User input for the message
input_sms = st.text_input("Enter the message")

# Add a Predict button
if st.button('Predict'):
    if input_sms:  # If input is provided
        # 1. Process (clean the text)
        transform_sms = clean_text(input_sms)

        # 2. Vectorize
        vector_input = cv.transform([transform_sms])

        # 3. Predict
        result = model.predict(vector_input)[0]

        # 4. Display result
        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")
    else:
        st.error("Please enter a message first!")
