import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import re
from typing import Dict, List, Optional
import time

# KAMIS URL
KAMIS_BASE_URL = "https://kamis.kilimo.go.ke"
KAMIS_MARKET_URL = f"{KAMIS_BASE_URL}/site/market"

# Product IDs for key commodities
KAMIS_PRODUCTS = {
    "tomatoes": {"id": 61, "name": "Tomatoes"},
    "onions": {"id": 158, "name": "Dry Onions"},
    "sukuma": {"id": 154, "name": "Kales/Sukuma Wiki"},
    "cabbage": {"id": 58, "name": "Cabbages"},
    "maize": {"id": 1, "name": "Dry Maize"},
    "beans": {"id": 29, "name": "Beans Red Haricot (Wairimu)"}
}

# Data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

# Track if initial download has been done
INITIAL_DOWNLOAD_MARKER = os.path.join(DATA_DIR, ".kamis_initial_download_complete")


def download_commodity_data(product_id: int, per_page: int = 3000, export_excel: bool = True) -> pd.DataFrame:
    """
    Downloads KAMIS data for a specific commodity using product ID.
    
    Args:
        product_id: KAMIS product ID (e.g., 61 for Tomatoes)
        per_page: Number of rows to fetch (default 3000 for historical, 100 for daily)
        export_excel: Whether to get Excel export format
        
    Returns:
        DataFrame with commodity data
    """
    try:
        # Build URL with product ID and pagination
        params = {
            'product': product_id,
            'per_page': per_page
        }
        
        if export_excel:
            params['export'] = 'excel'
        
        url = f"{KAMIS_MARKET_URL}"
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"  Downloading product ID {product_id} ({per_page} rows)...")
        response = session.get(url, params=params, timeout=60)
        response.raise_for_status()
        
        if export_excel and len(response.content) > 500:
            # Save temporarily and read as Excel
            temp_path = os.path.join(DATA_DIR, f"temp_product_{product_id}.xlsx")
            os.makedirs(DATA_DIR, exist_ok=True)
            
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            df = pd.read_excel(temp_path, engine='openpyxl')
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            print(f"  ✅ Downloaded {len(df)} rows for product {product_id}")
            return df
        else:
            # Parse HTML table as fallback
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            
            if table:
                rows = []
                for tr in table.find_all('tr')[1:]:  # Skip header
                    cells = [td.get_text().strip() for td in tr.find_all('td')]
                    if cells:
                        rows.append(cells)
                
                if rows:
                    headers = [th.get_text().strip() for th in table.find('thead').find_all('th')]
                    df = pd.DataFrame(rows, columns=headers)
                    print(f"  ✅ Scraped {len(df)} rows for product {product_id}")
                    return df
            
            print(f"  ⚠️ No data found for product {product_id}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"  ❌ Error downloading product {product_id}: {e}")
        return pd.DataFrame()


def download_all_commodities_historical(per_page: int = 3000) -> str:
    """
    Downloads historical data (up to 3000 rows) for all key commodities.
    This should be run once for initial data load.
    
    Args:
        per_page: Number of historical rows to fetch (default 3000)
        
    Returns:
        Path to the saved Excel file with all commodity data
    """
    print(f"Downloading historical data ({per_page} rows per commodity)...")
    print("=" * 70)
    
    all_data = []
    
    for crop_key, product_info in KAMIS_PRODUCTS.items():
        print(f"\n{product_info['name']}:")
        df = download_commodity_data(product_info['id'], per_page=per_page)
        
        if not df.empty:
            # Add crop identifier
            df['crop_category'] = crop_key
            all_data.append(df)
            time.sleep(1)  # Be nice to the server
    
    if not all_data:
        raise Exception("Failed to download any commodity data")
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Save to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(DATA_DIR, f"kamis_historical_{timestamp}.xlsx")
    
    combined_df.to_excel(output_path, index=False, engine='openpyxl')
    
    print("\n" + "=" * 70)
    print(f"✅ Downloaded {len(combined_df)} total rows")
    print(f"✅ Saved to: {output_path}")
    
    # Mark initial download as complete
    with open(INITIAL_DOWNLOAD_MARKER, 'w') as f:
        f.write(datetime.now().isoformat())
    
    return output_path


def download_todays_data() -> str:
    """
    Downloads only today's data for all key commodities.
    This should be used for daily updates after initial historical download.
    
    Returns:
        Path to the saved Excel file with today's data
    """
    print("Downloading today's data...")
    print("=" * 70)
    
    all_data = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    for crop_key, product_info in KAMIS_PRODUCTS.items():
        print(f"\n{product_info['name']}:")
        # Use smaller per_page for daily updates
        df = download_commodity_data(product_info['id'], per_page=100)
        
        if not df.empty:
            # Filter for today's date if Date column exists
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                today_data = df[df['Date'].dt.strftime('%Y-%m-%d') == today].copy()
                
                if not today_data.empty:
                    today_data['crop_category'] = crop_key
                    all_data.append(today_data)
                    print(f"  Found {len(today_data)} rows for today ({today})")
                else:
                    print(f"  No data for today ({today})")
            else:
                # If no date column, just take recent data
                recent_data = df.head(10).copy()
                recent_data['crop_category'] = crop_key
                all_data.append(recent_data)
        
        time.sleep(0.5)  # Be nice to the server
    
    if not all_data:
        print("⚠️ No data found for today. Using recent data instead.")
        # Fallback: get recent data without date filter
        for crop_key, product_info in KAMIS_PRODUCTS.items():
            df = download_commodity_data(product_info['id'], per_page=50)
            if not df.empty:
                df['crop_category'] = crop_key
                all_data.append(df.head(10))
    
    if not all_data:
        raise Exception("Failed to download any data")
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Save to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(DATA_DIR, f"kamis_daily_{timestamp}.xlsx")
    
    combined_df.to_excel(output_path, index=False, engine='openpyxl')
    
    print("\n" + "=" * 70)
    print(f"✅ Downloaded {len(combined_df)} rows for today")
    print(f"✅ Saved to: {output_path}")
    
    return output_path


def needs_initial_download() -> bool:
    """
    Check if initial historical download has been completed.
    
    Returns:
        True if initial download is needed, False otherwise
    """
    return not os.path.exists(INITIAL_DOWNLOAD_MARKER)


def download_kamis_excel(output_path: Optional[str] = None) -> str:
    """
    Downloads the full KAMIS market data as Excel file.
    The website has an "Export to Excel" functionality that we can trigger.
    
    To get ALL data, we need to request with a large page size parameter.
    
    Returns:
        Path to the downloaded Excel file
    """
    print("Downloading KAMIS data...")
    
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        # Set up session
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # The KAMIS export URL with parameters to get ALL data
        # Based on the web results, the export URL is: /site/market?&export=excel
        # We need to add a parameter to get all entries (not just first 10)
        excel_urls_to_try = [
            f"{KAMIS_MARKET_URL}?iDisplayLength=5000&export=excel",  # Request 5000 rows
            f"{KAMIS_MARKET_URL}?length=5000&export=excel",
            f"{KAMIS_MARKET_URL}?export=excel&length=5000",
            f"{KAMIS_MARKET_URL}?export=excel",  # Fallback to basic export
        ]
        
        excel_response = None
        successful_url = None
        
        for excel_url in excel_urls_to_try:
            try:
                print(f"Trying: {excel_url}")
                response = session.get(excel_url, timeout=60)
                if response.status_code == 200 and len(response.content) > 1000:
                    excel_response = response
                    successful_url = excel_url
                    break
            except Exception as e:
                print(f"  Failed: {e}")
                continue
        
        if not excel_response:
            print("Excel export failed. Trying table scraping...")
            # Fallback to scraping the page directly
            response = session.get(KAMIS_MARKET_URL, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            return scrape_kamis_table_to_excel(soup, output_path)
        
        # Save the Excel file
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DATA_DIR, f"kamis_data_{timestamp}.xlsx")
        
        with open(output_path, 'wb') as f:
            f.write(excel_response.content)
        
        print(f"✅ KAMIS data downloaded from: {successful_url}")
        print(f"✅ Saved to: {output_path}")
        
        # Check the file size
        file_size = os.path.getsize(output_path)
        print(f"   File size: {file_size:,} bytes")
        
        return output_path
        
    except Exception as e:
        print(f"Error downloading Excel: {e}")
        print("Falling back to table scraping...")
        
        # Fallback: scrape the table
        try:
            response = requests.get(KAMIS_MARKET_URL, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            return scrape_kamis_table_to_excel(soup, output_path)
        except Exception as e2:
            print(f"Error in fallback scraping: {e2}")
            raise


def scrape_kamis_ajax_data(output_path: Optional[str] = None) -> str:
    """
    Scrapes KAMIS data via the DataTables AJAX endpoint for complete data.
    This is more reliable than HTML scraping as it gets all data directly.
    
    Args:
        output_path: Path to save the Excel file
        
    Returns:
        Path to the saved Excel file
    """
    print("Scraping KAMIS via AJAX endpoint...")
    
    try:
        # DataTables often uses an AJAX endpoint
        # Common patterns: /site/market/data, /site/market?ajax=1, etc.
        ajax_endpoints = [
            f"{KAMIS_BASE_URL}/site/market/data",
            f"{KAMIS_MARKET_URL}?ajax=1",
            f"{KAMIS_MARKET_URL}/data",
        ]
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        # Parameters to request all data
        params = {
            'iDisplayStart': 0,
            'iDisplayLength': 10000,  # Request many rows
            'sEcho': 1
        }
        
        data = None
        for endpoint in ajax_endpoints:
            try:
                response = session.get(endpoint, params=params, timeout=30)
                if response.status_code == 200:
                    json_data = response.json()
                    if 'aaData' in json_data or 'data' in json_data:
                        data = json_data
                        print(f"✅ Successfully fetched data from: {endpoint}")
                        break
            except:
                continue
        
        if not data:
            raise Exception("Could not fetch data from AJAX endpoints")
        
        # Extract data
        rows = data.get('aaData') or data.get('data', [])
        
        if not rows:
            raise Exception("No data in AJAX response")
        
        # Create DataFrame
        # Assuming standard KAMIS columns
        columns = ['Commodity', 'Classification', 'Grade', 'Sex', 'Market', 
                  'Wholesale', 'Retail', 'Supply Volume', 'County', 'Date']
        
        df = pd.DataFrame(rows, columns=columns)
        
        # Save to Excel
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DATA_DIR, f"kamis_data_{timestamp}.xlsx")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"✅ Scraped {len(df)} rows via AJAX and saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"AJAX scraping failed: {e}")
        raise


def scrape_kamis_table_to_excel(soup: Optional[BeautifulSoup] = None, output_path: Optional[str] = None) -> str:
    """
    Scrapes the KAMIS table data and saves it as Excel.
    This is a fallback method that scrapes the HTML table directly.
    
    Args:
        soup: BeautifulSoup object (if already loaded)
        output_path: Path to save the Excel file
        
    Returns:
        Path to the saved Excel file
    """
    print("Scraping KAMIS table data from HTML...")
    
    try:
        # First try AJAX method
        try:
            return scrape_kamis_ajax_data(output_path)
        except Exception as e:
            print(f"AJAX method failed: {e}")
            print("Falling back to HTML scraping...")
        
        # HTML scraping fallback
        if soup is None:
            response = requests.get(KAMIS_MARKET_URL, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the data table
        table = soup.find('table') or soup.find('table', {'id': 'DataTables_Table_0'})
        
        if not table:
            raise Exception("Could not find data table on page")
        
        # Extract table data
        headers = []
        header_row = table.find('thead')
        if header_row:
            headers = [th.get_text().strip() for th in header_row.find_all('th')]
        
        if not headers:
            # Try to get headers from first row
            first_row = table.find('tr')
            if first_row:
                headers = [td.get_text().strip() for td in first_row.find_all(['th', 'td'])]
        
        # Extract data rows
        rows = []
        tbody = table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                row_data = [td.get_text().strip() for td in tr.find_all('td')]
                if row_data:
                    rows.append(row_data)
        else:
            # If no tbody, get all rows except first (header)
            all_rows = table.find_all('tr')[1:]
            for tr in all_rows:
                row_data = [td.get_text().strip() for td in tr.find_all('td')]
                if row_data:
                    rows.append(row_data)
        
        if not rows:
            print("Warning: No rows found in HTML table. The table might be loaded via JavaScript.")
            print("You may need to wait a moment and try again, or the data might be unavailable.")
        
        # Create DataFrame
        if headers and rows:
            df = pd.DataFrame(rows, columns=headers)
        elif rows:
            df = pd.DataFrame(rows)
        else:
            # Create empty DataFrame with at least the structure
            df = pd.DataFrame(columns=['Commodity', 'Classification', 'Grade', 'Sex', 'Market', 
                                      'Wholesale', 'Retail', 'Supply Volume', 'County', 'Date'])
            print("Warning: Created empty DataFrame. Data might be loaded dynamically.")
        
        # Save to Excel
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DATA_DIR, f"kamis_data_{timestamp}.xlsx")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"✅ Scraped {len(df)} rows from HTML and saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error scraping table: {e}")
        raise


