import os

print("WORKING DIRECTORY:", os.getcwd())
print("Contents of current dir:", os.listdir("."))

print("\nDoes data/ exist? ", os.path.exists("data"))
if os.path.exists("data"):
    print("data/:", os.listdir("data"))

print("\nDoes data/processed exist? ", os.path.exists("data/processed"))
if os.path.exists("data/processed"):
    print("data/processed/:", os.listdir("data/processed"))
