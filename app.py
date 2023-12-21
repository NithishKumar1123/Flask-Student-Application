import csv
from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt

def table_definition():
  table = []
  with open("data.csv", "r") as file_object:
    data = csv.reader(file_object)
    for row in data:
      table.append(row)
    file_object.close()
  for i in range(1, len(table)):
    for j in range(len(table[i])):
      table[i][j] = int(table[i][j])
  return table[1:]

def student(student_id, table):
  result = []
  total = 0
  flag = True
  for row in table:
    if(row[0] == student_id):
      flag = False
      result.append(row)
      total += row[2]
  if(flag):
    return (None, None)
  return (result, total)

def course(course_id, table):
  max = 0
  total = 0
  count = 0
  flag = True
  mark_list = []
  for row in table:
    if(row[1] == course_id):
      flag = False
      mark_list.append(row[2])
      total += row[2]
      count += 1
      if(max < row[2]):
        max = row[2]
  if(flag):
    return (None, None, None)
  avg = total / count
  return (avg, max, mark_list)

def figure(mark_list):
  plt.hist(mark_list, bins = 10)
  plt.xlabel('Marks')
  plt.ylabel('Frequency')
  plt.savefig('static\img.jpg')

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
  if request.method == "GET":
    return render_template("index.html")
  else:
    flag = False
    choice = request.form["ID"]
    ID = request.form["id_value"]
    table = table_definition()
    if(choice == 'student_id'):
      (result, total) = student(int(ID), table)
      if(result == None):
        flag = True
      else:
        return render_template("student_details.html", result = result, total = total)
    elif(choice == 'course_id'):
      (avg, max, mark_list) = course(int(ID), table)
      if(avg == None):
        flag = True
      else:
        figure(mark_list)
        return render_template("course_details.html", avg = avg, max = max)
    if(flag):
      return render_template("Wrong_inputs.html")

if __name__ == '__main__':
  app.run()