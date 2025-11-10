import mysql.connector


mydb = mysql.connector.connect(host='localhost', user='root', password='ansh_123')
mycursor = mydb.cursor()

# Create database 
mycursor.execute("CREATE DATABASE IF NOT EXISTS atm_machine")
mycursor.execute("USE atm_machine")

# Create the ATM_records table 
table = """
CREATE TABLE IF NOT EXISTS ATM_records (
    ACCOUNT_ID INT(4) PRIMARY KEY,
    PASSWORD INT(4),
    USER_NAME VARCHAR(20),
    CR_AMT INT DEFAULT 0,
    WITHDRAWAL INT DEFAULT 0,
    BALANCE INT DEFAULT 0
)
"""
mycursor.execute(table)


conn = mysql.connector.connect(host='localhost', user='root', password='ansh_123', database='atm_machine')
cursor = conn.cursor()

# Display the ATM menu
print("=" * 80)
print("                             Welcome to the ATM                        ")
print("=" * 80)
print("                        HERE IS THE ATM MENU                               ")
print("1. To create an account")
print("2. To login")
print("3. Exit")
print("=" * 80)

choice = int(input("ENTER YOUR CHOICE 1/2/3 :"))
print("=" * 80)

# Account creation logic
if choice == 1:
    user_response = "yes"
    while user_response == "yes":
        a_num = int(input("Enter a 4 digit number as your account id :"))
        
        # Check if account already exists
        select_query = f"SELECT * FROM ATM_records WHERE ACCOUNT_ID={a_num}"
        cursor.execute(select_query)
        data = cursor.fetchall()
        
        if len(data) == 1:
            print("="*80)
            print("The account number you are trying to create already exists.")
            user_response = input("Do you want to continue (yes/no)? ")
            print("="*80)
            if user_response.lower() == "no":
                print("Thank you...Please close this file before exiting.")
                break
        else:
            name = input("Enter your name as user name :")
            password = int(input("Enter your 4-digit password :"))
            
            # Insert new account
            insert_query = f"INSERT INTO ATM_records(ACCOUNT_ID, PASSWORD, USER_NAME) VALUES({a_num}, {password}, '{name}')"
            cursor.execute(insert_query)
            conn.commit()
        
            print("="*80)
            print("ACCOUNT SUCCESSFULLY CREATED!!")
            print("The MINIMUM BALANCE IS 1000")
            print("="*80)

            deposit = int(input("Enter the money to be Deposited: "))
            update_query = f"UPDATE ATM_records SET CR_AMT={deposit} WHERE ACCOUNT_ID={a_num}"
            cursor.execute(update_query)
            conn.commit()

            # Update balance after deposit
            update_balance_query = f"UPDATE ATM_records SET BALANCE = CR_AMT - WITHDRAWAL WHERE ACCOUNT_ID = {a_num}"
            cursor.execute(update_balance_query)
            conn.commit()

            print("SUCCESSFULLY DEPOSITED!!")
            print("Thank you...Please close this file before exiting.")
            break

