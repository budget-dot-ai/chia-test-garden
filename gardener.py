import os
import asyncio
from dotenv import load_dotenv
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH

# Load environment variables (from GitHub Secrets)
load_dotenv()
CHIA_SEED = os.getenv("CHIA_SEED")
PLANT_LAUNCHER_ID = os.getenv("PLANT_LAUNCHER_ID")
FERTILIZER_ASSET_ID = os.getenv("FERTILIZER_ASSET_ID")

async def scan_and_grow():
    print("🌱 Waking up the Gardener...")
    
    # 1. Connect to the local Chia Light Wallet RPC (Started by GitHub Actions)
    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    wallet_client = await WalletRpcClient.create(
        config["self_hostname"], config["wallet"]["rpc_port"], DEFAULT_ROOT_PATH, config
    )

    try:
        # 2. Check Wallet Inventory
        print("Checking inventory...")
        nfts = await wallet_client.get_nfts(wallet_id=2) # Assuming NFT wallet is ID 2
        
        my_plants = [nft for nft in nfts.get("nft_list", []) if nft.launcher_id == PLANT_LAUNCHER_ID]
        
        if not my_plants:
            print("No Smart Garden plants found in wallet. Going back to sleep.")
            return

        # 3. Check for Fertilizer
        # (In a full app, you'd check a CAT wallet balance here)
        has_fertilizer = True # Placeholder for CAT balance check
        
        for plant in my_plants:
            print(f"Found Plant! Coin ID: {plant.nft_coin_id}")
            
            # 4. Execute the "Magic" Transaction
            if has_fertilizer:
                print(f"🧪 Fertilizer detected! Burning fertilizer and boosting plant {plant.nft_coin_id}...")
                # Here is where the custom Chialisp Spend Bundle is pushed to the network.
                # await wallet_client.push_tx(custom_spend_bundle)
                print("✅ Success! Transaction submitted to the mempool.")
            else:
                print("No fertilizer found. Checking if 24 hours have passed for natural growth...")
                # Logic to check timestamp and submit natural growth spend bundle

    finally:
        # Always close the connection cleanly
        wallet_client.close()
        await wallet_client.wait_closed()
        print("💤 Gardener going back to sleep.")

if __name__ == "__main__":
    asyncio.run(scan_and_grow())
