This toolbox consists of 3 separate scripts that can be used in different combinations. The scripts within this toolbox are useful for classification and analysis of wires outage database with information about technical specification of wires and environmental parameters. Power outages are 
 The scripts can be utilized in different combinations to create sets of data  - for this purpose users can change expression which is provided as on of the function's input. Also tools  can be used outside of this function. 
 
The 3 scripts and their intended uses are:

Suitable_points - To ensure accurate data analysis, this tool filters out wires which are not suitable for analysis based on several parameters (excluded are wires with more then 25 percent located underground, backbone wires and too short for analysis wires (shoreter then 250m))
![alt text](Suitable_wires tool)

divide_by_ETT_status - Divide wires in 2 sets based on input parameters. This tool can be run several times (specifing new parameters) to separate groups to subgroups.

pair_points_by_distance - Pair points from treatment and control datasets based on the distance (within 10 km) and close values of length and tree cover and calculate difference in the outage rate between this wires.  We can create this pairing for any two sets of wires, received using previous tool to compare their parameters.
