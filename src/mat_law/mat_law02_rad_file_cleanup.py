# =============
# /MAT/LAW02/
# =============
def mat_law02_rad_file_cleanup():
    # File Path
    inputRadFile = "demo/fichier_sortie.rad"
    outputRadFile = "demo/rad_file_mat_law02_cleanup.txt"

    # Open File
    with open(outputRadFile, "w") as radFileClean:
        with open(inputRadFile, "r") as radFile:
            # Initialize variable
            matLaw02 = 0
            a = 0
            # The For loop, executes a set of instructions, once for each line of the RAD file
            for index, line in enumerate(radFile):

                # Check if '/MAT/LAW02/' exists in a row
                if '/MAT/LAW02/' in line:
                    # Add 12 to the matLaw02 variable
                    matLaw02 = 12
                    # Add a carriage return at the end of the line
                    radFileClean.write("\n")

                # Check if the variable matLaw02 is bigger than 0
                if matLaw02 > 0:

                    # Initialize variable
                    counterSpace = 0
                    counterCharacter = 1
                    counterString = 0

                    # Remove useless value
                    if matLaw02 != 10 and matLaw02 != 8 and matLaw02 != 6 and matLaw02 != 4 and matLaw02 != 2:

                        # The For loop, executes a set of instructions, once for each "characters" in Line
                        for space in line:

                            # Reset the variable when there is whitespace
                            if space.isspace() is True:
                                counterSpace += 1
                                counterCharacter = 0

                            # Write each "character" in outputRadFile if it is not a whitespace
                            if matLaw02 != 11:
                                if space.isspace() is False:
                                    # If counterCharacter is bigger than 1, it writes without a comma
                                    if counterCharacter >= 1:
                                        radFileClean.write(space)
                                    # Else it writes a comma
                                    else:
                                        radFileClean.write("," + space)
                                    counterSpace = 0
                                    counterCharacter += 1
                            else:
                                if space.isspace() is False:
                                    radFileClean.write(space)

                            # Write an "x" in outputRadFile if there are more than 18 whitespace
                            if counterSpace > 18:
                                catchInfo = "x"
                                radFileClean.write("," + catchInfo)
                                counterSpace = 0
                                # Add +1 to count "x" as a string
                                counterString += 1

                    # If matLaw02 is 3, it writes a comma at the end of the line.
                    if matLaw02 == 12:
                        radFileClean.write(",")

                    # Add 5 "x", if the line is null. len = count the number of characters | split() = delete whitespace
                    if len(str(line.split())) < 3:
                        catchInfo = "x" * 5
                        # Stringify the catchInfo variable, because it becomes a list.
                        toString = ','.join(catchInfo)
                        radFileClean.write("," + toString)

                    # Subtract 1
                    matLaw02 -= 1

        # Close File
        radFile.close()
    radFileClean.close()
