from ..prop_type1 import prop_type1_xlsx_creation


# =============
# /PROP/TYPE1/
# =============

def prop_type1_rad_file_cleanup():
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
    prop_type1_xlsx_creation.prop_type1_xlsx_creation()
