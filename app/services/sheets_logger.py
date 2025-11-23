import gspread
from datetime import datetime
import os
import json
from typing import Optional, List, Dict

# Try to import google-auth (preferred) and fall back to oauth2client
try:
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    USE_GOOGLE_AUTH = True
except ImportError:
    from oauth2client.service_account import ServiceAccountCredentials
    USE_GOOGLE_AUTH = False

# Configuration
CREDS_FILE = os.getenv("GOOGLE_SHEETS_CREDS_PATH", "credentials.json")
SHEET_NAME = os.getenv("GOOGLE_SHEETS_NAME", "AgroGhala_Logs")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID", None)  # Optional: use spreadsheet ID instead of name

# Required Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]


def get_sheet_service() -> Optional[gspread.Client]:
    """
    Authenticates and returns a gspread client for Google Sheets.
    
    Supports both google-auth (preferred) and oauth2client (legacy).
    
    Returns:
        Authenticated gspread client or None if authentication fails
    """
    try:
        # Check if credentials file exists
        if not os.path.exists(CREDS_FILE):
            print(f"❌ Credentials file not found: {CREDS_FILE}")
            print(f"   Please create a service account and download credentials.")
            print(f"   See GOOGLE_SHEETS_SETUP.md for instructions.")
            return None
        
        # Authenticate using appropriate library
        if USE_GOOGLE_AUTH:
            # Using modern google-auth library
            creds = ServiceAccountCredentials.from_service_account_file(
                CREDS_FILE, 
                scopes=SCOPES
            )
            client = gspread.authorize(creds)
            print(f"✅ Connected to Google Sheets (google-auth)")
        else:
            # Using legacy oauth2client library
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
            client = gspread.authorize(creds)
            print(f"✅ Connected to Google Sheets (oauth2client)")
        
        return client
        
    except FileNotFoundError:
        print(f"❌ Credentials file not found: {CREDS_FILE}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in credentials file: {CREDS_FILE}")
        return None
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        print(f"   Check credentials file and permissions.")
        return None


def get_or_create_spreadsheet(client: gspread.Client) -> Optional[gspread.Spreadsheet]:
    """
    Opens existing spreadsheet or creates a new one if it doesn't exist.
    
    Args:
        client: Authenticated gspread client
        
    Returns:
        Spreadsheet object or None
    """
    try:
        # Try to open by ID first (more reliable)
        if SPREADSHEET_ID:
            try:
                spreadsheet = client.open_by_key(SPREADSHEET_ID)
                print(f"✅ Opened spreadsheet by ID: {spreadsheet.title}")
                return spreadsheet
            except Exception as e:
                print(f"⚠️  Could not open spreadsheet by ID: {e}")
        
        # Try to open by name
        try:
            spreadsheet = client.open(SHEET_NAME)
            print(f"✅ Opened spreadsheet: {SHEET_NAME}")
            return spreadsheet
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet
            print(f"📝 Spreadsheet '{SHEET_NAME}' not found. Creating...")
            spreadsheet = client.create(SHEET_NAME)
            
            # Share with yourself (get email from credentials)
            try:
                with open(CREDS_FILE, 'r') as f:
                    creds_data = json.load(f)
                    service_email = creds_data.get('client_email')
                    if service_email:
                        spreadsheet.share(service_email, perm_type='user', role='writer')
                        print(f"✅ Shared with: {service_email}")
            except:
                pass
            
            print(f"✅ Created spreadsheet: {SHEET_NAME}")
            print(f"   ID: {spreadsheet.id}")
            print(f"   URL: {spreadsheet.url}")
            
            # Initialize worksheets
            initialize_spreadsheet(spreadsheet)
            
            return spreadsheet
            
    except Exception as e:
        print(f"❌ Error accessing spreadsheet: {e}")
        return None


