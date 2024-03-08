# Askaett's MTGO Collection Manager
#### Video Demo:  <URL HERE>
#### Description: Web application that's viewable on mobile to manage a collection of digital objects that's paginated and searchable. 
# INSTALLATION
  Pull project package from repo and download to local desktop. 
  Open instance of code editor (vscode) and create new folder. 
  Import project package to new folder. 
  
  preparing your environment:
    create virtual environment (python 3.11 or greater)
    Open new terminal and enter code app.py in terminal
    Install flask: python -pip install flask 
    Install the requirements folder: pip install -r requirements
    install cs50: pip3 install cs50
    install flask_sessions: pip install flask_session
    install helpers: pip install helpers
    install requests: pip install requests

  Modify sql database path:
    In the project folder saved to desktop, copy the path for the mtgocoll.db file. 
    In app.py line 20 - overwrite the existing path with the copied path from the mtgocoll.db file location
    duplicate the \ characters in your path to avoid triggering an unicode escape error:
      ex. "sqlite:///C:\\Users\\aaron\\OneDrive\\Desktop\\project\\mtgocoll.db"

## Add your own collection to the sqlite database
    
    If you would like to import your own collection: 
    Access your acount on Magic the Gethering Online 
    In the Collection tab,  click on your trade binder and click "Full Trade List". 
    Click the display icon for the Full Trade List and select "List View". 
    Hover over the full trade option and right click and select export
    Export list as a csv and save to desktop.
    In the csv, there will be some duplication due to multiple printings of the same card in a set with different arts.   Remove duplicate can be used to prevent failures when importing the CSV to the sql database. 
    Delete the mtgocoll.db file from your project folder. 
    In the terminal enter the command sqlite3 mtgocoll to create a new database folder. 
    in the sqlite3 use the following sqlite commands to create your tables:

      CREATE TABLE collection (card_name TEXT NOT NULL,
      quantity INTEGER NOT NULL, id INTEGER NOT NULL, 
      rarity TEXT NOT NULL, set_sym TEXT NOT NULL, 
      premium TEXT NOT NULL, 
      PRIMARY KEY (card_name, set_sym, premium)); 
  
      CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
      username TEXT NOT NULL, hash TEXT NOT NULL);

      Use command .mode csv to prepare for import. 
      Use command .import "your csv path" collection

### How to launch Askaett's MTGO Collection Manager 
  In your open project, in the terminal run code: python -m flask run
  this should open a flask instance in your local development environment on port 5000 
    *if there is another application utilining port 5000, close that application prior to 
    running Askaett's MTGO Collection Manager

  Control click on the hyperlinked port address to launch a browser instance of Askaett's MTGO Collection Manager
  If this is your first time accessing the program, you will need to register a username and password. 
  After registration, log in with username and password. 

#### Features of Askaett's MTGO Collection Manager
  Once logged into the collection manager, your collection should load dynamically from the sqlite database. 
  The collection is organized by set symbol (set_sym)
  The website is paginated and will dynamically add pages as your page forward
  The search function will search by text (case sensitive) any cards available on the current page. 
  
##### Future Features
  During development, I attempted to incorporate an API call to MTGJSON to export a price list that could be joined to the existing sqlite database file through a temp join and modify the index HTML to add a price column, however, I could not successfully code the api call and tokenization due to my limited development skills. 

###### Credits
    This project was based off of the CS50 Finance Shell, utilizing the sessions package, the sqlite3 package and the helpers package, which was incorporated Bootstrap, 
