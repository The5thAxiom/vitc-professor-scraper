file = open("info.txt", "r")
text = file.read()
file.close()

file = open("info.txt", "w")
file.write(
    ("[\n" + text.replace("}", "},") + "]").replace(",]", "]")
)
file.close()