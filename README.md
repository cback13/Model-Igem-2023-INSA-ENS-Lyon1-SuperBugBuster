# Model-Igem-2023-INSA-ENS-Lyon1-SuperBugBuster
You'll find here the codes used for the 2 types of simulations carried out as part of our Model for the iGEM 2023 competition, team INSA ENS Lyon1.  The IBM code corresponds to individual-centered modeling. The Model code corresponds to simulations based on our main model: the autonomous differential equation model.

## Packages required :

- numpy 1.24.4
- matplotlib 3.7.3
- imageio 2.31.4
- pygame 2.5.2
- tqdm 4.66.1


## Modifications to certain parameters for simulations.
Certain parameters can be modified to run simulations with different initial conditions:
For Model.py :

- To change the anhydrotetracycline induction time: line 14, change the TA1 value,
- To change the anhydrotetracycline concentration: line 82, change the value of A[k+1],
- To change the initial conditions: lines 52 to 57, change the values of C[0], R[0], Rc[0], S[0], Sc[0].

The correspondence between the names of the different variables used and their meaning can be found on the Model page of our wiki.
For IBM.py :

- To change the size of the 2D space: line 10, change the values of width, height,
- To change ball colors: lines 15 to 19,
- To change initial conditions for R, C and S: lines 95 to 97, change values in ranges.

The correspondence between the names of the different variables used and their meaning can be found on the Model page of our wiki.

## Colors used for the color blind model
- BLUE = (86, 180, 233)
- VERMILLON = (213, 94, 0)
- GREEN = (0, 158, 115)
- YELLOW = (240, 228, 66)
- ORANGE = (230, 159, 0)
