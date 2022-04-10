'''
Truth tables generation functions, it has lots of room 
for improvements, and functionality additions, so...
there ya go
'''

class truth_table:
    def __init__(self,inputs,results):
        self.inputs = inputs
        self.results = results

def generate_inputs(n):
    inputs = []
    value = [0]*n
    n = 2**n
    while(n > 0):
        inputs.append(value[:])
        index = len(value)-1
        carry = value[index]
        value[index] = not value[index]
        while(carry):
            index -= carry
            carry = value[index]
            value[index] = not value[index]
        n -= 1
    return inputs

def evaluate_truth_table(inputs, funcs):
    results = []
    for i in range(len(inputs)):
        results.append([])
    if type(funcs) is not list:
        funcs = [funcs]
    for func in funcs:
        for index in range(len(inputs)):
            results[index].append(func(inputs[index]))
    return truth_table(inputs,results)

def print_truth_table(table):
    if len(table.inputs) != len(table.results):
        print("mismatch")
        return None
    n = len(table.inputs)
    index = 0
    for i in range(n):
        print_str = str(index)
        print_str += "|"
        for inp in table.inputs[i]:
            print_str += str(1 if inp else 0)
        print_str += "|"
        for result in table.results[i]:
            print_str += str(1 if result else 0)
        print_str += "|"
        index += 1
        print(print_str)

