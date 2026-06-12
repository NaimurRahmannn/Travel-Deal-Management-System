VALID_TYPES = {"Budget", "Luxury", "Adventure", "Family"}


def validate_deal(data):
    if not data:
        return "Request body is required"
    if not data.get("destination"):
        return "destination cannot be empty"
    price = data.get("price")
    if price is None or price <= 0:
        return "price must be positive"
    rating = data.get("rating")
    if rating is not None and not (1 <= rating <= 5):
        return "rating must be between 1 and 5"
    if data.get("travel_type") not in VALID_TYPES:
        return "travel_type must be one of: Budget, Luxury, Adventure, Family"
    return None
