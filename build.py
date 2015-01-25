#!/usr/bin/python

import csv, sys, os
from os import listdir
from os.path import isfile, join

cwd = os.path.dirname(os.path.realpath(__file__))
csvdir = os.path.abspath(os.path.join(cwd,"csv"))
viewsdir = os.path.abspath(os.path.join(cwd,"views"))
outputdir = os.path.abspath(os.path.join(cwd,"output"))

bashfile = os.path.join(outputdir,"buildOutput.bash");
sqlfile = os.path.join(outputdir,"buildDb.sql");

sys.stdout = open(sqlfile, 'w')

reference = [];

def getRate(code,ratename):
  for ref in reference:
    if ref["code"] == code and ref["rate"] == ratename:
      return ref["id"];
  return "null"

with open("csv/vatrates.csv", 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='"')
  lines = []

  for x in reader:
    lines.append(x)

print "SET FOREIGN_KEY_CHECKS=0;\n"

print "DROP TABLE IF EXISTS vr_vatrates;"
print "CREATE TABLE vr_vatrates (";
print "  id INTEGER PRIMARY KEY NOT NULL,"
print "  country TEXT NOT NULL,"
print "  code VARCHAR(2) NOT NULL,"
print "  rate_name TEXT NOT NULL,"
print "  rate_value DOUBLE,"
print "  eusort INTEGER NOT NULL"
print ");\n\n"

#print "CREATE TABLE vatrates (";
#print "  id INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,"
#print "  country TEXT NOT NULL UNIQUE,"
#print "  code TEXT NOT NULL UNIQUE,"
#print "  standard_rate DOUBLE NOT NULL,"
#print "  reduced_rate_1 DOUBLE,"
#print "  reduced_rate_2 DOUBLE,"
#print "  super_reduced_rate DOUBLE,"
#print "  parking_rate DOUBLE"
#print ");\n"


sqlstart = "INSERT INTO vr_vatrates(id,country,code,rate_name,rate_value,eusort) VALUES("

colnames = [
    "country",
    "code",
    "standard",
    "reduced_1",
    "reduced_2",
    "super_reduced",
    "parking",
    "eusort"
    ]


sid = 0;
for i in range(1,len(lines)):
  row = lines[i]

  sqlmid = "\"" + row[0] + "\","
  sqlmid = sqlmid + "\"" + row[1] + "\","

  for x in range(2,7):
    sid = sid + 1
    sys.stdout.write(sqlstart)
    sys.stdout.write(str(sid) + ",")
    sys.stdout.write(sqlmid)
    sys.stdout.write("\"" + colnames[x] + "\",")
    if row[x]:
      sys.stdout.write(row[x])
    else:
      sys.stdout.write("null")
    sys.stdout.write(",")
    if row[7]:
      sys.stdout.write(row[7])
    else:
      sys.stdout.write("null")
    sys.stdout.write(");\n")

    ref = {}
    ref["code"] = row[1]
    ref["rate"] = colnames[x]
    ref["id"] = sid
    reference.append(ref)

  sid = sid + 1
  sys.stdout.write(sqlstart)
  sys.stdout.write(str(sid) + ",")
  sys.stdout.write(sqlmid)
  sys.stdout.write("\"exempt\",0,")
  if row[7]:
    sys.stdout.write(row[7])
  else:
    sys.stdout.write("null")
  sys.stdout.write(");\n")

  ref = {}
  ref["code"] = row[1]
  ref["rate"] = "exempt"
  ref["id"] = sid
  reference.append(ref)

vatfiles = [ f for f in listdir(csvdir) if isfile(join(csvdir,f)) ]

vatclasses = []

for f in vatfiles:
  n = os.path.basename(f)
  fn = os.path.splitext(n)[0]
  ext = os.path.splitext(n)[1]
  if ext == ".csv" and fn != "vatrates":
    vatclasses.append(fn)

for c in vatclasses:
  csvf = os.path.join(csvdir, c + ".csv")

  with open(csvf, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    lines = []
    for x in reader:
      lines.append(x)

  print "DROP TABLE IF EXISTS vr_raw_" + c + ";"

  print "CREATE TABLE vr_raw_" + c + "(";
  print "  code VARCHAR(2) NOT NULL UNIQUE PRIMARY KEY,"
  print "  rate INTEGER NOT NULL,"
  print "  comment TEXT,"
  print "  FOREIGN KEY (rate) REFERENCES vr_vatrates(id) ON DELETE CASCADE"
  print ");\n";

  sqlstart = "INSERT INTO vr_raw_" + c + "(code,rate,comment) VALUES("

  for i in range(1,len(lines)):
    try:
      row = lines[i]

      if(len(row) > 0):
        code = row[1]
        rate = row[2]
        comment = row[3];
        sid = getRate(code,rate)
    
        sys.stdout.write(sqlstart)
        sys.stdout.write("\"" + code + "\",")
        sys.stdout.write(str(sid) + ",")
        sys.stdout.write("\"" + comment + "\"")
        sys.stdout.write(");\n")
    except Exception as e:
      print "ERROR\n\n";      
      print e
      print c
      print row
      raise
      sys.exit(1)


  print

  print "DROP VIEW IF EXISTS vr_" + c + ";"

  print "CREATE VIEW"
  print "  vr_" + c;
  print "AS SELECT"
  print "  vr_vatrates.country,"
  print "  vr_raw_" + c + ".code,"
  print "  vr_vatrates.rate_name,"
  print "  vr_vatrates.rate_value as rate_percent,"
  print "  round(1 + vr_vatrates.rate_value / 100,2) as rate_multiplier,"
  print "  round(1 / (1 + (vr_vatrates.rate_value/100)),6) AS rate_inversed_multiplier,"
  print "  vr_raw_" + c + ".comment"
  print "FROM"
  print "  vr_raw_" + c + ", vr_vatrates"
  print "WHERE"
  print "  vr_raw_" + c + ".rate = vr_vatrates.id"
  print "ORDER BY"
  print "  vr_vatrates.eusort;";

print 

viewsfiles = [ f for f in listdir(viewsdir) if isfile(join(viewsdir,f)) ]
views = []

for f in viewsfiles:
  n = os.path.basename(f)
  fn = os.path.splitext(n)[0]
  ext = os.path.splitext(n)[1]

  if ext == ".sql":
    views.append(fn)


for v in views:
  view = os.path.join(viewsdir,v + ".sql")
  with open(view, 'r') as f:
    print f.read()
  print

print 
print "SET FOREIGN_KEY_CHECKS=1;"

sys.stdout = open(bashfile, 'w')

vatclasses.append("vattable")

print "#!/bin/bash"

for c in vatclasses:
  print
  print "echo 'select * from vr_" + c + "' | mysql -u $DBUSER --password=$DBPASS $DBNAME | sed -e 's/\\t/,/g' > " + c + ".csv"
  print
  print "echo '<html><head><title>" + c + "</title></head><body>' > " + c + ".html"
  print "echo '<h1>" + c + "</h1>' >> " + c + ".html"
  print "echo 'select * from vr_" + c + "' | mysql --html -u $DBUSER --password=$DBPASS $DBNAME >> " + c + ".html"
  print "echo '</body></html>' >> " + c + ".html"

