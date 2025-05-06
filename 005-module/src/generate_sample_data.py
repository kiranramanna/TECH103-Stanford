"""
Generate sample Miami hotel data for testing the search engine.
"""
import json
import os

# Sample Miami hotel data
SAMPLE_HOTELS = [
    {
        "name": "The Fontainebleau Miami Beach",
        "description": "Iconic luxury resort located on oceanfront Collins Avenue. Features elegant rooms, world-class dining, and a spectacular poolscape with luxury cabanas.",
        "location": "4441 Collins Avenue, Miami Beach, FL 33140",
        "amenities": ["Beach access", "Multiple pools", "Spa", "Fine dining", "Nightclub", "Fitness center"],
        "price_range": "$$$",
        "rating": 4.5,
        "reviews": [
            "Beautiful historic hotel with modern amenities",
            "Great beachfront location",
            "Excellent service but expensive"
        ]
    },
    {
        "name": "Biltmore Hotel Miami Coral Gables",
        "description": "Historic luxury hotel featuring Mediterranean architecture, championship golf course, and the largest hotel pool in the continental US.",
        "location": "1200 Anastasia Avenue, Coral Gables, FL 33134",
        "amenities": ["Golf course", "Massive pool", "Spa", "Tennis courts", "Fine dining", "Fitness center"],
        "price_range": "$$$",
        "rating": 4.6,
        "reviews": [
            "Stunning historic property",
            "Amazing golf course",
            "Beautiful architecture and grounds"
        ]
    },
    {
        "name": "1 Hotel South Beach",
        "description": "Eco-conscious luxury hotel with natural design elements, located directly on the beach with stunning ocean views.",
        "location": "2341 Collins Avenue, Miami Beach, FL 33139",
        "amenities": ["Rooftop pool", "Beach club", "Spa", "Plant-based dining", "Gym", "Electric car service"],
        "price_range": "$$$",
        "rating": 4.7,
        "reviews": [
            "Beautiful eco-friendly design",
            "Amazing rooftop views",
            "Great sustainable initiatives"
        ]
    },
    {
        "name": "The Standard Spa Miami Beach",
        "description": "Adult-only spa hotel offering a relaxed atmosphere, hydrotherapy spa, and waterfront yoga.",
        "location": "40 Island Avenue, Miami Beach, FL 33139",
        "amenities": ["Spa", "Yoga classes", "Waterfront pool", "Mediterranean restaurant", "Gardens"],
        "price_range": "$$",
        "rating": 4.3,
        "reviews": [
            "Perfect for relaxation",
            "Great spa facilities",
            "Beautiful bay views"
        ]
    },
    {
        "name": "Mandarin Oriental Miami",
        "description": "Luxury hotel on Brickell Key offering private beach, spa, and panoramic views of the city and bay.",
        "location": "500 Brickell Key Drive, Miami, FL 33131",
        "amenities": ["Private beach", "Spa", "Infinity pool", "Fine dining", "Fitness center"],
        "price_range": "$$$",
        "rating": 4.8,
        "reviews": [
            "Exceptional service",
            "Beautiful bay views",
            "Excellent restaurants"
        ]
    }
]

def generate_sample_data(output_path: str = "../data/miami_hotels.json"):
    """Generate and save sample hotel data.
    
    Args:
        output_path: Path where to save the JSON file
    """
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the data
    with open(output_path, 'w') as f:
        json.dump(SAMPLE_HOTELS, f, indent=2)
    
    print(f"Sample data saved to {output_path}")

if __name__ == "__main__":
    generate_sample_data() 