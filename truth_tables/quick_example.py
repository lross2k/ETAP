# Quick example of this script, saves a lot of time 
# if you need to work with a lot of bits

# Import the ttables script
import ttables as tt

# Test functions
xor = lambda i : i[0]*(not i[1]) + (not i[0])*i[1]
nand = lambda i : not (i[0] and i[1])

# Generate input table for 2 bits
inp = tt.generate_inputs(2)

# Evaluate the table with the given inputs and functions
table = tt.evaluate_truth_table(inp,[xor,nand])

# Print the index | inputs | results of the table
tt.print_truth_table(table)

