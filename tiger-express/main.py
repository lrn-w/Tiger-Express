from easygui import *
from barcode import barcode_reader
from tmessage import TEMessage
import time 
import MySQLdb

SMS_Notifications = True
tMessage = TEMessage(SMS_Notifications)
processlog = open('/home/pi/tiger-express/logs/PackageLog.txt', 'a')
pickuplog = open('/home/pi/tiger-express/logs/PickupLog.txt', 'a')
db = MySQLdb.connect("localhost", "pi", "raspberry", "tigerexp")
curs = db.cursor()

def empLogin():
	# prompt user login
	e_login = True
	while e_login:
		lmsg = "Enter Employee Id: "
		ltitle = "Employee Login"
		e_id = enterbox(lmsg,ltitle)
		# search employee id in database		
			   
		sql = "SELECT employeeid from EmployeeInf WHERE employeeid = %s" % (e_id)	
		curs.execute(sql)
		rw_count = curs.rowcount	
		
		# check if employee id exists
		if rw_count == 0:
			msgbox("Error! Employee ID not found.")
		
		#if exists go to start menu
		else:		
			strtmenu(e_id)
			e_login = False

def strtmenu(e_id):
	choice  = True
	while choice:				
		# prompt user for options		
		msg = "Select an option below to continue: "
		title = "Tiger Express Start Menu"
		choices = ["Process Package", "Package Pickup","Search Status" ,"Update Status", "Return Package"]
		choice = choicebox(msg,title,choices)
		
		# if option is process package
		if choice == "Process Package":
			processPackage(e_id)
		elif choice == "Package Pickup":
			packagePickup(e_id)
		elif choice == "Search Status":
			searchStatus()
		elif choice == "Update Status":
			updateStatus(e_id)
		elif choice == "Return Package":
			returnPackage(e_id)	
			
def processPackage(e_id):	
	response = False	
	while response == False:				
		# enter box information
		mboxnum = enterbox("Enter box number: ", "Process Package")
		msgbox("Scan barcode in terminal below: ")
		mtracking = barcode_reader()
		# display current entered values
		rmess = "Are the recorded items correct? " + "\nBox Number: " + mboxnum + "\nTracking Number: " + mtracking + "\nStatus: Processed" + "\nProcess Date: " + time.strftime("%m/%d/%Y") +"\nEmployee Id: " + e_id
		response = boolbox(rmess, "Package Confirmation", choices = ('[Y]es', '[N]o'), image=None, default_choice = 'Yes', cancel_choice= 'No')
		
	try:
		curDate = time.strftime('%Y-%m-%d %H:%M:%S')
		sql = "INSERT INTO PackageInf VALUES('%s', '%s', 'Processed', '%s', NULL, NULL, '%s')" % (mboxnum, mtracking, curDate, e_id)
		curs.execute(sql)
		db.commit()
	except:
		print("PackageInf: DB commit error, transaction being rolled back")
		db.rollback()
		exit
	# retrieve employee name
	sql = "SELECT name from EmployeeInf WHERE employeeid = '%s'" % (e_id)
	curs.execute(sql)
	result = curs.fetchone()
	# send notification
	tMessage.sendMessage("Package Processed", "Your package containing the tracking number: " + mtracking + " has been processed. The package was processed by: " + result[0] + ".")
	
	# write log
	print("-------------------------------------")
	print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Processed Package")
	processlog.write("\n-------------------------------------\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Processed")
	processlog.write("\n" + "Box Number: " + str(mboxnum) + " Tracking Number: " + str(mtracking) + " By Employee ID: " + str(e_id))
	
def packagePickup(e_id):	
	response = True
	while response:		
		# scan package by tracking num
		msgbox("Scan barcode in terminal below: ")
		mtracking = barcode_reader()
		try:
			curDate = time.strftime('%Y-%m-%d %H:%M:%S')
			sql = "UPDATE PackageInf SET status = 'Collected', pickup_date = '%s', employeeid = '%s' where tracking_num = '%s'" % (curDate,e_id, mtracking)
			curs.execute(sql)
			db.commit()
		except:
			print("PackageInf: DB commit error, transaction being rolled back")
			db.rollback()
			exit
		# retrieve box num for logging	
		sql = "SELECT box_num FROM PackageInf WHERE tracking_num = '%s'" % (mtracking)
		curs.execute(sql)
		result = curs.fetchone()
		mboxnum = result[0]
		
		# retrieve employee name
		sql = "SELECT name from EmployeeInf WHERE employeeid = '%s'" % (e_id)
		curs.execute(sql)
		result = curs.fetchone()
		# send notification
		tMessage.sendMessage("Package Collected", "Your package containing the tracking number: " + mtracking + " has been collected. The package was processed by: " + result[0] + ".")
		
		# write log
		print("-------------------------------------")
		print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Collected")
		pickuplog.write("\n-------------------------------------\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Collected")
		pickuplog.write("\n" + "Box Number: " + str(mboxnum) + " Tracking Number: " + str(mtracking) + " Employee ID: " + str(e_id))
		
		#prompt user to scan again
		mesg = "Do you wish to scan another package?"
		response = boolbox(mesg, "Package Pickup", choices = ('[Y]es', '[N]o'), image=None, default_choice = 'Yes', cancel_choice= 'No')
