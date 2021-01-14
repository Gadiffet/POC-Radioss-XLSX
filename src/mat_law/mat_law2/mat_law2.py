# =============
# /MAT/LAW02/
# =============

def mat_law2():
    # File Path
    inputRadFile = "demo/fichierSortie.rad"
    outputRadFile = "demo/radFileClean.txt"

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

                    # Check if the variable a is equal to 0, and add the first row in outputRadFile (it's used to add
                    # the name of the column)

                    # todo
                    if a == 0:
                        radFileClean.write("PROP/TYPE,PROP_TITLE,Ishell,Ismstr,Ish3m,Idrill,"
                                           "hm,hf,hr,dm,dn,N,Istrain,Thick,Ashear,"
                                           "Ithick,Iplas")
                        a = 1
                    # Check if the variable a is greater than 0, and add a carriage return at the end of the line
                    if a > 0:
                        radFileClean.write("\n")

                # Check if the variable matLaw02 is bigger than 0
                if matLaw02 > 0:
                    # Subtract 1
                    matLaw02 -= 1

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

                    # If matLaw02 is bigger than 3, it writes a comma at the end of the line.
                    if matLaw02 > 3:
                        radFileClean.write(",")

                    # If matLaw02 is equal to 2, it writes a "x" at the end of the Line (to complete the schema)
                    if matLaw02 == 2 and len(line.split()) + counterString < 4:
                        catchInfo = "x"
                        radFileClean.write("," + catchInfo)
                        counterSpace = 0

                    # If matLaw02 is equal to 0, it writes a "x" at the end of the Line (to complete the schema)
                    if matLaw02 == 0 and len(line.split()) + counterString < 8:
                        catchInfo = "x"
                        radFileClean.write("," + catchInfo)
                        counterSpace = 0

        # Close File
        radFile.close()
    radFileClean.close()
