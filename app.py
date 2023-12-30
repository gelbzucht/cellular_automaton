import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def visualize_state(state):
    """ Visualize the state with black and white boxes or emojis """
    return ''.join(['⬛' if bit == '1' else '⬜' for bit in state])

def next_state(current_line, rules_dict):
    """ Calculate the next state of the cellular automaton """
    extended_line = np.pad(current_line, 1, mode='constant')  # Pad for edge cases
    new_line = []

    for i in range(1, len(extended_line) - 1):
        window = ''.join(extended_line[i-1:i+2].astype(str))
        new_line.append(rules_dict.get(window, 0))  # Default to 0 if rule not found

    return np.array(new_line)

def run_simulation(initial_state, rules_dict, rounds):
    """ Run the cellular automaton simulation """
    states = [initial_state]
    for _ in range(rounds - 1):
        states.append(next_state(states[-1], rules_dict))

    return np.vstack(states)

# def plot_automaton(states):
#     """ Plot the cellular automaton states """
#     plt.figure(figsize=(10, 10))
#     plt.imshow(states, cmap='Greys', interpolation='nearest')
#     plt.axis('off')
#     st.pyplot(plt)

def plot_automaton(states):
    """ Plot the cellular automaton states with an improved design """
    cmap = mcolors.ListedColormap(['#f0f0f0', '#306998'])  # Light gray and blue color map
    plt.figure(figsize=(10, 10))
    plt.imshow(states, cmap=cmap, interpolation='nearest')

    # Adding grid lines
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, states.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, states.shape[0], 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", size=0)
    
    # Hide axes and display the plot
    plt.axis('off')
    st.pyplot(plt)

# Streamlit Interface
st.title("🔬 Interactive Cellular Automaton")
st.write("ℹ️ This is an interactive cellular automaton simulation, realized in streamlit. Inspired by David Sumpter's book <a href='https://www.goodreads.com/book/show/61242231-four-ways-of-thinking'>The Four Ways of Thinking</a> and his vivid description of <a href='https://en.wikipedia.org/wiki/Elementary_cellular_automaton'>Stephen Wolfram's Elementary Cellular Automaton.</a>. Depending on the transition rules, one can create I) stable, II) periodic, III) chaotic or IV) complex behaviour.", unsafe_allow_html=True)

st.markdown("---")
st.subheader("⚙️ Simulation Settings")
# User Inputs for Initial Line and Rounds in the same line
col1, col2 = st.columns(2)
with col1:
    initial_line_length = st.number_input("#️⃣ Number of Cells in Initial Line", min_value=1, max_value=1000, value=8)
with col2:
    rounds = st.number_input("🔁 Number of Rounds", min_value=1, max_value=100000, value=10)


# User Inputs for Initial Line
# initial_line_length = st.number_input("Number of Cells in Initial Line", min_value=1, max_value=1000, value=8)
initial_line = st.text_input("Initial Line (e.g., 10101100)", "1" * initial_line_length)
# rounds = st.number_input("＃ Number of Rounds", min_value=1, max_value=100000, value=10)

st.markdown("---")
# Display and input for each possible state in a single row
st.subheader("📐 Transition Rules")
# one liner describing the rules
st.write("ℹ️ The transition rules define how each cell evolves. Each possible state of a cell is represented by a 3-bit window (left cell, current cell, right cell). The user can select the next state of the cell for each possible window. The transition rules are applied to each cell in the automaton in each round.")
possible_states = [bin(i)[2:].zfill(3) for i in range(8)]
rules_dict = {}

# Create a single row for inputs
cols = st.columns(len(possible_states))
for i, state in enumerate(possible_states):
    with cols[i]:
        st.write(visualize_state(state))
        rules_dict[state] = st.selectbox("", [0, 1], key=state)

# Convert initial line to numpy array and run simulation
if st.button("🎬 Start Simulation"):
    initial_state = np.array([int(x) for x in initial_line.strip()])
    states = run_simulation(initial_state, rules_dict, rounds)
    
    # Plot and Display
    plot_automaton(states)


