import pandas as pd

# =============
# /PROP/TYPE1/
# =============

def prop_type1():
    # File Path
    inputRadFile = "demo/fichier_sortie.rad"
    outputRadFile = "demo/rad_file_clean.txt"

    # Open File
    with open(outputRadFile, "w") as radFileClean:
        with open(inputRadFile, "r") as radFile:
            # Initialize variable
            matLaw02 = 0
            propType1 = 0
            a = 0
            # The For loop, executes a set of instructions, once for each line of the RAD file
            for index, line in enumerate(radFile):

                # Check if '/PROP/TYPE1/' exists in a row
                if '/PROP/TYPE1/' in line:
                    # Add 5 to the propType1 variable
                    propType1 = 5
                    # Add a carriage return at the end of the line
                    radFileClean.write("\n")

                # Check if the variable propType1 is bigger than 0
                if propType1 > 0:
                    # Subtract 1
                    propType1 -= 1

                    # Initialize variable
                    counterSpace = 0
                    counterCharacter = 1
                    counterString = 0

                    # The For loop, executes a set of instructions, once for each "characters" in Line
                    for space in line:

                        # Reset the variable when there is whitespace
                        if space.isspace() is True:
                            counterSpace += 1
                            counterCharacter = 0

                        # Write each "character" in outputRadFile if it is not a whitespace
                        if space.isspace() is False:
                            # If counterCharacter is bigger than 1, it writes without a comma
                            if counterCharacter >= 1:
                                radFileClean.write(space)
                            # Else it writes a comma
                            else:
                                radFileClean.write("," + space)
                            counterSpace = 0
                            counterCharacter += 1

                        # Write an "x" in outputRadFile if there are more than 18 whitespace
                        if counterSpace > 18:
                            catchInfo = "x"
                            radFileClean.write("," + catchInfo)
                            counterSpace = 0
                            # Add +1 to count "x" as a string
                            counterString += 1

                    # Add 5 "x", if the line is null. len = count the number of characters | split() = delete whitespace
                    if len(str(line.split())) < 3:
                        catchInfo = "x" * 5
                        # Stringify the catchInfo variable, because it becomes a list.
                        toString = ','.join(catchInfo)
                        radFileClean.write("," + toString)

                    # If propType1 is bigger than 3, it writes a comma at the end of the line.
                    if propType1 > 3:
                        radFileClean.write(",")

                    # If propType1 is equal to 2, it writes a "x" at the end of the Line (to complete the schema)
                    if propType1 == 2 and len(line.split()) + counterString < 4:
                        catchInfo = "x"
                        radFileClean.write("," + catchInfo)
                        counterSpace = 0

                    # If propType1 is equal to 0, it writes a "x" at the end of the Line (to complete the schema)
                    if propType1 == 0 and len(line.split()) + counterString < 8:
                        catchInfo = "x"
                        radFileClean.write("," + catchInfo)
                        counterSpace = 0
        # Close File
        radFile.close()
    radFileClean.close()

    # Create XLSX File with outputRadFile
    read_file = pd.read_csv(outputRadFile)
    read_file.to_excel('demo/fichier_rad_en_xlsx_brut.xlsx',
                       header=['Suffix to add\nif necessary', "Radioss Part name", 'Ishell', 'Ismstr', 'Ish3m',
                               'Idrill', 'hm', 'hf', 'hr', 'dm',
                               'dn', 'N', 'Istrain', 'Thickness (mm)\nif external skin surfacic mesh', 'Ashear',
                               'empty1', 'Ithick', 'Iplas', 'empty2'],
                       index=False)

    # Merge template_prop_type1.xlsx with fichier_rad_en_xlsx.xlsx
    df = pd.DataFrame()
    df = df.append(pd.read_excel('prop_type/prop_type1/template_prop_type1.xlsx', usecols="A:AM"), ignore_index=True)
    df = df.append(pd.read_excel('demo/fichier_rad_en_xlsx_brut.xlsx', usecols="A:S"), ignore_index=True)
    df.head()
    df.to_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', index=False)

    # Merge test/fichier_entree.xlsx with fichier_rad_en_xlsx_exploitable.xlsx
    df = df.append(pd.read_excel('demo/fichier_entree.xlsx', usecols="A:W", header=[3]), ignore_index=True)
    df = df.append(pd.read_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', usecols="A:AM"), ignore_index=True)
    df.head()
    df.to_excel('../fichier_fusionner.xlsx')

    # todo
    # Test to show diff.
    # df1 = pd.read_excel('fichier_entree.xlsx', usecols="B:W", header=[3]).fillna(0)
    # df2 = pd.read_excel('fichier_rad_en_xlsx_exploitable.xlsx', usecols="A:AM").fillna(0)
    #
    # dfDiff = df1.copy()
    # for row in range(dfDiff.shape[0]):
    #     for col in range(dfDiff.shape[1]):
    #         value_OLD = df1.iloc[row, col]
    #         try:
    #             value_NEW = df2.iloc[row, col]
    #             if value_OLD == value_NEW:
    #                 dfDiff.iloc[row, col] = df2.iloc[row, col]
    #             else:
    #                 dfDiff.iloc[row, col] = ('{}-->{}').format(value_OLD, value_NEW)
    #         except:
    #             dfDiff.iloc[row, col] = ('{}-->{}').format(value_OLD, 'NaN')
    #
    # writer = pd.ExcelWriter("final.xlsx", engine='xlsxwriter')
    #
    # dfDiff.to_excel(writer, sheet_name='DIFF', index=False)
    # df2.to_excel(writer, sheet_name="fichier_rad_en_xlsx.xlsx", index=False)
    # df1.to_excel(writer, sheet_name="fichier_entree.xlsx", index=False)
    #
    # workbook = writer.book
    # worksheet = writer.sheets['DIFF']
    # worksheet.hide_gridlines(2)
    #
    # # define formats
    # white_fmt = workbook.add_format({'font_color': ' #ffffff '})
    # highlight_fmt = workbook.add_format({'font_color': '#FF0000', 'bg_color': '#B1B3B3'})
    #
    # # highlight changed cells
    # worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
    #                                            'criteria': 'containing',
    #                                            'value': '→',
    #                                            'format': highlight_fmt})
    # # highlight unchanged cells
    # worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
    #                                            'criteria': 'not containing',
    #                                            'value': '→',
    #                                            'format': white_fmt})
    # # save
    # writer.save()