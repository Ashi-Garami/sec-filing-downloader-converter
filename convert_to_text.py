from pathlib import Path
from bs4 import BeautifulSoup


def convert_html_to_text(html_file):
    """Convert one HTML file to text."""
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
    
    # Use BeautifulSoup to extract just the text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    # Create the output filename (same name but .txt instead of .htm)
    output_file = html_file.with_suffix('.txt')
    
    # Save the text
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return output_file


def main():
    print("HTML to Text Converter\n")
    
    # Get the current folder
    current_folder = Path.cwd()
    
    # Find all HTML files in 10-Q and 10-K subfolders
    html_files = list(current_folder.glob("*_10-Q_Filings/*.htm"))
    html_files += list(current_folder.glob("*_10-Q_Filings/*.html"))
    html_files += list(current_folder.glob("*_10-K_Filings/*.htm"))
    html_files += list(current_folder.glob("*_10-K_Filings/*.html"))
    
    if not html_files:
        print("No HTML files found in *_10-Q_Filings or *_10-K_Filings folders")
        print(f"Current directory: {current_folder}")
        return
    
    print(f"Found {len(html_files)} HTML files\n")
    
    # Convert each file
    for html_file in html_files:
        print(f"Converting: {html_file.name}")
        text_file = convert_html_to_text(html_file)
        print(f"  → Created: {text_file.name}\n")
    
    print("Done! All HTML files have been converted to .txt files")
    print("You can now upload the .txt files to NotebookLM")


if __name__ == "__main__":
    main()