def download_kamis_by_commodity(commodity: str) -> pd.DataFrame:
    """
    Downloads KAMIS data for a specific commodity by searching/filtering.
    
    Args:
        commodity: Name of commodity to search for
        
    Returns:
        DataFrame with the commodity data
    """
    print(f"Searching for commodity: {commodity}...")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Try to download with commodity filter
        # The URL might accept a search parameter
        search_urls = [
            f"{KAMIS_MARKET_URL}?search={commodity}&export=excel",
            f"{KAMIS_MARKET_URL}?sSearch={commodity}&export=excel",
            f"{KAMIS_MARKET_URL}?iDisplayLength=5000&sSearch={commodity}&export=excel",
        ]
        
        for url in search_urls:
            try:
                response = session.get(url, timeout=30)
                if response.status_code == 200 and len(response.content) > 1000:
                    # Save temporarily and read
                    temp_path = os.path.join(DATA_DIR, f"temp_{commodity}.xlsx")
                    with open(temp_path, 'wb') as f:
                        f.write(response.content)
                    
                    df = pd.read_excel(temp_path, engine='openpyxl')
                    os.remove(temp_path)
                    
                    # Check if we got relevant data
                    if 'Commodity' in df.columns:
                        matches = df[df['Commodity'].str.contains(commodity, case=False, na=False)]
                        if not matches.empty:
                            print(f"  Found {len(matches)} entries for {commodity}")
                            return matches
                    
                    print(f"  No matches found in response from: {url}")
            except Exception as e:
                print(f"  Failed: {e}")
                continue
        
        print(f"  Could not find data for {commodity}")
        return pd.DataFrame()
        
    except Exception as e:
        print(f"Error downloading commodity data: {e}")
        return pd.DataFrame()