# Login the account
elif choice == 2:
    user_response2 = "yes"
    while user_response2 == "yes":
        acct = int(input("ENTER YOUR ACCOUNT ID: "))
        account_query = f"SELECT * FROM ATM_records WHERE ACCOUNT_ID = {acct}"
        cursor.execute(account_query)
        data = cursor.fetchall()

        if len(data) == 1:
            pas = int(input("Enter your password :"))
            passw_query = f"SELECT PASSWORD FROM ATM_records WHERE ACCOUNT_ID={acct}"
            cursor.execute(passw_query)
            acc_info = cursor.fetchone()
            
            if pas == acc_info[0]:
                print("Successfully logged in!")
                print("    THESE CAN BE YOUR NEXT STEPS  ")
                print("1. Deposit money")
                print("2. Withdraw money")
                print("3. Transfer money")
                print("4. Check balance")
                print("=" * 80)
                r = int(input("Enter your choice: "))
                print("=" * 80)

                # Deposit logic
                if r == 1:
                    dep_amt = int(input("ENTER THE AMOUNT TO BE DEPOSITED :"))
                    update_credit_query = f"UPDATE ATM_records SET CR_AMT=CR_AMT + {dep_amt} WHERE ACCOUNT_ID={acct}"
                    cursor.execute(update_credit_query)
                    conn.commit()

                    update_balance_query = f"UPDATE ATM_records SET BALANCE = CR_AMT - WITHDRAWAL WHERE ACCOUNT_ID = {acct}"
                    cursor.execute(update_balance_query)
                    conn.commit()
                    print("Successfully Deposited!!")

                # Withdrawal logic
                elif r == 2:
                    with_amt = int(input("ENTER THE AMOUNT TO WITHDRAW: "))
                    balance_query = f"SELECT BALANCE FROM ATM_records WHERE ACCOUNT_ID = {acct}"
                    cursor.execute(balance_query)
                    balance = cursor.fetchone()

                    if with_amt > balance[0]:
                        print(f"You have less amount than {with_amt}. Please try again.")
                    else:
                        up_balance_query = f"UPDATE ATM_records SET BALANCE = BALANCE - {with_amt} WHERE ACCOUNT_ID = {acct}"
                        record_with_query = f"UPDATE ATM_records SET WITHDRAWAL = {with_amt} WHERE ACCOUNT_ID = {acct}"
                        cursor.execute(record_with_query)
                        cursor.execute(up_balance_query)
                        conn.commit()
                        print("Please collect the amount.")

                # Transfer logic
                elif r == 3:
                    t_acct = int(input("ENTER THE ACCOUNT_ID TO WHICH MONEY HAS TO BE TRANSFERRED :"))
                    check_amt_query = f"SELECT * FROM ATM_records WHERE ACCOUNT_ID = {t_acct}"
                    cursor.execute(check_amt_query)
                    acct_data = cursor.fetchall()

                    if len(acct_data) == 1:
                        print(f"Account {t_acct} exists!!")
                        transfer_amt = int(input("ENTER THE MONEY AMOUNT TO TRANSFER: "))
                        check_balance_query = f"SELECT BALANCE FROM ATM_records WHERE ACCOUNT_ID = {acct}"
                        cursor.execute(check_balance_query)
                        balance = cursor.fetchone()

                        if transfer_amt > balance[0]:
                            print(f"You have less amount than {transfer_amt}. Please try again..")
                        else:
                             debit_query = f"UPDATE ATM_records SET BALANCE=BALANCE - {transfer_amt} WHERE ACCOUNT_ID={acct}"  
                             credit_query = f"UPDATE ATM_records SET BALANCE=BALANCE + {transfer_amt} WHERE ACCOUNT_ID={t_acct}"
                             cursor.execute(debit_query)
                             cursor.execute(credit_query)  
                             conn.commit()  
                             print("Successfully transferred!")
                    else:
                        print("Account does not exist.")

                # Check balance
                elif r == 4:  
                    balance_query = f"SELECT BALANCE FROM ATM_records WHERE ACCOUNT_ID={acct}"   
                    cursor.execute(balance_query)  
                    balance = cursor.fetchone()  
                    print(f"Balance in your account: {balance[0]}")  

                continue_choice = input("Do you want to continue (yes/no)? ")  
                if continue_choice.lower() == "no":  
                    print("Thank you. Please close this file before exiting.")  
                    break  
            else:
                print("Wrong password.")  
                continue_choice = input("Do you want to continue (yes/no)? ")  
                if continue_choice.lower() == "no":  
                    break

        else:
            print("Your account does not exist.")  
            continue_choice = input("Do you want to continue (yes/no)? ")  
            if continue_choice.lower() == "no":  
                break

# Exit logic
elif choice == 3:  
    print("Exiting.")  
    print("Please close this file before exiting.")  
    cursor.close()  

