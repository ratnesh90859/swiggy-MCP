import multiprocessing
import uvicorn
import sys
import os

# Ensure project root is in path for all child processes
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_food():
    sys.path.insert(0, PROJECT_ROOT)
    from mock_servers.food_server import food
    uvicorn.run(food.sse_app(), host="0.0.0.0", port=8001)

def run_instamart():
    sys.path.insert(0, PROJECT_ROOT)
    from mock_servers.instamart_server import instamart
    uvicorn.run(instamart.sse_app(), host="0.0.0.0", port=8002)

def run_dineout():
    sys.path.insert(0, PROJECT_ROOT)
    from mock_servers.dineout_server import dineout
    uvicorn.run(dineout.sse_app(), host="0.0.0.0", port=8003)

if __name__ == "__main__":
    # Multiprocessing on Windows requires this
    multiprocessing.freeze_support()
    
    print("Starting Swiggy Mock MCP Servers...")
    print("  Food      → http://localhost:8001/sse")
    print("  Instamart → http://localhost:8002/sse")
    print("  Dineout   → http://localhost:8003/sse")

    processes = [
        multiprocessing.Process(target=run_food, name="food-mcp"),
        multiprocessing.Process(target=run_instamart, name="instamart-mcp"),
        multiprocessing.Process(target=run_dineout, name="dineout-mcp"),
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