def scrape_kamis_by_scraping_page() -> pd.DataFrame:
    """
    Scrapes KAMIS data directly from the webpage for our target commodities.
    Makes multiple requests to get data for different commodities.
    
    Returns:
        Combined DataFrame with all commodity data
    """
    print("Scraping KAMIS page for target commodities...")
    
    all_data = []
    
    # Target commodities and their search terms
    targets = {
        'Tomatoes': ['Tomato', 'Tomatoes'],
        'Kales': ['Kale', 'Sukuma', 'Sukuma Wiki'],
        'Onions': ['Onion', 'Onions', 'Dry Onion'],
        'Cabbage': ['Cabbage', 'Cabbages']
    }
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Get the main page
    response = session.get(KAMIS_MARKET_URL, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to find all data in the page source or table
    table = soup.find('table')
    if table:
        # Extract all visible data
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip header
            cells = [td.get_text().strip() for td in tr.find_all('td')]
            if cells:
                rows.append(cells)
        
        if rows:
            headers = [th.get_text().strip() for th in table.find('thead').find_all('th')] if table.find('thead') else None
            if headers:
                df = pd.DataFrame(rows, columns=headers)
                all_data.append(df)
    
    # Combine all data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"Scraped {len(combined_df)} rows from page")
        return combined_df
    
    return pd.DataFrame()


def get_cached_prices_for_today() -> Optional[Dict]:
    """
    Check if we've already scraped today and return cached prices.
    
    Returns:
        Dictionary with prices if today's data exists, None otherwise
    """
    today_str = datetime.now().strftime("%Y%m%d")
    
    # Look for today's data file
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check for daily file from today
    for filename in os.listdir(DATA_DIR):
        if filename.startswith(f"kamis_daily_{today_str}") and filename.endswith(".xlsx"):
            file_path = os.path.join(DATA_DIR, filename)
            
            # Check if file is recent (created today)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time.date() == datetime.now().date():
                print(f"✅ Found today's cached data: {filename}")
                try:
                    # Read and extract prices from cached file
                    df = pd.read_excel(file_path, engine='openpyxl')
                    prices = extract_nairobi_prices(df)
                    prices['source'] = 'cache'
                    prices['cached_file'] = filename
                    print(f"📦 Using cached prices from today")
                    return prices
                except Exception as e:
                    print(f"⚠️  Error reading cached file: {e}")
                    continue
    
    return None


def scrape_kamis(force_refresh: bool = False) -> Dict:
    """
    Scrapes KAMIS website for Nairobi wholesale prices.
    Returns a dictionary with date and prices for Tomato, Sukuma Wiki, Onion, and Cabbage.
    
    Smart caching strategy:
    - Checks if data has already been scraped today
    - If yes: Returns cached data (fast)
    - If no or force_refresh: Performs fresh scrape
    
    Smart download strategy:
    1. First time: Downloads 3000 historical rows per commodity
    2. Subsequent times: Downloads only today's data for efficiency
    3. Extracts Nairobi prices for target crops
    4. Falls back to reasonable defaults if needed
    
    Args:
        force_refresh: If True, bypasses cache and performs fresh scrape
    """
    print("Scraping KAMIS for Nairobi prices...")
    print("=" * 70)
    
    # Check for cached data (unless force refresh)
    if not force_refresh:
        cached_prices = get_cached_prices_for_today()
        if cached_prices:
            print("=" * 70)
            return cached_prices
        else:
            print("ℹ️  No cached data for today, performing fresh scrape...")
    else:
        print("🔄 Force refresh requested, bypassing cache...")
    
    try:
        # Check if we need initial historical download
        if needs_initial_download():
            print("\n🔄 Initial download: Fetching historical data (3000 rows per commodity)...")
            excel_path = download_all_commodities_historical(per_page=3000)
        else:
            print("\n🔄 Daily update: Fetching today's data only...")
            excel_path = download_todays_data()
        
        # Read the downloaded data
        df = pd.read_excel(excel_path, engine='openpyxl')
        
        print(f"\n📊 Processing {len(df)} rows...")
        
        # Extract Nairobi prices for our target crops
        prices = extract_nairobi_prices(df)
        
        if prices.get('source') == 'kamis':
            print(f"\n✅ Successfully extracted prices from KAMIS")
            return prices
        else:
            print(f"\n⚠️ Using default prices (crops not found in data)")
            return prices
        
    except Exception as e:
        print(f"\n❌ Error in scrape_kamis: {e}")
        print("Using fallback default prices...")
        
        # Fallback to reasonable defaults if scraping fails
        today = datetime.now().strftime("%Y-%m-%d")
        prices = {
            "date": today,
            "tomato": 80,
            "sukuma": 45,
            "onion": 100,
            "cabbage": 35,
            "source": "fallback"
        }
        return prices


def extract_nairobi_prices(df: pd.DataFrame) -> Dict:
    """
    Extracts Nairobi wholesale prices for key crops from the KAMIS data.
    
    Args:
        df: DataFrame with KAMIS data
        
    Returns:
        Dictionary with prices for tomato, sukuma, onion, and cabbage
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize prices
    prices = {
        "date": today,
        "tomato": None,
        "sukuma": None,
        "onion": None,
        "cabbage": None,
        "maize": None,
        "beans": None,
        "source": "kamis"
    }
    
    # Normalize column names
    df.columns = [col.lower().strip() for col in df.columns]
    
    # Check if we have crop_category column (from our new download method)
    if 'crop_category' in df.columns:
        # Use crop_category for easier matching
        crop_mapping = {
            "tomato": "tomatoes",
            "sukuma": "sukuma",
            "onion": "onions",
            "cabbage": "cabbage",
            "maize": "maize",
            "beans": "beans"
        }
        
        for key, category in crop_mapping.items():
            # Filter for this crop category
            crop_data = df[df['crop_category'] == category]
            
            if not crop_data.empty:
                # Filter for Nairobi if county column exists
                if 'county' in df.columns:
                    nairobi_data = crop_data[crop_data['county'].str.lower().str.contains('nairobi', na=False, case=False)]
                    if not nairobi_data.empty:
                        crop_data = nairobi_data
                
                # Or filter by market
                if 'market' in df.columns:
                    nairobi_markets = crop_data[crop_data['market'].str.lower().str.contains('nairobi|gikomba|wakulima|kangemi|kawangware', na=False, case=False)]
                    if not nairobi_markets.empty:
                        crop_data = nairobi_markets
                
                # Get the most recent entry with wholesale price
                if 'wholesale' in df.columns:
                    # Sort by date if available
                    if 'date' in df.columns:
                        crop_data = crop_data.sort_values('date', ascending=False)
                    
                    # Get wholesale prices and calculate average
                    wholesale_prices = []
                    for _, row in crop_data.head(5).iterrows():  # Take average of top 5 most recent
                        price = extract_price_value(row.get('wholesale'))
                        if price and price > 0:
                            wholesale_prices.append(price)
                    
                    if wholesale_prices:
                        avg_price = round(sum(wholesale_prices) / len(wholesale_prices))
                        prices[key] = avg_price
                        print(f"  ✅ {key.capitalize()}: KSh {avg_price}/kg (avg of {len(wholesale_prices)} prices)")
    
    else:
        # Fallback to old method: match by commodity name
        crop_mapping = {
            "tomato": ["tomato", "tomatoes"],
            "sukuma": ["kale", "sukuma", "sukuma wiki"],
            "onion": ["onion", "onions", "dry onion"],
            "cabbage": ["cabbage", "cabbages"],
            "maize": ["maize", "dry maize"],
            "beans": ["beans", "bean"]
        }
        
        for key, crop_names in crop_mapping.items():
            for crop_name in crop_names:
                if 'commodity' in df.columns:
                    mask = df['commodity'].str.lower().str.contains(crop_name, na=False, case=False)
                    
                    # Filter by county if available
                    if 'county' in df.columns:
                        mask = mask & df['county'].str.lower().str.contains('nairobi', na=False, case=False)
                    elif 'market' in df.columns:
                        mask = mask & df['market'].str.lower().str.contains('nairobi|gikomba', na=False, case=False)
                    
                    crop_data = df[mask]
                    
                    if not crop_data.empty:
                        if 'wholesale' in df.columns:
                            price_str = crop_data.iloc[0]['wholesale']
                            price = extract_price_value(price_str)
                            if price:
                                prices[key] = price
                                print(f"  ✅ {key.capitalize()}: KSh {price}/kg")
                                break
    
    # Fill in any missing prices with reasonable defaults
    defaults = {
        "tomato": 80,
        "sukuma": 45,
        "onion": 100,
        "cabbage": 35,
        "maize": 50,
        "beans": 120
    }
    
    any_defaults_used = False
    for key, default_price in defaults.items():
        if prices[key] is None:
            if key in ["tomato", "sukuma", "onion", "cabbage"]:  # Only warn for main crops
                print(f"  ⚠️  {key.capitalize()}: No Nairobi price found, using default KSh {default_price}/kg")
            prices[key] = default_price
            any_defaults_used = True
    
    # Update source if we used defaults
    if any_defaults_used:
        prices["source"] = "kamis_with_defaults"
    
    return prices


def extract_price_value(price_str: str) -> Optional[float]:
    """
    Extracts numeric price value from a string like "45.00/Kg" or "50.00".
    
    Args:
        price_str: String containing price
        
    Returns:
        Float price value or None
    """
    if not price_str or price_str == '-':
        return None
    
    try:
        # Remove currency symbols, /Kg, etc.
        price_str = str(price_str).replace('KSh', '').replace('/Kg', '').replace(',', '').strip()
        
        # Extract first number
        match = re.search(r'(\d+(?:\.\d+)?)', price_str)
        if match:
            return float(match.group(1))
    except:
        pass
    
    return None


def get_latest_kamis_file() -> Optional[str]:
    """
    Gets the path to the most recently downloaded KAMIS file.
    
    Returns:
        Path to the latest KAMIS Excel file or None
    """
    try:
        if not os.path.exists(DATA_DIR):
            return None
        
        kamis_files = [
            os.path.join(DATA_DIR, f) 
            for f in os.listdir(DATA_DIR) 
            if f.startswith('kamis_data_') and f.endswith('.xlsx')
        ]
        
        if not kamis_files:
            return None
        
        # Sort by modification time
        kamis_files.sort(key=os.path.getmtime, reverse=True)
        return kamis_files[0]
        
    except Exception as e:
        print(f"Error getting latest KAMIS file: {e}")
        return None


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 70)
    print("KAMIS Scraper Test")
    print("=" * 70)
    
    # Check if user wants to force initial download
    if len(sys.argv) > 1 and sys.argv[1] == '--initial':
        print("\n🔄 Forcing initial historical download...")
        if os.path.exists(INITIAL_DOWNLOAD_MARKER):
            os.remove(INITIAL_DOWNLOAD_MARKER)
            print("✅ Reset initial download marker")
    
    # Show download status
    if needs_initial_download():
        print("\n📥 Status: Initial download will be performed (3000 rows per commodity)")
    else:
        print("\n📥 Status: Daily update mode (today's data only)")
        marker_time = os.path.getmtime(INITIAL_DOWNLOAD_MARKER) if os.path.exists(INITIAL_DOWNLOAD_MARKER) else None
        if marker_time:
            marker_date = datetime.fromtimestamp(marker_time).strftime("%Y-%m-%d %H:%M:%S")
            print(f"   Initial download completed: {marker_date}")
    
    print("\n" + "-" * 70)
    
    # Test the scraper
    prices = scrape_kamis()
    
    print("\n" + "=" * 70)
    print("📊 EXTRACTED PRICES (Nairobi Wholesale)")
    print("=" * 70)
    
    # Main crops
    main_crops = ["tomato", "sukuma", "onion", "cabbage"]
    for crop in main_crops:
        if crop in prices and prices[crop] is not None:
            print(f"  🌾 {crop.capitalize():.<20} KSh {prices[crop]}/kg")
    
    # Additional crops
    if "maize" in prices and prices["maize"]:
        print(f"  🌽 {'Maize':.<20} KSh {prices['maize']}/kg")
    if "beans" in prices and prices["beans"]:
        print(f"  🫘 {'Beans':.<20} KSh {prices['beans']}/kg")
    
    print(f"\n  📅 Date: {prices['date']}")
    print(f"  📡 Source: {prices.get('source', 'kamis')}")
    print("=" * 70)
    
    # Show latest file info
    latest_file = get_latest_kamis_file()
    if latest_file:
        file_size = os.path.getsize(latest_file)
        file_time = datetime.fromtimestamp(os.path.getmtime(latest_file)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n📁 Latest KAMIS file:")
        print(f"   Path: {latest_file}")
        print(f"   Size: {file_size:,} bytes")
        print(f"   Modified: {file_time}")
        
        # Show row count
        try:
            df = pd.read_excel(latest_file, engine='openpyxl')
            print(f"   Rows: {len(df):,}")
            if 'crop_category' in df.columns:
                print(f"   Crops: {', '.join(df['crop_category'].unique())}")
        except:
            pass
    
    print("\n" + "=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)
    print("\nTip: Run with '--initial' flag to force historical download:")
    print("  python -m app.services.kamis_scraper --initial")
    print("=" * 70 + "\n")
