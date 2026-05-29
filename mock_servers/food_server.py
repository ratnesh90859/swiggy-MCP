# Food MCP stub — mirrors mcp.swiggy.com/food (14 tools).
# Mock data is AI-generated for local dev. See mock_servers/README.md.
import json
import random
from mcp.server.fastmcp import FastMCP

food = FastMCP("swiggy-food")

# --- discover tools ---

@food.tool()
def get_addresses() -> str:
    """Returns the user's saved delivery addresses. Always call this first to get addressId."""
    return json.dumps({
        "success": True,
        "data": {
            "addresses": [
                {
                    "addressId": "addr_home_001",
                    "tag": "Home",
                    "flatNo": "42B",
                    "building": "Sunrise Apartments",
                    "area": "Koramangala",
                    "city": "Bengaluru",
                    "pincode": "560034",
                    "latitude": 12.9352,
                    "longitude": 77.6245,
                    "isDefault": True,
                },
                {
                    "addressId": "addr_office_002",
                    "tag": "Office",
                    "flatNo": "Floor 3",
                    "building": "Embassy Tech Village",
                    "area": "Bellandur",
                    "city": "Bengaluru",
                    "pincode": "560103",
                    "latitude": 12.9279,
                    "longitude": 77.6733,
                    "isDefault": False,
                },
            ]
        },
        "message": "Addresses fetched successfully.",
    })


@food.tool()
def search_restaurants(addressId: str, query: str = "", offset: int = 0) -> str:
    """
    Search for food restaurants by query at the given addressId.
    Returns up to 8 results with availabilityStatus, distanceKm, rating, deliveryTime.
    Only OPEN restaurants should be recommended.
    """
    return json.dumps({
        "success": True,
        "data": {
            "restaurants": [
                {
                    "restaurantId": "rest_biryani_house_01",
                    "name": "Biryani House",
                    "cuisine": ["Biryani", "Mughlai"],
                    "rating": 4.5,
                    "ratingCount": 3200,
                    "distanceKm": 2.1,
                    "deliveryTimeRange": "25-35 MIN",
                    "deliveryTimeSpoken": "about 30 minutes",
                    "shortDescription": "Famous for Dum Biryani, great value.",
                    "longDescription": "Biryani House | 4.5★ | 2.1 km | 25-35 min | Biryani, Mughlai",
                    "availabilityStatus": "OPEN",
                    "offers": ["50% off up to ₹100"],
                    "widget": "restaurant-card",
                },
                {
                    "restaurantId": "rest_paradise_02",
                    "name": "Paradise Biryani",
                    "cuisine": ["Biryani", "Andhra"],
                    "rating": 4.3,
                    "ratingCount": 2800,
                    "distanceKm": 3.8,
                    "deliveryTimeRange": "35-45 MIN",
                    "deliveryTimeSpoken": "about 40 minutes",
                    "shortDescription": "Iconic Hyderabadi Biryani since 1953.",
                    "longDescription": "Paradise Biryani | 4.3★ | 3.8 km | 35-45 min | Hyderabadi",
                    "availabilityStatus": "OPEN",
                    "offers": [],
                    "widget": "restaurant-card",
                },
                {
                    "restaurantId": "rest_kebab_factory_03",
                    "name": "Kebab Factory",
                    "cuisine": ["North Indian", "Kebabs"],
                    "rating": 4.4,
                    "ratingCount": 1900,
                    "distanceKm": 5.2,
                    "deliveryTimeRange": "40-50 MIN",
                    "deliveryTimeSpoken": "about 45 minutes",
                    "shortDescription": "Best kebabs and curries in town.",
                    "longDescription": "Kebab Factory | 4.4★ | 5.2 km | 40-50 min | North Indian",
                    "availabilityStatus": "OPEN",
                    "offers": ["Free delivery on orders above ₹299"],
                    "widget": "restaurant-card",
                },
                {
                    "restaurantId": "rest_far_cafe_04",
                    "name": "Far Away Cafe",
                    "cuisine": ["Continental", "Cafe"],
                    "rating": 4.1,
                    "ratingCount": 800,
                    "distanceKm": 6.5,
                    "deliveryTimeRange": "50-60 MIN",
                    "deliveryTimeSpoken": "about 55 minutes",
                    "shortDescription": "Cozy cafe with great coffee and sandwiches.",
                    "longDescription": "Far Away Cafe | 4.1★ | 6.5 km | 50-60 min | Continental",
                    "availabilityStatus": "OPEN",
                    "offers": [],
                    "widget": "restaurant-card",
                },
            ]
        },
        "message": f"Found 4 restaurants for '{query}'.",
    })