def updateStatus(e_id):
	response = True
	while response:		
		# scan package by tracking num
		msgbox("Scan barcode in terminal below: ")
		mtracking = barcode_reader()
		# prompt user to set status
		pstatus = enterbox("Enter status update: ", "Status Update")	
		try:
			curDate = time.strftime('%Y-%m-%d %H:%M:%S')
			sql = "UPDATE PackageInf SET status = '%s', pickup_date = '%s', employeeid = '%s' where tracking_num = '%s'" % (pstatus, curDate, e_id, mtracking)
			curs.execute(sql)
			db.commit()
		except:
			print("PackageInf: DB commit error, transaction being rolled back")
			db.rollback()
			exit
		# retrieve box num for logging	
		sql = "SELECT box_num FROM PackageInf WHERE tracking_num = '%s'" % (mtracking)
		curs.execute(sql)
		result = curs.fetchone()
		mboxnum = result[0]
		
		# write log
		print("-------------------------------------")
		print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Status Updated")
		processlog.write("\n-------------------------------------\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Status Updated")
		processlog.write("\n" + "Box Number: " + str(mboxnum) + " Tracking Number: " + str(mtracking) + " Employee ID: " + str(e_id))
		
		#prompt user to scan again
		mesg = "Do you wish to scan another package?"
		response = boolbox(mesg, "Package Stat Update", choices = ('[Y]es', '[N]o'), image=None, default_choice = 'Yes', cancel_choice= 'No')
	
	
def returnPackage(e_id):
	response = True
	while response:		
		# scan package by tracking num
		msgbox("Scan barcode in terminal below: ")
		mtracking = barcode_reader()
		try:
			curDate = time.strftime('%Y-%m-%d %H:%M:%S')
			sql = "UPDATE PackageInf SET status = 'Returned', return_date = '%s', employeeid = '%s' where tracking_num = '%s'" % (curDate,e_id, mtracking)
			curs.execute(sql)
			db.commit()
		except:
			print("PackageInf: DB commit error, transaction being rolled back")
			db.rollback()
			exit
		# retrieve box num for logging	
		sql = "SELECT box_num FROM PackageInf WHERE tracking_num = '%s'" % (mtracking)
		curs.execute(sql)
		result = curs.fetchone()
		mboxnum = result[0]
		
		# retrieve employee name
		sql = "SELECT name from EmployeeInf WHERE employeeid = '%s'" % (e_id)
		curs.execute(sql)
		result = curs.fetchone()
		# send notification
		tMessage.sendMessage("Package Returned", "Your package containing the tracking number: " + mtracking + " has been returned to sender. The package was processed by: " + result[0] + ".")
		
		# write log
		print("-------------------------------------")
		print(time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Returned")
		processlog.write("\n-------------------------------------\n" + time.strftime("%m/%d/%Y %I:%M:%S %p") + " - Package Returned")
		processlog.write("\n" + "Box Number: " + str(mboxnum) + " Tracking Number: " + str(mtracking) + " Employee ID: " + str(e_id))
		
		#prompt user to scan again
		mesg = "Do you wish to scan another package?"
		response = boolbox(mesg, "Package Return", choices = ('[Y]es', '[N]o'), image=None, default_choice = 'Yes', cancel_choice= 'No')

def searchStatus():
	# imp button for box num srch, or simply entering trking
	# scan package by tracking num
	msgbox("Scan barcode in terminal below: ")
	mtracking = barcode_reader()
	try:
		curDate = time.strftime('%Y-%m-%d %H:%M:%S')
		sql = "SELECT status from PackageInf WHERE tracking_num = '%s'" % (mtracking)
		curs.execute(sql)
		db.commit()
	except:
		print("PackageInf: DB commit error, transaction being rolled back")
		db.rollback()
		exit
	result = curs.fetchone()
	msgbox("The status for tracking number " +mtracking + " is: " + result[0], "Package Status")
	
if __name__ == '__main__':
	empLogin()
