# Dineout MCP stub — mirrors mcp.swiggy.com/dineout (8 tools).
# Only FREE reservations are supported here. Mock data is AI-generated.
import json
import random
import time
from typing import Union
from mcp.server.fastmcp import FastMCP

dineout = FastMCP("swiggy-dineout")

_bookings: dict = {}

# --- find tools ---

@dineout.tool()
def search_restaurants_dineout(location: str, query: str = "", date: str = "", partySize: Union[int, str] = 2) -> str:
    """
    Search Dineout restaurants by location/cuisine for table booking.
    NOT for food delivery — use Food MCP for that.
    Returns distanceKm; always mention distance for restaurants > 10 km.
    """
    partySize = int(partySize)
    return json.dumps({"success": True, "data": {"restaurants": [
        {
            "restaurantId": "dine_italia_01",
            "name": "Trattoria Italia",
            "cuisine": ["Italian", "Continental"],
            "area": "Koramangala",
            "distanceKm": 1.8,
            "rating": 4.6,
            "ratingCount": 1200,
            "priceForTwo": 1400,
            "availabilityStatus": "OPEN",
            "hasFreeTables": True,
            "offers": ["20% off on pre-booked tables"],
            "shortDescription": "Authentic Italian in a cozy setting.",
            "widget": "restaurant-card",
        },
        {
            "restaurantId": "dine_barbeque_02",
            "name": "Barbeque Nation",
            "cuisine": ["BBQ", "North Indian"],
            "area": "Indiranagar",
            "distanceKm": 4.2,
            "rating": 4.4,
            "ratingCount": 3800,
            "priceForTwo": 1800,
            "availabilityStatus": "OPEN",
            "hasFreeTables": True,
            "offers": ["Free welcome drinks on booking"],
            "shortDescription": "Live grill experience, great for groups.",
            "widget": "restaurant-card",
        },
        {
            "restaurantId": "dine_toit_03",
            "name": "Toit Brewpub",
            "cuisine": ["Continental", "Pub"],
            "area": "Indiranagar",
            "distanceKm": 4.5,
            "rating": 4.5,
            "ratingCount": 5100,
            "priceForTwo": 1600,
            "availabilityStatus": "OPEN",
            "hasFreeTables": True,
            "offers": [],
            "shortDescription": "Bangalore's favorite craft beer destination.",
            "widget": "restaurant-card",
        },
    ]}, "message": f"Found 3 restaurants for '{query}' in {location}."})


@dineout.tool()
def get_restaurant_details(restaurantId: str) -> str:
    """Get full details, menu highlights, and offers for a Dineout restaurant."""
    return json.dumps({"success": True, "data": {
        "restaurantId": restaurantId,
        "name": "Trattoria Italia",
        "address": "12, 80 Feet Rd, Koramangala, Bengaluru - 560034",
        "rating": 4.6,
        "priceForTwo": 1400,
        "cuisine": ["Italian", "Continental"],
        "timings": "12:00 PM – 11:00 PM",
        "features": ["Live Music on Weekends", "Rooftop Seating", "Valet Parking"],
        "menuHighlights": ["Wood-fired Pizza", "Truffle Pasta", "Tiramisu"],
        "offers": [{"title": "20% off", "description": "On pre-booked tables. Min 2 guests."}],
    }, "message": "Restaurant details fetched."})


@dineout.tool()
def get_saved_locations() -> str:
    """Get the user's saved Dineout locations for restaurant discovery."""
    return json.dumps({"success": True, "data": {"locations": [
        {"locationId": "loc_koramangala", "name": "Koramangala", "city": "Bengaluru", "latitude": 12.9352, "longitude": 77.6245},
        {"locationId": "loc_indiranagar", "name": "Indiranagar", "city": "Bengaluru", "latitude": 12.9784, "longitude": 77.6408},
    ]}, "message": "Saved locations fetched."})


# --- reserve tools ---