@food.tool()
def get_restaurant_menu(restaurantId: str, addressId: str) -> str:
    """Get full menu categories for a restaurant. Call before search_menu to discover categories."""
    return json.dumps({
        "success": True,
        "data": {
            "restaurantId": restaurantId,
            "categories": [
                {"categoryId": "cat_biryani", "name": "Biryani", "itemCount": 8},
                {"categoryId": "cat_kebabs", "name": "Kebabs & Starters", "itemCount": 12},
                {"categoryId": "cat_mains", "name": "Main Course", "itemCount": 10},
                {"categoryId": "cat_breads", "name": "Breads", "itemCount": 6},
                {"categoryId": "cat_desserts", "name": "Desserts", "itemCount": 5},
                {"categoryId": "cat_beverages", "name": "Beverages", "itemCount": 8},
            ],
        },
        "message": "Menu categories fetched.",
    })


@food.tool()
def search_menu(restaurantId: str, addressId: str, query: str = "", category: str = "") -> str:
    """Search within a restaurant's menu. Use category from get_restaurant_menu for fresh results."""
    return json.dumps({
        "success": True,
        "data": {
            "restaurantId": restaurantId,
            "items": [
                {
                    "itemId": "item_chicken_biryani_01",
                    "name": "Chicken Biryani",
                    "description": "Aromatic basmati rice cooked with tender chicken.",
                    "price": 349,
                    "rating": 4.6,
                    "isVeg": False,
                    "isBestseller": True,
                    "variants": [
                        {"variantId": "var_half", "name": "Half Plate", "price": 249},
                        {"variantId": "var_full", "name": "Full Plate", "price": 349},
                    ],
                    "addons": [
                        {"addonId": "add_raita", "name": "Raita", "price": 40},
                        {"addonId": "add_salan", "name": "Mirchi Salan", "price": 50},
                    ],
                },
                {
                    "itemId": "item_veg_biryani_02",
                    "name": "Veg Dum Biryani",
                    "description": "Fresh vegetables slow-cooked with aromatic spices.",
                    "price": 279,
                    "rating": 4.3,
                    "isVeg": True,
                    "isBestseller": False,
                    "variants": [
                        {"variantId": "var_full_veg", "name": "Full Plate", "price": 279},
                    ],
                    "addons": [],
                },
                {
                    "itemId": "item_mutton_biryani_03",
                    "name": "Mutton Biryani",
                    "description": "Slow-cooked mutton with fragrant basmati rice.",
                    "price": 449,
                    "rating": 4.7,
                    "isVeg": False,
                    "isBestseller": True,
                    "variants": [
                        {"variantId": "var_full_mut", "name": "Full Plate", "price": 449},
                    ],
                    "addons": [
                        {"addonId": "add_raita", "name": "Raita", "price": 40},
                    ],
                },
            ],
        },
        "message": f"Menu items for '{query or category}' fetched.",
    })


# --- cart tools ---

_food_cart: dict = {}


@food.tool()
def update_food_cart(
    restaurantId: str,
    cartItems: list,
    addressId: str,
    restaurantName: str = "",
) -> str:
    """
    Add or update items in the food cart. cartItems is a list of item objects with
    itemId, quantity, variantId (optional), and addons (optional list of addonIds).
    NEVER add items from different restaurants simultaneously.
    """
    global _food_cart
    _food_cart = {
        "restaurantId": restaurantId,
        "restaurantName": restaurantName,
        "addressId": addressId,
        "items": cartItems,
        "subtotal": sum(300 for _ in cartItems),  # flat ₹300 per item, real pricing comes from prod
        "deliveryFee": 30,
        "taxes": 25,
        "total": sum(300 for _ in cartItems) + 55,
        "availablePaymentMethods": ["COD"],
        "offers": {"coupon_applied": None, "coupon_discount": 0},
    }
    return json.dumps({
        "success": True,
        "data": _food_cart,
        "message": f"Cart updated with {len(cartItems)} item(s).",
    })


@food.tool()
def get_food_cart() -> str:
    """Get the current food cart state including items, costs, and available payment methods."""
    if not _food_cart:
        return json.dumps({"success": True, "data": {"items": [], "total": 0}, "message": "Cart is empty."})
    return json.dumps({"success": True, "data": _food_cart, "message": "Cart fetched."})


