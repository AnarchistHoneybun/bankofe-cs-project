import mysql.connector

'''
BANK OF E : Online Banking Platform
Copyright: Mehul Arora 2020
Test Admin ID Password:
    sociallyencrypted, mrrobot59
    tyrellwellick, joanna66
'''
db = mysql.connector.connect(host='localhost', username='root', password='mysql12345', database='bankofe')
cursor = db.cursor()
ctr = 0  # Checks if login was successful
last = 1  # Used to calculate last customer/transaction ID


def isKYCDone(cid):
    """Check if a customer has filled their KYC.

    Keyword arguments:
    cid -- customer ID
    """
    cursor.execute(("SELECT kyc_docnum FROM customerdetails WHERE cust_id={}".format(cid)))
    a = cursor.fetchall()
    r = a[0]
    for x in r:
        condition = x
    return condition


def updatedBalance(cid):
    """Returns updated balance after a transaction.

    Keyword arguments:
    cid -- customer ID
    """
    cursor.execute(("SELECT balance FROM customerbalance WHERE cust_id={} ;".format(cid)))
    a = cursor.fetchall()[0]
    for x in a:
        print("Updated Balance :- ", x)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


def transaction(dcust, ccust, amount):
    """Fills details of the transaction in to the TRANSACTIONS table of database BANKOFE

    Keyword arguments:
    dcust -- the customer ID from which the amount has been debited
    dcust -- the customer ID to which the amount has been credited
    amount -- value being transferred in rs.

    Note:
        A "NULL" value means there is a deposit or withdrawal by the customer.
    """
    cursor.execute("SELECT MAX(transac_id) FROM transactions;")
    a = cursor.fetchall()
    a = a[0]
    for x in a:
        last = x
    if last is None:
        transac_id = 111111
    else:
        transac_id = 1 + last
    cursor.execute(("INSERT INTO transactions VALUES ({},{},{},{},NOW());".format(transac_id, dcust, ccust, amount)))
    db.commit()


def moneyDeposit(cid):
    """Function to handle money deposits.

    Keyword arguments:
    cid -- customer ID
    """
    money_deposited = int(input('Amount to be deposited :- '))
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    cursor.execute(("UPDATE customerbalance SET balance = balance + {} WHERE cust_id={};".format(money_deposited, cid)))
    cursor.execute(("UPDATE customerbalance SET last_transaction_time=NOW() WHERE cust_id={};".format(cid)))
    db.commit()
    transaction("NULL", cid, money_deposited)
    updatedBalance(cid)


def moneyWithdraw(cid):
    """Function to handle money withdrawals.

    Keyword arguments:
    cid -- customer ID
    """
    money_withdrawn = int(input('Amount to be withdrawn :- '))
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    cursor.execute(("UPDATE customerbalance SET balance = balance - {} WHERE cust_id={};".format(money_withdrawn, cid)))
    cursor.execute(("UPDATE customerbalance SET last_transaction_time=NOW() WHERE cust_id={};".format(cid)))
    transaction(cid, "NULL", money_withdrawn)
    updatedBalance(cid)


def moneyTransfer(cid):
    """Function to handle money transfers.

    Keyword arguments:
    cid -- customer ID
    """
    money_transferred = int(input('Amount to be transferred :- '))
    depositAcc = int(input("Enter account ID to which money is to be transferred"))
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    cursor.execute(("UPDATE customerbalance SET balance = balance - {} where cust_id={}".format(
        money_transferred, cid)))
    cursor.execute(("UPDATE customerbalance SET balance = balance + {} where cust_id={}".format(
        money_transferred, depositAcc)))
    cursor.execute((
        "UPDATE customerbalance SET last_transaction_time=NOW() WHERE cust_id = {};)".format(
            cid)), multi=True)
    cursor.execute((
        "UPDATE customerbalance SET last_transaction_time=NOW() WHERE cust_id = {};)".format(
            depositAcc)), multi=True)
    db.commit()
    transaction(cid, depositAcc, money_transferred)
    updatedBalance(cid)


