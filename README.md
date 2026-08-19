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



 <div class="row quick-links">
        <!-- Visitors -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">Quick links</div>
          </div>
          <div class="box-body" style="padding:8px 16px">


            <a class="box" href="#">
              <div class="box-link">
                <i style="color: #592CEB;" class="bi bi-calendar-event"></i>
              </div>
              <div>Add Timetable</div>
            </a>


            <a href="#" class="box">
              <div class="box-link">
                <i style="color: #0bba5d;" class="bi bi-file-earmark-plus"></i>
              </div>
              <div>Add Test</div>
            </a>

            <a href="#" class="box">
              <div class="box-link">
                <i style="color: #EF671A;" class="bi bi-mortarboard"></i>
              </div>
              <div>Add Exam</div>
            </a>

            <a href="#" class="box">
              <div class="box-link">
                <i style="color: #247DF8;" class="bi bi-file-earmark-arrow-up"></i>
              </div>
              <div>Upload Notes</div>
            </a>

            <a href="#" class="box">
              <div class="box-link">
                <i style="color: #623AE2;" class="bi bi-chat-square-text"></i>
              </div>
              <div style="color: #623AE2;">Post Announcement</div>
            </a>


          </div>
        </div>
      </div>