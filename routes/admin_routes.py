from flask import Blueprint, render_template, request, redirect
from helpers import build_admin_questions_list, isBlank

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['POST', 'GET'])
def admin_view(dbConnector):
    adminUser = request.form.get("adminId")
    if isBlank(adminUser):
        return redirect('/login')
    qName = request.form.get("q_name")
    delQ = request.form.get("deleteQuestion")

    if not isBlank(qName):
        try:
            dbConnector.executeSQL("UPDATE Questionz SET Accepted=TRUE WHERE Question=%s", (qName,))
        except Exception as e:
            print("ERROR: %s" % str(e))
    elif not isBlank(delQ):
        try:
            dbConnector.executeSQL("DELETE FROM Questionz WHERE Question=%s", (delQ,))
        except Exception as e:
            print("ERROR: %s" % str(e))
    q_list = build_admin_questions_list(dbConnector, adminUser, False)
    b_list = build_admin_questions_list(dbConnector, adminUser, True)
    return render_template('admin.html', admin=adminUser, questions_list=q_list, bank_list=b_list)
