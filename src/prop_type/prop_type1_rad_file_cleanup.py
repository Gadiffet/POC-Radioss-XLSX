# =============
# /PROP/TYPE1/
# =============
def prop_type1_rad_file_cleanup():
    # File Path
    inputRadFile = "demo/fichier_sortie.rad"
    outputRadFile = "demo/rad_file_prop_type1_cleanup.txt"
    indexPropType1List = []
    radFileIndex = []
    propType1 = 0

    # Open File
    with open(outputRadFile, "w") as radFileClean:
        with open(inputRadFile, "r") as radFile:

            for index, lineTest in enumerate(radFile, start=0):
                if index >= 4700119:
                    radFileIndex.append([index, lineTest])

            for index, lineTes in radFileIndex:
                if '/PROP/TYPE1/' in lineTes:
                    indexPropType1List.append(index - 3)

            indexPropType1List.pop(-1)

            # The For loop, executes a set of instructions, once for each line of the RAD file
            for index in indexPropType1List:
                for index2, line in radFileIndex:
                    if index2 == index:
                        # Add 5 to the propType1 variable
                        propType1 = 8
                        # Add a carriage return at the end of the line
                        radFileClean.write("\n")

                    # Check if the variable propType1 is bigger than 0
                    if propType1 > 0:

                        # Initialize variable
                        counterSpace = 0
                        counterCharacter = 1
                        counterString = 0

                        if propType1 != 4:
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

                        if propType1 == 6 and len(line.split()) + counterString < 3:
                            catchInfo = "x"
                            radFileClean.write("," + catchInfo)
                            radFileClean.write("," + catchInfo)

                        # If propType1 is bigger than 3, it writes a comma at the end of the line.
                        if propType1 == 8 or propType1 == 6:
                            radFileClean.write(",")

                        # Subtract 1
                        propType1 -= 1
        # Close File
        radFile.close()
    radFileClean.close()