# Import app object from __init__ inside website dir
from website import createAPP

# Declare app object
app = createAPP()

# Execute the application
if __name__ == '__main__':
    with app.app_context():
        from website import create_database
        create_database(app)
    app.run(debug=True)