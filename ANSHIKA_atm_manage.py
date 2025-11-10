import mysql.connector

# ===============================================================
#                      DATABASE CONNECTION
# ===============================================================

# Connect to MySQL (without selecting a database yet)
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ansh_123'
)
mycursor = mydb.cursor()


# ===============================================================
#                     DATABASE & TABLE CREATION
# ===============================================================

# Create database if it doesn't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS atm_machine")
mycursor.execute("USE atm_machine")

# Create table if it doesn't exist
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


# ===============================================================
#                      RECONNECT TO DATABASE
# ===============================================================

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ansh_123',
    database='atm_machine'
)
cursor = conn.cursor()


# ===============================================================
#                          ATM MENU
# ===============================================================

print("=" * 80)
print("                             Welcome to the ATM                        ")
print("=" * 80)
print("                            HERE IS THE ATM MENU                       ")
print("1. Create an Account")
print("2. Login")
print("3. Exit")
print("=" * 80)

choice = int(input("ENTER YOUR CHOICE (1/2/3): "))
print("=" * 80)


# ===============================================================
#                    ACCOUNT CREATION SECTION
# ===============================================================

if choice == 1:
    while True:
        a_num = int(input("Enter a 4-digit number as your account ID: "))
        cursor.execute(f"SELECT * FROM ATM_records WHERE ACCOUNT_ID = {a_num}")
        data = cursor.fetchall()

        if len(data) == 1:
            print("=" * 80)
            print("The account number you are trying to create already exists.")
            cont = input("Do you want to try another? (yes/no): ").lower()

            if cont == "no":
                break
        else:
            name = input("Enter your name: ")
            password = int(input("Enter a 4-digit password: "))

            cursor.execute(
                "INSERT INTO ATM_records (ACCOUNT_ID, PASSWORD, USER_NAME) VALUES (%s, %s, %s)", 
                (a_num, password, name)
            )
            conn.commit()

            print("=" * 80)
            print("ACCOUNT SUCCESSFULLY CREATED!!")
            print("The MINIMUM BALANCE IS 1000")
            print("=" * 80)

            # ---------------------- DEPOSIT SECTION ----------------------

            deposit = int(input("Enter the money to be deposited: "))
            cursor.execute("UPDATE ATM_records SET CR_AMT = %s WHERE ACCOUNT_ID = %s", (deposit, a_num))
            cursor.execute("UPDATE ATM_records SET BALANCE = CR_AMT - WITHDRAWAL WHERE ACCOUNT_ID = %s", (a_num,))
            conn.commit()

            print("SUCCESSFULLY DEPOSITED!!")
            print("Thank you. Please close this file before exiting.")
            break




# ===============================================================
#                        LOGIN SECTION
# ===============================================================

elif choice == 2:
    while True:
        acct = int(input("ENTER YOUR ACCOUNT ID: "))
        cursor.execute(f"SELECT * FROM ATM_records WHERE ACCOUNT_ID = {acct}")
        data = cursor.fetchall()

        if len(data) == 1:
            pas = int(input("Enter your password: "))
            cursor.execute(f"SELECT PASSWORD FROM ATM_records WHERE ACCOUNT_ID = {acct}")
            acc_info = cursor.fetchone()

            if pas == acc_info[0]:
                print("Successfully logged in!")
                print("=" * 80)
                print("    THESE CAN BE YOUR NEXT STEPS  ")
                print("1. Deposit money")
                print("2. Withdraw money")
                print("3. Transfer money")
                print("4. Check balance")
                print("=" * 80)

                action = int(input("Enter your choice: "))


                # =======================================================
                #                      DEPOSIT SECTION
                # =======================================================

                if action == 1:
                    dep_amt = int(input("Enter the amount to deposit: "))
                    cursor.execute("UPDATE ATM_records SET CR_AMT = CR_AMT + %s WHERE ACCOUNT_ID = %s", (dep_amt, acct))
                    cursor.execute("UPDATE ATM_records SET BALANCE = CR_AMT - WITHDRAWAL WHERE ACCOUNT_ID = %s", (acct,))
                    conn.commit()
                    print("Successfully Deposited!!")


                # =======================================================
                #                     WITHDRAWAL SECTION
                # =======================================================

                elif action == 2:
                    with_amt = int(input("Enter the amount to withdraw: "))
                    cursor.execute("SELECT BALANCE FROM ATM_records WHERE ACCOUNT_ID = %s", (acct,))
                    balance = cursor.fetchone()[0]

                    if with_amt > balance:
                        print(f"You have insufficient funds (Available: {balance}).")
                    else:
                        cursor.execute("UPDATE ATM_records SET WITHDRAWAL = WITHDRAWAL + %s WHERE ACCOUNT_ID = %s",
                                       (with_amt, acct))
                        cursor.execute("UPDATE ATM_records SET BALANCE = BALANCE - %s WHERE ACCOUNT_ID = %s",
                                       (with_amt, acct))
                        conn.commit()
                        print("Please collect your cash.")


                # =======================================================
                #                      TRANSFER SECTION
                # =======================================================

                elif action == 3:
                    t_acct = int(input("Enter the recipient ACCOUNT_ID: "))
                    cursor.execute("SELECT * FROM ATM_records WHERE ACCOUNT_ID = %s", (t_acct,))
                    target_data = cursor.fetchall()

                    if len(target_data) == 1:
                        transfer_amt = int(input("Enter the amount to transfer: "))
                        cursor.execute("SELECT BALANCE FROM ATM_records WHERE ACCOUNT_ID = %s", (acct,))
                        balance = cursor.fetchone()[0]

                        if transfer_amt > balance:
                            print("Insufficient funds for transfer.")
                        else:
                            cursor.execute("UPDATE ATM_records SET BALANCE = BALANCE - %s WHERE ACCOUNT_ID = %s",
                                           (transfer_amt, acct))
                            cursor.execute("UPDATE ATM_records SET BALANCE = BALANCE + %s WHERE ACCOUNT_ID = %s",
                                           (transfer_amt, t_acct))
                            conn.commit()
                            print("Transfer successful!")
                    else:
                        print("Recipient account does not exist.")


                # =======================================================
                #                      BALANCE SECTION
                # =======================================================

                elif action == 4:
                    cursor.execute("SELECT BALANCE FROM ATM_records WHERE ACCOUNT_ID = %s", (acct,))
                    balance = cursor.fetchone()[0]
                    print(f"Your current balance is: {balance}")

                cont = input("Do you want to perform another operation? (yes/no): ").lower()
                if cont == "no":
                    break
            else:
                print("Wrong password.")
                cont = input("Try again? (yes/no): ").lower()
                if cont == "no":
                    break
        else:
            print("Account not found.")
            cont = input("Try again? (yes/no): ").lower()
            if cont == "no":
                break


# ===============================================================
#                          EXIT SECTION
# ===============================================================

elif choice == 3:
    print("Exiting...")
    print("Thank you for using our ATM service.")

else:
    print("Invalid choice. Please try again.")

cursor.close()
conn.close()




































