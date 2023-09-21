# Import Packages & Extensions
from sqlalchemy.orm import deferred
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

# Create database objects for DB tables
class userAccount(db.Model, UserMixin):
    __tablename__ = 'user_account'
    accountTableID = db.Column(db.Integer(), primary_key=True)
    userEmail = db.Column(db.String(320), unique=True, nullable=False)
    userFirstName = db.Column(db.String(230), nullable=False)
    userLastName = db.Column(db.String(230), nullable=False)
    hash = db.Column(db.String(150))
    accountDate = db.Column(db.DateTime(timezone=True), default=func.now())
    '''Relationships'''
    user_pictures = db.relationship('userPictures', back_populates='user_pics', uselist=False)
    subject_lessons = db.relationship('subjectLessons', back_populates='student_user', uselist=False)
    language_arts_course = db.relationship('languageArts', back_populates='ela_student', uselist=False)
    history_course = db.relationship('history', back_populates='hist_student', uselist=False)
    math_course = db.relationship('math', back_populates='mth_student', uselist=False)
    science_course = db.relationship('science', back_populates='sci_student', uselist=False)
    social_studies_course = db.relationship('socialStudies', back_populates='social_studies_student', uselist=False)
    student_report = db.relationship('studentReport', back_populates='gradeBook', uselist=False)

    '''Override get_id()'''
    def get_id(self):
        return (self.accountTableID)

    '''Initialize objects'''
    def __init__(self, userEmail, userFirstName, userLastName, hash):
        self.userEmail = userEmail
        self.userFirstName = userFirstName
        self.userLastName = userLastName
        self.hash = hash

    '''Set object as strings'''
    def __repr__(self):
        return f'<userAccount {self.accountTableID}, {self.userEmail}, {self.userFirstName}, {self.userLastName}>'


class userPictures(db.Model):
    __tablename__ = 'user_pictures'
    userpxTableID = db.Column(db.Integer, primary_key=True)
    userpxUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    userpxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    '''Use deferred for lazy load'''
    userpxUploadPic = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    user_pics = db.relationship('userAccount', back_populates='user_pictures')

    '''Initialize Objects'''
    def __init__(self, userpxUserID, userpxDateTime, userpxUploadPic):
        self.userpxUserID = userpxUserID
        self.userpxDateTime = userpxDateTime
        self.userpxUploadPic = userpxUploadPic

    '''Set object as strings'''
    def __repr__(self):
        return f'<userPictures {self.userpxUserID}, {self.userpxDateTime}, {self.userpxUploadPic}>'



class subjectLessons(db.Model):
    __tablename__ = 'subject_lessons'
    subTableID = db.Column(db.Integer, primary_key=True)
    subUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    subDueDate = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    subSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    subTopic = db.Column(db.String(255), nullable=True, index=True)
    subDescription = db.Column(db.String(255), nullable=True, index=True)
    subLessonNumber = db.Column(db.Integer, nullable=True, index=True)
    subPageNumber = db.Column(db.Integer, nullable=True)
    subQuestion = db.Column(db.String(255), nullable=True, index=True)
    subAnswer = db.Column(db.String(255), nullable=True, index=True)
    '''Relationships'''
    student_user = db.relationship('userAccount', back_populates='subject_lessons')
    subject_pictures = db.relationship('subjectPictures', back_populates='subject_lessons')

    '''Initialize Objects'''
    def __init__(self, subUserID, subDueDate, subSubjectCode, subTopic,
                 subDescription, subLessonNumber, subPageNumber,
                 subQuestion, subAnswer):
        self.subUserID = subUserID
        self.subDueDate = subDueDate
        self.subSubjectCode = subSubjectCode
        self.subTopic = subTopic
        self.subDescription = subDescription
        self.subLessonNumber = subLessonNumber
        self.subPageNumber = subPageNumber
        self.subQuestion = subQuestion
        self.subAnswer = subAnswer

    '''Set object as strings'''
    def __repr__(self):
        return f'<subjectLessons {self.subTableID}, {self.subDueDate}, {self.subSubjectCode}, {self.subTopic}, {self.subDescription}, {self.subLessonNumber}, {self.subPageNumber}, {self.subQuestion}, {self.subAnswer}>'



