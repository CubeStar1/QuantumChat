from fastapi import FastAPI, HTTPException

from app_functions import quantum_compute
from app_functions import generate_code
from app_functions import get_correct_measurements
from generate_bb84_key import bb84_qkd_protocol
from generate_e91_key import e91_qkd_protocol, simulate_e91_protocol
import random
import time

def generate_random_pairings(length):
    all_pairings = [[[0,1], [2,3]], [[0,2], [1,3]], [[0,3], [1,2]]]
    return [random.choice(all_pairings) for _ in range(length)]
def generate_random_groupings(length):
    return [random.randint(0,1) for _ in range(length)]

correction_bits = 1

app = FastAPI()

@app.get("/bs_key/{desired_key_length}")
async def get_bs_key(desired_key_length: int):
    if desired_key_length <= 0:
        raise HTTPException(status_code=400, detail="Number of bits must be positive")
    desired_key_length = desired_key_length
    start_time = time.time()  # Start the timer
    alice_code, bob_code = "", ""
    while len(alice_code) <= desired_key_length:
        # Generate random pairings and groupings for Alice and Bob
        alice_pairings = generate_random_pairings(10)
        alice_groupings = generate_random_groupings(10)
        bob_pairings = generate_random_pairings(10)
        bob_groupings = generate_random_groupings(10)
        alice_json = {"pairings": alice_pairings, "groupings": alice_groupings, "correct_measurements": []}
        bob_json = {"pairings": bob_pairings, "groupings": bob_groupings, "correct_measurements": []}
        alice_json, bob_json = quantum_compute(alice_json, bob_json)
        alice_json, bob_json = quantum_compute(alice_json, bob_json)
        alice_json["code"] = generate_code(alice_json["correct_measurements"])
        bob_json["code"] = generate_code(bob_json["correct_measurements"])
        alice_code += alice_json["code"]
        bob_code += bob_json["code"]

    alice_code = alice_code[:desired_key_length]
    bob_code = bob_code[:desired_key_length]
    end_time = time.time()  # Stop the timer
    time_taken = end_time - start_time  # Calculate the time taken
    # Return the keys
    return {"alice_key": alice_code, "bob_key": bob_code, "time_taken": time_taken, "protocol": "BS"}


@app.get("/bb84_key/{desired_key_length}")
async def get_vv84_key(desired_key_length: int):
    if desired_key_length <= 0:
        raise HTTPException(status_code=400, detail="Number of bits must be positive")
    st = time.time()
    shared_key = bb84_qkd_protocol(desired_key_length)
    et = time.time()
    time_taken = et - st
    return {"alice_key": shared_key, "bob_key": shared_key, "time_taken": str(time_taken) , "protocol": "BB84"}


@app.get("/e91_key/{desired_key_length}")
async def get_e91_key(desired_key_length: int):
    if desired_key_length <= 0:
        raise HTTPException(status_code=400, detail="Number of bits must be positive")
    st = time.time()
    alice_key, bob_key = e91_qkd_protocol(desired_key_length)
    et = time.time()
    time_taken = et - st
    return {"alice_key": alice_key, "bob_key": bob_key, "time_taken": str(time_taken) , "protocol": "E91"}