import pandas as pd
import re


def xlsx_creation():
    # RadFile
    matLawRadFile = "demo/rad_file_mat_law02_cleanup.txt"
    propTypeRadFile = "demo/rad_file_prop_type1_cleanup.txt"

    # XLSXFile
    globalTemplateXLSX = "global_template.xlsx"
    globalExploitableXLSX = "demo/global_xlsx_exploitable.xlsx"

    propTypeXLSXBrut = "demo/prop_type1_rad_xlsx_brut.xlsx"
    propTypeXLSXExploitable = "demo/prop_type1_rad_xlsx_exploitable.xlsx"

    matLawXLSXBrut = "demo/mat_law02_rad_xlsx_brut.xlsx"

    inputXLSXFile = "demo/fichier_entree.xlsx"

    # Create prop_type1 XLSX
    prop_type1 = pd.read_csv(propTypeRadFile)
    prop_type1.to_excel(propTypeXLSXBrut,
                        header=['part', 'Radioss Part name\nMTCC','prop_ID', 'mat_ID', 'subset_ID', 'virtual_thick' ,'prop_type1', 'Ishell', 'Ismstr',
                                'Ish3n','hm', 'hf', 'hr', 'dm','dn', 'N', 'Istrain', 'Thickness (mm)\nif external skin surfacic mesh\nMTCC', 'Ashear',
                                'empty1', 'Ithick', 'Iplas'],
                        index=False)

    # Create mat_law01 XLSX
    mat_law01 = pd.read_csv(matLawRadFile)
    mat_law01.to_excel(matLawXLSXBrut,
                       header=['mat_law02', 'Radioss material card\nMTCC', 'RHO', 'E', 'v', 'Iflag', 'a', 'b', 'n',
                               'FPS Value %\nMTCC', 'smax', 'c', 'e0', 'ICC', 'Fsmooth', 'Fcut', 'm', 'Tmelt', 'rho0Cp',
                               'Ti'],
                       index=False)

    # Merge global_template.xlsx with prop_type1_rad__xlsx_brut.xlsx
    df = pd.DataFrame()
    df = df.append(pd.read_excel(globalTemplateXLSX, usecols="A:BH"), ignore_index=True)
    df = df.append(pd.read_excel(propTypeXLSXBrut, usecols="A:V"), ignore_index=True)
    df.to_excel(propTypeXLSXExploitable, index=False)

    # Merge mat_law1_rad__xlsx_brut.xlsx with prop_type1_rad_xlsx_exploitable.xlsx
    df1 = pd.DataFrame()
    df1 = df1.append(pd.read_excel(propTypeXLSXExploitable, usecols="A:BH"), ignore_index=True)
    df1 = df1.append(pd.read_excel(matLawXLSXBrut, usecols="A:T"), ignore_index=True)
    df1.to_excel(globalExploitableXLSX, index=False)

    # Test to show diff.
    df2 = pd.read_excel(inputXLSXFile, usecols="B:Y", header=[1]).fillna("")
    df3 = pd.read_excel(globalExploitableXLSX, usecols="A:BH").fillna("")

    dfEntry = df2.copy()
    dfOut = df3.copy()
    maxColEntry = int(dfEntry.shape[1]) - 1

    for col in range(dfEntry.shape[1]):
        for row in range(dfEntry.shape[0]):

            # Thickness + Radios Part Name + Shell Properties
            try:
                if col == dfEntry.columns.get_loc("Parts and Components\nCMAG"):
                    for row2 in range(dfOut.shape[0]):

                        # Init Var
                        inputThicknessColumn = dfEntry.columns.get_loc(
                            "Thickness (mm)\nif external skin surfacic mesh\nMTCC")
                        inputMeshTypColumn = dfEntry.iloc[row, dfEntry.columns.get_loc("Mesh type\nMTCC /CMAG")]

                        rawValueEntry = df2.iloc[row, col]
                        if rawValueEntry.find('-') != -1 and rawValueEntry != "E-Bridge":
                            valueEntry = rawValueEntry.split("-", 1)
                            valueEntry = valueEntry[0].replace(" ", "_").lower()
                        elif rawValueEntry.find('(') != -1:
                            valueEntry = rawValueEntry.split("\n", 1)
                            valueEntry = valueEntry[0].replace(" ", "_").lower()
                        elif rawValueEntry == "":
                            valueEntry = rawValueEntry.replace("", "empty").lower()
                        else:
                            valueEntry = rawValueEntry.replace(" ", "_").lower()

                        if valueEntry[-1] == "_":
                            valueEntry = valueEntry[:-1]
                        elif valueEntry[0] == "_":
                            valueEntry = valueEntry[:0]

                        rawValueOut = df3.iloc[row2, df3.columns.get_loc("Radioss Part name\nMTCC")]
                        valueOut = re.split(r'(?<=\D)(?=\d)', rawValueOut)
                        valueOut = valueOut[0].lower()

                        if valueOut != "" and valueOut[-1] == "_":
                            valueOut = valueOut[:-1]

                        if valueEntry == valueOut:
                            rawValueEntryThickness = df2.iloc[row, inputThicknessColumn]
                            valueEntryThickness = rawValueEntryThickness.split(" ", 1)
                            # todo : Fix multiple thickness
                            valueEntryThickness = int(float(valueEntryThickness[0].replace(",", ".") or 0))

                            valueOutThickness = int(df3.iloc[row2, dfOut.columns.get_loc(
                                "Thickness (mm)\nif external skin surfacic mesh\nMTCC")] or 0)

                            goodValue = '{} ! mm'.format(valueOutThickness)
                            badValue = '{}-->{}'.format(valueOutThickness, valueEntryThickness)

                            # External Skin Shell Mesh | GOOD
                            if valueEntryThickness == valueOutThickness and inputMeshTypColumn == 'External skin shell mesh':
                                dfEntry.iloc[row, inputThicknessColumn] = goodValue

                            # External Skin Shell Mesh | NOT GOOD
                            if valueEntryThickness != valueOutThickness and inputMeshTypColumn == 'External skin shell mesh':
                                dfEntry.iloc[row, inputThicknessColumn] = badValue

                            # Mid-Surface Shell Mesh | GOOD
                            if int(valueOutThickness) > 1 and inputMeshTypColumn == 'Mid-surface shell mesh':
                                dfEntry.iloc[row, inputThicknessColumn] = goodValue

                            # Mid-Surface Shell Mesh | VERIFY
                            if int(valueOutThickness) == 1 and inputMeshTypColumn == 'Mid-surface shell mesh':
                                dfEntry.iloc[row, inputThicknessColumn] = '{} ?'.format(valueOutThickness)

                            # Mid-Surface Shell Mesh | NOT GOOD
                            if int(valueOutThickness) < 1 and inputMeshTypColumn == 'Mid-surface shell mesh':
                                dfEntry.iloc[row, inputThicknessColumn] = badValue

                            # Radioss Part (user control)
                            dfEntry.iloc[row, dfEntry.columns.get_loc("Radioss Part name\nMTCC")] = valueOut

                            # Shell Properties
                            for col3 in range(dfOut.shape[1]):
                                if col3 > maxColEntry:
                                    # Init var
                                    Ishell = dfOut.columns.get_loc("Ishell")
                                    outputCellValue = dfOut.iloc[row, col3]
                                    goodValue2 = '{} !'.format(outputCellValue)
                                    badValue2 = '-->{}'.format(outputCellValue)
                                    outputThicknessColumn = dfOut.iloc[row, inputThicknessColumn]

                                    # Break Idrill
                                    if col3 == dfOut.columns.get_loc("mat_law02"):
                                        break

                                    # No value
                                    if outputCellValue == 'x':
                                        dfOut.loc[row, col3] = ('{} ?').format(outputCellValue)

                                    # Ishell
                                    if col3 == Ishell:
                                        if outputThicknessColumn < 7 and \
                                                outputCellValue == 24:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if 7 <= outputThicknessColumn <= 10 and \
                                                outputCellValue == 4:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputThicknessColumn > 10 and \
                                                outputCellValue == 1:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputThicknessColumn < 7 and \
                                                outputCellValue != 24 and outputCellValue != 'x' or 7 <= \
                                                outputThicknessColumn <= 10 and \
                                                outputCellValue != 4 and outputCellValue != 'x' or \
                                                outputThicknessColumn > 10 and \
                                                outputCellValue != 1 and outputCellValue != 'x':
                                            dfEntry.loc[row, col3] = badValue2

                                    # Ismstr & Ish3n & Istrain & Ithick & Iplas
                                    if col3 == dfOut.columns.get_loc("Ismstr") or col3 == dfOut.columns.get_loc(
                                            "Ish3n") or col3 == dfOut.columns.get_loc(
                                        "Istrain") or col3 == dfOut.columns.get_loc(
                                        "Ithick") or col3 == dfOut.columns.get_loc("Iplas"):
                                        if outputCellValue == 2:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputCellValue != 2 and outputCellValue != 'x':
                                            dfEntry.loc[row, col3] = badValue2

                                    # hm & hf & hr
                                    if col3 == dfOut.columns.get_loc("hm") or col3 == dfOut.columns.get_loc(
                                            "hf") or col3 == dfOut.columns.get_loc("hr"):
                                        if outputCellValue == 0.01:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputCellValue != 0.01 and outputCellValue != 'x':
                                            dfEntry.loc[row, col3] = badValue2

                                    # dm && dn
                                    if col3 == dfOut.columns.get_loc("dm") or col3 == dfOut.columns.get_loc("dn"):
                                        if outputCellValue == 0:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputCellValue != 0 and outputCellValue != 'x':
                                            dfEntry.loc[row, col3] = badValue2

                                    # N
                                    if col3 == dfOut.columns.get_loc("N"):
                                        if outputThicknessColumn >= 1 and \
                                                outputCellValue == 5:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputThicknessColumn < 1 and \
                                                outputCellValue == 3:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputThicknessColumn >= 1 and \
                                                outputCellValue != 5 and outputCellValue != 'x' or \
                                                outputThicknessColumn < 1 and \
                                                outputCellValue != 3 and outputCellValue != 'x':
                                            dfEntry.loc[row, col3] = badValue2

                                    # Ashear
                                    if col3 == dfOut.columns.get_loc("Ashear"):
                                        if outputCellValue == 5 / 6:
                                            dfEntry.loc[row, col3] = goodValue2
                                        if outputCellValue != 5 / 6 and outputCellValue != 'x':
                                            dfEntry.loc[row, col3] = badValue2
            except Exception as e:
                print(e)

            # Radios Mat. Card
            try:
                i = 0
                inputRadiossMatNameColumn = dfEntry.columns.get_loc("Radioss material card\nMTCC")
                outputRadiossMatNameColumn = dfOut.columns.get_loc("Radioss material card\nMTCC")
                if col == inputRadiossMatNameColumn:
                    for row3 in range(dfOut.shape[0]):
                        outputFPSValueColumn = dfOut.iloc[row3, dfOut.columns.get_loc("FPS Value %\nMTCC")]
                        outputMatIDValueColumn = int(dfOut.iloc[row, dfOut.columns.get_loc("mat_ID")] or 0)

                        badValue3 = '{}-->{}'.format(valueOutThickness, valueEntryThickness)
                        goodValue3 = '{} !'.format(outputFPSValueColumn)

                        # if dfEntry.iloc[row, dfEntry.columns.get_loc("Radioss Part name\nMTCC")] == dfOut.iloc[row3, dfOut.columns.get_loc("Radioss Part name\nMTCC")]:
                        #     if outputMatIDValueColumn == 7:
                        #         dfEntry.iloc[row, inputRadiossMatNameColumn] = "DP780_ODG2_MED-5"
                        #         print("ouais")

                        if 'ODG3' in dfEntry.iloc[row, inputRadiossMatNameColumn] and dfEntry.iloc[
                            row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")] == "Yes":
                            dfEntry.iloc[
                                row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")] = '{} !'.format(
                                dfEntry.iloc[row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")])

                        if 'ODG3' in dfEntry.iloc[row, inputRadiossMatNameColumn] and dfEntry.iloc[
                            row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")] != "Yes":
                            dfEntry.iloc[
                                row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")] = '-->{}'.format(
                                dfEntry.iloc[row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")])

                        if dfEntry.iloc[row, inputRadiossMatNameColumn] == dfOut.iloc[row3, outputRadiossMatNameColumn]:
                            # todo global : More scalability with %
                            # todo Link between RadiosMat and MatID

                            # getMatId = dfOut.iloc[row3, dfOut.columns.get_loc("mat_law02")].split("/")
                            # getMatId = int(getMatId[-1] or 9999)
                            #
                            # if getMatId == 7:
                            #     print('test1', getMatId)
                            #
                            # if outputMatIDValueColumn == 7:
                            #     print('test2', outputMatIDValueColumn)
                            #
                            # if dfEntry.iloc[
                            #     row, inputRadiossMatNameColumn] == "DP780_ODG2_MED-5" and outputMatIDValueColumn == 7:
                            #     print("test3")
                            #
                            # if outputMatIDValueColumn == getMatId:
                            #     print("test4")
                            #
                            # if dfEntry.iloc[
                            #     row, inputRadiossMatNameColumn] == "DP780_ODG2_MED-5" and outputMatIDValueColumn == getMatId:
                            #     print("work")

                            # if dfEntry.iloc[row, inputRadiossMatNameColumn].find("ODG3") != 1:
                            #     print("find")
                            #
                            # if dfEntry.iloc[row, dfEntry.columns.get_loc("Expected failure criterion\nCMAG")] == "Yes":
                            #     print("findYes")

                            # DP780_ODG2_MED-5
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "DP780_ODG2_MED-5" and outputFPSValueColumn != 0.15:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = badValue3
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "DP780_ODG2_MED-5" and outputFPSValueColumn == 0.15:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = goodValue3

                            # CP1000_ODG2_LOT-5
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "CP1000_ODG2_LOT-5" and outputFPSValueColumn != 0.09:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = badValue3
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "CP1000_ODG2_LOT-5" and outputFPSValueColumn == 0.09:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = goodValue3

                            # HD340LA_ODG2_MED-5
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "HD340LA_ODG2_MED-5" and outputFPSValueColumn != 0.21:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = badValue3
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "HD340LA_ODG2_MED-5" and outputFPSValueColumn == 0.21:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = goodValue3

                            # HD380LA_ODG2_MED-5
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "HD380LA_ODG2_MED-5" and outputFPSValueColumn != 0.19:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = badValue3
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "HD380LA_ODG2_MED-5" and outputFPSValueColumn == 0.19:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = goodValue3

                            # todo E335D_ODG2_MED-5_johnson : More scalability with "Name"
                            # E335D_ODG2_MED-5_johnson
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "E335D_ODG2_MED-5_johnson" and outputFPSValueColumn != 0.15:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = badValue3
                            if dfEntry.iloc[row, inputRadiossMatNameColumn] == "E335D_ODG2_MED-5_johnson" and outputFPSValueColumn == 0.15:
                                dfEntry.iloc[row, dfEntry.columns.get_loc("FPS Value %\nMTCC")] = goodValue3



            except Exception as e:
                print(e)

    oui = pd.read_excel(globalExploitableXLSX, usecols="A:AK", nrows=1).columns

    writer = pd.ExcelWriter("../final.xlsx", engine='xlsxwriter')
    dfEntry.to_excel(writer, sheet_name='DIFF', header=oui, index=False)

    workbook = writer.book
    worksheet = writer.sheets['DIFF']
    worksheet.hide_gridlines(2)

    # define formats
    white_fmt = workbook.add_format({'font_color': ' #ffffff '})
    highlight_error = workbook.add_format({'font_color': '#FF0000', 'bg_color': '#B1B3B3'})
    highlight_verify = workbook.add_format({'font_color': '#FF0000', 'bg_color': '#FFAA00'})
    highlight_good = workbook.add_format({'font_color': '#FF0000', 'bg_color': '#42FF00'})

    # highlight error cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                               'criteria': 'containing',
                                               'value': '-->',
                                               'format': highlight_error})

    # highlight good cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                               'criteria': 'containing',
                                               'value': '!',
                                               'format': highlight_good})

    # highlight verify cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                               'criteria': 'containing',
                                               'value': '?',
                                               'format': highlight_verify})

    # highlight unchanged cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                               'criteria': 'not containing',
                                               'value': '→',
                                               'format': white_fmt})
    # save
    writer.save()
