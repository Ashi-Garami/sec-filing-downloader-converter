# SEC Filing Downloader & Converter

Download SEC 10-Q and 10-K filings and convert them to text format for analysis.

## Requirements
- Python 3.7 or higher
- Install dependencies: `pip install requests beautifulsoup4 lxml`

## Scripts Included

### 1. download_filings.py
Downloads 10-Q (quarterly) and 10-K (annual) filings from SEC EDGAR database.

**Usage:**
```bash
python download_filings.py
```
- Enter a stock ticker when prompted (e.g., AAPL, MSFT, TSLA)
- Downloads 8 most recent 10-Q filings
- Downloads 3 most recent 10-K filings
- Creates separate folders: `TICKER_10-Q_Filings` and `TICKER_10-K_Filings`

### 2. convert_to_text.py
Converts downloaded HTML files to plain text format for upload to NotebookLM or other analysis tools.

**Usage:**
```bash
python convert_to_text.py
```
- Automatically finds all folders containing "10-Q" or "10-K" in their name
- Converts all .htm and .html files to .txt format
- Saves text files in the same folder as the HTML files
- Ready to upload to NotebookLM!

## Workflow

1. **Download filings:**
```bash
   python download_filings.py
```
   
2. **Convert to text:**
```bash
   python convert_to_text.py
```

3. **Upload to NotebookLM** - Use the generated .txt files for AI-powered analysis

## Notes
- Both scripts work on Windows, Mac, and Linux
- HTML files can be opened in any web browser
- Text files preserve all content but remove HTML formatting
- Folder names are flexible - any folder with "10-Q" or "10-K" will be detected

## Troubleshooting
- **403 Forbidden errors:** Make sure you've added your email to the User-Agent header
- **No files found:** Check that you're running the script in the same directory as your filing folders
- **Import errors:** Run `pip install requests beautifulsoup4`
