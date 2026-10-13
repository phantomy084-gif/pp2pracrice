file = open("sample.txt", "a")

file.write("New line 1\n")
file.write("New line 2\n")

file.close()

file = open("sample.txt", "r")
print(file.read())
file.close()