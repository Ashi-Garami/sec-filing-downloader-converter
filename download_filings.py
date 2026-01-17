from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re


def get_filings(ticker, filing_type, count=8):
    """Retrieve filings for a given ticker and filing type (10-Q or 10-K)."""
    base_url = "https://www.sec.gov"
    search_url = (
        f"{base_url}/cgi-bin/browse-edgar"
        f"?action=getcompany&CIK={ticker}&type={filing_type}&count={count}"
        f"&owner=exclude&output=atom"
    )
    headers = {"User-Agent": "YourName Contact@example.com"}
    
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "xml")
    entries = soup.find_all("entry")
    
    filings = []
    for entry in entries:
        filing_date = entry.find("filing-date").text
        accession_number = entry.find("accession-number").text
        filing_href = entry.find("link")["href"]
        
        doc_link = _get_document_link(filing_href, headers, base_url, filing_type)
        
        filings.append({
            "filing_date": filing_date,
            "accession_number": accession_number,
            "filing_url": filing_href,
            "document_link": doc_link,
        })
    
    return filings


def _get_document_link(filing_href, headers, base_url, filing_type):
    """Extract the primary document link from a filing page."""
    try:
        filing_page = requests.get(filing_href, headers=headers)
        filing_soup = BeautifulSoup(filing_page.content, "html.parser")
        
        docs_table = filing_soup.find("table", class_="tableFile")
        if not docs_table:
            return None
        
        # Search for the filing type in lowercase
        search_term = filing_type.lower()
        
        for row in docs_table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 4:
                doc_type = cols[3].text.strip().lower()
                
                if search_term in doc_type and "graphic" not in doc_type:
                    doc_link_tag = cols[2].find("a")
                    if doc_link_tag:
                        doc_href = doc_link_tag.get("href", "")
                        if doc_href:
                            full_url = base_url + doc_href
                            if "/ix?doc=" in full_url:
                                match = re.search(r'doc=(/Archives/edgar/data/[^\s]+)', full_url)
                                if match:
                                    return base_url + match.group(1)
                            return full_url
        
        return None
    except Exception as e:
        print(f"Error fetching document link: {e}")
        return None


def download_documents(filings, ticker, filing_type):
    """Download all available documents to a local folder."""
    folder = Path(f"{ticker.upper()}_{filing_type}_Filings")
    folder.mkdir(exist_ok=True)
    
    headers = {"User-Agent": "YourName Contact@example.com"}
    
    for filing in filings:
        url = filing["document_link"]
        if not url:
            print(f"Skipping {filing['filing_date']} - no document found")
            continue
        
        if url.endswith(".htm") or url.endswith(".html"):
            ext = "htm"
        elif url.endswith(".pdf"):
            ext = "pdf"
        else:
            ext = "htm"
            
        filename = f"{ticker.upper()}_{filing_type}_{filing['filing_date']}.{ext}"
        filepath = folder / filename
        
        print(f"Downloading: {filename}")
        try:
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
            
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"  ✓ Successfully downloaded")
        except requests.RequestException as e:
            print(f"  ✗ Failed: {e}")
    
    return folder


if __name__ == "__main__":
    ticker = input("Enter stock ticker: ").strip().upper()
    
    print(f"\n{'='*60}")
    print(f"Downloading filings for {ticker}")
    print('='*60)
    
    # Download 10-Q filings
    print(f"\n--- Searching for 10-Q filings ---")
    tenq_filings = get_filings(ticker, "10-Q", count=9)
    
    if not tenq_filings:
        print(f"No 10-Q filings found for {ticker}")
    else:
        print(f"Found {len(tenq_filings)} 10-Q filings\n")
        tenq_folder = download_documents(tenq_filings, ticker, "10-Q")
        print(f"\n10-Q files saved to: {tenq_folder.absolute()}")
    
    # Download 10-K filings
    print(f"\n--- Searching for 10-K filings ---")
    tenk_filings = get_filings(ticker, "10-K", count=3)
    
    if not tenk_filings:
        print(f"No 10-K filings found for {ticker}")
    else:
        print(f"Found {len(tenk_filings)} 10-K filings\n")
        tenk_folder = download_documents(tenk_filings, ticker, "10-K")
        print(f"\n10-K files saved to: {tenk_folder.absolute()}")
    
    print(f"\n{'='*60}")
    print("Download complete!")
    print('='*60)