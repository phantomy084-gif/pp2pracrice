import shutil
import os

os.makedirs("folder1", exist_ok=True)
os.makedirs("folder2", exist_ok=True)

shutil.copy("sample.txt", "folder1/sample.txt")
shutil.move("folder1/sample.txt", "folder2/sample.txt")

print("File copied and moved")