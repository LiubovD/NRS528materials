import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox Wires Analysis"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Suitable_points, divide_by_ETT_status]

class Suitable_points(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Suitable_points"
        self.description = "Filtering out provided wires based on pre-selected factor of suitability"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        wires_midpoint_database = arcpy.Parameter(name="wires_midpoint_database",
                                     displayName="Wires midpoint database",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        wires_midpoint_database.value = r"D:\Luba\PhD_project_one_and_only_folder_on_PC\powerLines_zones_midPoints\powerLines_zones_midPoints.shp"
        params.append(input_line)

        suitable_wires = arcpy.Parameter(name="output",
                                 displayName="Output",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        suitable_wires.value = r"D:\Luba\pythonArcGIS\toolbox\my_toolbox\suitable_wires.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output)

        expression = arcpy.Parameter(name="expression",
                                         displayName="expression for excluding not suitable for analysis wires",
                                         datatype="GPString",
                                         parameterType="Required",  # Required|Optional|Derived
                                         direction="Input")  # Input|Output
        expression.value = "backbone = 0 AND UG_ratio < 0.25 AND length_km > 0.25"
        params.append(output)
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

        return

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
        arcpy.MakeFeatureLayer_management(suitable_wires, wires_treatment, where_clause=expression_1)

        # Get control wires
        arcpy.MakeFeatureLayer_management(suitable_wires, wires_control, where_clause=expression_2)

        return

