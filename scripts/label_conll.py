import pandas as pd
import nltk
import re
import os

# Ensure NLTK data
nltk.download('punkt')

# Common Amharic terms
product_keywords = {'ልጆች', 'ጫማ', 'ማቀዝቀዣ', 'ቦርሳ', 'ልብስ', 'ቲሸርት', 'ስልክ', 'ባትሪ', 'ሰዓት'}
location_keywords = {'አዲስ', 'አበባ', 'ቦሌ', 'መርካቶ', 'ፒያሳ', 'አዳማ', 'ባህር', 'ዳር'}
price_indicators = {'ዋጋ', 'በ', 'ብር'}

def label_token(token, prev_token, next_token):
    # Price: Look for numbers or "ዋጋ"/"ብር" patterns
    if re.match(r'^\d+$', token) or token in {'ብር'}:
        if prev_token in price_indicators or next_token in price_indicators:
            return 'I-PRICE' if prev_token in price_indicators else 'B-PRICE'
    elif token in price_indicators:
        return 'B-PRICE'
    # Location: Match known locations
    elif token in location_keywords:
        return 'I-LOC' if prev_token in location_keywords else 'B-LOC'
    # Product: Match known products
    elif token in product_keywords:
        return 'I-Product' if prev_token in product_keywords else 'B-Product'
    return 'O'

# Load data
input_file = 'output/preprocessed/content.csv' if os.path.exists('output/preprocessed/content.csv') else 'output/processed/raw_telegram_data.csv'
df = pd.read_csv(input_file)
messages = df['text'].head(50).tolist()  # Take 50 messages

# Label messages
output_lines = []
for msg in messages:
    if not isinstance(msg, str):
        continue
    tokens = nltk.word_tokenize(msg)
    for i, token in enumerate(tokens):
        prev_token = tokens[i-1] if i > 0 else ''
        next_token = tokens[i+1] if i < len(tokens)-1 else ''
        label = label_token(token, prev_token, next_token)
        output_lines.append(f"{token} {label}")
    output_lines.append("")  # Blank line

# Save to file
os.makedirs('output/labeled', exist_ok=True)
with open('output/labeled/conll_labeled_data.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
print("Labeled data saved to output/labeled/conll_labeled_data.txt")