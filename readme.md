This is a collection of tables listing the VAT rates for different classes of goods. The tables 
are intended as a help for when trying to figure out how to comply with the 2015 EU VAT directives.

For a more readable format, refer to http://www.vatwiki.eu, where all tables are available in
rendered format.

# Usage

The base data is available in CSV files under "csv". The "vatrates.csv" is the master table. The other files
are VAT rates specified per type of goods.

The script "build.py" will generate a SQL script based on the csv data. This is usable in a MySQL environment.

The script will also generate another script for rendering compiled tables based on the data put in a database.

So, steps for using the material avaiable here would normally be:

* Check if the csv data under "csv" looks sane
* Run build.py
* Insert the generated SQL data in a mysql database, for example:

    mysql -u MYUSER --password=MYPASS MYDATABASE < buildDb.sql

* Run the generated script for building all tables, for example:

    DBNAME=MYDATABASE DBPASS=MYPASSWORD DBUSER=MYUSERl . buildOutput.bash

Having run these (replace MYUSER, MYDATABASE and MYPASSWORD with applicable values), the generated tables 
will be available in the "output" directory.

# License and terms for usage

The contents of this repo is provided on an as-is basis. The information is compiled from public sources and 
user contributions. There is no guarantee whatsoever that the information is correct, up to date or applicable 
for any purpose. You are free to use the information provided here for any purpose whatsoever, but in doing so 
you recognize that you are doing this at your own risk, and that the repo owner and contributors cannot be held 
liable for any consequences. No matter what is written here, it is still your responsibility to check the 
authoritative VAT references and check with your local tax authority that what you do is legal and correct.

If so desired, you can consider anything provided in this repo as licensed under CC0.

