source = input("Enter source filename: ")
destination = input("Enter destination filename: ")

with open(source, "r") as file:
    content = file.read()

with open(destination, "w") as file:
    file.write(content)

print("Content copied successfully")