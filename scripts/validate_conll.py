def validate_conll(file_path):
    valid_labels = {'B-Product', 'I-Product', 'B-LOC', 'I-LOC', 'B-PRICE', 'I-PRICE', 'O'}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) != 2:
                print(f"Error at line {i+1}: Expected token and label, got {line}")
            elif parts[1] not in valid_labels:
                print(f"Error at line {i+1}: Invalid label {parts[1]}")
        else:
            continue
    print("CoNLL file validation complete.")

if __name__ == '__main__':
    validate_conll('data/labeled/labeled_data.conll')