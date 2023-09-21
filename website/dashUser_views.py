# Import Packages & Extensions
from flask import Blueprint, render_template, current_app
from flask_login import current_user, login_required
from .models import subjectLessons
from datetime import datetime
from . import db
import pytz

# Declare Blueprint object
dashUser_views = Blueprint('dashUser_views', __name__)


# Declare routes
@dashUser_views.route('/profile')
@login_required
def profile():
    """Optimized database queries"""
    """Fetch all required columns from subjectLessons table"""
    adminData = db.session.query(
        subjectLessons.subDueDate,
        subjectLessons.subSubjectCode,
        subjectLessons.subTopic,
        subjectLessons.subDescription,
        subjectLessons.subLessonNumber
    ).all()

    """Assign today's date"""
    newYorkTZ = pytz.timezone(current_app.config['TIMEZONE'])
    curr_datetime = datetime.now(newYorkTZ)
    currDate = curr_datetime.today().date()
    currentDate = datetime.now()

    """Convert dates to an American format"""
    dteFormat = "%A, %B %d, %Y"
    currentDate = currentDate.strftime(dteFormat)

    """Extract specific columns from the adminData query result"""
    adminDates = [row[0].strftime("%m-%d-%Y") for row in adminData]
    adminTopics = [row[2] for row in adminData]
    adminDescriptions = [row[3] for row in adminData]

    """Remove unwanted special characters"""
    adminTopics = [topic.replace("'", "").replace("(", "").replace(")", "") for topic in adminTopics]
    adminDescriptions = [desc.replace("'", "").replace("(", "").replace(")", "") for desc in adminDescriptions]

    """Create dictionaries to store the data for each row"""
    adminLessonData = [{'subDueDate': row[0].strftime("%Y-%m-%d"),
                        'subSubjectCode': row[1],
                        'subTopic': row[2],
                        'subDescription': row[3],
                        'subLessonNumber': row[4]} for row in adminData]

    """Filter admin lesson data by current date and subject code"""
    ela_data = [item for item in adminLessonData if item['subDueDate'] == currDate.strftime("%Y-%m-%d") and item['subSubjectCode'].lower() == 'ela']
    hist_data = [item for item in adminLessonData if item['subDueDate'] == currDate.strftime("%Y-%m-%d") and item['subSubjectCode'].lower() == 'his']
    mth_data = [item for item in adminLessonData if item['subDueDate'] == currDate.strftime("%Y-%m-%d") and item['subSubjectCode'].lower() == 'mth']
    sci_data = [item for item in adminLessonData if item['subDueDate'] == currDate.strftime("%Y-%m-%d") and item['subSubjectCode'].lower() == 'sci']
    soc_data = [item for item in adminLessonData if item['subDueDate'] == currDate.strftime("%Y-%m-%d") and item['subSubjectCode'].lower() == 'soc']

    return render_template('profile.html', user = current_user,
                           currentDate = currentDate,
                           adminDates = ', '.join(adminDates),
                           adminTopics = ', '.join(adminTopics),
                           adminDescriptions = ', '.join(adminDescriptions),
                           elaLessonData = ela_data,
                           histLessonData = hist_data,
                           mthLessonData = mth_data,
                           sciLessonData = sci_data,
                           socLessonData = soc_data)