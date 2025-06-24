import pandas as pd
import regex as re
import os

def parse_ner_train(file_path):
    place_names = set()
    location_phrases = []
    current_phrase = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                token, label = line.split()
                if label == 'B-LOC':
                    place_names.add(token)
                    if current_phrase:
                        location_phrases.append(current_phrase)
                    current_phrase = [token]
                elif label == 'I-LOC' and current_phrase:
                    current_phrase.append(token)
                else:
                    if current_phrase:
                        location_phrases.append(current_phrase)
                        current_phrase = []
            else:
                if current_phrase:
                    location_phrases.append(current_phrase)
                    current_phrase = []
    if current_phrase:
        location_phrases.append(current_phrase)
    return place_names, location_phrases

def load_product_keywords():
    return {'ሙዝ', 'ጫማ', 'ልብስ', 'ቦርሳ', 'ቲሸርት', 'ኮት'}

def label_tokens(tokens, place_names, location_phrases, product_keywords):
    labeled_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Multi-token location phrases
        matched_phrase = False
        for phrase in location_phrases:
            phrase_length = len(phrase)
            if i + phrase_length <= len(tokens) and tokens[i:i + phrase_length] == phrase:
                labeled_tokens.append((tokens[i], 'B-LOC'))
                for j in range(1, phrase_length):
                    labeled_tokens.append((tokens[i + j], 'I-LOC'))
                i += phrase_length
                matched_phrase = True
                break
        if matched_phrase:
            continue
        # Price detection
        if re.match(r'በ[0-9]+', token) or (i + 1 < len(tokens) and tokens[i + 1] == 'ብር'):
            labeled_tokens.append((token, 'B-PRICE'))
            if i + 1 < len(tokens) and tokens[i + 1] == 'ብር':
                labeled_tokens.append((tokens[i + 1], 'I-PRICE'))
                i += 2
            else:
                i += 1
        # Single-token location
        elif token in place_names:
            labeled_tokens.append((token, 'B-LOC'))
            if i + 1 < len(tokens) and tokens[i + 1] in place_names:
                labeled_tokens.append((tokens[i + 1], 'I-LOC'))
                i += 2
            else:
                i += 1
        # Product detection
        elif token in product_keywords:
            labeled_tokens.append((token, 'B-Product'))
            if i + 1 < len(tokens) and tokens[i + 1] in {'ለልጆች', 'ለሴቶች', 'ለወንዶች'}:
                labeled_tokens.append((tokens[i + 1], 'I-Product'))
                i += 2
            else:
                i += 1
        else:
            labeled_tokens.append((token, 'O'))
            i += 1
    return labeled_tokens

def generate_conll(input_path, ner_train_path, output_path):
    place_names, location_phrases = parse_ner_train(ner_train_path)
    product_keywords = load_product_keywords()
    df = pd.read_csv(input_path, encoding='utf-8')
    with open(output_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            tokens = eval(row['tokens']) if isinstance(row['tokens'], str) else row['tokens']
            labeled_tokens = label_tokens(tokens, place_names, location_phrases, product_keywords)
            for token, label in labeled_tokens:
                f.write(f"{token} {label}\n")
            f.write("\n")
    print(f"CoNLL file saved to {output_path}")

if __name__ == '__main__':
    os.makedirs('data/labeled', exist_ok=True)
    generate_conll(
        'data/processed/preprocessed_data.csv',
        'data/ner_train.txt',
        'data/labeled/labeled_data.conll'
    )