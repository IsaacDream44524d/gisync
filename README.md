user = db.session.scalar(select(User).options(joinedload(User.post))).all()

if user.profile_pic
 -> show img 

else
 -> display initials via api (hhtps://ui-avatar.com/api/?name={{current_user.username}}&background=random)

 FIX THE DARK MODE, WHEN REFRESHED DARK MODE IS REMOVED AND WHEN CHANGED PAGES

 users = [
    user(
        fullname=student['fullname'],
        email=student['email'],
        year=student['year']
        
    )

    for student in students
 ]

 db.session.add_all(users)
 db.session.commit

 disable login when changing password