import streamlit as st
import sys
import time

sys.path.append('C:\\Users\\avina\\PycharmProjects\\QC-API-v1')
from qkd.generate_t22_key import generate_random_pairings, generate_random_groupings, quantum_compute, generate_code

def page_shared_key():
    st.title("🔑 Simulate T22 QKD Protocol")
    st.markdown(
        "#### Please enter the desired key length and click the button to generate a secure shared key using quantum computation."
    )

    with st.container(border=True):
        st.markdown("### Key Generation Input")
        desired_key_length = st.number_input('Enter desired key length:', min_value=1, max_value=1000, value=10)

    if st.button('Generate Shared Key', key='generate_shared_key', use_container_width=True):
        start_time = time.time()

        alice_code, bob_code = "", ""
        while len(alice_code) <= desired_key_length:
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

        end_time = time.time()
        time_taken = end_time - start_time

        # Store the results in session state
        st.session_state['t22_alice_code'] = alice_code
        st.session_state['t22_bob_code'] = bob_code
        st.session_state['t22_time_taken'] = time_taken

    # Retrieve the results from session state
    if 't22_alice_code' in st.session_state:
        alice_code = st.session_state['t22_alice_code']
        bob_code = st.session_state['t22_bob_code']
        time_taken = st.session_state['t22_time_taken']

        with st.container(border=True):
            st.markdown("### Generated Codes")
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.subheader('Alice Code')
                    st.markdown(f"{alice_code}")
            with col2:
                with st.container(border=True):
                    st.subheader('Bob Code')
                    st.markdown(f"{bob_code}")
            with st.container(border=True):
                st.markdown(f"#### Time taken to generate the key: {int(time_taken)} seconds")

page_shared_key()
