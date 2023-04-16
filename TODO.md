ETAP tool TODO list

Roadmap
-[ ] Try to automatically determine date format
-[ ] Setup automatic tests

Done
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
