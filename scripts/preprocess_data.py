import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import re
import os

# Load raw data
df = pd.read_csv('output/processed/raw_telegram_data.csv', encoding='utf-8')

def preprocess_amharic_text(text):
    if not isinstance(text, str):
        return []
    # Preserve Amharic characters
    text = re.sub(r'[^\w\s\u1200-\u137F]', '', text)
    tokens = word_tokenize(text)
    return tokens

# Apply preprocessing
df['tokens'] = df['text'].apply(preprocess_amharic_text)
df_metadata = df[['channel', 'message_id', 'date', 'views', 'sender_id', 'photo_path']]
df_content = df[['message_id', 'text', 'tokens']]
os.makedirs('output/preprocessed', exist_ok=True)
df_metadata.to_csv('output/preprocessed/metadata.csv', index=False, encoding='utf-8')
df_content.to_csv('output/preprocessed/content.csv', index=False, encoding='utf-8')
print("Preprocessed data saved to output/preprocessed/")