def welcome_message():
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('*****  WELCOME TO BANK OF E  *****')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


def deleteAcc():
    """Function to handle account deletion."""
    us = input("Enter your username :- ")
    p = (input("Enter your password :-"))
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    cursor.execute("SELECT * FROM credentials WHERE userid='{}' AND pwd='{}';".format(us, p))
    data_login = cursor.fetchall()
    cursor.execute("DELETE FROM customerdetails WHERE cust_id={};".format(data_login[0][2]))
    cursor.execute("DELETE FROM customerbalance WHERE cust_id={};".format(data_login[0][2]))
    cursor.execute(("DELETE FROM credentials WHERE userid ='{}'".format(us)))
    db.commit()
    print("Account deleted.")


def login():
    """Function to handle customer login.

    Returns:
    data_login -- A list containing matching records from the table CREDENTIALS of database BANKOFE
    """
    while True:
        us = input("Enter your username :- ")
        p = (input("Enter your password :-"))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        cursor.execute(("SELECT * FROM credentials where userid='{}' and pwd='{}';".format(us, p)))
        data_login = cursor.fetchall()
        if len(data_login) != 0:
            globals()['ctr'] = 1
            break
        else:
            print('LOGIN FAILED')
            print("USERNAME OR PASSWORD IS WRONG")
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    return data_login


def userinterface():
    """Interface through which customer interacts with the database"""
    global condition
    cdetails = login()
    if globals()['ctr'] == 1:
        cust_id = cdetails[0][2]
        print("LOGIN SUCCESSFUL")
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        while True:
            print('Press 1 for depositing money')
            print('Press 2 for withdrawing money')
            print('Press 3 for doing kyc')
            print('Press 4 for checking balance')
            print('Press 5 to transfer money to other account')
            print('Press 6 for logging out')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            ch = int(input("Enter your option :- "))
            if ch == 1:
                moneyDeposit(cust_id)
            elif ch == 2:
                moneyWithdraw(cust_id)
            elif ch == 3:
                cond = isKYCDone(cust_id)
                if cond is None:
                    print('For KYC you need to provide either one of the following Government IDs.')
                    print('Press 1 for Aadhar Card')
                    print('Press 2 for Voter ID Card')
                    print('Press 3 for PAN Card')
                    print('Press 4 for Driving License')
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    cho = int(input("Enter your choice :- "))
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    if cho == 1:
                        ad = (input("Aadhar Number :- "))
                        cursor.execute(
                            ("UPDATE customerdetails set kyc_docnum='{}' where cust_id={}".format(ad, cust_id)))
                        db.commit()
                        print("KYC Done")
                    elif cho == 2:
                        vi = (input("Voter Id Number :- "))
                        cursor.execute(
                            ("UPDATE customerdetails SET kyc_docnum='{}'' WHERE cust_id={}".format(vi, cust_id)))
                        db.commit()
                        print("KYC Done")
                    elif cho == 3:
                        pc = (input("Pan Card Number :- "))
                        cursor.execute(
                            ("UPDATE customerdetails SET kyc_docnum='{}' WHERE cust_id={}".format(pc, cust_id)))
                        db.commit()
                        print("KYC Done")
                    elif ch == 4:
                        dl = (input("Driving License Number :- "))
                        cursor.execute(
                            ("UPDATE customerdetails SET kyc_docnum='{}' WHERE cust_id={}".format(dl, cust_id)))
                        db.commit()
                        print("KYC Done")
                    else:
                        print('Wrong Choice')
                else:
                    print('KYC Already Done')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            elif ch == 4:
                q = "SELECT balance FROM customerbalance WHERE cust_id={};".format(cust_id)
                cursor.execute(q)
                a = cursor.fetchall()
                a = a[0]
                for x in a:
                    print("Balance :- ", x)
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            elif ch == 5:
                cond1 = isKYCDone(cust_id)
                if cond1 is None:
                    print()
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    print("IMPORTANT:")
                    print("Update KYC first to make payments.")
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                else:
                    moneyTransfer(cust_id)
            elif ch == 6:
                break
            else:
                print("Wrong Option ")
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


