"""
Buyers Service - Manages buyer data from Excel file
"""
import pandas as pd
import os
from typing import Dict, List, Optional

# Path to buyers data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
BUYERS_FILE = os.path.join(DATA_DIR, "buyers.xlsx")


def get_all_buyers() -> List[Dict]:
    """
    Get all buyers from the Excel file.
    
    Returns:
        List of buyer dictionaries
    """
    try:
        if not os.path.exists(BUYERS_FILE):
            print(f"⚠️  Buyers file not found: {BUYERS_FILE}")
            return get_mock_buyers()
        
        # Read Excel file
        df = pd.read_excel(BUYERS_FILE, engine='openpyxl')
        
        # Convert to list of dictionaries
        buyers = df.to_dict('records')
        
        print(f"✅ Loaded {len(buyers)} buyers from Excel")
        return buyers
        
    except Exception as e:
        print(f"❌ Error reading buyers file: {e}")
        return get_mock_buyers()


def get_buyers_by_type(buyer_type: str) -> List[Dict]:
    """
    Get buyers filtered by type.
    
    Args:
        buyer_type: Type of buyer (Hotel, Restaurant, Mama Mboga, Supermarket, Wholesaler)
        
    Returns:
        List of buyers matching the type
    """
    all_buyers = get_all_buyers()
    
    # Filter by type (case-insensitive)
    filtered = [
        buyer for buyer in all_buyers 
        if buyer.get('Buyer Type', '').lower() == buyer_type.lower()
    ]
    
    print(f"🔍 Found {len(filtered)} buyers of type '{buyer_type}'")
    return filtered


def get_buyers_by_county(county: str) -> List[Dict]:
    """
    Get buyers filtered by county.
    
    Args:
        county: County name
        
    Returns:
        List of buyers in that county
    """
    all_buyers = get_all_buyers()
    
    # Filter by county (case-insensitive)
    filtered = [
        buyer for buyer in all_buyers 
        if buyer.get('County', '').lower() == county.lower()
    ]
    
    print(f"🔍 Found {len(filtered)} buyers in '{county}'")
    return filtered


def get_buyers_by_crop(crop: str) -> List[Dict]:
    """
    Get buyers interested in a specific crop.
    
    Args:
        crop: Crop name (e.g., "Tomatoes", "Sukuma Wiki")
        
    Returns:
        List of buyers interested in that crop
    """
    all_buyers = get_all_buyers()
    
    # Filter by crop interest (case-insensitive, partial match)
    filtered = [
        buyer for buyer in all_buyers 
        if crop.lower() in buyer.get('Crops Interested', '').lower()
    ]
    
    print(f"🔍 Found {len(filtered)} buyers interested in '{crop}'")
    return filtered


def get_buyer_by_id(buyer_id: str) -> Optional[Dict]:
    """
    Get a specific buyer by ID.
    
    Args:
        buyer_id: Buyer ID (e.g., "BYR001")
        
    Returns:
        Buyer dictionary or None if not found
    """
    all_buyers = get_all_buyers()
    
    for buyer in all_buyers:
        if buyer.get('Buyer ID') == buyer_id:
            print(f"✅ Found buyer: {buyer.get('Buyer Name')}")
            return buyer
    
    print(f"❌ Buyer not found: {buyer_id}")
    return None


def get_buyer_types() -> List[str]:
    """
    Get list of all unique buyer types.
    
    Returns:
        List of buyer type strings
    """
    all_buyers = get_all_buyers()
    types = list(set(buyer.get('Buyer Type', '') for buyer in all_buyers))
    types.sort()
    return types


def get_buyer_counties() -> List[str]:
    """
    Get list of all unique counties where buyers are located.
    
    Returns:
        List of county strings
    """
    all_buyers = get_all_buyers()
    counties = list(set(buyer.get('County', '') for buyer in all_buyers))
    counties.sort()
    return counties


