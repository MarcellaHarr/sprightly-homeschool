# Import Packages & Extensions
from .models import userAccount, userPictures, subjectLessons, languageArtsPics, historyPics, mathPics, sciencePics, socialStudiesPics, studentReport
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from datetime import datetime
from . import db
import base64
import re

# Declare Blueprint object
webTemps_views = Blueprint('webTemps_views', __name__)

# Global
"""Custom Jinja2 filter to convert binary image data to base64"""
def to_base64(binary_data):
    return base64.b64encode(binary_data).decode('utf-8')

@webTemps_views.app_template_global('default_picture')
def default_picture():
    with open('static/img/studentPortraitPic.jpg', 'rb') as image_file:
        default_image_data = image_file.read()
    return base64_encode_filter(default_image_data)


# Declare routes
"""Add the custom filter to Jinja2 environment"""
@webTemps_views.app_template_filter('b64encode')
def base64_encode_filter(binary_data):
    return to_base64(binary_data)

@webTemps_views.route('/elaLessons')
@login_required
def elaLessonsPage():
    """Language Arts"""

    """Query DB Table Columns"""
    lessonDueDate = db.session.query(subjectLessons.subDueDate).all()
    lessonDescptn = db.session.query(subjectLessons.subDescription).all()
    lessnNumber = db.session.query(subjectLessons.subLessonNumber).all()


    """Convert date column to an American format"""
    adminDueDate = [date_obj.strftime("%m-%d-%Y") for date_obj, in lessonDueDate]

    """Iterate through table columns"""
    adminLessonNumber = lessnNumber[0][0] if lessnNumber else None


    """Remove unwanted special characters"""
    adminLessonDescription = [description[0].replace("'", "").replace("(", "").replace(")", "") for description in lessonDescptn]
    if adminLessonNumber is not None:
        adminLessonNumber = re.sub(r'[(),]', '', str(adminLessonNumber))

    """Fetch all rows with the required columns from the database table"""
    adminLessonRows = db.session.query(subjectLessons.subDueDate,
                                       subjectLessons.subSubjectCode,
                                       subjectLessons.subLessonNumber,
                                       subjectLessons.subDescription).all()

    """Create a dictionary to store lesson data for each row"""
    elaTable = [{'subDueDate': row[0].strftime("%Y-%m-%d"), 'subSubjectCode': row[1], 'subLessonNumber': row[2], 'subDescription': row[3]} for row in adminLessonRows]

    """Use a set to store the unique lesson numbers"""
    unique_lessons = set()

    """Create a list to store the filtered data with only one entry per unique lesson number"""
    filtered_ela_table = []

    for lesson in elaTable:
        lesson_number = lesson['subLessonNumber']
        subject_code = lesson['subSubjectCode']
        if lesson_number not in unique_lessons and subject_code.lower() == 'ela':
            unique_lessons.add(lesson_number)
            filtered_ela_table.append(lesson)


    return render_template('elaLessons.html', currentUser = current_user, adminDueDate = ', '.join(adminDueDate)\
                           , adminLessonDescription = ', '.join(adminLessonDescription), elaTable = filtered_ela_table)

@webTemps_views.route('/historyLessons')
@login_required
def historyPage():
    """History"""

    """Query DB Table Columns"""
    lessonDueDate = db.session.query(subjectLessons.subDueDate).all()
    lessonDescptn = db.session.query(subjectLessons.subDescription).all()
    lessnNumber = db.session.query(subjectLessons.subLessonNumber).all()


    """Convert date column to an American format"""
    adminDueDate = [date_obj.strftime("%m-%d-%Y") for date_obj, in lessonDueDate]

    """Iterate through table columns"""
    adminLessonNumber = lessnNumber[0][0] if lessnNumber else None


    """Remove unwanted special characters"""
    adminLessonDescription = [description[0].replace("'", "").replace("(", "").replace(")", "") for description in lessonDescptn]
    if adminLessonNumber is not None:
        adminLessonNumber = re.sub(r'[(),]', '', str(adminLessonNumber))

    """Fetch all rows with the required columns from the database table"""
    adminLessonRows = db.session.query(subjectLessons.subDueDate,
                                       subjectLessons.subSubjectCode,
                                       subjectLessons.subLessonNumber,
                                       subjectLessons.subDescription).all()

    """Create a dictionary to store lesson data for each row"""
    histTable = [{'subDueDate': row[0].strftime("%Y-%m-%d"), 'subSubjectCode': row[1], 'subLessonNumber': row[2], 'subDescription': row[3]} for row in adminLessonRows]

    """Use a set to store the unique lesson numbers"""
    unique_lessons = set()

    """Create a list to store the filtered data with only one entry per unique lesson number"""
    filtered_hist_table = []

    for lesson in histTable:
        lesson_number = lesson['subLessonNumber']
        subject_code = lesson['subSubjectCode']
        if lesson_number not in unique_lessons and subject_code.lower() == 'his':
            unique_lessons.add(lesson_number)
            filtered_hist_table.append(lesson)

    return render_template('historyLessons.html'\
                           , currentUser = current_user, adminDueDate = ', '.join(adminDueDate),
                           adminLessonDescription = ', '.join(adminLessonDescription), histTable = filtered_hist_table)

