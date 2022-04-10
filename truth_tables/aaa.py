import ttables # Use the ttables.py file

# Simple AND function
def example(inputs):
    # You define the amount of bits each function can handle
    if len(inputs) != 2:
        print("This function only works for 2 bit inputs")
        exit()
    A = inputs[0]
    B = inputs[1]
    return (A and B)

inputs = ttables.generate_inputs(2) # Generate input table for 2 bits

table = ttables.evaluate_truth_table(inputs,[example]) # Solve the table

# Print the table, format is as follows:
# index | inputs | results

ttables.print_truth_table(table)

