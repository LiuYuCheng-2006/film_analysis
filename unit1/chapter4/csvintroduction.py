# with open("csv_data/01.csv","w",encoding="utf-8") as f:
#     f.write("姓名,年龄,性别,爱好\n")
#     f.write("小王,18,男,football\n")
#     f.write("小李,18,女,Python\n")
#     f.write("小张,18,男,C++\n")
#
# with open("csv_data/01.csv","r",encoding="utf-8") as f:
#
#     for line in f:
#         print(line.strip())
import csv
with open("csv_data/02.csv","w",encoding="utf-8",newline="") as f:
     writer=csv.DictWriter(f,fieldnames=["name","age","gender","hobby"])
     writer.writeheader()
     writer.writerow({"name":"xiaowang","age":18,"gender":"male","hobby":"football,Java"})
     writer.writerow({"name":"xiaoli","age":18,"gender":"female","hobby":"Python"})
     writer.writerow({"name":"xiaozhang","age":18,"gender":"male","hobby":"C++"})
     writer.writerow({"name":"taoge","age":19,"gender":"male","hobby":"Go"})
with open("csv_data/02.csv","r",encoding="utf-8") as f:
     reader = csv.DictReader(f)
     for row in reader:
          print(row)


