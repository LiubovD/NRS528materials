import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox Wires Analysis"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Suitable_points, divide_by_ETT_status, pair_points_by_distance]

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
        arcpy.Select_analysis(suitable_wires, wires_treatment, expression_1)

        # Get control wires
        arcpy.Select_analysis(suitable_wires, wires_control, expression_2)

        return


class pair_points_by_distance(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "pair_points_by_distance"
        self.description = "We are pairing points from treatment group with point from control group"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
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

        # paired_wires_table = arcpy.Parameter(name="paired_wires_table",
        #                                   displayName="paired_wires_table",
        #                                   datatype="DETable",
        #                                   parameterType="Required",  # Required|Optional|Derived
        #                                   direction="Output",  # Input|Output
        #                                   )
        # paired_wires_table.value = "paired_wires_table_2"  # This is a default value that can be over-ridden in the toolbox
        # params.append(paired_wires_table)

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

        years = ["TS_%s" % yr for yr in range(2013, 2018)]

        #pts_1 = list()
        #pts_2 = list()
        #fields = []
        fields_names = ["X_1", "Y_1", "ID_1", "treeCov_1", "length_1", "outages_1", "X_2", "Y_2", "ID_2", "treeCov_2", "length_2",
                        "outages_2", "dist"]
        arcpy.CreateTable_management(workspace, "paired_wires_table.dbf")
        for field_name in fields_names:
            arcpy.AddField_management("paired_wires_table.dbf", field_name, "text")
        arcpy.AddField_management("paired_wires_table.dbf", "outage_dif", "float")
        fields_names.append("outage_dif")
        IDs_of_controls_used = []
        with arcpy.da.SearchCursor(wires_treatment,["Shape@XY", "Up_Dev_ID", "pTreeCov", "length_km"] + years) as cursor_1:
            fields = []
            for row_1 in cursor_1:
                XY_1, ID_1, treeCov_1, length_1 = row_1[0], row_1[1], row_1[2], row_1[3]
                X_1, Y_1 = XY_1[0], XY_1[1]
                outages_1 = sum(row_1[4:])
                fields.extend((X_1, Y_1, ID_1, treeCov_1, length_1, outages_1))
                with arcpy.da.SearchCursor(wires_control,
                                           ["Shape@XY", "Up_Dev_ID", "pTreeCov", "length_km"] + years) as cursor_2:
                    for row_2 in cursor_2:
                        XY_2, ID_2, treeCov_2, length_2 = row_2[0], row_2[1], row_2[2], row_2[3]
                        X_2, Y_2 = XY_2[0], XY_2[1]
                        outages_2 = sum(row_2[4:])
                        dst = ((X_1 - X_2) ** 2 + (Y_1 - Y_2) ** 2) ** 0.5
                        if (0 < dst <= 10000) and (length_1 * 0.8 <= length_2 <= length_1 * 1.2) and (treeCov_1 * 0.8 <= treeCov_2 <= treeCov_1 * 1.2) and (outages_1 != 0 or outages_2 != 0):
                            if ID_2 not in IDs_of_controls_used:
                                IDs_of_controls_used.append(ID_2)
                                outage_dif = outages_1 - outages_2
                                fields.extend((X_2, Y_2, ID_2, treeCov_2, length_2, outages_2, dst, outage_dif))
                                with arcpy.da.InsertCursor("paired_wires_table.dbf", fields_names) as cursor:
                                    print(len(fields_names))
                                    print(len(fields))
                                    cursor.insertRow(fields)

                                    # for row in fields_names:
                                    #     if row[0] is None:
                                    #         pass
                                    #     else:
                                            #cursor.updateRow(row)
                                            # print(type(fields_names))
                                            # print(type(fields))







        # rateDiff_ar = np.array(rateDiffs)  # create array
        # mean = rateDiff_ar.mean()
        # stDev = rateDiff_ar.std()
        # median = np.median(rateDiffs)
        # sterr = stDev / ((len(rateDiffs)) ** 0.5)
        # _CI_95 = [mean - 1.96 * sterr, mean + 1.96 * sterr]
        #
        # print("ETT to no ETT\n")
        # print(" mean= %s\n median=%s\n stDev=%s\n stdErr=%s\n CI_95=%s to %s\n n=%s" % (
        # mean, median, stDev, sterr, _CI_95[0], _CI_95[1], len(rateDiffs)))
        #
        # # paired t-test
        # print(stats.ttest_rel(ratesInsl, ratesBare))
        #
        # # Wilcoxon test
        # print(stats.wilcoxon(ratesInsl, ratesBare, zero_method="wilcox"))

        return

def main():
    tool = pair_points_by_distance()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()