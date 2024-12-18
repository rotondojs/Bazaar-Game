import sys
import json
import asyncio
import threading

from Bazaar.Client.client import Client
from Bazaar.Common.JSON.deserializer import BazaarDeserializer


def read_stdin():
    try:
        data = sys.stdin.read()
        json_data = json.loads(data)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error reading JSON from STDIN: {e}")
        sys.exit(1)

def run_coroutine_in_thread(coroutine):
    """
    Helper function to run an async coroutine in a thread.
    """
    asyncio.run(coroutine)

async def main():
    # Read input from STDIN
    input_data = read_stdin()

    # Extract client configurations
    players = BazaarDeserializer.actors_to_mechanisms(input_data)

    # Initialize clients
    tasks = []
    threads = []
    for player in players:
        #TODO: port should be passed in
        client = Client(host="127.0.0.1", port=10000, player_name=await player.name(), player=player)
        print(client.player_name)
        tasks.append(client)

        client_thread = threading.Thread(target=run_coroutine_in_thread, args=(client.connect(),))
        client_thread.daemon = True
        client_thread.start()

        threads.append((client_thread, client))

    for client_thread, client in threads:
        while not client.signed_up:
            print(f"Waiting for client {client.player_name} to sign up...")
            await asyncio.sleep(0.1)

        # Wait for thread to complete
        client_thread.join()
        print(f"Client {client.player_name} has signed up and thread completed.")

    #for client in tasks:
        #try:
            #TODO: threading is blocking or incorrect arg
            #client_thread = threading.Thread(target=run_coroutine_in_thread, args=(client.connect(),))
            #client_thread.daemon = True
            #client_thread.start()
            #print(client_thread.join())
            #while not client.signed_up:
                #pass
        #except Exception as e:
            #print(e)
            #pass


if __name__ == "__main__":
    asyncio.run(main())
