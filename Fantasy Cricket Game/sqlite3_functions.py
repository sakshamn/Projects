"""SQLite Basic Functions.

SQLite databases are serverless and self-contained, since they read and write data to a file.
So, you don't even need to install and run an SQLite server to perform database operations!
You can see that creating tables in SQLite is very similar to using raw SQL.
All you have to do is store the query in a string variable and then pass that variable to
cursor.execute()

In this module there shall be custom functions to perform SQLite Queries.
They can be imported to any module to serve as standard function templates to call.
"""

## Imports
import sqlite3

## Global Variables
PATH = r"/home/ubuntu/Desktop/SQLDB"

## Functions
def create_connection(path) :
    """Define a function that accepts the path to the SQLite database.

    If the database exists at the specified location, then a connection to the database is
    established.
    Otherwise, a new database is created at the specified location, and a connection is
    established.
    This connection object can be used to execute queries on an SQLite database.
    """
    try :
        _connection = sqlite3.connect(path)
        print("Connection to SQLITE3 DB successful.")
        return _connection
    except sqlite3.Error as _err :
        print(f"Received an Error {_err}")


def execute_query(connection, query) :
    """To execute queries in SQLite, use cursor.execute()."""

    _cursor = connection.cursor()
    try :
        _cursor.execute(query)
        connection.commit()
        print(f"\nQuery\n{query}\nexecuted successfully.\n")
    except sqlite3.Error as _err :
        print(f"The error '{_err}' occurred.")


def execute_read_query(connection, query):
    """To execute queries in SQLite, use cursor.execute()."""

    _cursor = connection.cursor()
    try:
        _cursor.execute(query)
        _result = _cursor.fetchall()
        print(f"\nRead Query\n{query}\nexecuted successfully.\n")
        return _result
    except sqlite3.Error as _err:
        print(f"The error '{_err}' occurred")


def create_table(connection, name, attributes) :
    """CREATE TABLES AKA ENTRIES."""

    _table = """CREATE TABLE IF NOT EXISTS %s (\n""" %(name)
    for _key in attributes :
        _table += f"\t{attributes[_key]}\n"
    _table += ");"

    ## Call execute_query() to create the table.
    execute_query(connection, _table)


def create_record(connection, table_name, fields, values) :
    """CREATE RECORDS AKA ROWS IN THE TABLE.
    """
    ## REPLACE shall work only when UNIQUE is specified in the column when creating the TABLE.
    ## It shall replace if same name record already exists otherwise it shall add as a new record.
    _record = """REPLACE INTO\n\t%s %s\nVALUES\n\t%s\n;""" % (table_name, fields, values)

    ## Call execute_query() to insert records into your tables.
    execute_query(connection, _record)


def select_record(connection, query) :
    """SELECTING RECORDS FROM DATABASE TABLES USING "SELECT" QUERIES.

    This function accepts the connection object and the SELECT query and returns the selected
    record.
    To select records using SQLite, you can again use cursor.execute().
    However, after you've done this, you'll need to call .fetchall().
    This method returns a list of tuples where each tuple is mapped to the corresponding row
    in the retrieved records.

    The SELECT query selects all the users from the users table.
    This is passed to the execute_read_query(), which returns all the records from the users
    table.
    The records are then traversed and printed to the console.

    Note: It's not recommended to use SELECT * on large tables since it can result in a large
    number of I/O operations
    that increase the network traffic.
    """
    _records = execute_read_query(connection, query)

    for _record in _records:
        print(_record)

    return _records


