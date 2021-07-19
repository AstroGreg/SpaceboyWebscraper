import os

for file in os.listdir("images"):
    filename = os.fsdecode(file)
    os.path.join("images", filename)
    pre, ext = os.path.splitext(os.path.join("images", filename))
    os.rename(os.path.join("images", filename), pre + ".jpg")