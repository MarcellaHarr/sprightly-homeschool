# Import Packages & Extensions
from .models import subjectLessons, subjectPictures, science, sciencePics
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from collections import defaultdict
from flask import make_response
from datetime import datetime
from . import db, cache
import base64

# Declare Blueprint object
scienceLesson_views = Blueprint('scienceLesson_views', __name__)

# Global
"""Custom Jinja2 filter to convert binary image data to base64"""
def to_base64(binary_data):
    return base64.b64encode(binary_data).decode('utf-8')


# Declare routes
"""Add the custom filter to Jinja2 environment"""
@scienceLesson_views.app_template_filter('b64encode')
def base64_encode_filter(binary_data):
    return to_base64(binary_data)


@scienceLesson_views.route('/sciViewLesson/<int:lesson_number>', methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=900, key_prefix='sciViewLesson')
def sciViewLesson(lesson_number):
    """Retrieve data from tables"""
    if request.method == 'POST':
        """Get the submitted form data"""
        form_data = request.form

        """Create a list to store science entries"""
        science_entries = []

        """Process the form data and populate science entries"""
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
                filtered_sci_rows = [row for row in adminSubRow if row['subQuestion'] == question and row['subSubjectCode'] == 'SCI']

                """Science table"""
                for lesson_data in filtered_sci_rows:
                    sub_topc = lesson_data['subTopic']
                    sub_lesson = lesson_data['subLessonNumber']
                    sub_desc = lesson_data['subDescription']

                sci_entry = science(
                    sciUserID = current_user.accountTableID,
                    sciDueDate = datetime.today().date(),
                    sciPageCurriculum = 'The Good & the Beautiful',
                    sciLevel = 'Marine Biology 3.0',
                    sciTopic = sub_topc,
                    sciDescription = sub_desc,
                    sciLesson = sub_lesson,
                    sciQuestion = question,
                    sciResponse = sub_answer
                )
                science_entries.append(sci_entry)

        """Add all science entries to the session"""
        db.session.add_all(science_entries)

        """Commit the session to save changes to the science table"""
        db.session.commit()


    """Science Pictures"""
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

    """Create a list to store the filtered data with only one entry per unique lesson number and 'SCI' subject code"""
    filtered_sci_questions = []

    for lesson_row in adminLessonRow:
        lesson_num = lesson_row['subLessonNumber']
        subject_code = lesson_row['subSubjectCode'].casefold()
        if lesson_num in unique_subpx_lessons and subject_code == 'sci' and lesson_num == lesson_number:
            filtered_sci_questions.append(lesson_row['subQuestion'])

    """Query admin subject pictures' table directly for the required data"""
    adminPicsTable = db.session.query(subjectPictures.subpxDateTime,
                                      subjectPictures.subpxLessonNumber,
                                      subjectPictures.subpxLessonPic).filter(subjectPictures.subpxSubjectCode == 'SCI',
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
    response = make_response(render_template('sciViewLesson.html',
                           currentUser = current_user,
                           currDate = currDate,
                           adminUploadDate = ', '.join(adminUploadDate),
                           tableLessonNumber = tableLessonNumber,
                           tableSubjectCode = tableSubjectCode,
                           sciQuestions = filtered_sci_questions,
                           imagesByLesson = images_by_lesson,
                           lesson_number = lesson_number))
    
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@scienceLesson_views.route('/sciViewUploads/<int:lesson_number>', methods=['GET', 'POST'])
@login_required
def sciViewUploads(lesson_number):
    """Upload"""

    if request.method == 'POST':
        """Assign browser files to vars"""
        fileA = request.files.get('fileA')
        fileB = request.files.get('fileB')
        fileC = request.files.get('fileC')

        """Set user ID to histPics DB table relation"""
        scipxUserID = current_user.accountTableID

        """Assign to current time"""
        scipxDateTime = datetime.now()

        """Assign subject code"""
        scipxSubjectCode = 'SCI'

        """Set table"""
        upload = sciencePics(
            scipxUserID = scipxUserID,
            scipxDateTime = scipxDateTime,
            scipxSubjectCode = scipxSubjectCode,
            scipxUploadPicA = fileA.read(),
            scipxUploadPicB = fileB.read(),
            scipxUploadPicC = fileC.read()
        )
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded files: fileA={fileA.filename}, fileB={fileB.filename}, fileC={fileC.filename}'

    return render_template('sciViewLesson.html', currentUser = current_user, lesson_number = lesson_number)