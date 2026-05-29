# JSON-based test case definitions
TEST_SCENARIOS = [
    {
        "id": "MT-01",
        "name": "Macro-Sync (Food -> IM)",
        "turns": [
            {
                "query": "Find a high-protein chicken dish from a nearby restaurant.",
                "expected_tools": ["search_restaurants"]
            },
            {
                "query": "Add the best option to my cart.",
                "expected_tools": ["update_food_cart"]
            },
            {
                "query": "I need more protein. Find a 200ml chocolate protein shake on Instamart and add it.",
                "expected_tools": ["search_products", "update_cart"]
            }
        ]
    },
    {
        "id": "MT-02",
        "name": "Dineout Slot Discovery",
        "turns": [
            {
                "query": "Find Italian restaurants in Koramangala.",
                "expected_tools": ["search_restaurants_dineout"]
            },
            {
                "query": "Pick one and show me slots for 2 people tonight.",
                "expected_tools": ["get_available_slots"]
            }
        ]
    }
]