@webTemps_views.route('/mathLessons')
@login_required
def mathPage():
    """Math"""

    """Query DB Table Columns"""
    lessonDueDate = db.session.query(subjectLessons.subDueDate).all()
    lessonDescptn = db.session.query(subjectLessons.subDescription).all()
    lessnNumber = db.session.query(subjectLessons.subLessonNumber).all()


    """Convert date column to an American format"""
    adminDueDate = [date_obj.strftime("%m-%d-%Y") for date_obj, in lessonDueDate]

    """Iterate through table columns"""
    adminLessonNumber = lessnNumber[0][0] if lessnNumber else None


    """Remove unwanted special characters"""
    adminLessonDescription = [description[0].replace("'", "").replace("(", "").replace(")", "") for description in lessonDescptn]
    if adminLessonNumber is not None:
        adminLessonNumber = re.sub(r'[(),]', '', str(adminLessonNumber))

    """Fetch all rows with the required columns from the database table"""
    adminLessonRows = db.session.query(subjectLessons.subDueDate,
                                       subjectLessons.subSubjectCode,
                                       subjectLessons.subLessonNumber,
                                       subjectLessons.subDescription).all()

    """Create a dictionary to store lesson data for each row"""
    mthTable = [{'subDueDate': row[0].strftime("%Y-%m-%d"), 'subSubjectCode': row[1], 'subLessonNumber': row[2], 'subDescription': row[3]} for row in adminLessonRows]

    """Use a set to store the unique lesson numbers"""
    unique_lessons = set()

    """Create a list to store the filtered data with only one entry per unique lesson number"""
    filtered_mth_table = []

    for lesson in mthTable:
        lesson_number = lesson['subLessonNumber']
        subject_code = lesson['subSubjectCode']
        if lesson_number not in unique_lessons and subject_code.lower() == 'mth':
            unique_lessons.add(lesson_number)
            filtered_mth_table.append(lesson)

    return render_template('mathLessons.html', currentUser = current_user, adminDueDate = ', '.join(adminDueDate),
                           adminLessonDescription = ', '.join(adminLessonDescription), mthTable = filtered_mth_table)

@webTemps_views.route('/scienceLessons')
@login_required
def sciencePage():
    """Science"""

    """Query DB Table Columns"""
    lessonDueDate = db.session.query(subjectLessons.subDueDate).all()
    lessonDescptn = db.session.query(subjectLessons.subDescription).all()
    lessnNumber = db.session.query(subjectLessons.subLessonNumber).all()


    """Convert date column to an American format"""
    adminDueDate = [date_obj.strftime("%m-%d-%Y") for date_obj, in lessonDueDate]

    """Iterate through table columns"""
    adminLessonNumber = lessnNumber[0][0] if lessnNumber else None


    """Remove unwanted special characters"""
    adminLessonDescription = [description[0].replace("'", "").replace("(", "").replace(")", "") for description in lessonDescptn]
    if adminLessonNumber is not None:
        adminLessonNumber = re.sub(r'[(),]', '', str(adminLessonNumber))

    """Fetch all rows with the required columns from the database table"""
    adminLessonRows = db.session.query(subjectLessons.subDueDate,
                                       subjectLessons.subSubjectCode,
                                       subjectLessons.subLessonNumber,
                                       subjectLessons.subDescription).all()

    """Create a dictionary to store lesson data for each row"""
    sciTable = [{'subDueDate': row[0].strftime("%Y-%m-%d"), 'subSubjectCode': row[1], 'subLessonNumber': row[2], 'subDescription': row[3]} for row in adminLessonRows]

    """Use a set to store the unique lesson numbers"""
    unique_lessons = set()

    """Create a list to store the filtered data with only one entry per unique lesson number"""
    filtered_sci_table = []

    for lesson in sciTable:
        lesson_number = lesson['subLessonNumber']
        subject_code = lesson['subSubjectCode']
        if lesson_number not in unique_lessons and subject_code.lower() == 'sci':
            unique_lessons.add(lesson_number)
            filtered_sci_table.append(lesson)

    return render_template('scienceLessons.html', currentUser = current_user, adminDueDate = ', '.join(adminDueDate),
                           adminLessonDescription = ', '.join(adminLessonDescription), sciTable = filtered_sci_table)

