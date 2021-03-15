import pandas as pd


def prop_type1_xlsx_creation():
    inputRadFile = "demo/fichier_sortie.rad"
    outputRadFile = "demo/rad_file_clean.txt"

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
    df.to_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', index=False)

    # Merge demo/fichier_entree.xlsx with fichier_rad_en_xlsx_exploitable.xlsx
    df2 = pd.DataFrame()
    df2 = df2.append(pd.read_excel('demo/fichier_entree.xlsx', usecols="A:W", header=[3]), ignore_index=True)
    df2 = df2.append(pd.read_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', usecols="A:AM"), ignore_index=True)
    df2.to_excel('../fichier_fusionner.xlsx')

    # todo
    # Test to show diff.
    df3 = pd.read_excel('demo/fichier_entree.xlsx', usecols="B:W", header=[3]).fillna(0)
    df4 = pd.read_excel('demo/fichier_rad_en_xlsx_exploitable.xlsx', usecols="A:AM").fillna(0)

    dfEntry = df3.copy()
    dfOut = df4.copy()
    for col in range(dfEntry.shape[1]):
        for row in range(dfEntry.shape[0]):
            if col == 8:
                for col2 in range(dfOut.shape[1]):
                    for row2 in range(dfOut.shape[0]):
                        valueEntry = df3.iloc[row, col]
                        try:
                            valueOut = df4.iloc[row2, col2]
                            if valueEntry == valueOut:
                                valueEntry = df3.iloc[row, 12]
                                valueOut = df4.iloc[row2, 12]
                                if valueEntry != valueOut:
                                    dfEntry.iloc[row, 12] = ('{}-->{}').format(valueEntry, valueOut)
                        except:
                            dfEntry.iloc[row, col] = ('{}-->{}').format(valueEntry, 'NaN')

    writer = pd.ExcelWriter("../final.xlsx", engine='xlsxwriter')

    dfEntry.to_excel(writer, sheet_name='DIFF', index=False)

    workbook = writer.book
    worksheet = writer.sheets['DIFF']
    worksheet.hide_gridlines(2)

    # define formats
    white_fmt = workbook.add_format({'font_color': ' #ffffff '})
    highlight_fmt = workbook.add_format({'font_color': '#FF0000', 'bg_color': '#B1B3B3'})

    # highlight changed cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                               'criteria': 'containing',
                                               'value': '-->',
                                               'format': highlight_fmt})
    # highlight unchanged cells
    worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                               'criteria': 'not containing',
                                               'value': '→',
                                               'format': white_fmt})
    # save
    writer.save()
