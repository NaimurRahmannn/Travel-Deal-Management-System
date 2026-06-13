VALID_TYPES = {"Budget", "Luxury", "Adventure", "Family"}
SORTABLE_FIELDS = {"price", "rating", "destination", "travel_type", "platform", "id"}
VALID_ORDERS = {"asc", "desc"}

def validate_deal(data):
    if not data:
        return "Request body is required"
    if not data.get("destination"):
        return "destination cannot be empty"
    if not data.get("platform"):
        return "platform cannot be empty"
    price = data.get("price")
    if price is None or isinstance(price, bool) or not isinstance(price, (int, float)):
        return "price must be a number"
    if price <= 0:
        return "price must be positive"
    rating = data.get("rating")
    if rating is not None:
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            return "rating must be a number"
        if not (1 <= rating <= 5):
            return "rating must be between 1 and 5"
    if data.get("travel_type") not in VALID_TYPES:
        return "travel_type must be one of: Budget, Luxury, Adventure, Family"
    return None

def parse_price(raw_value, field_name):
    if raw_value is None:
        return None, None
    try:
        return float(raw_value), None
    except (TypeError, ValueError):
        return None, f"{field_name} must be a number"

def validate_price_range(min_price, max_price):
    if min_price is not None and min_price < 0:
        return "min_price cannot be negative"
    if max_price is not None and max_price < 0:
        return "max_price cannot be negative"
    if min_price is not None and max_price is not None and max_price < min_price:
        return "max_price cannot be smaller than min_price"
    return None

def validate_sort_params(sort_by, order):
    if sort_by not in SORTABLE_FIELDS:
        return f"Invalid sort field. Allowed: {', '.join(sorted(SORTABLE_FIELDS))}"
    if order not in VALID_ORDERS:
        return "order must be 'asc' or 'desc'"
    return None
