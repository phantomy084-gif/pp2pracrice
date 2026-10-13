import string

for letter in string.ascii_uppercase:
    filename = letter + ".txt"

    with open(filename, "w") as file:
        file.write("This is file " + filename)

print("26 files created")