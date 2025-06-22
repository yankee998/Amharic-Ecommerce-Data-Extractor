import pandas as pd
import nltk
import os

# Ensure NLTK data is downloaded
nltk.download('punkt')

# Load data
input_file = 'output/preprocessed/content.csv' if os.path.exists('output/preprocessed/content.csv') else 'output/processed/raw_telegram_data.csv'
df = pd.read_csv(input_file)
messages = df['text'].head(30).tolist()  # Take first 30 messages

# Tokenize and prepare CoNLL template
output_lines = []
for msg in messages:
    if not isinstance(msg, str):
        continue
    tokens = nltk.word_tokenize(msg)
    for token in tokens:
        # Placeholder label (to be manually edited)
        output_lines.append(f"{token} O")
    output_lines.append("")  # Blank line between messages

# Save to file
os.makedirs('output/labeled', exist_ok=True)
with open('output/labeled/conll_labeled_data.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
print("CoNLL template saved to output/labeled/conll_labeled_data.txt. Please manually label the entities.")