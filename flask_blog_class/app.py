import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#function to retruive post from database
def get_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    
    return post

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get connection to data base
    conn = get_db_connection()

    #execute a query to read al posts from the posts table
    posts + conn.execute('SELECT * FROM posts').fetchall()

    #close connection 
    conn.close()

    #send the posts to the index
    return render_template('index.html', posts=posts)

    
# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #determine if page is being requested with POST or GET
    if request.method == 'POST':
        #get title and content that was subbed
        title = request.form['title']
        content = request.form['content']

        #display error if title or content is not subbed
        #else make database conn and insert the blog post content
        if not title:
            flash("Title is required")
        elif not content:
            flash("Content is required")
        else:
            conn = get_db_connection()
            #insert data
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        

    return render_template('create.html')

#create a route to edit a post. load page with get or post 
#pass the post id as url paramerter 
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    #get post from database 
    post = get_post(id)
    
    #determine if the page was requested with get or post
    if request.method == 'POST':
        #get title and content
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()

            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))


        #if POST process form data. get the data and validate it, update the post and get to home
    
    #if GET display page
    return render_template('edit.html', post=post)

app.run()