class subjectPictures(db.Model):
    __tablename__ = 'subject_pictures'
    subpxTableID = db.Column(db.Integer, primary_key=True)
    subpxUserID = db.Column(db.Integer, db.ForeignKey('subject_lessons.subTableID', ondelete="CASCADE"))
    subpxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    subpxSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    subpxLessonNumber = db.Column(db.Integer, nullable=True, index=True)
    subpxFilename = db.Column(db.String(255), nullable=True, index=True)
    '''Use deferred for lazy load'''
    subpxLessonPic = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    subject_lessons = db.relationship('subjectLessons', back_populates='subject_pictures')

    '''Initialize Objects'''
    def __init__(self, subpxUserID, subpxDateTime, subpxSubjectCode,
                 subpxLessonNumber, subpxFilename, subpxLessonPic):
        self.subpxUserID = subpxUserID
        self.subpxDateTime = subpxDateTime
        self.subpxSubjectCode = subpxSubjectCode
        self.subpxLessonNumber = subpxLessonNumber
        self.subpxFilename = subpxFilename
        self.subpxLessonPic = subpxLessonPic

    '''Set object as strings'''
    def __repr__(self):
        return f'<subjectPictures {self.subpxTableID}, {self.subpxDateTime}, {self.subpxSubjectCode}, {self.subpxLessonNumber}, {self.subpxFilename}, {self.subpxLessonPic}>'


class languageArts(db.Model):
    __tablename__ = 'language_arts'
    elaTableID = db.Column(db.Integer, primary_key=True)
    elaUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    elaDueDate = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    elaPageCurriculum = db.Column(db.String(255), nullable=True, index=True)
    elaLevel = db.Column(db.Integer, nullable=True)
    elaTopic = db.Column(db.String(255), nullable=True, index=True)
    elaDescription = db.Column(db.String(255), nullable=True, index=True)
    elaLesson = db.Column(db.Integer, nullable=True, index=True)
    elaQuestion = db.Column(db.String(255), nullable=True, index=True)
    elaResponse = db.Column(db.String(255), nullable=True, index=True)
    '''Relationships'''
    ela_student = db.relationship('userAccount', back_populates='language_arts_course')
    language_pixs = db.relationship('languageArtsPics', back_populates='language_subject')

    '''Initialize Objects'''
    def __init__(self, elaUserID, elaDueDate, elaPageCurriculum, elaLevel,
                 elaTopic, elaDescription, elaLesson, elaQuestion, elaResponse):
        self.elaUserID = elaUserID
        self.elaDueDate = elaDueDate
        self.elaPageCurriculum = elaPageCurriculum
        self.elaLevel = elaLevel
        self.elaTopic = elaTopic
        self.elaDescription = elaDescription
        self.elaLesson = elaLesson
        self.elaQuestion = elaQuestion
        self.elaResponse = elaResponse

    '''Set object as strings'''
    def __repr__(self):
        return f'<languageArts {self.elaTableID}, {self.elaDueDate}, {self.elaTopic}, {self.elaDescription}, {self.elaLesson}, {self.elaPageCurriculum}, {self.elaQuestion}, {self.elaResponse}>'


class languageArtsPics(db.Model):
    __tablename__ = 'language_arts_pics'
    elapxTableID = db.Column(db.Integer, primary_key=True)
    elapxUserID = db.Column(db.Integer, db.ForeignKey('language_arts.elaUserID', ondelete="CASCADE"))
    elapxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    elapxSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    '''Use deferred for lazy load'''
    elapxUploadPicA = deferred(db.Column(db.LargeBinary, nullable=True))
    elapxUploadPicB = deferred(db.Column(db.LargeBinary, nullable=True))
    elapxUploadPicC = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    language_subject = db.relationship('languageArts', back_populates='language_pixs')

    '''Initialize Objects'''
    def __init__(self, elapxUserID, elapxDateTime, elapxSubjectCode, elapxUploadPicA, elapxUploadPicB, elapxUploadPicC):
        self.elapxUserID = elapxUserID
        self.elapxDateTime = elapxDateTime
        self.elapxSubjectCode = elapxSubjectCode
        self.elapxUploadPicA = elapxUploadPicA
        self.elapxUploadPicB = elapxUploadPicB
        self.elapxUploadPicC = elapxUploadPicC

    '''Set object as strings'''
    def __repr__(self):
        return f'<languageArtsPics {self.elapxTableID}, {self.elapxDateTime}, {self.elapxSubjectCode}, {self.elapxUploadPicA}, {self.elapxUploadPicB}, {self.elapxUploadPicC}>'