def get_mock_buyers() -> List[Dict]:
    """
    Returns mock buyer data as a fallback.
    
    Returns:
        List of mock buyer dictionaries
    """
    return [
        {
            "Buyer ID": "BYR001",
            "Buyer Name": "Sarova Stanley Hotel",
            "Buyer Type": "Hotel",
            "County": "Nairobi",
            "Location": "Nairobi CBD",
            "Contact Phone": "+254720123001",
            "Crops Interested": "Tomatoes, Onions, Cabbage, Sukuma Wiki",
            "Weekly Volume (kg)": 500,
            "Quality Required": "Grade A",
            "Payment Terms": "Net 30",
            "Price Range (KSh/kg)": "40-55",
            "Status": "Active",
            "Verified": "Yes",
            "Registration Date": "2025-01-15"
        },
        {
            "Buyer ID": "BYR002",
            "Buyer Name": "Java House Ltd",
            "Buyer Type": "Restaurant Chain",
            "County": "Nairobi",
            "Location": "Westlands",
            "Contact Phone": "+254733456002",
            "Crops Interested": "Tomatoes, Sukuma Wiki, Cabbage",
            "Weekly Volume (kg)": 300,
            "Quality Required": "Grade A",
            "Payment Terms": "Net 15",
            "Price Range (KSh/kg)": "40-55",
            "Status": "Active",
            "Verified": "Yes",
            "Registration Date": "2025-01-18"
        },
        {
            "Buyer ID": "BYR003",
            "Buyer Name": "Mama Njeri's Greengrocers",
            "Buyer Type": "Mama Mboga",
            "County": "Kiambu",
            "Location": "Ruaka",
            "Contact Phone": "+254745678003",
            "Crops Interested": "Tomatoes, Sukuma Wiki, Onions, Cabbage",
            "Weekly Volume (kg)": 150,
            "Quality Required": "Grade B",
            "Payment Terms": "Cash on Delivery",
            "Price Range (KSh/kg)": "30-45",
            "Status": "Active",
            "Verified": "Yes",
            "Registration Date": "2025-01-20"
        }
    ]


def get_buyers_by_commodity(county: str = "Nairobi", limit_per_crop: int = 2) -> Dict[str, List[Dict]]:
    """
    Get buyers organized by commodity (2 per crop for Nairobi).
    
    Args:
        county: County to filter by (default: Nairobi)
        limit_per_crop: Maximum buyers per crop (default: 2)
        
    Returns:
        Dictionary with crops as keys and list of buyers as values
        {
            "Tomatoes": [buyer1, buyer2],
            "Sukuma": [buyer1, buyer2],
            "Onions": [buyer1, buyer2],
            "Cabbage": [buyer1, buyer2]
        }
    """
    crops = {
        "Tomatoes": [],
        "Sukuma": [],
        "Onions": [],
        "Cabbage": []
    }
    
    # Get all Nairobi buyers
    nairobi_buyers = get_buyers_by_county(county)
    
    # For each crop, find buyers interested in it
    for crop_name in crops.keys():
        for buyer in nairobi_buyers:
            crops_interested = buyer.get('Crops Interested', '')
            
            # Check if buyer is interested in this crop
            if crop_name.lower() in crops_interested.lower() or \
               (crop_name == "Sukuma" and "sukuma" in crops_interested.lower()):
                
                # Add to list if not already at limit
                if len(crops[crop_name]) < limit_per_crop:
                    crops[crop_name].append(buyer)
    
    print(f"📊 Organized buyers by commodity for {county}:")
    for crop, buyers in crops.items():
        print(f"   {crop}: {len(buyers)} buyers")
    
    return crops


def get_buyer_stats() -> Dict:
    """
    Get statistics about buyers.
    
    Returns:
        Dictionary with buyer statistics
    """
    all_buyers = get_all_buyers()
    
    # Count by type
    type_counts = {}
    for buyer in all_buyers:
        buyer_type = buyer.get('Buyer Type', 'Unknown')
        type_counts[buyer_type] = type_counts.get(buyer_type, 0) + 1
    
    # Count by county
    county_counts = {}
    for buyer in all_buyers:
        county = buyer.get('County', 'Unknown')
        county_counts[county] = county_counts.get(county, 0) + 1
    
    # Calculate total weekly volume
    total_volume = sum(buyer.get('Weekly Volume (kg)', 0) for buyer in all_buyers)
    
    # Count active buyers
    active_count = sum(1 for buyer in all_buyers if buyer.get('Status') == 'Active')
    
    return {
        "total_buyers": len(all_buyers),
        "active_buyers": active_count,
        "total_weekly_volume_kg": total_volume,
        "buyers_by_type": type_counts,
        "buyers_by_county": county_counts
    }


if __name__ == "__main__":
    # Test the service
    print("Testing Buyers Service...")
    print("=" * 70)
    
    # Get all buyers
    buyers = get_all_buyers()
    print(f"\n📊 Total buyers: {len(buyers)}")
    
    # Get buyer types
    types = get_buyer_types()
    print(f"\n🏢 Buyer types: {', '.join(types)}")
    
    # Get buyers by type
    hotels = get_buyers_by_type("Hotel")
    print(f"\n🏨 Hotels: {len(hotels)}")
    
    # Get buyers by county
    nairobi_buyers = get_buyers_by_county("Nairobi")
    print(f"\n📍 Nairobi buyers: {len(nairobi_buyers)}")
    
    # Get buyers by crop
    tomato_buyers = get_buyers_by_crop("Tomatoes")
    print(f"\n🍅 Tomato buyers: {len(tomato_buyers)}")
    
    # Get stats
    stats = get_buyer_stats()
    print(f"\n📈 Stats:")
    print(f"   Active: {stats['active_buyers']}/{stats['total_buyers']}")
    print(f"   Weekly volume: {stats['total_weekly_volume_kg']:,} kg")