@webTemps_views.route('/socialLessons')
@login_required
def socialPage():
    """Scocial Studies"""

    """Query DB Table Columns"""
    lessonDueDate = db.session.query(subjectLessons.subDueDate).all()
    lessonDescptn = db.session.query(subjectLessons.subDescription).all()
    lessnNumber = db.session.query(subjectLessons.subLessonNumber).all()


    """Convert date column to an American format"""
    adminDueDate = [date_obj.strftime("%m-%d-%Y") for date_obj, in lessonDueDate]

    """Iterate through table columns"""
    adminLessonNumber = lessnNumber[0][0] if lessnNumber else None


    """Remove unwanted special characters"""
    adminLessonDescription = [description[0].replace("'", "").replace("(", "").replace(")", "") for description in lessonDescptn]
    if adminLessonNumber is not None:
        adminLessonNumber = re.sub(r'[(),]', '', str(adminLessonNumber))

    """Fetch all rows with the required columns from the database table"""
    adminLessonRows = db.session.query(subjectLessons.subDueDate,
                                       subjectLessons.subSubjectCode,
                                       subjectLessons.subLessonNumber,
                                       subjectLessons.subDescription).all()

    """Create a dictionary to store lesson data for each row"""
    socTable = [{'subDueDate': row[0].strftime("%Y-%m-%d"), 'subSubjectCode': row[1], 'subLessonNumber': row[2], 'subDescription': row[3]} for row in adminLessonRows]

    """Use a set to store the unique lesson numbers"""
    unique_lessons = set()

    """Create a list to store the filtered data with only one entry per unique lesson number"""
    filtered_soc_table = []

    for lesson in socTable:
        lesson_number = lesson['subLessonNumber']
        subject_code = lesson['subSubjectCode']
        if lesson_number not in unique_lessons and subject_code.lower() == 'soc':
            unique_lessons.add(lesson_number)
            filtered_soc_table.append(lesson)

    return render_template('socialLessons.html', currentUser = current_user, adminDueDate = ', '.join(adminDueDate),
                           adminLessonDescription = ', '.join(adminLessonDescription), socTable = filtered_soc_table)

@webTemps_views.route('/studentPic', methods=['GET', 'POST'])
@login_required
def studentPic():
    """Student Upload Picture"""
    if 'bg_image' in request.files:

        """Set upload date"""
        uploadDate = datetime.today().date()

        """Fetch current user's accountTableID"""
        user_account = userAccount.query.get(current_user.accountTableID)
        userpxUserID = user_account.accountTableID

        """Assign to form's data"""
        uploaded_file = request.files['bg_image']
        image_data = uploaded_file.read()

        """Fetch current user's existing picture"""
        existing_picture = userPictures.query.filter_by(userpxUserID=userpxUserID).first()

        """Compare the uploaded image with the existing picture"""
        if existing_picture and existing_picture.userpxUploadPic != image_data:
            """Update the existing picture"""
            existing_picture.userpxUploadPic = image_data
            existing_picture.userpxDateTime = uploadDate
            db.session.commit()
        elif not existing_picture:
            """Insert into table if no existing picture"""
            upload = userPictures(userpxUserID=userpxUserID,
                                  userpxDateTime=uploadDate,
                                  userpxUploadPic=image_data)
            db.session.add(upload)
            db.session.commit()

        """Redirect"""
        return redirect(url_for('webTemps_views.studentPortfolio'))

    else:
        """Insert the default image for new users"""
        user_account = userAccount.query.get(current_user.accountTableID)
        userpxUserID = user_account.accountTableID

        default_image_path = "../static/img/studentPortraitPic.jpg"
        with open(default_image_path, 'rb') as default_image_file:
            default_image_data = default_image_file.read()

        existing_picture = userPictures.query.filter_by(userpxUserID=userpxUserID).first()
        if not existing_picture:
            uploadDate = datetime.today().date()

            upload = userPictures(userpxUserID=userpxUserID,
                                  userpxDateTime=uploadDate,
                                  userpxUploadPic=default_image_data)
            db.session.add(upload)
            db.session.commit()

        return redirect(url_for('webTemps_views.studentPortfolio'))

