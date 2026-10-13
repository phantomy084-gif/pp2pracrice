filename = input("Enter filename: ")

with open(filename, "r") as file:
    lines = file.readlines()

print("Number of lines:", len(lines))
