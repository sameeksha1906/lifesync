# attractions_logic.py

class Attraction:
    """Represents a local attraction."""
    def __init__(self, name, latitude, longitude, description, category, address="", phone=""):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.category = category  # e.g., "park", "clinic", "wellness"
        self.address = address
        self.phone = phone


    def get_details(self):
        """Returns a dictionary of attraction details."""
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "category": self.category,
            "address": self.address,
            "phone": self.phone
        }

    def __str__(self):
        return f"{self.name} ({self.category})"


class LocalAttractionsManager:
    """Manages the list of attractions."""
    def __init__(self):
        self.attractions = []
        self._prepopulate_data()

    def _prepopulate_data(self):
        """Adds some sample attractions."""
        self.add_attraction(Attraction("City Central Park", 37.7749, -122.4194, "A large urban park with walking trails and gardens.", "Park", "123 Park Ave", "555-0101"))
        self.add_attraction(Attraction("Mindful Wellness Center", 37.7750, -122.4200, "Offers yoga, meditation, and therapy sessions.", "Wellness", "456 Wellness Blvd", "555-0102"))
        self.add_attraction(Attraction("Community Health Clinic", 37.7760, -122.4210, "Provides general health and mental health services.", "Clinic", "789 Health St", "555-0103"))
        self.add_attraction(Attraction("Serene Lakeside Trail", 37.8000, -122.4300, "Peaceful trail for walking and reflection by the lake.", "Park", "101 Lake Rd", "N/A"))
        self.add_attraction(Attraction("The Quiet Library", 37.7900, -122.4100, "A calm place for reading and study.", "Quiet Space", "202 Book St", "555-0104"))
        self.add_attraction(Attraction("Art Therapy Studio", 37.7850, -122.4150, "Creative space for therapeutic art.", "Therapy", "303 Creative Ln", "555-0105"))


    def add_attraction(self, attraction):
        """Adds an attraction to the list."""
        self.attractions.append(attraction)

    def get_all_attractions(self):
        return self.attractions

    def get_attractions_by_category(self, category):
        """Filters attractions by category."""
        category_lower = category.lower()
        return [attraction for attraction in self.attractions if attraction.category.lower() == category_lower]

    def get_categories(self):
        """Returns a list of unique attraction categories."""
        return sorted(list(set(att.category for att in self.attractions)))

# Initialise a global manager instance for the app to use
attractions_manager = LocalAttractionsManager()

if __name__ == "__main__":
    print("Available categories:", attractions_manager.get_categories())
    parks = attractions_manager.get_attractions_by_category("Park")
    for park in parks:
        print(park.get_details())