import pandas as pd
import regex as re
import os

def preprocess_amharic_text(text):
    if not isinstance(text, str):
        return []
    # Normalize: remove extra spaces, keep Amharic script and punctuation
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove non-Amharic characters except spaces and punctuation
    text = re.sub(r'[^\u1200-\u137F\s.,!?]', '', text)
    # Tokenize: split on spaces and ensure multi-token phrases are separated
    tokens = []
    for token in text.split():
        # Further split if tokens are concatenated (e.g., መገናኛመሰረት)
        sub_tokens = re.findall(r'[\u1200-\u137F]+', token)
        tokens.extend(sub_tokens)
    return tokens

def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path, encoding='utf-8')
    df['tokens'] = df['text'].apply(preprocess_amharic_text)
    df['metadata'] = df[['channel', 'message_id', 'date', 'sender', 'views']].to_dict('records')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df[['channel', 'message_id', 'date', 'sender', 'views', 'text', 'tokens']].to_csv(output_path, index=False, encoding='utf-8')
    print(f"Preprocessed data saved to {output_path}")

if __name__ == '__main__':
    preprocess_data('data/raw/telegram_data.csv', 'data/processed/preprocessed_data.csv')