def admininterface():
    while True:
        print('Press 1 for finding customer')
        print('Press 2 for viewing ledger')
        print('Press 3 for viewing transaction table')
        print('Press 4 for locating transaction')
        print('Press 5 to log out')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        ch = int(input("Enter your option :- "))
        if ch == 1:
            checkCust = int(input("Enter Customer ID"))
            cursor.execute(("SELECT * FROM customerdetails WHERE cust_id={};".format(checkCust)))
            res = cursor.fetchall()
            for x in res:
                for i in x:
                    print(i)
                print("\n")
        elif ch == 2:
            cursor.execute("SELECT * FROM customerbalance;")
            print("Customer ID| Balance| Last Transaction Time")
            print(cursor.fetchall())
        elif ch == 3:
            cursor.execute("SELECT * FROM transactions;")
            print("Transaction ID| Deposited to| Credited From| Amount| Transaction Time")
            res = cursor.fetchall()
            for i in res:
                print(i)
        elif ch == 4:
            checkTrnsc = int(input("Enter Transaction ID"))
            cursor.execute(("SELECT * FROM transactions WHERE transac_id={};".format(checkTrnsc)))
            res = cursor.fetchall()
            for x in res:
                for i in x:
                    print(i)
                print("\n")
        elif ch == 5:
            break


while True:
    welcome_message()
    print('Press 1 for Online Banking')
    print('Press 2 for Registering a new bank account')
    print('Press 3 for Deleting your account')
    print('Press 4 for Admin Panel')
    print('Press 5 for Exit')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    choice = int(input("Option :- "))
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    if choice == 1:
        userinterface()
    elif choice == 2:
        cursor.execute("SELECT MAX(cust_id) FROM customerdetails;")
        a = cursor.fetchall()
        a = a[0]
        for x in a:
            last = x
        if last is None:
            custid = 111111
        else:
            custid = 1 + last
        print('Fill these details to register your account ')
        name = input("Enter your name :")
        address = (input("Enter your address :"))
        dob = (input("Enter your date of birth(YYYY/MM/DD) :"))
        gender = int(input("Enter your gender (1 for Male, 2 for Female, 3 for Trans, 4 for Non-Binary) :"))
        phone = input('Enter your 10 digit mobile number:')
        emailid = input("Enter your email-id:")
        occupation = input("Enter your occupation:")
        user = str(custid) + "." + name[0].capitalize()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        kyc = 'false'
        query = "INSERT INTO customerdetails VALUES({},'{}','{}','{}',NULL,{},'{}','{}','{}');".format(custid, name,
                                                                                                       address,
                                                                                                       dob, gender,
                                                                                                       phone,
                                                                                                       emailid,
                                                                                                       occupation)
        cursor.execute(query)
        print("We have registered your details.")
        print("Your username to log in to the bank portal is: ", user)
        print("Now, you should set a password for logging in to the bank portal.")
        print("For your safety, we recommend using a password more than 8 characters long.")
        pwd = input("Enter password:")
        query = "INSERT INTO credentials VALUES('{}','{}',{},0);".format(user, pwd, custid)
        cursor.execute(query)
        cursor.execute(("INSERT INTO customerbalance VALUES ({},0,NULL)".format(custid)))
        print("Your account has been successfully registered. You can use online banking now.")
        db.commit()
    elif choice == 3:
        deleteAcc()
    elif choice == 4:
        # Handle access to the admin interface.
        adetails = login()
        if globals()['ctr'] == 1:
            admin = adetails[0][3]
            if admin == 1:
                print("LOGIN SUCCESSFUL")
                admininterface()
            else:
                print("This account is not authorised to access this page.")
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    elif choice == 5:
        break
    else:
        print('Wrong Option')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