def initialize_spreadsheet(spreadsheet: gspread.Spreadsheet):
    """
    Sets up the initial structure of the spreadsheet with proper worksheets and headers.
    
    Args:
        spreadsheet: The spreadsheet to initialize
    """
    try:
        # Rename default sheet to "Activity_Log"
        try:
            default_sheet = spreadsheet.sheet1
            default_sheet.update_title("Activity_Log")
        except:
            default_sheet = spreadsheet.add_worksheet("Activity_Log", rows=1000, cols=10)
        
        # Set up Activity Log headers
        activity_headers = [
            "Date", "Farmer Name", "County", "Prices Sent", 
            "Weather Summary", "Farmer Reply", "Buyer List Sent", "Timestamp"
        ]
        default_sheet.update('A1:H1', [activity_headers])
        default_sheet.format('A1:H1', {'textFormat': {'bold': True}})
        
        # Create Farmers worksheet
        try:
            farmers_sheet = spreadsheet.add_worksheet("Farmers", rows=100, cols=5)
            farmer_headers = ["Name", "Phone", "County", "Crops", "Status"]
            farmers_sheet.update('A1:E1', [farmer_headers])
            farmers_sheet.format('A1:E1', {'textFormat': {'bold': True}})
            
            # Add sample farmers
            sample_farmers = [
                ["John Kamau", "254712345678", "Nairobi", "Tomatoes, Sukuma", "Active"],
                ["Mary Wanjiku", "254723456789", "Kiambu", "Cabbage, Onions", "Active"],
                ["Peter Ochieng", "254734567890", "Nakuru", "Maize, Beans", "Active"]
            ]
            farmers_sheet.update('A2:E4', sample_farmers)
            print("   ✅ Created Farmers worksheet with sample data")
        except Exception as e:
            print(f"   ⚠️  Could not create Farmers worksheet: {e}")
        
        # Create Buyers worksheet
        try:
            buyers_sheet = spreadsheet.add_worksheet("Buyers", rows=100, cols=5)
            buyer_headers = ["Name", "Crop", "Price (KSh/kg)", "Phone", "Location"]
            buyers_sheet.update('A1:E1', [buyer_headers])
            buyers_sheet.format('A1:E1', {'textFormat': {'bold': True}})
            
            # Add sample buyers
            sample_buyers = [
                ["Nairobi Greens Ltd", "Tomatoes", "60", "254701111111", "Gikomba"],
                ["Fresh Harvest Co", "Sukuma", "35", "254702222222", "Wakulima"],
                ["Veggie Traders", "Cabbage", "30", "254703333333", "Kangemi"],
                ["Onion Wholesalers", "Onions", "90", "254704444444", "Marikiti"]
            ]
            buyers_sheet.update('A2:E5', sample_buyers)
            print("   ✅ Created Buyers worksheet with sample data")
        except Exception as e:
            print(f"   ⚠️  Could not create Buyers worksheet: {e}")
        
        print(f"✅ Spreadsheet initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing spreadsheet: {e}")

def log_activity(farmer_name: str, county: str, prices_sent: str, 
                 weather_summary: str, farmer_reply: str, buyer_list_sent: str) -> bool:
    """
    Logs activity to Google Sheets Activity_Log worksheet.
    
    Args:
        farmer_name: Name of the farmer
        county: Farmer's county
        prices_sent: Prices that were sent to farmer
        weather_summary: Weather information sent
        farmer_reply: Farmer's response (YES/NO/Pending)
        buyer_list_sent: Whether buyer list was sent (Yes/No)
        
    Returns:
        True if logging succeeded, False otherwise
    """
    try:
        client = get_sheet_service()
        if not client:
            print("⚠️  Skipping logging due to connection failure.")
            return False

        spreadsheet = get_or_create_spreadsheet(client)
        if not spreadsheet:
            print("⚠️  Could not access spreadsheet.")
            return False
        
        # Get or create Activity_Log worksheet
        try:
            sheet = spreadsheet.worksheet("Activity_Log")
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.sheet1
            try:
                sheet.update_title("Activity_Log")
            except:
                pass
        
        # Prepare row data
        now = datetime.now()
        row = [
            now.strftime("%Y-%m-%d"),
            farmer_name,
            county,
            str(prices_sent),
            weather_summary,
            farmer_reply,
            str(buyer_list_sent),
            now.strftime("%H:%M:%S")
        ]
        
        # Append row
        sheet.append_row(row)
        print(f"✅ Logged activity for {farmer_name} to Google Sheets")
        return True
        
    except Exception as e:
        print(f"❌ Error logging to sheets: {e}")
        return False

def get_farmers() -> List[Dict]:
    """
    Reads farmers from Google Sheets Farmers worksheet.
    
    Returns:
        List of farmer dictionaries with keys: name, phone, county, crops, status
        Returns mock data if connection fails
    """
    try:
        client = get_sheet_service()
        if not client:
            print("⚠️  Using mock farmer data (no Google Sheets connection)")
            return [
                {"Name": "John Kamau", "Phone": "254712345678", "County": "Nairobi", 
                 "Crops": "Tomatoes, Sukuma", "Status": "Active"},
                {"Name": "Mary Wanjiku", "Phone": "254723456789", "County": "Kiambu", 
                 "Crops": "Cabbage, Onions", "Status": "Active"},
                {"Name": "Peter Ochieng", "Phone": "254734567890", "County": "Nakuru", 
                 "Crops": "Maize, Beans", "Status": "Active"}
            ]
        
        spreadsheet = get_or_create_spreadsheet(client)
        if not spreadsheet:
            print("⚠️  Using mock farmer data (could not access spreadsheet)")
            return get_farmers()  # Return mock data
        
        try:
            sheet = spreadsheet.worksheet("Farmers")
        except gspread.WorksheetNotFound:
            print("⚠️  Farmers worksheet not found. Using mock data.")
            return get_farmers()  # Return mock data
        
        farmers = sheet.get_all_records()
        
        # Filter active farmers
        active_farmers = [f for f in farmers if f.get('Status', '').lower() == 'active']
        
        print(f"✅ Retrieved {len(active_farmers)} active farmers from Google Sheets")
        return active_farmers
        
    except Exception as e:
        print(f"❌ Error reading farmers: {e}")
        return []