class history(db.Model):
    __tablename__ = 'history'
    histTableID = db.Column(db.Integer, primary_key=True)
    histUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    histDueDate = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    histPageCurriculum = db.Column(db.String(255), nullable=True, index=True)
    histLevel = db.Column(db.Integer, nullable=True)
    histTopic = db.Column(db.String(255), nullable=True, index=True)
    histDescription = db.Column(db.String(255), nullable=True, index=True)
    histLesson = db.Column(db.Integer, nullable=True, index=True)
    histQuestion = db.Column(db.String(255), nullable=True, index=True)
    histResponse = db.Column(db.String(255), nullable=True, index=True)
    '''Relationships'''
    hist_student = db.relationship('userAccount', back_populates='history_course')
    history_pixs = db.relationship('historyPics', back_populates='history_subject')

    '''Initialize Objects'''
    def __init__(self, histUserID, histDueDate, histPageCurriculum, histLevel,
                histTopic, histDescription, histLesson, histQuestion, histResponse):
        self.histUserID = histUserID
        self.histDueDate = histDueDate
        self.histPageCurriculum = histPageCurriculum
        self.histLevel = histLevel
        self.histTopic = histTopic
        self.histDescription = histDescription
        self.histLesson = histLesson
        self.histQuestion = histQuestion
        self.histResponse = histResponse

    '''Set object as strings'''
    def __repr__(self):
        return f'<history {self.histTableID}, {self.histDueDate}, {self.histTopic}, {self.histDescription}, {self.histLesson}, {self.histPageCurriculum}, {self.histQuestion}, {self.histResponse}>'


class historyPics(db.Model):
    __tablename__ = 'history_pics'
    histpxTableID = db.Column(db.Integer, primary_key=True)
    histpxUserID = db.Column(db.Integer, db.ForeignKey('history.histUserID', ondelete="CASCADE"))
    histpxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    histpxSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    '''Use deferred for lazy load'''
    histpxUploadPicA = deferred(db.Column(db.LargeBinary, nullable=True))
    histpxUploadPicB = deferred(db.Column(db.LargeBinary, nullable=True))
    histpxUploadPicC = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    history_subject = db.relationship('history', back_populates='history_pixs')

    '''Initialize Objects'''
    def __init__(self, histpxUserID, histpxDateTime, histpxSubjectCode, histpxUploadPicA, histpxUploadPicB, histpxUploadPicC):
        self.histpxUserID = histpxUserID
        self.histpxDateTime = histpxDateTime
        self.histpxSubjectCode = histpxSubjectCode
        self.histpxUploadPicA = histpxUploadPicA
        self.histpxUploadPicB = histpxUploadPicB
        self.histpxUploadPicC = histpxUploadPicC

    '''Set object as strings'''
    def __repr__(self):
        return f'<historyPics {self.histpxTableID}, {self.histpxDateTime}, {self.histpxSubjectCode}, {self.histpxUploadPicA}, {self.histpxUploadPicB}, {self.histpxUploadPicC}>'


class math(db.Model):
    __tablename__ = 'math'
    mthTableID = db.Column(db.Integer, primary_key=True)
    mthUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    mthDueDate = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    mthPageCurriculum = db.Column(db.String(255), nullable=True, index=True)
    mthLevel = db.Column(db.Integer, nullable=True)
    mthTopic = db.Column(db.String(255), nullable=True, index=True)
    mthDescription = db.Column(db.String(255), nullable=True, index=True)
    mthLesson = db.Column(db.Integer, nullable=True, index=True)
    mthQuestion = db.Column(db.String(255), nullable=True, index=True)
    mthResponse = db.Column(db.String(255), nullable=True, index=True)
    '''Relationships'''
    mth_student = db.relationship('userAccount', back_populates='math_course')
    math_pixs = db.relationship('mathPics', back_populates='math_subject')

    '''Initialize Objects'''
    def __init__(self, mthUserID, mthDueDate, mthPageCurriculum, mthLevel,
                mthTopic, mthDescription, mthLesson, mthQuestion, mthResponse):
        self.mthUserID = mthUserID
        self.mthDueDate = mthDueDate
        self.mthPageCurriculum = mthPageCurriculum
        self.mthLevel = mthLevel
        self.mthTopic = mthTopic
        self.mthDescription = mthDescription
        self.mthLesson = mthLesson
        self.mthQuestion = mthQuestion
        self.mthResponse = mthResponse

    '''Set object as strings'''
    def __repr__(self):
        return f'<math {self.mthTableID}, {self.mthDueDate}, {self.mthPageCurriculum}, {self.mthTopic}, {self.mthDescription}, {self.mthLesson}, {self.mthQuestion}, {self.mthResponse}>'


