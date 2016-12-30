from app import db,bcrypt
from app.models import AsciiArt, Users

db.drop_all()
print "just dropped table"
db.create_all()

user = Users(username="jeff", password=bcrypt.generate_password_hash("123456"))
db.session.add(user)

one = AsciiArt(title = "Test Title", art = "This is test art")
one.user_id = 1
one.lat =  42.363633
one.lon = -87.844794
db.session.add(one)
db.session.commit()

print "Successful import"