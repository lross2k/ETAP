# Big example, shows a more potentially frustrating 
# or tedious real life example

# Import the ttables script
import ttables as tt

# Test functions
def forward_motor(inputs):
    forward = inputs[0]
    reverse = inputs[1]
    start_forward = inputs[2]
    stop = inputs[3]
    overload = inputs[4]
    return start_forward*(forward and not reverse)*(not stop and not overload)
def reverse_motor(inputs):
    forward = inputs[0]
    reverse = inputs[1]
    start_reverse = inputs[2]
    stop = inputs[3]
    overload = inputs[4]
    return start_reverse*(reverse and not forward)*(not stop and not overload)

# Generate input table for 6 bits
inp = tt.generate_inputs(5)

# Evaluate the table with the given inputs and functions
table = tt.evaluate_truth_table(inp,[forward_motor,reverse_motor])

# Print the index | inputs | results of the table
tt.print_truth_table(table)

