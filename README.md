user = db.session.scalar(select(User).options(joinedload(User.post))).all()

if user.profile_pic
 -> show img 

else
 -> display initials via api (hhtps://ui-avatar.com/api/?name={{current_user.username}}&background=random)