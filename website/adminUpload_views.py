# Import Packages & Extensions
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import subjectLessons, subjectPictures
from datetime import datetime
from . import db
import base64


# Custom Jinja2 filter to convert binary image data to base64
def to_base64(binary_data):
    return base64.b64encode(binary_data).decode('utf-8')


# Declare Blueprint object
adminUpload_views = Blueprint('adminUpload_views', __name__)


# Declare routes
@adminUpload_views.route("/insert", methods=['GET', 'POST'])
@login_required
def insert():

    """Initialize table"""
    subTbl = None

    """Pull language arts table's form fields"""
    if request.method == 'GET':
        return render_template('uploads.html', currentUser=current_user)
    
    """Get user inputs & store in table"""
    if request.method == 'POST':
        subDateTime_str = request.form.get('subDueDate')
        subDueDate = datetime.strptime(subDateTime_str, '%Y-%m-%d')
        subSubjectCode = request.form.get('subSubjectCode')
        subTopic = request.form.get('subTopic')
        subDescription = request.form.get('subDescription')
        subLessonNumber = request.form.get('subLessonNumber')
        subPageNumber = request.form.get('subPageNumber')
        subQuestion = request.form.get('subQuestion')
        subAnswer = request.form.get('subAnswer')

        """Set DB table relationships w/o uselist to current user"""
        currentUser = current_user.accountTableID
        print(currentUser)
        subPics = current_user.accountTableID


        """Assign DB table cols to form fields"""
        subTbl = subjectLessons(subUserID = subPics,
                            subDueDate = subDueDate,
                            subSubjectCode = subSubjectCode,
                            subTopic = subTopic,
                            subDescription = subDescription,
                            subLessonNumber = subLessonNumber,
                            subPageNumber = subPageNumber,
                            subQuestion = subQuestion,
                            subAnswer = subAnswer)
        db.session.add(subTbl)

        """Commit all above"""
        db.session.commit()

        """Return a success response"""
        return jsonify({"success": True})
    
    return render_template('uploads.html', currentUser=current_user, subTbl=subTbl)



@adminUpload_views.route('/uploads', methods=['GET', 'POST'])
@login_required
def uploads():
    """Upload"""
    if request.method == 'POST':

        """Get user input"""
        subpxLessonNumber = request.form.get("subpxLessonNumber")
        subpxSubjectCode = request.form.get('subpxSubjectCode')
        subpxDueDate = request.form.get('subpxDueDate')
        DueDate = datetime.strptime(subpxDueDate, '%Y-%m-%d')

        """Assign browser file to var"""
        file = request.files['file']

        """Set DB table relationships w/o uselist to current user"""
        currentUser = current_user.accountTableID
        print(currentUser)
        subPics = current_user.accountTableID

        """Set elapxUserID to elaPics DB table relation"""
        subpxUserID = subPics

        """Assign to form's due date"""
        subpxDateTime = DueDate

        """Insert fields into table"""
        upload = subjectPictures(subpxUserID = subpxUserID,
                                  subpxDateTime = subpxDateTime,
                                  subpxSubjectCode = subpxSubjectCode,
                                  subpxLessonNumber = subpxLessonNumber,
                                  subpxFilename = file.filename, 
                                  subpxLessonPic = file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename}'
    return render_template('uploads.html', currentUser=current_user)
