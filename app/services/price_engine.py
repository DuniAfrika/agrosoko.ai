def calculate_fair_prices(wholesale_prices):
    """
    Applies pricing formula:
    fair_price = wholesale_price - transport_cost - (0.15 * wholesale_price)
    
    Transport cost per kg:
    • Tomato: 4
    • Sukuma: 3
    • Onion: 5
    • Cabbage: 3
    
    Broker cut: 15%
    """
    
    TRANSPORT_COSTS = {
        "tomato": 4,
        "sukuma": 3,
        "onion": 5,
        "cabbage": 3
    }
    
    BROKER_CUT_PERCENT = 0.15
    
    fair_prices = {}
    
    for crop, cost in TRANSPORT_COSTS.items():
        if crop in wholesale_prices:
            wholesale = wholesale_prices[crop]
            # Formula: fair_price = wholesale_price - transport_cost - (0.15 * wholesale_price)
            fair_price = wholesale - cost - (BROKER_CUT_PERCENT * wholesale)
            fair_prices[f"fair_{crop}"] = int(fair_price) # Rounding to int as per example output
            
    return fair_prices

if __name__ == "__main__":
    mock_wholesale = {"tomato": 100, "sukuma": 50, "onion": 120, "cabbage": 40}
    print(calculate_fair_prices(mock_wholesale))
