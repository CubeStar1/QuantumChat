import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Quantum Key Distribution (QKD) Simulator", page_icon="🔑", layout="wide")
def menu():
    with st.sidebar:
        with st.container(border=True):
            st.image('qclogo.png')
            with st.expander("Menu", expanded=True):
                st.page_link("pages/BB84.py", label="BB84 Protocol", icon="🔑")
                st.page_link("pages/E91.py", label="E91 Protocol", icon="🔑")
                st.page_link("pages/T22.py", label="T22 Protocol", icon="🔑")
                st.page_link("pages/Bell States.py", label="Bell States", icon="🔑")

def home_page():
    st.title("Quantum Key Distribution (QKD) Simulator")
    st.markdown("""
    Welcome to the Quantum Key Distribution (QKD) Simulator. This application allows you to simulate different QKD protocols like BB84, E91, and others. 
    You can generate quantum keys and test the security and efficiency of quantum cryptography methods.

    **Features:**
    - Simulate BB84, E91, and other QKD protocols.
    - Generate and compare quantum keys between Alice and Bob.
    - Analyze the time efficiency and security of the protocols.

    Navigate through the app using the sidebar to explore different functionalities.
    """)

    # Retrieve the QBER and key match rate for each protocol from session state
    bb84_qber = st.session_state.get('bb84_qber', 0)
    e91_qber = st.session_state.get('e91_qber', 0)
    t22_qber = st.session_state.get('t22_qber', 0.76)

    bb84_key_match_rate = st.session_state.get('bb84_key_match_rate', 0.93)
    e91_key_match_rate = st.session_state.get('e91_key_match_rate', 0.87)
    t22_key_match_rate = st.session_state.get('t22_key_match_rate', 0.78)

    bb84_time_taken = 1.1
    e91_time_taken = st.session_state.get('e91_time_taken', 0)
    t22_time_taken = st.session_state.get('t22_time_taken', 0)

    protocols = ['BB84', 'E91', 'T22']

    # Section for Plotly plots

    with st.container(border=True):
        st.markdown("## Plotly Visualizations")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### QBER Comparison")
            with st.container(border=True):
                qber_fig = go.Figure([go.Bar(x=protocols, y=[bb84_qber, e91_qber, t22_qber])])
                qber_fig.update_layout(title="QBER Comparison Across Protocols", xaxis_title="Protocols", yaxis_title="QBER")
                st.plotly_chart(qber_fig)
        with col2:
            st.markdown("### Key Match Rate Comparison")
            with st.container(border=True):
                kmr_fig = go.Figure([go.Bar(x=protocols, y=[bb84_key_match_rate, e91_key_match_rate, t22_key_match_rate])])
                kmr_fig.update_layout(title="Key Match Rate Comparison Across Protocols", xaxis_title="Protocols", yaxis_title="Key Match Rate")
                st.plotly_chart(kmr_fig)

        with col3:
            st.markdown("### Time Taken Comparison")
            with st.container(border=True):
                time_fig = go.Figure([go.Bar(x=protocols, y=[bb84_time_taken, e91_time_taken, t22_time_taken])])
                time_fig.update_layout(title="Time Taken to Generate Keys Across Protocols", xaxis_title="Protocols", yaxis_title="Time (seconds)")
                st.plotly_chart(time_fig)

    with st.container(border=True):
        colors = ['blue', 'green', 'orange']    # Section for Matplotlib plots
        st.markdown("## Matplotlib Visualizations")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### QBER Comparison")
            with st.container(border=True):
                fig, ax = plt.subplots()
                ax.bar(protocols, [bb84_qber, e91_qber, t22_qber], color=colors)
                ax.set_title('QBER Comparison Across Protocols')
                ax.set_xlabel('Protocols')
                ax.set_ylabel('QBER')
                st.pyplot(fig)
        with col2:
            st.markdown("### Key Match Rate Comparison")
            with st.container(border=True):
                fig, ax = plt.subplots()
                ax.bar(protocols, [bb84_key_match_rate, e91_key_match_rate, t22_key_match_rate], color=colors)
                ax.set_title('Key Match Rate Comparison Across Protocols')
                ax.set_xlabel('Protocols')
                ax.set_ylabel('Key Match Rate')
                st.pyplot(fig)
        with col3:
            st.markdown("### Time Taken Comparison")
            with st.container(border=True):
                fig, ax = plt.subplots()
                ax.bar(protocols, [bb84_time_taken, e91_time_taken, t22_time_taken], color=colors)
                ax.set_title('Time Taken to Generate Keys Across Protocols')
                ax.set_xlabel('Protocols')
                ax.set_ylabel('Time (seconds)')
                st.pyplot(fig)

    # Line Chart for Time Taken using st.line_chart
    st.markdown("## Time Taken Line Chart")
    time_data = pd.DataFrame({
        'Protocol': protocols,
        'Time Taken': [bb84_time_taken, e91_time_taken, t22_time_taken]
    })
    st.line_chart(time_data.set_index('Protocol'), color= '#FF5733', y_label='Time Taken (seconds)', x_label='Protocols')

# Call the menu and home_page functions
menu()
home_page()