class mathPics(db.Model):
    __tablename__ = 'math_pics'
    mthpxTableID = db.Column(db.Integer, primary_key=True)
    mthpxUserID = db.Column(db.Integer, db.ForeignKey('math.mthUserID', ondelete="CASCADE"))
    mthpxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    mthpxSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    '''Use deferred for lazy load'''
    mthpxUploadPicA = deferred(db.Column(db.LargeBinary, nullable=True))
    mthpxUploadPicB = deferred(db.Column(db.LargeBinary, nullable=True))
    mthpxUploadPicC = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    math_subject = db.relationship('math', back_populates='math_pixs')

    '''Initialize Objects'''
    def __init__(self, mthpxUserID, mthpxDateTime, mthpxSubjectCode, mthpxUploadPicA, mthpxUploadPicB, mthpxUploadPicC):
        self.mthpxUserID = mthpxUserID
        self.mthpxDateTime = mthpxDateTime
        self.mthpxSubjectCode = mthpxSubjectCode
        self.mthpxUploadPicA = mthpxUploadPicA
        self.mthpxUploadPicB = mthpxUploadPicB
        self.mthpxUploadPicC = mthpxUploadPicC

    '''Set object as strings'''
    def __repr__(self):
        return f'<mathPics {self.mthpxTableID}, {self.mthpxDateTime}, {self.mthpxSubjectCode}, {self.mthpxUploadPicA}, {self.mthpxUploadPicB}, {self.mthpxUploadPicC}>'


class science(db.Model):
    __tablename__ = 'science'
    sciTableID = db.Column(db.Integer, primary_key=True)
    sciUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    sciDueDate = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    sciPageCurriculum = db.Column(db.String(255), nullable=True, index=True)
    sciLevel = db.Column(db.Integer, nullable=True)
    sciTopic = db.Column(db.String(255), nullable=True, index=True)
    sciDescription = db.Column(db.String(255), nullable=True, index=True)
    sciLesson = db.Column(db.Integer, nullable=True, index=True)
    sciQuestion = db.Column(db.String(255), nullable=True, index=True)
    sciResponse = db.Column(db.String(255), nullable=True, index=True)
    '''Relationships'''
    sci_student = db.relationship('userAccount', back_populates='science_course')
    science_pixs = db.relationship('sciencePics', back_populates='science_subject')

    '''Initialize Objects'''
    def __init__(self, sciUserID, sciDueDate, sciPageCurriculum, sciLevel,
                sciTopic, sciDescription, sciLesson, sciQuestion, sciResponse):
        self.sciUserID = sciUserID
        self.sciDueDate = sciDueDate
        self.sciPageCurriculum = sciPageCurriculum
        self.sciLevel = sciLevel
        self.sciTopic = sciTopic
        self.sciDescription = sciDescription
        self.sciLesson = sciLesson
        self.sciQuestion = sciQuestion
        self.sciResponse = sciResponse

    '''Set object as strings'''
    def __repr__(self):
        return f'<science {self.sciTableID}, {self.sciDueDate}, {self.sciPageCurriculum}, {self.sciTopic}, {self.sciDescription}, {self.sciLesson}, {self.sciQuestion}, {self.sciResponse}>'


class sciencePics(db.Model):
    __tablename__ = 'science_pics'
    scipxTableID = db.Column(db.Integer, primary_key=True)
    scipxUserID = db.Column(db.Integer, db.ForeignKey('science.sciUserID', ondelete="CASCADE"))
    scipxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    scipxSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    '''Use deferred for lazy load'''
    scipxUploadPicA = deferred(db.Column(db.LargeBinary, nullable=True))
    scipxUploadPicB = deferred(db.Column(db.LargeBinary, nullable=True))
    scipxUploadPicC = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    science_subject = db.relationship('science', back_populates='science_pixs')

    '''Initialize Objects'''
    def __init__(self, scipxUserID, scipxDateTime, scipxSubjectCode, scipxUploadPicA, scipxUploadPicB, scipxUploadPicC):
        self.scipxUserID = scipxUserID
        self.scipxDateTime = scipxDateTime
        self.scipxSubjectCode = scipxSubjectCode
        self.scipxUploadPicA = scipxUploadPicA
        self.scipxUploadPicB = scipxUploadPicB
        self.scipxUploadPicC = scipxUploadPicC

    '''Set object as strings'''
    def __repr__(self):
        return f'<sciencePics {self.scipxTableID}, {self.scipxDateTime}, {self.scipxSubjectCode}, {self.scipxUploadPicA}, {self.scipxUploadPicB}, {self.scipxUploadPicC}>'


