# COSC61 Term Project: NBA Player Database #
Analyzing NBA player statistics and salaries, a student project by Cha Krupka for COSC61 at Dartmouth College.
## Installation Instructions ##
_Warning: these steps are for **Mac** users specifically. They **may need to be modified** based on the system you use._  
_Another note: if MySQL Workbench is installed, you can simply import the database using the provided dump file (importnbaplayers.sql) and MySQL Workbench import wizard into a localhost connection. Skip to #19 in this case._
1. Download files (Green button [<> Code] --> Download ZIP)
2. Open terminal
3. Install homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
4. Do whatever it tells you to do, then check succesful install with `brew help`
5. `brew install mysql`
6. `brew services start mysql`
7. `mysql -u root` or `mysql -u root -p` depending on whether you set a password for mysql
8. `CREATE DATABASE nbaplayers;`
9. `exit`
10. Paste into terminal but don't hit enter (omit -p if you didn't set a password): `mysql -u root -p nbaplayers < ` (make sure the space is at the end)
11. Drag "importnbaplayers.sql" from downloaded files into terminal window, then hit enter
12. Check import:
13. `mysql -u root -p` or `mysql -u root`
14. `SHOW DATABASES;`
15. `USE nbaplayers`
16. `SHOW TABLES;`
17. `SELECT * FROM players;` (should return 2408 rows)
18. `exit`
19. Install necessary modules:
20. `brew install python`
21. `pip3 install flask`
22. `pip3 install mysql-connector-python`
23. Close terminal, open the folder of downloaded files
24. Open "flask_app" and then open "app.py" with a texteditor of your choice (TextEdit is fine)
25. Under "DATABASE_CONFIG":
26. Set the username to "root" and the password to whatever you set
27. **Important: If you didnt set a password, remove the password line entirely**
28. Save the file
29. Open up terminal again, paste but don't hit enter: `cd ` (include space)
30. Drag the "flask_app" folder from the downloaded files into the terminal window, then hit enter
31. Then enter `export FLASK_APP=app`, then `flask run`
32. Navigate to http://127.0.0.1:5000/
