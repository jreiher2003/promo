from app import db,bcrypt
from app.ascii.models import AsciiArt
from app.users.models import Users, Role, UserRoles

db.drop_all()
# print "just dropped table"
db.create_all()

# user = Users(email="jeffreiher@gmail.com", password="123456")
role = Role(name="user",description="Basic User of Site")
db.session.add_all([role])
db.session.commit()


# user_role = UserRoles(id=1, user_id=1,role_id=1)
# one = AsciiArt(title = "Test Title", art = "This is test art")
# one.user_id = 1
# one.lat =  42.363633
# one.lon = -87.844794
# db.session.add_all([one,user_role])
# db.session.commit()

print "Successful import"