def main() :
    """Main starting point."""

    _connection = create_connection(PATH)

    ## You'll create four tables:
    ##     users
    ##     posts
    ##     comments
    ##     likes

    _attributes = {    
        1 : "id INTEGER PRIMARY KEY AUTOINCREMENT,",
        2 : "name TEXT NOT NULL,",
        3 : "age INTEGER,",
        4 : "gender TEXT,",
        5 : "nationality TEXT"
    }
    create_table(_connection, "users", _attributes)

    ## Since, there's a one-to-many relationship between users and posts, you can see a
    ## foreign key user_id in the posts table that references the id column in the users table.
    _attributes = {    
        1 : "id INTEGER PRIMARY KEY AUTOINCREMENT,",
        2 : "title TEXT NOT NULL,",
        3 : "description TEXT NOT NULL,",
        4 : "user_id INTEGER NOT NULL,",
        5 : "FOREIGN KEY (user_id) REFERENCES users (id)"
    }
    create_table(_connection, "posts", _attributes)

    _attributes = {    
        1 : "id INTEGER PRIMARY KEY AUTOINCREMENT,",
        2 : "user_id INTEGER NOT NULL,",
        3 : "post_id INTEGER NOT NULL,",
        4 : "FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)"
    }
    create_table(_connection, "likes", _attributes)

    _attributes = {    
        1 : "id INTEGER PRIMARY KEY AUTOINCREMENT,",
        2 : "text TEXT NOT NULL,",
        3 : "user_id INTEGER NOT NULL,",
        4 : "post_id INTEGER NOT NULL,",
        5 : "FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)"
    }
    create_table(_connection, "comments", _attributes)

    _fields = "(name, age, gender, nationality)"
    _values = """
    ('James', 25, 'male', 'USA'),
    ('Leila', 32, 'female', 'France'),
    ('Brigitte', 35, 'female', 'England'),
    ('Mike', 40, 'male', 'Denmark'),
    ('Elizabeth', 21, 'female', 'Canada')
    """
    create_record(_connection, "users", _fields, _values)


    ## It's important to mention that the user_id column of the posts table is a foreign key
    ## that references the id column of the users table. This means that the user_id column
    ## must contain a value that already exists in the id column of the users table.
    ## If it doesn't exist, then you'll see an error.
    _fields = "(title, description, user_id)"
    _values = """
    ("Happy", "I am feeling very happy today", 1),
    ("Hot Weather", "The weather is very hot today", 2),
    ("Help", "I need some help with my work", 2),
    ("Great News", "I am getting married", 1),
    ("Interesting Game", "It was a fantastic game of tennis", 5),
    ("Party", "Anyone up for a late-night party today?", 3)
    """
    create_record(_connection, "posts", _fields, _values)


    _fields = "(user_id, post_id)"
    _values = """
    (1, 6),
    (2, 3),
    (1, 5),
    (5, 4),
    (2, 4),
    (4, 2),
    (3, 6)
    """
    create_record(_connection, "likes", _fields, _values)


    _fields = "(text, user_id, post_id)"
    _values = """
    ('Count me in', 1, 6),
    ('What sort of help?', 5, 3),
    ('Congrats buddy', 2, 4),
    ('I was rooting for Nadal though', 4, 5),
    ('Help with your thesis?', 2, 3),
    ('Many congratulations', 5, 4)
    """
    create_record(_connection, "comments", _fields, _values)

    ## Select all the records from the users table.
    _select_users = "SELECT * from users"
    select_record(_connection, _select_users)

    ## Select all the records from the posts table.
    _select_posts = "SELECT * from posts"
    select_record(_connection, _select_posts)

    ## Select all the records from the likes table.
    _select_likes = "SELECT * from likes"
    select_record(_connection, _select_likes)

    ## Select all the records from the comments table.
    _select_comments = "SELECT * from comments"
    select_record(_connection, _select_comments)


    ## Execute complex queries involving JOIN operations to retrieve data from two related
    ## tables.
    ## The following script returns the user ids and names, along with the description of the
    ## posts that these users posted.

    ## The INNER JOIN keyword selects records that have matching values in both tables.
    ## SELECT column_name(s)
    ## FROM table1
    ## INNER JOIN table2
    ## ON table1.column_name = table2.column_name;
    _select_users_posts = """
        SELECT
            users.id,
            users.name,
            posts.description
        FROM
            posts
        INNER JOIN
            users
        ON
            users.id = posts.user_id
    """
        
    _users_posts = execute_read_query(_connection, _select_users_posts)
    
    for _users_post in _users_posts:
        print(_users_post)


    ## You can also select data from three related tables by implementing multiple JOIN
    ## operators.
    ## The following script returns all posts, along with the comments on the posts and the
    ## names of the users who posted the comments.
    select_posts_comments_users = """
        SELECT
            posts.description as post,
            text as comment,
            name
        FROM
            posts
        INNER JOIN
            comments
        ON
            posts.id = comments.post_id
        INNER JOIN
            users
        ON
            users.id = comments.user_id
    """
    
    posts_comments_users = execute_read_query(
        _connection, select_posts_comments_users
    )
    
    for posts_comments_user in posts_comments_users:
        print(posts_comments_user)
    


if __name__ == "__main__" :
    main()
    input("\nPress the Enter key to exit..\n")

