# ETAP tool TODO list

# Roadmap
## For Version 1.1
-[ ] Setup automatic tests
-[ ] Implement a better step changer algorithm, no hard coding
-[ ] Clean the load_lump function, as it is a hard coded mess
-[ ] Study if _write_openpyxl is needed, as it has never been used
-[ ] set_values has 2 nested ifs, optimize this
-[ ] Optimize the performance using some profiler

Done
# Version 1.0
-[x] Write a class ETAP_Lump that generates the base structure
    -[x] Generate empty structure 
    -[x] Print structure
    -[x] Add values to empty structure
    -[x] Generate structure out of existing xlsx file
    -[x] Generate xls file out of the actual values
    -[x] Generate xlsx file out of the actual values
    -[x] Generate structure out of existing xls file
    -[x] Take input time as datetime format
-[x] Add functionality to change the timestep of the available data
    -[x] Allow to change the time step from a higher to a lower timestep
    -[x] Allow to change the time step from a lower to a hieght timestep
-[x] Create some standard abstraction utilities
    -[x] to 60 min
    -[x] to 15 min
    -[x] to 30 min
    -[x] glob to 60 min
    -[x] glob to 30 min
    -[x] glob to 15 min
-[x] Try to automatically determine date format
