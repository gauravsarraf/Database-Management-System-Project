import sys
import random
import qdarkstyle
import pymysql as mdb
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from LMS_FULL_UI import Ui_lms
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from subprocess import Popen

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.ui = Ui_lms()
        self.ui.setupUi(self)
        self.setFixedSize(798,645)
        self.menu()
        self.connect_to_db()
        self.ui.login_frame.hide()
        self.ui.new_user_frame.hide()
        self.ui.view_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.login_activator()
        self.show()

    def connect_to_db(self):
        try:
            global db, cur
            db = mdb.connect("35.224.85.0", "appuser", "root", "LMS")
            cur = db.cursor()
            self.ui.stat.setText("CONNECTED!")
        except mdb.Error as e:
            self.ui.stat.setText("NOT CONNECTED!")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\sarra\\Downloads\\LMS\\images\\connected.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon2 = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\sarra\\Downloads\\LMS\\images\\disconnected.png"), QtGui.QIcon.Normal,QtGui.QIcon.On)
        try:
            if (db.open):
                con_status.setIcon(icon)
            else:
                con_status.setIcon(icon2)
        except mdb.Error as e:
            con_status.setIcon(icon2)

    def login_activator(self):
        self.setWindowTitle("LMS-Login")
        self.ui.new_user_frame.hide()
        self.ui.view_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.ui.view_status_frame.hide()
        self.ui.approve_leave_frame.hide()
        self.ui.login_frame.show()
        self.ui.u_name.clear()
        self.ui.pwd.clear()

        def fill_form():
            global urname
            urname = self.ui.u_name.text()
            pd = self.ui.pwd.text()

            if not urname:
                self.ui.stat.setText("Please check your input!")
                return
            elif not pd:
                self.ui.stat.setText("Please check your input!")
                return
            else:
                result = cur.execute("SELECT * FROM USERS WHERE USER = %s AND PASS = %s;", (urname, pd), )
                if result > 0:

                    self.setStatusTip("Welcome!")
                    self.ui.login_frame.hide()
                    self.view_activator()
                else:
                    self.ui.stat.setText("Please check your input!")

        def call_newuser():
            self.ui.login_frame.hide()
            self.new_user_activator()

        self.ui.login_bt.clicked.connect(fill_form)
        self.ui.login_bt.setStatusTip("Login?")
        self.ui.nw_ur_bt.clicked.connect(call_newuser)
        self.ui.nw_ur_bt.setStatusTip("New to BMSIT?")

    def new_user_activator(self):
        self.setWindowTitle("LMS-New User")
        self.ui.login_frame.hide()
        self.ui.view_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.ui.view_status_frame.hide()
        self.ui.approve_leave_frame.hide()
        self.ui.new_user_frame.show()

        def fill_form():
            def savedata():
                if desig_select == 0:
                    desig = 'HOD'
                elif desig_select == 1:
                    desig = 'Associate Professor'
                elif desig_select == 2:
                    desig = 'Assistant Professor'
                elif desig_select == 3:
                    desig = 'Support Staff'
                elif desig_select == 4:
                    desig = 'Student'

                cur.execute("INSERT INTO USERS VALUES(%s, %s);", (ur_name, pwd))
                cur.execute("INSERT INTO DEPT_DATA VALUES(%s, %s, %s);", (int(dept_id), dept, per_id))
                cur.execute("INSERT INTO EMP_DATA VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",
                            (f_name, l_name, per_id, dob, ur_name, reporting_id, desig, int(free_leave)))

            f_name = self.ui.f_name_2.text()
            l_name = self.ui.l_name_2.text()
            per_id = self.ui.per_id_2.text()
            dob_original = self.ui.date_2.date()
            dob = dob_original.toPyDate()
            ur_name = self.ui.ur_name_2.text()
            pwd = self.ui.pwd_3.text()
            cmf_pwd = self.ui.cfm_pwd_2.text()
            dept_select = self.ui.dept_select_2.currentIndex()
            reporting_id = self.ui.reporting_id_2.text()
            desig_select = self.ui.desig_select_2.currentIndex()
            free_leave = self.ui.free_leave_2.text()
            if dept_select == 0:
                self.ui.dept_id_2.setText('1')
                dept = 'CSE'
                dept_id = 1
            elif dept_select == 1:
                self.ui.dept_id_2.setText('2')
                dept = 'ISE'
                dept_id = 2
            elif dept_select == 2:
                self.ui.dept_id_2.setText('3')
                dept = 'ECE'
                dept_id = 3
            elif dept_select == 3:
                self.ui.dept_id_2.setText('4')
                dept = 'MECH'
                dept_id = 4
            elif dept_select == 4:
                self.ui.dept_id_2.setText('5')
                dept = 'TC'
                dept_id = 5
            elif dept_select == 5:
                self.ui.dept_id_2.setText('6')
                dept = 'EEE'
                dept_id = 6
            elif dept_select == 6:
                self.ui.dept_id_2.setText('7')
                dept = 'CIVIL'
                dept_id = 7
            elif dept_select == 7:
                self.ui.dept_id_2.setText('8')
                dept = 'MCA'
                dept_id = 8
            else:
                self.ui.dept_id_2.setText('9')
                dept = 'ARCH'
                dept_id = 9

            if not f_name:
                self.setStatusTip("Please check your input!")
                return
            elif not l_name:
                self.setStatusTip("Please check your input!")
                return
            elif not per_id:
                self.setStatusTip("Please check your input!")
                return
            elif not dob:
                self.setStatusTip("Please check your input!")
                return
            elif not dob_original:
                self.setStatusTip("Please check your input!")
                return
            elif not ur_name:
                self.setStatusTip("Please check your input!")
                return
            elif not pwd:
                self.setStatusTip("Please check your input!")
                return
            elif not cmf_pwd:
                self.setStatusTip("Please check your input!")
                return
            elif not reporting_id:
                self.setStatusTip("Please check your input!")
                return
            elif not free_leave:
                self.setStatusTip("Please check your input!")
                return
            elif pwd != cmf_pwd:
                self.setStatusTip("Your Password does not match! Please check your input!!")
                return
            elif len(pwd) <8 or str.isalnum(pwd):
                self.setStatusTip("Your Password does not meet the constrain! Please check your input!!")
                return
            else:
                check_save = QMessageBox.question(self, 'Save?',
                                                  "Are you sure you want save the input data?",
                                                  QMessageBox.Yes | QMessageBox.No)
                if check_save == QMessageBox.Yes:
                    savedata()
                    self.setStatusTip("Welcome!")
                    self.ui.new_user_frame.hide()
                    self.login_activator()
                    db.commit()
                else:
                    return

        def show_tip():
            self.ui.f_name_2.setStatusTip("Your First Name?")
            self.ui.l_name_2.setStatusTip("Your Last Name?")
            self.ui.per_id_2.setStatusTip(
                "EX: If your Dept is CSE, then CSExxx is your Emp_Id (xxx being some number). 000-050 reserved for staff only.")
            self.ui.ur_name_2.setStatusTip(
                "Can only contain letters, numbers, dashes (-), periods (.), and underscores (_)."
                "Must be a minimum of 5 characters and a maximum 32 characters")
            self.ui.dept_id_2.setStatusTip("Will Be Set Automatically!")
            self.ui.dept_select_2.setStatusTip("Your Department?")
            self.ui.date_2.setStatusTip("Enter in xx-mon-xx format!")
            self.ui.pwd.setStatusTip("Minimum length is 8 characters, maximum is 128.  "
                                     "It must contain one special character (e.g. !, @, #, $ etc.), one number and one alphabet.")
            self.ui.cfm_pwd_2.setStatusTip("Reenter your password!")
            self.ui.free_leave_2.setStatusTip("Free number of leaves allowed per year")
            self.ui.desig_select_2.setStatusTip("Your designation")
            self.ui.reporting_id_2.setStatusTip("Person ID of your reporting head!")

        def clear():
            self.ui.f_name_2.clear()
            self.ui.l_name_2.clear()
            self.ui.per_id_2.clear()
            self.ui.ur_name_2.clear()
            self.ui.dept_id_2.setText('--')
            self.ui.pwd_3.clear()
            self.ui.cfm_pwd_2.clear()
            self.ui.free_leave_2.clear()
            self.ui.reporting_id_2.clear()
            self.ui.dept_select_2.setCurrentIndex(0)
            self.ui.desig_select_2.setCurrentIndex(0)
            self.ui.date_2.clear()

        self.ui.save_bt_2.clicked.connect(fill_form)
        self.ui.save_bt_2.setStatusTip("Save the entered information?")
        self.ui.clear_bt_2.clicked.connect(clear)
        self.ui.clear_bt_2.setStatusTip("Clear entered information?")
        self.ui.return_bt_2.setText("Return to Login Page")
        self.ui.return_bt_2.clicked.connect(self.login_activator)
        self.ui.return_bt_2.setStatusTip("Return to Login Page without creating user?")
        #self.ui.date_2.setCalendarPopup(True)
        self.onlyInt = QIntValidator()
        self.ui.free_leave_2.setValidator(self.onlyInt)
        show_tip()

    def view_activator(self):
        self.setWindowTitle("LMS-View")
        self.ui.new_user_frame.hide()
        self.ui.login_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.ui.view_status_frame.hide()
        self.ui.approve_leave_frame.hide()
        self.ui.view_frame.show()
        def fill_info():
            cur.execute(
                "SELECT EMP_DATA.PER_ID, EMP_DATA.REP_PER_ID, EMP_DATA.DESIGNATION, EMP_DATA.FREE_LEAVES, EMP_DATA.F_NAME, EMP_DATA.L_NAME FROM EMP_DATA WHERE EMP_DATA.USER = %s;",
                (urname))
            result = cur.fetchone()
            per_id = result[0]
            rep_per_id = result[1]
            desig = result[2]
            free_leave = result[3]
            f_name = result[4]
            l_name = result[5]
            wl_text = "Welcome " + f_name + " " + l_name + "!"
            self.ui.ur_name_lab.setText(urname)
            self.ui.per_id_lab.setText(per_id)
            self.ui.reporting_id_lab.setText(rep_per_id)
            self.ui.desig_lab.setText(desig)
            self.ui.free_leaves_lab.setText(str(free_leave))
            self.ui.wl_name.setText(wl_text)
            cur.execute(
                "SELECT DEPT_DATA.DEPT_ID, DEPT_DATA.DEPT_NAME FROM DEPT_DATA, EMP_DATA WHERE EMP_DATA.PER_ID = %s AND DEPT_DATA.PER_ID = EMP_DATA.PER_ID;",
                (per_id))
            result1 = cur.fetchone()
            dept_id = result1[0]
            dept_name = result1[1]
            self.ui.dept_id_lab.setText(str(dept_id))
            self.ui.dept_lab.setText(dept_name)
            if desig == "Student":
                self.ui.approve_leave.setEnabled(False)
            else:
                self.ui.approve_leave.setEnabled(True)
        def view_status():
            self.ui.view_frame.hide()
            self.view_status_activator()
            self.setStatusTip("View Leave Status")
        def apply_leave():
            self.ui.view_frame.hide()
            self.apply_leave_activator()
            self.setStatusTip("Apply for new leave?")
        def approve_leave():
            self.ui.view_frame.hide()
            self.approve_leave_activator()
            self.setStatusTip("Approve pending leaves?")
        def edit_info():
            self.ui.view_frame.hide()
            self.edit_info_activator()
            self.setStatusTip("Edit Personal Information?")
        def logout():
            choice = QMessageBox.question(self, 'Quit?',
                                          "Are you sure you want to logout?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.ui.view_frame.hide()
                self.login_activator()
            else:
                pass

        fill_info()
        self.ui.view_status.clicked.connect(view_status)
        self.ui.view_status.setStatusTip("View your leave status!")
        self.ui.apply_leave.clicked.connect(apply_leave)
        self.ui.apply_leave.setStatusTip("Apply for a new leave?")
        self.ui.approve_leave.clicked.connect(approve_leave)
        self.ui.approve_leave.setStatusTip("Approve pending leaves?")
        self.ui.edit_info.clicked.connect(edit_info)
        self.ui.edit_info.setStatusTip("Edit your personal information?")
        self.ui.logout.clicked.connect(logout)
        self.ui.logout.setStatusTip("Logout?")

    def edit_info_activator(self):
        self.setWindowTitle("LMS-Edit Info")
        self.ui.login_frame.hide()
        self.ui.view_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.ui.view_status_frame.hide()
        self.ui.approve_leave_frame.hide()
        self.ui.new_user_frame.show()

        def show_tip():
            self.ui.f_name_2.setStatusTip("Your First Name?")
            self.ui.l_name_2.setStatusTip("Your Last Name?")
            self.ui.per_id_2.setStatusTip(
                "EX: If your Dept is CSE, then CSExxx is your Emp_Id (xxx being some number). 000-050 reserved for staff only.")
            self.ui.ur_name_2.setStatusTip(
                "Can only contain letters, numbers, dashes (-), periods (.), and underscores (_)."
                "Must be a minimum of 5 characters and a maximum 32 characters")
            self.ui.dept_id_2.setStatusTip("Will Be Set Automatically!")
            self.ui.dept_select_2.setStatusTip("Your Department?")
            self.ui.date_2.setStatusTip("Enter in xx-mon-xx format!")
            self.ui.pwd.setStatusTip("Minimum length is 8 characters, maximum is 128.  "
                                     "It must contain one special character (e.g. !, @, #, $ etc.), one number and one alphabet.")
            self.ui.cfm_pwd_2.setStatusTip("Reenter your password!")
            self.ui.free_leave_2.setStatusTip("Free number of leaves allowed per year")
            self.ui.desig_select_2.setStatusTip("Your designation")
            self.ui.reporting_id_2.setStatusTip("Person ID of your reporting head!")

        def clear():
            self.ui.f_name_2.clear()
            self.ui.l_name_2.clear()
            self.ui.per_id_2.clear()
            self.ui.ur_name_2.clear()
            self.ui.dept_id_2.setText('--')
            self.ui.pwd_3.clear()
            self.ui.cfm_pwd_2.clear()
            self.ui.free_leave_2.clear()
            self.ui.reporting_id_2.clear()
            self.ui.dept_select_2.setCurrentIndex(0)
            self.ui.desig_select_2.setCurrentIndex(0)
            self.ui.date_2.clear()

        def show_preve_info():

            cur.execute("SELECT EMP_DATA.F_NAME, EMP_DATA.L_NAME, EMP_DATA.DOB, EMP_DATA.REP_PER_ID, EMP_DATA.DESIGNATION, EMP_DATA.FREE_LEAVES, EMP_DATA.PER_ID FROM EMP_DATA WHERE EMP_DATA.USER = %s;", (urname))
            result1 = cur.fetchone()
            cur.execute("SELECT USERS.PASS FROM USERS WHERE USERS.USER = %s;", (urname))
            result2 = cur.fetchone()
            cur.execute("SELECT DEPT_NAME, DEPT_ID FROM DEPT_DATA, EMP_DATA WHERE DEPT_DATA.PER_ID = EMP_DATA.PER_ID AND EMP_DATA.USER = %s;", (urname))
            result3 = cur.fetchone()
            if result3[1] == 0:
                dept = 'CSE'
                dept_id = 0
            elif result3[1] == 1:
                dept = 'ISE'
                dept_id = 1
            elif result3[1] == 2:
                dept = 'ECE'
                dept_id = 2
            elif result3[1] == 3:
                dept = 'MECH'
                dept_id = 3
            elif result3[1] == 4:
                dept = 'TC'
                dept_id = 4
            elif result3[1] == 5:
                dept = 'EEE'
                dept_id = 5
            elif result3[1] == 6:
                dept = 'CIVIL'
                dept_id = 6
            elif result3[1] == 7:
                dept = 'MCA'
                dept_id = 7
            else:
                dept = 'ARCH'
                dept_id = 8
            global desig
            if result1[4] == 'HOD':
                desig = 0
            elif result1[4] == 'Associate Professor':
                desig = 1
            elif result1[4] == 'Assistant Professor':
                desig = 2
            elif result1[4]== 'Support Staff':
                desig = 3
            elif result1[4] == 'Student':
                desig = 4

            f_name = result1[0]
            l_name = result1[1]
            per_id = result1[6]
            dob = result1[2]
            pwd = result2[0]
            reporting_id = result1[3]
            free_leave = result1[5]
            self.ui.f_name_2.setText(f_name)
            self.ui.l_name_2.setText(l_name)
            self.ui.per_id_2.setText(per_id)
            self.ui.date_2.setDate(dob)
            self.ui.ur_name_2.setText(urname)
            self.ui.pwd_3.setText(pwd)
            self.ui.cfm_pwd_2.setText(pwd)
            self.ui.dept_select_2.setCurrentIndex((dept_id - 1))
            self.ui.reporting_id_2.setText(reporting_id)
            self.ui.desig_select_2.setCurrentIndex(desig)
            self.ui.free_leave_2.setText(str(free_leave))
            self.ui.dept_id_2.setText(str(dept_id))
            global old_per_id
            old_per_id = per_id

        def fill_form():
            def savedata():
                if desig_select == 0:
                    desig = 'HOD'
                elif desig_select == 1:
                    desig = 'Associate Professor'
                elif desig_select == 2:
                    desig = 'Assistant Professor'
                elif desig_select == 3:
                    desig = 'Support Staff'
                elif desig_select == 4:
                    desig = 'Student'
                cur.execute(
                    "UPDATE EMP_DATA SET EMP_DATA.F_NAME = %s, EMP_DATA.L_NAME = %s, EMP_DATA.PER_ID = %s, EMP_DATA.DOB = %s, EMP_DATA.USER = %s, EMP_DATA.REP_PER_ID = %s, EMP_DATA.DESIGNATION = %s, EMP_DATA.FREE_LEAVES = %s WHERE EMP_DATA.USER = %s",
                    (f_name, l_name, per_id_new, dob, ur_name, reporting_id, desig, str(free_leave), urname))
                cur.execute("UPDATE DEPT_DATA SET DEPT_DATA.DEPT_ID = %s, DEPT_DATA.DEPT_NAME = %s, DEPT_DATA.PER_ID = %s WHERE DEPT_DATA.PER_ID = %s;", (str(dept_id), dept, per_id_new, old_per_id))
                cur.execute("UPDATE USERS SET USERS.USER = %s, USERS.PASS =%s WHERE USERS.USER = %s;", (ur_name, pwd, urname))

            f_name = self.ui.f_name_2.text()
            l_name = self.ui.l_name_2.text()
            per_id_new = self.ui.per_id_2.text()
            dob_original = self.ui.date_2.date()
            dob = dob_original.toPyDate()
            ur_name = self.ui.ur_name_2.text()
            pwd = self.ui.pwd_3.text()
            cmf_pwd = self.ui.cfm_pwd_2.text()
            dept_select = self.ui.dept_select_2.currentIndex()
            reporting_id = self.ui.reporting_id_2.text()
            desig_select = self.ui.desig_select_2.currentIndex()
            free_leave = self.ui.free_leave_2.text()
            if dept_select == 0:
                self.ui.dept_id_2.setText('1')
                dept = 'CSE'
                dept_id = 1
            elif dept_select == 1:
                self.ui.dept_id_2.setText('2')
                dept = 'ISE'
                dept_id = 2
            elif dept_select == 2:
                self.ui.dept_id_2.setText('3')
                dept = 'ECE'
                dept_id = 3
            elif dept_select == 3:
                self.ui.dept_id_2.setText('4')
                dept = 'MECH'
                dept_id = 4
            elif dept_select == 4:
                self.ui.dept_id_2.setText('5')
                dept = 'TC'
                dept_id = 5
            elif dept_select == 5:
                self.ui.dept_id_2.setText('6')
                dept = 'EEE'
                dept_id = 6
            elif dept_select == 6:
                self.ui.dept_id_2.setText('7')
                dept = 'CIVIL'
                dept_id = 7
            elif dept_select == 7:
                self.ui.dept_id_2.setText('8')
                dept = 'MCA'
                dept_id = 8
            else:
                self.ui.dept_id_2.setText('9')
                dept = 'ARCH'
                dept_id = 9

            if not f_name:
                self.setStatusTip("Please check your input!")
                return
            elif not l_name:
                self.setStatusTip("Please check your input!")
                return
            elif not per_id_new:
                self.setStatusTip("Please check your input!")
                return
            elif not dob:
                self.setStatusTip("Please check your input!")
                return
            elif not dob_original:
                self.setStatusTip("Please check your input!")
                return
            elif not ur_name:
                self.setStatusTip("Please check your input!")
                return
            elif not pwd:
                self.setStatusTip("Please check your input!")
                return
            elif not cmf_pwd:
                self.setStatusTip("Please check your input!")
                return
            elif not reporting_id:
                self.setStatusTip("Please check your input!")
                return
            elif not free_leave:
                self.setStatusTip("Please check your input!")
                return
            elif pwd != cmf_pwd:
                self.setStatusTip("Your Password does not match! Please check your input!!")
                return
            else:
                check_save = QMessageBox.question(self, 'Save?',
                                                  "Are you sure you want save the input data?",
                                                  QMessageBox.Yes | QMessageBox.No)
                if check_save == QMessageBox.Yes:
                    savedata()
                    self.setStatusTip("Welcome!")
                    db.commit()
                    clear()
                    self.ui.new_user_frame.hide()
                    self.view_activator()
                else:
                    return

        show_preve_info()
        show_tip()
        self.ui.date_2.setCalendarPopup(True)
        self.onlyInt = QIntValidator()
        self.ui.free_leave_2.setValidator(self.onlyInt)
        self.ui.save_bt_2.clicked.connect(fill_form)
        self.ui.save_bt_2.setStatusTip("Update the entered information?")
        self.ui.clear_bt_2.clicked.connect(clear)
        self.ui.clear_bt_2.setStatusTip("Clear entered information?")
        self.ui.return_bt_2.setText("Return to Dashboard")
        self.ui.return_bt_2.setStatusTip("Return to Dashboard without making any changes?")
        self.ui.return_bt_2.clicked.connect(self.view_activator)

    def apply_leave_activator(self):
        self.setWindowTitle("LMS-Apply Leave")
        self.ui.new_user_frame.hide()
        self.ui.login_frame.hide()
        self.ui.view_frame.hide()
        self.ui.view_status_frame.hide()
        self.ui.approve_leave_frame.hide()
        self.ui.apply_leave_frame.show()
        def fill_info():
            cur.execute(
                "SELECT EMP_DATA.PER_ID, EMP_DATA.REP_PER_ID, EMP_DATA.DESIGNATION, EMP_DATA.FREE_LEAVES, EMP_DATA.F_NAME, EMP_DATA.L_NAME FROM EMP_DATA WHERE EMP_DATA.USER = %s;",
                (urname))
            result = cur.fetchone()
            global per_id
            per_id = result[0]
            rep_per_id = result[1]
            global desig
            desig = result[2]
            free_leave = result[3]
            f_name = result[4]
            l_name = result[5]
            wl_text = "Welcome " + f_name + " " + l_name + "!"
            self.ui.ur_name_lab_al_5.setText(urname)
            self.ui.per_id_lab_al_5.setText(per_id)
            self.ui.reporting_id_lab_al_5.setText(rep_per_id)
            self.ui.desig_lab_al_5.setText(desig)
            self.ui.free_leaves_lab_al_5.setText(str(free_leave))
            self.ui.wl_name_al_5.setText(wl_text)
            cur.execute(
                "SELECT DEPT_DATA.DEPT_ID, DEPT_DATA.DEPT_NAME FROM DEPT_DATA, EMP_DATA WHERE EMP_DATA.PER_ID = %s AND DEPT_DATA.PER_ID = EMP_DATA.PER_ID;",
                (per_id))
            result1 = cur.fetchone()
            dept_id = result1[0]
            dept_name = result1[1]
            self.ui.dept_id_lab_al_5.setText(str(dept_id))
            self.ui.dept_lab_al_5.setText(dept_name)
            if desig == "Student":
                self.ui.rep_per_id_al_5.setEnabled(False)
                self.ui.label_90.setEnabled(False)
                self.ui.rep_per_id_al_5.setText("--")
            else:
                self.ui.rep_per_id_al_5.setEnabled(True)
                self.ui.label_90.setEnabled(True)
        def clear():
            self.ui.start_date_al_5.clear()
            self.ui.end_date_al_5.clear()
            self.ui.leave_reason_5.clear()
            self.ui.rep_per_id_al_5.clear()
            self.ui.pri_select_5.setCurrentIndex(0)
        def show_status():
            self.ui.start_date_al_5.setStatusTip("Enter the start date of your leave.")
            self.ui.end_date_al_5.setStatusTip("Enter the end date of your leave.")
            self.ui.leave_reason_5.setStatusTip("Enter the reason of your leave. (not more than 200 characters!)")
            self.ui.rep_per_id_al_5.setStatusTip("Enter the PER_ID of the replacement peron for the day!")
            self.ui.pri_select_5.setStatusTip("Enter the priority of your leave, choose wisely!")
        global leaveid
        leaveid = random.randint(1, 99)
        def savedata():

            startdate_ori = self.ui.start_date_al_5.date()
            enddate_ori = self.ui.end_date_al_5.date()
            startdate = startdate_ori.toPyDate()
            enddate = enddate_ori.toPyDate()
            lp_temp = self.ui.pri_select_5.currentIndex()
            global leavepriority
            if  lp_temp == 0:
                leavepriority = '1'
            elif lp_temp == 1:
                leavepriority = '2'
            elif lp_temp == 2:
                leavepriority = '3'
            elif lp_temp == 3:
                leavepriority = '4'
            leavereason = self.ui.leave_reason_5.text()
            rep_per = self.ui.rep_per_id_al_5.text()
            req_date = startdate
            days1 = enddate-startdate
            totaldays = days1.days
            status = "NOT APPROVED"
            rejec_reason = "--"

            if not startdate_ori:
                self.setStatusTip("Please check your input!")
                return
            elif not enddate_ori:
                self.setStatusTip("Please check your input!")
                return
            elif not lp_temp:
                self.setStatusTip("Please check your input!")
                return
            elif not leavereason:
                self.setStatusTip("Please check your input!")
                return
            elif not rep_per:
                self.setStatusTip("Please check your input!")
                return
            elif totaldays < 1:
                self.setStatusTip("Please check your date input!")
                return
            else:
                cur.execute("INSERT INTO LEAVE_REQUEST VALUES(%s, %s, %s, %s);", (str(leaveid), rep_per, per_id, req_date))
                cur.execute("INSERT INTO LEAVE_INFO VALUES(%s, %s, %s, %s, %s, %s, %s, %s);", (str(leaveid), str(totaldays), leavereason, str(leavepriority), startdate, enddate, status, rejec_reason))

        def save_info():
            choice = QMessageBox.question(self, 'Quit?',
                                            "Are you sure you want to apply for leave? Leave ID:"+str(leaveid),
                                            QMessageBox.Yes | QMessageBox.No)

            if choice == QMessageBox.Yes:
                savedata()
                self.setStatusTip("Leave Applied!")
                db.commit()
                self.ui.apply_leave_frame.hide()
                clear()
                self.ui.view_frame.show()
                self.view_activator()
            else:
                pass
        fill_info()
        show_status()
        self.ui.clear_bt_al_5.clicked.connect(clear)
        self.ui.clear_bt_al_5.setStatusTip("Clear the enter information?")
        global inc
        inc = 0
        if inc < 1:
            self.ui.save_bt_al_5.clicked.connect(save_info)
            self.ui.save_bt_al_5.setStatusTip("Save the information?")
            inc = +1
        inc = 0
        self.ui.return_bt_al_5.clicked.connect(self.view_activator)
        self.ui.return_bt_al_5.setStatusTip("Return to Dashboard without applying for leave?")

    def view_status_activator(self):
        self.setWindowTitle("LMS-View Status")
        self.ui.new_user_frame.hide()
        self.ui.login_frame.hide()
        self.ui.view_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.ui.approve_leave_frame.hide()
        self.ui.view_status_frame.show()

        def fill_info():
            cur.execute(
                "SELECT EMP_DATA.PER_ID, EMP_DATA.REP_PER_ID, EMP_DATA.DESIGNATION, EMP_DATA.FREE_LEAVES, EMP_DATA.F_NAME, EMP_DATA.L_NAME FROM EMP_DATA WHERE EMP_DATA.USER = %s;",
                (urname))
            result = cur.fetchone()
            global per_id
            per_id = result[0]
            rep_per_id = result[1]
            global desig
            desig = result[2]
            free_leave = result[3]
            f_name = result[4]
            l_name = result[5]
            wl_text = "Welcome " + f_name + " " + l_name + "!"
            self.ui.ur_name_lab_vs.setText(urname)
            self.ui.per_id_lab_vs.setText(per_id)
            self.ui.reporting_id_lab_vs.setText(rep_per_id)
            self.ui.desig_lab_vs.setText(desig)
            self.ui.free_leaves_lab_vs.setText(str(free_leave))
            self.ui.wl_name_vs.setText(wl_text)
            cur.execute(
                "SELECT DEPT_DATA.DEPT_ID, DEPT_DATA.DEPT_NAME FROM DEPT_DATA, EMP_DATA WHERE EMP_DATA.PER_ID = %s AND DEPT_DATA.PER_ID = EMP_DATA.PER_ID;",
                (per_id))
            result1 = cur.fetchone()
            dept_id = result1[0]
            dept_name = result1[1]
            self.ui.dept_id_lab_vs.setText(str(dept_id))
            self.ui.dept_lab_al_5.setText(dept_name)

        def load_data():
            cur.execute(
                "SELECT LEAVE_INFO.LEAVE_ID, LEAVE_INFO.START_DATE, LEAVE_INFO.STATUS, LEAVE_INFO.REJECT_REASON FROM LEAVE_INFO, LEAVE_REQUEST WHERE LEAVE_REQUEST.PER_ID = %s AND LEAVE_REQUEST.LEAVE_ID = LEAVE_INFO.LEAVE_ID;", (per_id))
            result = cur.fetchall()
            self.ui.vs_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.ui.vs_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.vs_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        fill_info()
        load_data()
        self.ui.return_bt.clicked.connect(self.view_activator)
        self.ui.return_bt_al_5.setStatusTip("Return to Dashboard?")
        self.ui.refresh_bt.clicked.connect(load_data)
        self.ui.refresh_bt.setStatusTip("Refresh the information?")

    def approve_leave_activator(self):
        self.setWindowTitle("LMS-Approve Leave")
        self.ui.login_frame.hide()
        self.ui.view_frame.hide()
        self.ui.apply_leave_frame.hide()
        self.ui.view_status_frame.hide()
        self.ui.new_user_frame.hide()
        self.ui.approve_leave_frame.show()

        def fill_info():
            cur.execute("SELECT EMP_DATA.PER_ID, EMP_DATA.F_NAME, EMP_DATA.L_NAME FROM EMP_DATA WHERE EMP_DATA.USER = %s;",(urname))
            result = cur.fetchone()
            global per_id
            per_id = result[0]
            f_name = result[1]
            l_name = result[2]
            wl_text = "Welcome " + f_name + " " + l_name + "!"
            self.ui.wl_name_approve_name_3.setText(wl_text)
            cur.execute("SELECT DEPT_DATA.DEPT_NAME FROM DEPT_DATA, EMP_DATA WHERE EMP_DATA.PER_ID = %s AND DEPT_DATA.PER_ID = EMP_DATA.PER_ID;", (per_id))
            result1 = cur.fetchone()
            global dept_name
            dept_name = result1[0]

            cur.execute(
                "SELECT LEAVE_INFO.STATUS, DEPT_DATA.DEPT_NAME, EMP_DATA.F_NAME, EMP_DATA.PER_ID, LEAVE_REQUEST.LEAVE_ID, LEAVE_INFO.START_DATE, LEAVE_INFO.END_DATE, LEAVE_INFO.TOTAL_DAYS, LEAVE_INFO.LEAVE_PRI, LEAVE_INFO.LEAVE_REASON, LEAVE_INFO.REJECT_REASON, LEAVE_REQUEST.REP_EMP_ID FROM DEPT_DATA, EMP_DATA, LEAVE_REQUEST, LEAVE_INFO WHERE DEPT_DATA.DEPT_NAME = %s AND DEPT_DATA.PER_ID =  EMP_DATA.PER_ID AND EMP_DATA.PER_ID = LEAVE_REQUEST.PER_ID AND LEAVE_REQUEST.LEAVE_ID = LEAVE_INFO.LEAVE_ID;", (dept_name))
            result_leaves = cur.fetchall()
            self.ui.approve_table.setRowCount(0)

            for row_number, row_data in enumerate(result_leaves):
                self.ui.approve_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if column_number == 0:
                        if str(data) == 'APPROVED':
                            self.ui.approve_table.setItem(row_number, column_number, QTableWidgetItem("APPROVED"))
                        else:
                            self.ui.approve_table.setItem(row_number, column_number, QTableWidgetItem("NOT APPROVED"))
                    else:
                        pass
                    self.ui.approve_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        def savedata():
            stat = [self.ui.approve_table.item(row, 0).text() for row in range(self.ui.approve_table.rowCount())]
            reason = [self.ui.approve_table.item(row, 10).text() for row in range(self.ui.approve_table.rowCount())]
            leave_id = [self.ui.approve_table.item(row, 4).text() for row in range(self.ui.approve_table.rowCount())]
            for i in range(len(stat)):
                cur.execute("UPDATE LEAVE_INFO SET LEAVE_INFO.STATUS = %s, LEAVE_INFO.REJECT_REASON = %s WHERE LEAVE_INFO.LEAVE_ID = %s;",(stat[i], reason[i], leave_id[i]))

        def save_info():
            choice = QMessageBox.question(self, 'Quit?',
                                            "Are you sure you want to make the following changes?",
                                            QMessageBox.Yes | QMessageBox.No)

            if choice == QMessageBox.Yes:
                savedata()
                self.setStatusTip("Changes Saved Successfully")
                db.commit()
                self.ui.approve_leave_frame.hide()
                self.ui.view_frame.show()
                self.view_activator()
            else:
                pass

        fill_info()
        self.ui.return_bt_approve_3.clicked.connect(self.view_activator)
        self.ui.return_bt_approve_3.setStatusTip("Return to Dashboard without making any changes?")
        self.ui.save_bt_approve_3.clicked.connect(save_info)
        self.ui.save_bt_approve_3.setStatusTip("Save these changes?")

    def menu(self):
        def call_quit():
            choice = QMessageBox.question(self, 'Quit?',
                                          "Are you sure you want to exit?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                db.close()
                sys.exit()
            else:
                pass

        def call_login():
            choice1 = QMessageBox.question(self, 'Quit?',
                                           "Are you sure you want to leave this page?",
                                           QMessageBox.Yes | QMessageBox.No)
            if choice1 == QMessageBox.Yes:
                self.login_activator()
                self.ui.u_name.clear()
                self.ui.pwd.clear()
            else:
                pass

        def call_about():
            Popen(["python", "LMS_ABOUT_CONTROLLER.py"])

        global con_status
        mainmenu = self.menuBar()
        lg_pg_menu = mainmenu.addMenu('  Login Page  ')
        about_menu = mainmenu.addMenu('  About  ')
        quit_menu = mainmenu.addMenu('  Quit  ')
        con_status = mainmenu.addMenu("", )

        exit_bt = QAction('Exit', self)
        exit_bt.setShortcut('Ctrl+Q')
        exit_bt.setStatusTip('Exit application')
        exit_bt.triggered.connect(call_quit)
        quit_menu.addAction(exit_bt)

        lg_bt = QAction('Login Page', self)
        lg_bt.setShortcut('Ctrl+L')
        lg_bt.setStatusTip('Login Page')
        lg_bt.triggered.connect(call_login)
        lg_pg_menu.addAction(lg_bt)

        ab_bt = QAction('About Page', self)
        ab_bt.setShortcut('Ctrl+I')
        ab_bt.setStatusTip('About Page')
        ab_bt.triggered.connect(call_about)
        about_menu.addAction(ab_bt)

        con_bt = QAction('Reconnect', self)
        con_bt.setShortcut('Ctrl+R')
        con_bt.setStatusTip('Reconnect')
        con_bt.triggered.connect(self.connect_to_db)
        con_status.addAction(con_bt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    instance = Window()
    sys.exit(app.exec_())