class socialStudies(db.Model):
    __tablename__ = 'social_studies'
    socTableID = db.Column(db.Integer, primary_key=True)
    socUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    socDueDate = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    socPageCurriculum = db.Column(db.String(255), nullable=True, index=True)
    socLevel = db.Column(db.Integer, nullable=True)
    socTopic = db.Column(db.String(255), nullable=True, index=True)
    socDescription = db.Column(db.String(255), nullable=True, index=True)
    socLesson = db.Column(db.Integer, nullable=True, index=True)
    socQuestion = db.Column(db.String(255), nullable=True, index=True)
    socResponse = db.Column(db.String(255), nullable=True, index=True)
    '''Relationships'''
    social_studies_student = db.relationship('userAccount', back_populates='social_studies_course')
    social_pixs = db.relationship('socialStudiesPics', back_populates='social_studies_subject')

    '''Initialize Objects'''
    def __init__(self, socUserID, socDueDate, socPageCurriculum, socLevel,
                socTopic, socDescription, socLesson, socQuestion, socResponse):
        self.socUserID = socUserID
        self.socDueDate = socDueDate
        self.socPageCurriculum = socPageCurriculum
        self.socLevel = socLevel
        self.socTopic = socTopic
        self.socDescription = socDescription
        self.socLesson = socLesson
        self.socQuestion = socQuestion
        self.socResponse = socResponse

    '''Set object as strings'''
    def __repr__(self):
        return f'<socialStudies {self.socTableID}, {self.socDueDate}, {self.socPageCurriculum}, {self.socTopic}, {self.socDescription}, {self.socLesson}, {self.socQuestion}, {self.socResponse}>'


class socialStudiesPics(db.Model):
    __tablename__ = 'social_studies_pics'
    socpxTableID = db.Column(db.Integer, primary_key=True)
    socpxUserID = db.Column(db.Integer, db.ForeignKey('social_studies.socUserID', ondelete="CASCADE"))
    socpxDateTime = db.Column(db.DateTime(timezone=True), default=func.now(), index=True, nullable=True)
    socpxSubjectCode = db.Column(db.String(255), nullable=True, index=True)
    '''Use deferred for lazy load'''
    socpxUploadPicA = deferred(db.Column(db.LargeBinary, nullable=True))
    socpxUploadPicB = deferred(db.Column(db.LargeBinary, nullable=True))
    socpxUploadPicC = deferred(db.Column(db.LargeBinary, nullable=True))
    '''Relationships'''
    social_studies_subject = db.relationship('socialStudies', back_populates='social_pixs')

    '''Initialize Objects'''
    def __init__(self, socpxUserID, socpxDateTime, socpxSubjectCode, socpxUploadPicA, socpxUploadPicB, socpxUploadPicC):
        self.socpxUserID = socpxUserID
        self.socpxDateTime = socpxDateTime
        self.socpxSubjectCode = socpxSubjectCode
        self.socpxUploadPicA = socpxUploadPicA
        self.socpxUploadPicB = socpxUploadPicB
        self.socpxUploadPicC = socpxUploadPicC

    '''Set object as strings'''
    def __repr__(self):
        return f'<socialStudiesPics {self.socpxUserID}, {self.socpxDateTime}, {self.socpxSubjectCode}, {self.socpxUploadPicA}, {self.socpxUploadPicB}, {self.socpxUploadPicC}>'


class studentReport(db.Model):
    __tablename__ = 'student_report'
    ssrTableID = db.Column(db.Integer, primary_key=True)
    ssrUserID = db.Column(db.Integer, db.ForeignKey('user_account.accountTableID', ondelete="CASCADE"))
    ssrSubjectCode = db.Column(db.String(5), nullable=True, index=True)
    ssrLessonNumber = db.Column(db.Integer, nullable=False)
    ssrScore = db.Column(db.Float, nullable=False)
    '''Relationships'''
    gradeBook = db.relationship('userAccount', back_populates='student_report')

    '''Initialize Objects'''
    def __init__(self, ssrUserID, ssrSubjectCode, ssrLessonNumber, ssrScore):
        self.ssrUserID = ssrUserID
        self.ssrSubjectCode = ssrSubjectCode
        self.ssrLessonNumber = ssrLessonNumber
        self.ssrScore = ssrScore

    '''Set object as strings'''
    def __repr__(self):
        return f'<studentReport {self.ssrUserID}, {self.ssrSubjectCode}, {self.ssrLessonNumber}, {self.ssrScore}>'

