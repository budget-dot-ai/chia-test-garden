import json
import time
import requests
import os

# --- Configuration ---
API_URL = "https://api.mintgarden.io/nfts/"
NFT_ID = "nft1..."  # YOUR REAL NFT ID HERE

# Growth intervals in seconds (86400 = 1 day)
LEVEL_2_AGE = 86400
LEVEL_3_AGE = 172800
LEVEL_4_AGE = 259200

BASE_CID = "bafybeiafimixsflngcez3wj6uhbxb5rj323fcfoavh42ulevvqexnz624"
IMAGES = {
    1: f"ipfs://{BASE_CID}/1-chachi-sun-sprout-RS.png",
    2: f"ipfs://{BASE_CID}/2-chachi-sun-grow-RS.png",
    3: f"ipfs://{BASE_CID}/3-chachi-sun-bloom-RS.png",
    4: f"ipfs://{BASE_CID}/4-chachi-sun-full-RS.png"
}
STAGE_NAMES = {1: "Sprout", 2: "Grow", 3: "Bloom", 4: "Full"}

# File paths (where GitHub stores our tracking data and the public JSON)
STATE_FILE = "state.json"
METADATA_FILE = "metadata/chachi_001.json"

def get_state():
    """Reads our internal state (owner and last transfer time)"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    # Default state if running for the first time
    return {"owner_did": "", "last_transfer_time": time.time()}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def update_metadata_file(level, age_in_seconds):
    """Writes the actual JSON file that GitHub Pages will serve"""
    metadata = {
        "format": "CHIP-0007",
        "name": f"Chachi Sun - {STAGE_NAMES[level]}",
        "description": "An evolving Chachi Sun NFT that resets upon trading.",
        "attributes": [
            {"trait_type": "Growth Stage", "value": STAGE_NAMES[level]},
            {"trait_type": "Level", "value": level},
            {"trait_type": "Age (Days)", "value": int(age_in_seconds // 86400)}
        ],
        "collection": {
            "name": "Chachi Sun Evolution",
            "id": "chachi_sun_collection"
        },
        "uris": [IMAGES[level]]
    }
    
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Updated metadata to Level {level}")

def main():
    state = get_state()
    current_time = time.time()
    
    # 1. Check the blockchain via MintGarden
    try:
        response = requests.get(f"{API_URL}{NFT_ID}")
        if response.status_code == 200:
            data = response.json()
            current_owner = data.get('owner_did') or data.get('owner_address')
            
            # 2. Did the owner change? Reset the clock!
            if current_owner and current_owner != state["owner_did"]:
                print(f"Trade detected! New owner: {current_owner}")
                state["owner_did"] = current_owner
                state["last_transfer_time"] = current_time
                save_state(state)
    except Exception as e:
        print(f"Error checking API: {e}")

    # 3. Calculate Age and Level
    age_in_seconds = current_time - state["last_transfer_time"]
    
    level = 1
    if age_in_seconds >= LEVEL_4_AGE:
        level = 4
    elif age_in_seconds >= LEVEL_3_AGE:
        level = 3
    elif age_in_seconds >= LEVEL_2_AGE:
        level = 2
        
    # 4. Write the new JSON file
    update_metadata_file(level, age_in_seconds)

if __name__ == "__main__":
    main()
