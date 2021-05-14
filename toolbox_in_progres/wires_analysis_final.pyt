#This toolbox consists of 3 separate scripts that can be used in different combinations. 
#The scripts within this toolbox are useful for classification and analysis of wires outage database 
#with information about technical specification of wires and environmental parameters. 
#Power outages are The scripts can be utilized in different combinations to create sets of data - 
#for this purpose users can change expression which is provided as on of the function's input. 
#Also tools can be used outside of this function.

#Three tools have following names - Suitable_points, divide_by_ETT_status and pair_points_by_distance.



import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox Wires Analysis"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Suitable_points, divide_by_ETT_status, pair_points_by_distance]

#Suitable_points - To ensure accurate data analysis, this tool filters out wires 
#which are not suitable for analysis based on several parameters 
#(excluded are wires with more then 25 percent located underground, b
#ackbone wires and too short for analysis wires (shoreter then 250m))  

class Suitable_points(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Suitable_points"
        self.description = "Filtering out provided wires based on pre-selected factor of suitability"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Parameters for this function - input geodatabase of wires with various parameters and environmental factors, 
        #output geodatabased and expression to filter out points which are not suitable
        params = []
        wires_midpoint_database = arcpy.Parameter(name="wires_midpoint_database",
                                     displayName="Wires midpoint database",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        wires_midpoint_database.value = r"D:\Luba\PhD_project_one_and_only_folder_on_PC\powerLines_zones_midPoints\powerLines_zones_midPoints.shp"
        params.append(wires_midpoint_database)

        suitable_wires = arcpy.Parameter(name="output",
                                 displayName="Output",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        suitable_wires.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\suitable_wires.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(suitable_wires)

        expression = arcpy.Parameter(name="expression",
                                         displayName="expression for excluding not suitable for analysis wires",
                                         datatype="GPString",
                                         parameterType="Required",  # Required|Optional|Derived
                                         direction="Input")  # Input|Output
        expression.value = "backbone = 0 AND UG_ratio < 0.25 AND length_km > 0.25"
        params.append(expression)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        wires_midpoint_database = parameters[0].valueAsText
        suitable_wires = parameters[1].valueAsText
        expression = parameters[2].valueAsText
        arcpy.Select_analysis(wires_midpoint_database, suitable_wires, expression)
        arcpy.AddMessage("Filtering out non-suitable points")

        return
#divide_by_ETT_status - Divide wires in 2 sets based on input parameters. 
#This tool can be run several times (specifing new parameters) to separate groups to subgroups.

class divide_by_ETT_status(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "divide_by_ETT_status"
        self.description = "We are creating 2 groups of wires for further analysis - treated with ETT and non-treated with ETT"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        suitable_wires = arcpy.Parameter(name="suitable_wires",
                                     displayName="suitable_wires",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input")  # Input|Output
        suitable_wires.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\suitable_wires.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(suitable_wires)

        expression_1 = arcpy.Parameter(name="expression_1",
                                    displayName="expression for treated wires",
                                    datatype="GPString",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Input")  # Input|Output
        expression_1.value = "ETTprimYr > 2011 AND ETTprimYr < 2013"
        params.append(expression_1)

        expression_2 = arcpy.Parameter(name="expression_2",
                                    displayName="expression for control wires",
                                    datatype="GPString",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Input")  # Input|Output
        expression_2.value = "pctETT = 0"
        params.append(expression_2)

        wires_treatment = arcpy.Parameter(name="output_treatment_wires",
                                          displayName="Output Treatment Wires",
                                          datatype="DEFeatureClass",
                                          parameterType="Required",  # Required|Optional|Derived
                                          direction="Output",  # Input|Output
                                          )
        wires_treatment.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\wires_treatment.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(wires_treatment)

        wires_control = arcpy.Parameter(name="output_control_wires",
                                          displayName="Output Control Wires",
                                          datatype="DEFeatureClass",
                                          parameterType="Required",  # Required|Optional|Derived
                                          direction="Output",  # Input|Output
                                          )
        wires_control.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\wires_control.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(wires_control)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        suitable_wires = parameters[0].valueAsText
        expression_1 = parameters[1].valueAsText
        expression_2 = parameters[2].valueAsText
        wires_treatment = parameters[3].valueAsText
        wires_control = parameters[4].valueAsText

        years = ["TS_%s" % yr for yr in range(2013, 2018)]  # outage years to include

        # Get treatment wires
        arcpy.Select_analysis(suitable_wires, wires_treatment, expression_1)

        # Get control wires
        arcpy.Select_analysis(suitable_wires, wires_control, expression_2)
        
        arcpy.AddMessage("Creating two sets of wires - treatment and control")

        return

#pair_points_by_distance - Pair points from treatment and control datasets based on the distance (within 10 km)
#and close values of length and tree cover and calculate difference in the outage rate between this wires. 
#We can create this pairing for any two sets of wires, received using previous tool to compare their parameters.

class pair_points_by_distance(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "pair_points_by_distance"
        self.description = "We are pairing points from treatment group with point from control group"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # define two sets of wires we are going to analyze as 2 parameters
        params = []
        wires_treatment = arcpy.Parameter(name="treatment_wires",
                                          displayName="Treatment Wires",
                                          datatype="DEFeatureClass",
                                          parameterType="Required",  # Required|Optional|Derived
                                          direction="Input",  # Input|Output
                                          )
        wires_treatment.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\wires_treatment.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(wires_treatment)

        wires_control = arcpy.Parameter(name="control_wires",
                                        displayName="Control Wires",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        wires_control.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\wires_control.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(wires_control)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        wires_treatment = parameters[0].valueAsText
        wires_control = parameters[1].valueAsText
#        paired_wires_table = parameters[2].valueAsText

        workspace = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox"
        arcpy.env.overwriteOutput = True
        
        # years for which outage rate is calculated
        years = ["TS_%s" % yr for yr in range(2013, 2018)]
        
        # fields in database which we will be analysing in this tool
        fields_names = ["X_1", "Y_1", "ID_1", "treeCov_1", "length_1", "outages_1", "X_2", "Y_2", "ID_2", "treeCov_2", "length_2",
                        "outages_2", "dist"]
        
        # create table where we will be storing paired wires
        arcpy.CreateTable_management(workspace, "paired_wires_table.dbf")
        # add all text fields
        for field_name in fields_names:
            arcpy.AddField_management("paired_wires_table.dbf", field_name, "text")
        # add outage difference field which should be treated as float
        arcpy.AddField_management("paired_wires_table.dbf", "outage_dif", "float")
        fields_names.append("outage_dif")
        IDs_of_controls_used = []
        
        # use cursor_2 for taking content of the second dataset - I places it outside of function so it wouldn't reopen every cicle thus would save time processing
        cursor_2 = arcpy.da.SearchCursor(wires_control,
                                   ["Shape@XY", "Up_Dev_ID", "pTreeCov", "length_km"] + years)
        # used cursor_1 to take content of the first dataset
        with arcpy.da.SearchCursor(wires_treatment,["Shape@XY", "Up_Dev_ID", "pTreeCov", "length_km"] + years) as cursor_1:
            # let's go through all the rows of first set 
            for row_1 in cursor_1:
                fields = []
                #naming fields
                XY_1, ID_1, treeCov_1, length_1 = row_1[0], row_1[1], row_1[2], row_1[3]
                # separating X from Y
                X_1, Y_1 = XY_1[0], XY_1[1]
                # let's summarize outages for all selected years
                outages_1 = sum(row_1[4:])
                fields = [X_1, Y_1, ID_1, treeCov_1, length_1, outages_1]
                # let's go through second set
                for row_2 in cursor_2:
                        #naming fields
                        XY_2, ID_2, treeCov_2, length_2 = row_2[0], row_2[1], row_2[2], row_2[3]
                        # separating X from Y
                        X_2, Y_2 = XY_2[0], XY_2[1]
                        # let's summarize outages for all selected years
                        outages_2 = sum(row_2[4:])
                        # calculate distance between points
                        dst = ((X_1 - X_2) ** 2 + (Y_1 - Y_2) ** 2) ** 0.5
                        # if distance is less then 10 km and length of wire and tree canopy cover is no more different then +- 20 % then we found a pair for our point
                        if (0 < dst <= 10000) and (length_1 * 0.8 <= length_2 <= length_1 * 1.2) and (treeCov_1 * 0.8 <= treeCov_2 <= treeCov_1 * 1.2) and (outages_1 != 0 or outages_2 != 0):
                            # if our wire was already used in previous pair - skip it, we only use a wire once
                            if ID_2 in IDs_of_controls_used:
                                continue
                            # otherwire we are placing in the list of used points and add in the table together with point from first set + difference in outages between them
                            else:
                                IDs_of_controls_used.append(ID_2)
                                print(IDs_of_controls_used)
                                print(ID_2)
                                outage_dif = outages_1 - outages_2
                                with arcpy.da.InsertCursor("paired_wires_table.dbf", fields_names) as cursor:
                                    fields.extend((X_2, Y_2, ID_2, treeCov_2, length_2, outages_2, dst, outage_dif))
                                    cursor.insertRow(fields)
                                    break
                                    arcpy.AddMessage("Creating table of paired wires")

        return
