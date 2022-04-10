# Truth tables script
This is a very simple script to quickly generate the complete truth table for one or more boolean
functions, there is a lot that could be improved, and a lot that could be added, feel free to 
contribute if you'd like to

## Usage
```py
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
```

This code will give the following output

```txt
0|00|0|
1|01|0|
2|10|0|
3|11|1|
```

## Some other output examples

```txt
XOR
0|00|0|
1|01|1|
2|10|1|
3|11|0|
```

```txt
XOR and NAND
0|00|01|
1|01|11|
2|10|11|
3|11|00|
```

```txt
Two custom functions for 5 bits
0|00000|00|
1|00001|00|
2|00010|00|
3|00011|00|
4|00100|00|
5|00101|00|
6|00110|00|
7|00111|00|
8|01000|00|
9|01001|00|
10|01010|00|
11|01011|00|
12|01100|01|
13|01101|00|
14|01110|00|
15|01111|00|
16|10000|00|
17|10001|00|
18|10010|00|
19|10011|00|
20|10100|10|
21|10101|00|
22|10110|00|
23|10111|00|
24|11000|00|
25|11001|00|
26|11010|00|
27|11011|00|
28|11100|00|
29|11101|00|
30|11110|00|
31|11111|00|
```

