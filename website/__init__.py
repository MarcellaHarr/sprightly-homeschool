# Packages & Extensions
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_caching import Cache
from flask import Flask


# Declare database object
db = SQLAlchemy()
cache = Cache()

# Name DB
DB_NAME = 'SprightlyHomeschool.db'

# Create the app function
def createAPP():
    app = Flask(__name__, instance_relative_config=True)

    """Configure timezone to America New York"""
    app.config["TIMEZONE"] ='America/New_York'

    """Configure security settings"""
    app.config["SECRET_KEY"] = '20232024SchoolYRv2023JU23rd'

    """Register DB location"""
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    """Configure Cache value"""
    app.config["CACHE_TYPE"] = 'memcached'

    """Initialize Cache"""
    cache.init_app(app)

    """Initialize DB"""
    db.init_app(app)

    """Initialize Flask-Migrate"""
    migrate = Migrate(app, db)

    """Declare blueprints"""
    from .authUser_views import authUser_views
    from .adminUpload_views import adminUpload_views
    from .dashUser_views import dashUser_views
    from .elaLesson_views import elaLesson_views
    from .historyLesson_views import historyLesson_views
    from .mathLesson_views import mathLesson_views
    from .scienceLesson_views import scienceLesson_views
    from .socialLesson_views import socialLesson_views
    from .webTemps_views import webTemps_views

    """Register blueprints"""
    app.register_blueprint(authUser_views, url_prefix='/')
    app.register_blueprint(adminUpload_views, url_prefix='/')
    app.register_blueprint(dashUser_views, url_prefix='/')
    app.register_blueprint(elaLesson_views, url_prefix='/')
    app.register_blueprint(historyLesson_views, url_prefix='/')
    app.register_blueprint(mathLesson_views, url_prefix='/')
    app.register_blueprint(scienceLesson_views, url_prefix='/')
    app.register_blueprint(socialLesson_views, url_prefix='/')
    app.register_blueprint(webTemps_views, url_prefix='/')

    """Verify if Tables has been created"""
    from .models import userAccount

    """Create the DB"""
    def create_database(app):
        with app.app_context():
            db.create_all()

    """Initialize & redirect user"""
    login_manager = LoginManager()
    login_manager.login_view = 'authUser_views.login'
    login_manager.init_app(app)

    """Instruct how to load the user"""
    @login_manager.user_loader
    def load_user(userAccount_accountTableID):
        return userAccount.query.get(int(userAccount_accountTableID))

    """Link user log and DB's Table"""
    @login_manager.user_loader
    def get_user(userAccount_accountTableID):
        return userAccount.query.get(int(userAccount_accountTableID))

    """Execute DB creation"""
    create_database(app)

    return app