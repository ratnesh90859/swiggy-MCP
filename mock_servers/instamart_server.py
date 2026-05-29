# Instamart MCP stub — mirrors mcp.swiggy.com/im (13 tools).
# Mock data is AI-generated for local dev. See mock_servers/README.md.
import json
import random
from mcp.server.fastmcp import FastMCP

instamart = FastMCP("swiggy-instamart")

_im_cart: dict = {}
_im_orders: dict = {}

# --- discover tools ---

@instamart.tool()
def get_addresses() -> str:
    """Returns saved delivery addresses. Use addressId for all product queries."""
    return json.dumps({"success": True, "data": {"addresses": [
        {"addressId": "addr_home_001", "tag": "Home", "area": "Koramangala", "city": "Bengaluru", "isDefault": True},
        {"addressId": "addr_office_002", "tag": "Office", "area": "Bellandur", "city": "Bengaluru", "isDefault": False},
    ]}, "message": "Addresses fetched."})


@instamart.tool()
def create_address(flatNo: str, building: str, area: str, city: str, pincode: str, tag: str = "Home", latitude: float = 12.9352, longitude: float = 77.6245) -> str:
    """Create a new delivery address."""
    return json.dumps({"success": True, "data": {"addressId": f"addr_{tag.lower()}_{random.randint(100,999)}", "tag": tag}, "message": f"Address '{tag}' created."})


@instamart.tool()
def delete_address(addressId: str) -> str:
    """Delete a saved delivery address."""
    return json.dumps({"success": True, "data": {"deleted": True}, "message": "Address deleted."})


@instamart.tool()
def search_products(addressId: str, query: str, offset: int = 0) -> str:
    """Search groceries at the delivery address. Returns variants — always show to user before adding to cart."""
    return json.dumps({"success": True, "data": {"products": [
        {"productId": "prod_amul_milk_01", "name": "Amul Taaza Full Cream Milk", "brand": "Amul", "category": "Dairy", "rating": 4.6, "variants": [
            {"variantId": "var_500ml", "name": "500 ml", "price": 28, "inStock": True},
            {"variantId": "var_1L", "name": "1 Litre", "price": 54, "inStock": True},
        ]},
        {"productId": "prod_tata_tea_02", "name": "Tata Tea Premium", "brand": "Tata", "category": "Beverages", "rating": 4.4, "variants": [
            {"variantId": "var_250g", "name": "250 g", "price": 89, "inStock": True},
            {"variantId": "var_500g", "name": "500 g", "price": 172, "inStock": True},
        ]},
        {"productId": "prod_fortune_oil_03", "name": "Fortune Sunflower Oil", "brand": "Fortune", "category": "Oils", "rating": 4.5, "variants": [
            {"variantId": "var_1L_oil", "name": "1 Litre", "price": 145, "inStock": True},
        ]},
    ]}, "message": f"Found products for '{query}'."})


@instamart.tool()
def your_go_to_items(addressId: str) -> str:
    """Returns frequently ordered Instamart items for quick restock."""
    return json.dumps({"success": True, "data": {"items": [
        {"productId": "prod_amul_milk_01", "name": "Amul Taaza 1L", "lastOrderedQty": 2},
        {"productId": "prod_tata_tea_02", "name": "Tata Tea 250g", "lastOrderedQty": 1},
    ]}, "message": "Go-to items fetched."})


# --- cart tools ---

@instamart.tool()
def update_cart(addressId: str, cartItems: list) -> str:
    """Add/update grocery cart. cartItems: [{ productId, variantId, quantity }]. Follow with get_cart."""
    global _im_cart
    subtotal = len(cartItems) * 100
    _im_cart = {"addressId": addressId, "items": cartItems, "subtotal": subtotal, "deliveryFee": 25, "handlingFee": 10, "total": subtotal + 35, "availablePaymentMethods": ["COD"]}
    return json.dumps({"success": True, "data": _im_cart, "message": f"Cart updated with {len(cartItems)} item(s)."})


@instamart.tool()
def get_cart() -> str:
    """Get current Instamart cart state."""
    if not _im_cart:
        return json.dumps({"success": True, "data": {"items": [], "total": 0}, "message": "Cart is empty."})
    return json.dumps({"success": True, "data": _im_cart, "message": "Cart fetched."})


@instamart.tool()
def clear_cart() -> str:
    """Clear the Instamart cart entirely."""
    global _im_cart
    _im_cart = {}
    return json.dumps({"success": True, "data": {}, "message": "Cart cleared."})


# --- order ---

@instamart.tool()
def checkout() -> str:
    """
    Place Instamart order. NON-IDEMPOTENT. On 5xx, call get_orders before retrying.
    Requires explicit user confirmation. Simulates 20% transient 503.
    """
    if random.random() < 0.2:
        raise Exception("UPSTREAM_ERROR: Simulated transient 503 – please retry.")
    orderId = f"order_im_{random.randint(10000,99999)}"
    _im_orders[orderId] = {"orderId": orderId, "status": "PLACED", "total": _im_cart.get("total", 0), "estimatedDelivery": "10-20 MIN"}
    return json.dumps({"success": True, "data": {"orderId": orderId, "status": "PLACED"}, "message": "Swiggy Instamart order placed successfully! Delivery in 10-20 minutes."})


# --- tracking ---

@instamart.tool()
def get_orders() -> str:
    """Get recent Instamart orders. Call after 5xx on checkout to guard idempotency."""
    return json.dumps({"success": True, "data": {"orders": list(_im_orders.values())}, "message": "Orders fetched."})


@instamart.tool()
def get_order_details(orderId: str) -> str:
    """Get details for a specific Instamart order."""
    order = _im_orders.get(orderId)
    if not order:
        return json.dumps({"success": False, "error": {"message": f"Order {orderId} not found."}})
    return json.dumps({"success": True, "data": order, "message": "Order fetched."})


@instamart.tool()
def track_order(orderId: str) -> str:
    """Real-time delivery tracking for an active Instamart order."""
    status = random.choice(["PLACED", "PACKED", "OUT_FOR_DELIVERY", "DELIVERED"])
    return json.dumps({"success": True, "data": {"orderId": orderId, "status": status, "eta": "8 minutes"}, "message": f"Status: {status}"})


# --- support ---

@instamart.tool()
def report_error(orderId: str, issue: str) -> str:
    """Report an issue with an Instamart order."""
    return json.dumps({"success": True, "data": {"ticketId": f"ticket_{random.randint(1000,9999)}"}, "message": f"Issue reported for {orderId}. Support will contact you."})