@dineout.tool()
def get_available_slots(restaurantId: str, date: str, partySize: Union[int, str] = 2) -> str:
    """
    Get available booking time slots for a restaurant.
    IMPORTANT: Use the EXACT integer slotId and integer reservationTime values from this
    response when calling create_cart and book_table. Do NOT convert them to strings or floats.
    Only FREE slots (isFree=true, bookingPrice=0) can be booked.
    """
    partySize = int(partySize)
    base_ts = int(time.time()) + 3600
    return json.dumps({"success": True, "data": {"slots": [
        {
            "reservationTime": base_ts,
            "reservationTimeDisplay": "7:00 PM",
            "availableSeats": 8,
            "deals": [{"slotId": 4001, "itemId": f"{restaurantId}-ticket_7pm", "isFree": True, "bookingPrice": 0, "title": "Free Table Booking"}],
        },
        {
            "reservationTime": base_ts + 3600,
            "reservationTimeDisplay": "8:00 PM",
            "availableSeats": 4,
            "deals": [{"slotId": 4002, "itemId": f"{restaurantId}-ticket_8pm", "isFree": True, "bookingPrice": 0, "title": "Free Table Booking"}],
        },
        {
            "reservationTime": base_ts + 7200,
            "reservationTimeDisplay": "9:00 PM",
            "availableSeats": 2,
            "deals": [{"slotId": 4003, "itemId": f"{restaurantId}-ticket_9pm", "isFree": True, "bookingPrice": 0, "title": "Free Table Booking"}],
        },
    ]}, "message": f"Slots available for {date}, party of {partySize}."})


@dineout.tool()
def create_cart(restaurantId: str, slotId: Union[int, str], itemId: str, guestCount: Union[int, str]) -> str:
    """
    Create a Dineout booking cart. Required step before book_table.
    Pass slotId and guestCount as integers exactly as returned by get_available_slots.
    """
    slotId = int(slotId)
    guestCount = int(guestCount)
    return json.dumps({"success": True, "data": {
        "cartId": f"dine_cart_{random.randint(1000,9999)}",
        "restaurantId": restaurantId,
        "slotId": slotId,
        "itemId": itemId,
        "guestCount": guestCount,
        "bookingPrice": 0,
        "isFree": True,
    }, "message": "Dineout cart created. Proceed to book_table."})


@dineout.tool()
def book_table(
    restaurantId: str,
    slotId: Union[int, str],
    itemId: str,
    reservationTime: Union[int, str],
    guestCount: Union[int, str],
    latitude: Union[float, str],
    longitude: Union[float, str],
) -> str:
    """
    Book a table at a restaurant. Only FREE reservations (bookingPrice=0) are supported.
    NON-IDEMPOTENT: On 5xx failure, call get_booking_status before retrying.
    Requires explicit user confirmation. Simulates 20% transient 503.
    Pass slotId, reservationTime, guestCount as integers; latitude/longitude as floats.
    All values must be taken verbatim from get_available_slots and get_saved_locations responses.
    """
    slotId = int(slotId)
    reservationTime = int(float(reservationTime))
    guestCount = int(guestCount)
    latitude = float(latitude)
    longitude = float(longitude)

    if random.random() < 0.2:
        raise Exception("UPSTREAM_ERROR: Simulated transient 503 – please retry.")

    bookingId = f"booking_{random.randint(10000, 99999)}"
    _bookings[bookingId] = {
        "bookingId": bookingId,
        "restaurantId": restaurantId,
        "slotId": slotId,
        "reservationTime": reservationTime,
        "guestCount": guestCount,
        "status": "CONFIRMED",
        "bookingPrice": 0,
    }
    return json.dumps({"success": True, "data": {
        "bookingId": bookingId,
        "status": "CONFIRMED",
        "confirmationCode": f"SW{random.randint(100000,999999)}",
    }, "message": "Table booked successfully! Check your Swiggy app for confirmation details."})


# --- manage ---

@dineout.tool()
def get_booking_status(bookingId: str) -> str:
    """
    Get status of a Dineout table booking.
    IMPORTANT: Call after 5xx on book_table to check before retrying (idempotency guard).
    """
    booking = _bookings.get(bookingId)
    if not booking:
        return json.dumps({"success": False, "error": {"message": f"Booking {bookingId} not found."}})
    return json.dumps({"success": True, "data": booking, "message": "Booking status fetched."})


# --- support ---

@dineout.tool()
def report_error(bookingId: str, issue: str) -> str:
    """Report an issue with a Dineout booking."""
    return json.dumps({"success": True, "data": {"ticketId": f"ticket_{random.randint(1000,9999)}"}, "message": f"Issue reported for booking {bookingId}."})
