# Import Packages & Extensions
from .models import subjectLessons, subjectPictures, math, mathPics
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from collections import defaultdict
from flask import make_response
from datetime import datetime
from . import db, cache
import base64

# Declare Blueprint object
mathLesson_views = Blueprint('mathLesson_views', __name__)


# Global
"""Custom Jinja2 filter to convert binary image data to base64"""
def to_base64(binary_data):
    return base64.b64encode(binary_data).decode('utf-8')


# Declare routes
"""Add the custom filter to Jinja2 environment"""
@mathLesson_views.app_template_filter('b64encode')
def base64_encode_filter(binary_data):
    return to_base64(binary_data)


@mathLesson_views.route('/mthViewLesson/<int:lesson_number>', methods=['GET', 'POST'])
@cache.cached(timeout=900, key_prefix='mthViewLesson')
@login_required
def mthViewLesson(lesson_number):
    """Retrieve data from tables"""
    if request.method == 'POST':
        """Get the submitted form data"""
        form_data = request.form

        """Create a list to store math entries"""
        math_entries = []

        """Process the form data and populate math entries"""
        for key, value in form_data.items():
            if key.startswith('response_'):
                lesson_number = int(key.split('_')[1])
                sub_answer = value.casefold()

                """Get the corresponding question for the current response"""
                question_key = f'question_{lesson_number}'
                question = form_data.get(question_key, '')

                """Fetch the current lesson from subjectLessons"""
                adminSubjectTable = db.session.query(subjectLessons.subSubjectCode,
                                                     subjectLessons.subTopic,
                                                     subjectLessons.subLessonNumber,
                                                     subjectLessons.subDescription,
                                                     subjectLessons.subQuestion).all()

                """Create a dictionary to store lesson data for each row"""
                adminSubRow = [{'subSubjectCode': row[0],
                                'subTopic': row[1],
                                'subLessonNumber': row[2],
                                'subDescription': row[3],
                                'subQuestion': row[4]} for row in adminSubjectTable]

                """Create a list to store the filtered data with only one entry per unique lesson number"""
                filtered_mth_rows = [row for row in adminSubRow if row['subQuestion'] == question and row['subSubjectCode'] == 'MTH']

                """Math table"""
                for lesson_data in filtered_mth_rows:
                    sub_topc = lesson_data['subTopic']
                    sub_lesson = lesson_data['subLessonNumber']
                    sub_desc = lesson_data['subDescription']

                mth_entry = math(
                    mthUserID = current_user.accountTableID,
                    mthDueDate = datetime.today().date(),
                    mthPageCurriculum = 'The Good & the Beautiful',
                    mthLevel = 'Level 6',
                    mthTopic = sub_topc,
                    mthDescription = sub_desc,
                    mthLesson = sub_lesson,
                    mthQuestion = question,
                    mthResponse = sub_answer
                )
                math_entries.append(mth_entry)

        """Add all math entries to the session"""
        db.session.add_all(math_entries)

        """Commit the session to save changes to the math table"""
        db.session.commit()


    """Math Pictures"""
    """Set current date"""
    currDate = datetime.today().date()

    """Query admin lesson number and question from table"""
    adminLessonData = db.session.query(subjectLessons.subDueDate,
                                       subjectLessons.subSubjectCode,
                                       subjectLessons.subLessonNumber,
                                       subjectLessons.subQuestion).all()

    """Convert date column to an American format"""
    adminUploadDate = [date_obj[0].strftime("%m-%d-%Y") for date_obj in adminLessonData]

    """Extract the list of unique lesson numbers and subject codes for the current date"""
    tableSubjectCode = [item[1] for item in adminLessonData]
    tableLessonNumber = [item[2] for item in adminLessonData]

    """Create dictionary list to store data for each row"""
    adminLessonRow = [{'subDueDate': row[0].strftime("%Y-%m-%d"), 'subSubjectCode': row[1], 'subLessonNumber': row[2], 'subQuestion': row[3]} for row in adminLessonData]

    """Use a set to store the unique lesson numbers"""
    unique_subpx_lessons = set(tableLessonNumber)

    """Create a list to store the filtered data with only one entry per unique lesson number and 'MTH' subject code"""
    filtered_mth_questions = []

    for lesson_row in adminLessonRow:
        lesson_num = lesson_row['subLessonNumber']
        subject_code = lesson_row['subSubjectCode'].casefold()
        if lesson_num in unique_subpx_lessons and subject_code == 'mth' and lesson_num == lesson_number:
            filtered_mth_questions.append(lesson_row['subQuestion'])


    """Query admin subject pictures' table directly for the required data"""
    adminPicsTable = db.session.query(subjectPictures.subpxDateTime,
                                      subjectPictures.subpxLessonNumber,
                                      subjectPictures.subpxLessonPic).filter(subjectPictures.subpxSubjectCode == 'MTH',
                                                                             subjectPictures.subpxLessonNumber == lesson_number).all()

    """Create a dictionary to store images by lesson number"""
    images_by_lesson = defaultdict(list)

    for item in adminPicsTable:
        """Get the binary image data"""
        binary_image_data = item[2]

        """Determine the image format (e.g., JPEG, PNG, GIF) based on the binary data"""
        image_format = "jpeg"

        """Convert the binary image data to base64 and include the correct MIME type"""
        base64_image_data = base64.b64encode(binary_image_data).decode()
        data_url = f"data:image/{image_format};base64,{base64_image_data}"

        """Store image data with the data URL in the dictionary"""
        image_data = {
            'subpxDateTime': item[0].strftime("%m-%d-%Y"),
            'subpxLessonPic': data_url
        }
        images_by_lesson[item[1]].append(image_data)

    """Create a response with appropriate headers to disable caching"""
    response = make_response(render_template('mthViewLesson.html',
                           currentUser = current_user,
                           currDate = currDate,
                           adminUploadDate = ', '.join(adminUploadDate),
                           tableLessonNumber = tableLessonNumber,
                           tableSubjectCode = tableSubjectCode,
                           mthQuestions = filtered_mth_questions,
                           imagesByLesson = images_by_lesson,
                           lesson_number = lesson_number))
    
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@mathLesson_views.route('/mthViewUploads/<int:lesson_number>', methods=['GET', 'POST'])
@login_required
def mthViewUploads(lesson_number):
    """Upload"""

    if request.method == 'POST':
        """Assign browser files to vars"""
        fileA = request.files.get('fileA')
        fileB = request.files.get('fileB')
        fileC = request.files.get('fileC')

        """Set user ID to histPics DB table relation"""
        mthpxUserID = current_user.accountTableID

        """Assign to current time"""
        mthpxDateTime = datetime.now()

        """Assign subject code"""
        mthpxSubjectCode = 'MTH'

        """Set table"""
        upload = mathPics(
            mthpxUserID = mthpxUserID,
            mthpxDateTime = mthpxDateTime,
            mthpxSubjectCode = mthpxSubjectCode,
            mthpxUploadPicA = fileA.read(),
            mthpxUploadPicB = fileB.read(),
            mthpxUploadPicC = fileC.read()
        )
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded files: fileA={fileA.filename}, fileB={fileB.filename}, fileC={fileC.filename}'

    return render_template('mthViewLesson.html', currentUser = current_user, lesson_number = lesson_number)