# Amharic E-commerce Data Extractor

Welcome to the **Amharic E-commerce Data Extractor**, a project designed to scrape and analyze e-commerce data from Ethiopian Telegram channels, preprocess the data, and label it for Named Entity Recognition (NER) to identify **Products**, **Prices**, and **Locations** in Amharic text. This project is part of a data science initiative to understand e-commerce trends in Ethiopia.

## 🚀 Project Overview

- **Objective**: Extract product listings from Telegram channels, preprocess the data, and label entities in CoNLL format for NER tasks.
- **Dataset**: Uses data from [Shageronlinestore Google Drive](https://drive.google.com/drive/folders/1hcTasx2JP69YhE8jMJtPr3frRHlJwVtm) and [Amharic NER dataset](https://github.com/uhh-lt/ethiopicmodels/blob/master/am/data/NER/train.txt).
- **Tasks Completed**:
  - **Task 1**: Data ingestion and preprocessing.
  - **Task 2**: Automatic labeling of 50 messages in CoNLL format.
- **Repository**: [GitHub](https://github.com/yankee998/Amharic-Ecommerce-Data-Extractor)

## 📂 Project Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   └── __init__.py
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
├── scripts/
│   ├── __init__.py
│   ├── README.md
│   ├── process_existing_data.py
│   ├── telegram_scraper.py
│   ├── preprocess_data.py
│   ├── label_conll.py
├── venv/
└── output/
    ├── data/
    │   ├── channels_to_crawl.xlsx
    │   ├── telegram_data.xls
    │   ├── telegram_scraper.py
    │   ├── photos.zip
    │   ├── ner_train.txt
    ├── processed/
    │   ├── existing_telegram_data.csv
    │   ├── raw_telegram_data.csv
    ├── preprocessed/
    │   ├── metadata.csv
    │   ├── content.csv
    ├── previews/
    └── labeled/
        └── conll_labeled_data.txt
```

## 🛠️ Setup Instructions

### Prerequisites
- **Python**: 3.13.3
- **VS Code**: Recommended with Python extension.
- **PowerShell**: For running commands on Windows.
- **Telegram API Credentials**: Obtain from [my.telegram.org](https://my.telegram.org).

### Installation
1. **Clone the Repository**:
   ```powershell
   git clone https://github.com/yankee998/Amharic-Ecommerce-Data-Extractor.git
   cd Amharic-Ecommerce-Data-Extractor
   ```

2. **Set Up Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
   Dependencies (`requirements.txt`):
   ```
   telethon==1.36.0
   pandas==2.2.3
   nltk==3.9.1
   aiohttp==3.10.5
   openpyxl==3.1.5
   ```

4. **Download NLTK Data**:
   ```powershell
   python -m nltk.downloader punkt
   ```

5. **Add Telegram API Credentials**:
   - Get `api_id`, `api_hash`, and `phone` from [my.telegram.org](https://my.telegram.org).
   - Update `scripts/telegram_scraper.py` with your credentials:
     ```python
     api_id = YOUR_ACTUAL_API_ID  # Integer
     api_hash = 'YOUR_ACTUAL_API_HASH'  # String
     phone = 'YOUR_PHONE_NUMBER'  # String, e.g., '+251912345678'
     ```

6. **Place Sample Data**:
   - Download from [Shageronlinestore Google Drive](https://drive.google.com/drive/folders/1hcTasx2JP69YhE8jMJtPr3frRHlJwVtm):
     - `channels_to_crawl.xlsx`
     - `telegram_data.xls`
     - `telegram_scraper.py`
     - `photos.zip`
   - Download [ner_train.txt](https://github.com/uhh-lt/ethiopicmodels/blob/master/am/data/NER/train.txt) from GitHub.
   - Move to `output/data/`:
     ```powershell
     New-Item -ItemType Directory -Path output\data -Force
     Move-Item -Path $HOME\Downloads\channels_to_crawl.xlsx -Destination output\data\
     Move-Item -Path $HOME\Downloads\telegram_data.xls -Destination output\data\
     Move-Item -Path $HOME\Downloads\telegram_scraper.py -Destination output\data\
     Move-Item -Path $HOME\Downloads\photos.zip -Destination output\data\
     Move-Item -Path $HOME\Downloads\ner_train.txt -Destination output\data\
     ```

## 🚀 Usage

1. **Task 1: Data Ingestion and Preprocessing**:
   - Process existing data:
     ```powershell
     .\venv\Scripts\python.exe scripts\process_existing_data.py
     ```
     Output: `output/processed/existing_telegram_data.csv`
   - Scrape Telegram channels:
     ```powershell
     .\venv\Scripts\python.exe scripts\telegram_scraper.py
     ```
     Output: `output/processed/raw_telegram_data.csv`, images in `output/previews/`
   - Preprocess text:
     ```powershell
     .\venv\Scripts\python.exe scripts\preprocess_data.py
     ```
     Output: `output/preprocessed/metadata.csv`, `output/preprocessed/content.csv`

2. **Task 2: Label Dataset in CoNLL Format**:
   - Automatically label 50 messages:
     ```powershell
     .\venv\Scripts\python.exe scripts\label_conll.py
     ```
     Output: `output/labeled/conll_labeled_data.txt`
   - Example CoNLL format:
     ```
     ልጆች B-Product
     ጫማ I-Product
     በ O
     አዲስ B-LOC
     አበባ I-LOC
     ዋጋ B-PRICE
     1000 I-PRICE
     ብር I-PRICE
     ```

3. **View Results**:
   - Check labeled data in `output/labeled/conll_labeled_data.txt`.
   - Inspect CSVs in `output/processed/` and `output/preprocessed/` using VS Code or Excel.

## 📊 Next Steps
- **Task 3**: Fine-tune an NER model using `output/labeled/conll_labeled_data.txt` and `output/data/ner_train.txt`.
- Improve Amharic tokenization with tools like `amseg`.
- Enhance labeling accuracy with machine learning.

## 🐛 Troubleshooting
- **API Errors**: Ensure valid credentials in `telegram_scraper.py`.
- **File Not Found**: Verify `output/data/` contains all sample files.
- **Encoding Issues**: Files use UTF-8; check for BOM or corruption.
- **NLTK Issues**: Run `python -m nltk.downloader punkt`.

## 📚 Resources
- [Telethon Documentation](https://docs.telethon.dev/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NLTK Documentation](https://www.nltk.org/)
- [Amharic NER Dataset](https://github.com/uhh-lt/ethiopicmodels)
- [GitHub Repository](https://github.com/yankee998/Amharic-Ecommerce-Data-Extractor)

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## 📜 License
This project is licensed under the MIT License.

---

**Happy Scraping!** 🎉 For issues, contact via [GitHub Issues](https://github.com/yankee998/Amharic-Ecommerce-Data-Extractor/issues).