import pandas as pd
import re


def prop_type1_xlsx_creation():
    outputRadFile = "demo/rad_file_clean.txt"

    # Create XLSX File with outputRadFile
    read_file = pd.read_csv(outputRadFile)
    read_file.to_excel('demo/fichier_rad_en_xlsx_brut.xlsx',
                       header=['Suffix to add\nif necessary\nMTCC', "Radioss Part name\nMTCC", 'Ishell', 'Ismstr',
                               'Ish3m',
                               'Idrill', 'hm', 'hf', 'hr', 'dm',
                               'dn', 'N', 'Istrain', 'Thickness (mm)\nif external skin surfacic mesh\nMTCC', 'Ashear',
                               'empty1', 'Ithick', 'Iplas', 'empty2'],
                       index=False)

    # Merge template_prop_type1.xlsx with fichier_rad_en_xlsx.xlsx
    df = pd.DataFrame()
    df = df.append(pd.read_excel('prop_type/prop_type1/template_prop_type1.xlsx', usecols="A:AN"), ignore_index=True)
    df = df.append(pd.read_excel('demo/fichier_rad_en_xlsx_brut.xlsx', usecols="A:S"), ignore_index=True)
    df.to_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', index=False)

    # Merge demo/fichier_entree.xlsx with fichier_rad_en_xlsx_exploitable.xlsx
    df1 = pd.DataFrame()
    df1 = df1.append(pd.read_excel('demo/fichier_entree.xlsx', usecols="B:Y", header=[1]), ignore_index=True)
    df1 = df1.append(pd.read_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', usecols="A:AN"), ignore_index=True)
    df1.to_excel('../fichier_fusionner.xlsx')

    # Test to show diff.
    df2 = pd.read_excel('demo/fichier_entree.xlsx', usecols="B:Y", header=[1]).fillna("")
    df3 = pd.read_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', usecols="A:AM", header=[0]).fillna("")

    dfEntry = df2.copy()
    dfOut = df3.copy()
    maxColEntry = int(dfEntry.shape[1]) - 1
    valueEntry = "empty"

    for col in range(dfEntry.shape[1]):
        for row in range(dfEntry.shape[0]):

            # Thickness + Radios Part Name
            if col == df3.columns.get_loc("Parts and Components\nCMAG"):
                for row2 in range(dfOut.shape[0]):

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

                    try:
                        rawValueOut = df3.iloc[row2, df3.columns.get_loc("Radioss Part name\nMTCC")]
                        valueOut = re.split(r'(?<=\D)(?=\d)', rawValueOut)
                        valueOut = valueOut[0].lower()
                        try:
                            if valueOut[-1] == "_":
                                valueOut = valueOut[:-1]
                        except:
                            print(valueOut)

                        if valueEntry == valueOut:
                            rawValueEntryThickness = df2.iloc[
                                row, df2.columns.get_loc("Thickness (mm)\nif external skin surfacic mesh\nMTCC")]
                            valueEntryThickness = rawValueEntryThickness.split(" ", 1)
                            # todo : Fix multiple thickness
                            valueEntryThickness = int(float(valueEntryThickness[0].replace(",", ".") or 0))

                            valueOutThickness = int(df3.iloc[row2, df3.columns.get_loc(
                                "Thickness (mm)\nif external skin surfacic mesh\nMTCC")])

                            # External Skin Shell Mesh | GOOD
                            if valueEntryThickness == valueOutThickness and dfEntry.iloc[
                                row, df3.columns.get_loc("Mesh type\nMTCC /CMAG")] == 'External skin shell mesh':
                                dfEntry.iloc[row, dfEntry.columns.get_loc(
                                    "Thickness (mm)\nif external skin surfacic mesh\nMTCC")] = ('{} ! mm').format(
                                    valueOutThickness)

                            # External Skin Shell Mesh | NOT GOOD
                            if valueEntryThickness != valueOutThickness and dfEntry.iloc[
                                row, df3.columns.get_loc("Mesh type\nMTCC /CMAG")] == 'External skin shell mesh':
                                dfEntry.iloc[row, dfEntry.columns.get_loc(
                                    "Thickness (mm)\nif external skin surfacic mesh\nMTCC")] = ('{}-->{}').format(
                                    valueOutThickness, valueEntryThickness)

                            # Mid-Surface Shell Mesh | GOOD
                            if int(valueOutThickness) > 1 and dfEntry.iloc[
                                row, df3.columns.get_loc("Mesh type\nMTCC /CMAG")] == 'Mid-surface shell mesh':
                                dfEntry.iloc[row, dfEntry.columns.get_loc(
                                    "Thickness (mm)\nif external skin surfacic mesh\nMTCC")] = ('{} ! mm').format(
                                    valueOutThickness)

                            # Mid-Surface Shell Mesh | VERIFY
                            if int(valueOutThickness) == 1 and dfEntry.iloc[
                                row, df3.columns.get_loc("Mesh type\nMTCC /CMAG")] == 'Mid-surface shell mesh':
                                dfEntry.iloc[row, dfEntry.columns.get_loc(
                                    "Thickness (mm)\nif external skin surfacic mesh\nMTCC")] = ('{} ?').format(
                                    valueOutThickness)

                            # Mid-Surface Shell Mesh | NOT GOOD
                            if int(valueOutThickness) < 1 and dfEntry.iloc[
                                row, df3.columns.get_loc("Mesh type\nMTCC /CMAG")] == 'Mid-surface shell mesh':
                                dfEntry.iloc[row, dfEntry.columns.get_loc(
                                    "Thickness (mm)\nif external skin surfacic mesh\nMTCC")] = ('{}-->{}').format(
                                    valueOutThickness, valueEntryThickness)

                            dfEntry.iloc[row, dfEntry.columns.get_loc("Radioss Part name\nMTCC")] = valueOut

                    except Exception as e:
                        print(e)
                        rawValueEntryThickness = df2.iloc[
                            row, df2.columns.get_loc("Thickness (mm)\nif external skin surfacic mesh\nMTCC")]
                        valueEntryThickness = rawValueEntryThickness.split(" ", 1)
                        dfEntry.iloc[
                            row2, dfEntry.columns.get_loc("Thickness (mm)\nif external skin surfacic mesh\nMTCC")] = (
                            '{}-->{}').format(valueEntryThickness, 'NaN')

            # Shell Properties
            if col == maxColEntry:
                for col3 in range(dfOut.shape[1]):
                    if col3 > maxColEntry:
                        dfEntry.loc[row, col3] = dfOut.iloc[row, col3]

    writer = pd.ExcelWriter("../final.xlsx", engine='xlsxwriter')
    dfEntry.to_excel(writer, sheet_name='DIFF', index=False)

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
                                               'value': '! mm',
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
