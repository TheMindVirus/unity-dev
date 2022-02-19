file1 = open("sample.json", "r")
data1 = file1.read()
file1.close()

file2 = open("test.json", "r")
data2 = file2.read()
file2.close()

print(data1 == data2)