@webTemps_views.route('/studentPortfolio')
@login_required
def studentPortfolio():
    """Student Portfolio"""
    """Query student name and profile picture"""
    studentFullName = db.session.query(userAccount.userFirstName, userAccount.userLastName).filter_by(accountTableID=current_user.accountTableID).all()
    studentPicture = db.session.query(userPictures.userpxUploadPic).filter_by(userpxUserID=current_user.accountTableID).first()

    """Query tables to perform eager loading"""
    ela_pictures = languageArtsPics.query.options(joinedload(languageArtsPics.language_subject)).filter_by(elapxUserID=current_user.accountTableID).all()
    hist_pictures = historyPics.query.options(joinedload(historyPics.history_subject)).filter_by(histpxUserID=current_user.accountTableID).all()
    mth_pictures = mathPics.query.options(joinedload(mathPics.math_subject)).filter_by(mthpxUserID=current_user.accountTableID).all()
    sci_pictures = sciencePics.query.options(joinedload(sciencePics.science_subject)).filter_by(scipxUserID=current_user.accountTableID).all()
    soc_pictures = socialStudiesPics.query.options(joinedload(socialStudiesPics.social_studies_subject)).filter_by(socpxUserID=current_user.accountTableID).all()

    """Get student's fullname"""
    studentFN = str(studentFullName).replace("[('", '').replace("', '", ' ').replace("')]", '')

    """Retrieve pictures for each subject"""
    pictures = {
        'language arts': [(pic.elapxUploadPicA, pic.elapxUploadPicB, pic.elapxUploadPicC) for pic in ela_pictures] if ela_pictures else None,
        'history': [(pic.histpxUploadPicA, pic.histpxUploadPicB, pic.histpxUploadPicC) for pic in hist_pictures] if hist_pictures else None,
        'math': [(pic.mthpxUploadPicA, pic.mthpxUploadPicB, pic.mthpxUploadPicC) for pic in mth_pictures] if mth_pictures else None,
        'science': [(pic.scipxUploadPicA, pic.scipxUploadPicB, pic.scipxUploadPicC) for pic in sci_pictures] if sci_pictures else None,
        'social studies': [(pic.socpxUploadPicA, pic.socpxUploadPicB, pic.socpxUploadPicC) for pic in soc_pictures] if soc_pictures else None
    }

    """Retrieve the base64-encoded image data as a string"""
    studentPicture = studentPicture.userpxUploadPic if studentPicture else None

    """Manually entered subject scores"""
    manual_scores = {
        'language arts': calculate_subject_score(current_user.accountTableID, 'ELA'),
        'history': calculate_subject_score(current_user.accountTableID, 'HIS'),
        'math': calculate_subject_score(current_user.accountTableID, 'MTH'),
        'science': calculate_subject_score(current_user.accountTableID, 'SCI'),
        'social studies': calculate_subject_score(current_user.accountTableID, 'SOC')
    }

    return render_template('studentPortfolio.html', 
                           currentUser = current_user,
                           studentFN = studentFN,
                           pictures = pictures,
                           studentPicture = studentPicture,
                           manual_scores = manual_scores)

# Dynamic stucent grades function
def calculate_subject_score(user_id, subject_code):
    """Query the database to calculate the score for the specified user, subject, and lesson"""
    score = studentReport.query.filter_by(ssrUserID=user_id, ssrSubjectCode=subject_code).all()

    if score:
        """Calculate the average score"""
        total_score = sum(score.ssrScore for score in score)
        average_score = total_score / len(score)
        return average_score

    return 0