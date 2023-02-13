class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:regopi09@localhost:3306/timetable"
    SQLALCHEMY_TRACK_MODIFICATIOS = False

    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'