def get_buyers(crop: str) -> List[Dict]:
    """
    Reads buyers from Google Sheets for a specific crop.
    
    Args:
        crop: Crop name to filter buyers by (e.g., "Tomatoes", "Sukuma")
        
    Returns:
        List of buyer dictionaries matching the crop
        Returns mock data if connection fails
    """
    try:
        client = get_sheet_service()
        if not client:
            print(f"⚠️  Using mock buyer data for {crop}")
            return [
                {"Name": "Nairobi Greens Ltd", "Crop": crop, "Price (KSh/kg)": "90", 
                 "Phone": "254701111111", "Location": "Gikomba"},
                {"Name": "Fresh Harvest Co", "Crop": crop, "Price (KSh/kg)": "85", 
                 "Phone": "254702222222", "Location": "Wakulima"}
            ]
        
        spreadsheet = get_or_create_spreadsheet(client)
        if not spreadsheet:
            return get_buyers(crop)  # Return mock data
        
        try:
            sheet = spreadsheet.worksheet("Buyers")
        except gspread.WorksheetNotFound:
            print(f"⚠️  Buyers worksheet not found. Using mock data for {crop}.")
            return get_buyers(crop)  # Return mock data
        
        all_buyers = sheet.get_all_records()
        
        # Filter by crop (case-insensitive)
        matching_buyers = [
            b for b in all_buyers 
            if b.get('Crop', '').lower() == crop.lower()
        ]
        
        print(f"✅ Retrieved {len(matching_buyers)} buyers for {crop}")
        return matching_buyers
        
    except Exception as e:
        print(f"❌ Error reading buyers: {e}")
        return []


def test_connection() -> bool:
    """
    Tests the Google Sheets connection and displays information.
    
    Returns:
        True if connection successful, False otherwise
    """
    print("\n" + "=" * 70)
    print("Google Sheets Connection Test")
    print("=" * 70)
    
    # Check credentials file
    print(f"\n1. Checking credentials file...")
    print(f"   Path: {CREDS_FILE}")
    
    if not os.path.exists(CREDS_FILE):
        print(f"   ❌ File not found!")
        print(f"\n   To fix:")
        print(f"   1. Create a Google Cloud service account")
        print(f"   2. Download credentials JSON file")
        print(f"   3. Save as: {CREDS_FILE}")
        return False
    else:
        print(f"   ✅ File exists")
        
        # Check file content
        try:
            with open(CREDS_FILE, 'r') as f:
                creds_data = json.load(f)
                print(f"   📧 Service Account: {creds_data.get('client_email', 'N/A')}")
                print(f"   🆔 Project ID: {creds_data.get('project_id', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Could not read credentials: {e}")
    
    # Test connection
    print(f"\n2. Testing connection...")
    client = get_sheet_service()
    
    if not client:
        print(f"   ❌ Connection failed")
        return False
    
    # Test spreadsheet access
    print(f"\n3. Testing spreadsheet access...")
    print(f"   Spreadsheet name: {SHEET_NAME}")
    
    spreadsheet = get_or_create_spreadsheet(client)
    
    if not spreadsheet:
        print(f"   ❌ Could not access spreadsheet")
        return False
    
    print(f"   ✅ Spreadsheet URL: {spreadsheet.url}")
    
    # List worksheets
    print(f"\n4. Checking worksheets...")
    worksheets = spreadsheet.worksheets()
    for ws in worksheets:
        row_count = ws.row_count
        print(f"   📄 {ws.title} ({row_count} rows)")
    
    # Test reading farmers
    print(f"\n5. Testing farmer data...")
    farmers = get_farmers()
    print(f"   Found {len(farmers)} farmers")
    if farmers:
        print(f"   Sample: {farmers[0].get('Name', 'N/A')} from {farmers[0].get('County', 'N/A')}")
    
    # Test reading buyers
    print(f"\n6. Testing buyer data...")
    buyers = get_buyers("Tomatoes")
    print(f"   Found {len(buyers)} buyers for Tomatoes")
    if buyers:
        print(f"   Sample: {buyers[0].get('Name', 'N/A')} @ KSh {buyers[0].get('Price (KSh/kg)', 'N/A')}/kg")
    
    # Test logging
    print(f"\n7. Testing activity logging...")
    success = log_activity(
        farmer_name="Test Farmer",
        county="Test County",
        prices_sent="Tomato: 50, Sukuma: 30",
        weather_summary="Rain: 20%",
        farmer_reply="Test",
        buyer_list_sent="No"
    )
    
    if success:
        print(f"   ✅ Test log entry created")
    else:
        print(f"   ❌ Logging failed")
    
    print("\n" + "=" * 70)
    print("✅ Google Sheets connection test complete!")
    print("=" * 70)
    print(f"\n📝 Spreadsheet URL: {spreadsheet.url}")
    print("   Open this URL to view your data\n")
    
    return True


if __name__ == "__main__":
    # Run connection test
    test_connection()