@food.tool()
def fetch_food_coupons(restaurantId: str) -> str:
    """Fetch available discount coupons for a restaurant."""
    return json.dumps({
        "success": True,
        "data": {
            "coupons": [
                {"code": "WELCOME50", "description": "50% off up to ₹100 on your first order.", "discount": 100, "minOrderValue": 199},
                {"code": "TRYNEW", "description": "₹75 off on orders above ₹299.", "discount": 75, "minOrderValue": 299},
            ]
        },
        "message": "Coupons fetched.",
    })


@food.tool()
def apply_food_coupon(couponCode: str) -> str:
    """Apply a coupon to the current food cart. Check coupon_discount > 0 to confirm it's active."""
    global _food_cart
    if _food_cart:
        _food_cart["offers"]["coupon_applied"] = couponCode
        _food_cart["offers"]["coupon_discount"] = 75
        _food_cart["total"] = max(0, _food_cart.get("total", 0) - 75)
    return json.dumps({
        "success": True,
        "data": {"coupon_applied": couponCode, "coupon_discount": 75},
        "message": f"Coupon {couponCode} applied. You save ₹75!",
    })


@food.tool()
def flush_food_cart() -> str:
    """Clear/empty the entire food cart."""
    global _food_cart
    _food_cart = {}
    return json.dumps({"success": True, "data": {}, "message": "Cart cleared successfully."})


# --- order ---

_food_orders: dict = {}


@food.tool()
def place_food_order(addressId: str, paymentMethod: str = "COD") -> str:
    """
    Place the food delivery order.
    NON-IDEMPOTENT: On 5xx failure, call get_food_orders to check before retrying.
    RESTRICTION: Cart total must be below ₹1000 (beta restriction).
    ALWAYS requires prior user confirmation.
    Simulates 20% transient 503 failure to demonstrate retry plugin behaviour.
    """
    # ~20% chance of a 503 to make the retry plugin kick in during demos
    if random.random() < 0.2:
        raise Exception("UPSTREAM_ERROR: Simulated transient 503 – please retry.")

    cart_total = _food_cart.get("total", 0)
    if cart_total >= 1000:
        return json.dumps({
            "success": False,
            "error": {"message": f"Order value ₹{cart_total} exceeds ₹1000 beta cap. Please use the Swiggy app for larger orders."},
        })

    orderId = f"order_food_{random.randint(10000, 99999)}"
    _food_orders[orderId] = {
        "orderId": orderId,
        "status": "PLACED",
        "restaurant": _food_cart.get("restaurantName", "Restaurant"),
        "total": cart_total,
        "paymentMethod": paymentMethod,
        "deliveryAddress": addressId,
        "estimatedDelivery": "30-35 MIN",
    }

    return json.dumps({
        "success": True,
        "data": {"orderId": orderId, "status": "PLACED", "estimatedDelivery": "30-35 MIN"},
        "message": f"Swiggy order placed successfully! Your food will arrive in 30-35 minutes.",
    })


# --- tracking ---

@food.tool()
def get_food_orders() -> str:
    """
    Get list of recent food orders.
    IMPORTANT: Call this after a 5xx failure on place_food_order to check if the order went through
    before retrying (check-then-retry idempotency pattern).
    """
    return json.dumps({
        "success": True,
        "data": {"orders": list(_food_orders.values())},
        "message": "Orders fetched.",
    })


@food.tool()
def get_food_order_details(orderId: str) -> str:
    """Get full details for a specific food order by orderId."""
    order = _food_orders.get(orderId)
    if not order:
        return json.dumps({"success": False, "error": {"message": f"Order {orderId} not found."}})
    return json.dumps({"success": True, "data": order, "message": "Order details fetched."})


@food.tool()
def track_food_order(orderId: str) -> str:
    """Get real-time delivery tracking status for an active food order."""
    statuses = ["PLACED", "ACCEPTED", "PREPARING", "PICKED_UP", "OUT_FOR_DELIVERY", "DELIVERED"]
    current = random.choice(statuses)
    return json.dumps({
        "success": True,
        "data": {
            "orderId": orderId,
            "status": current,
            "deliveryPartner": {"name": "Ramesh", "phone": "XXXXXXXXXX"},
            "eta": "12 minutes",
            "liveLocation": {"latitude": 12.9320, "longitude": 77.6200},
        },
        "message": f"Order is currently: {current}",
    })


# --- support ---

@food.tool()
def report_error(orderId: str, issue: str) -> str:
    """Report an issue with a food order to Swiggy support."""
    return json.dumps({
        "success": True,
        "data": {"ticketId": f"ticket_{random.randint(1000, 9999)}", "status": "OPEN"},
        "message": f"Issue reported for order {orderId}. Our team will reach out shortly.",
    })
