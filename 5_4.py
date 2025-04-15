import mysql.connector
import random
import smtplib

# Connect to the MySQL database
db = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='itsar_smart_meter',
    username='root',
    password='242004@Me',
)

# Function to generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to send OTP via email
def send_otp_email(user_id, otp):
    # Set up email details
    sender_email = "mukesheppili17@gmail.com"
    sender_password = "ktcobmjgnemhiudq"
    receiver_email = email  # Replace with the user's email
    subject = 'OTP for Deletion Confirmation'
    message = f'Hello User {user_id},\n\nYour OTP for deletion confirmation is: {otp}.\n\nThank you.'
    email_message = f"Subject: {subject}\nFrom: {sender_email}\nTo: {receiver_email}\n\n{message}"

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, email_message)
        print("OTP sent to your email. Please check your inbox.")

    except smtplib.SMTPException:
        print("Failed to send OTP. Please try again later.")

       

# Function to send confirmation email
def send_confirmation_email(user_id, deletion_status):
    # Set up email details
    sender_email = "mukesheppili17@gmail.com"
    sender_password = "ktcobmjgnemhiudq"
    receiver_email = email  # Replace with the user's email
    subject = 'Deletion Confirmation'
    message = f'Hello User {user_id},\n\nYour {selected} deletion request has been {"successful" if deletion_status else "canceled"}.\n\nThank you.'
    email_message = f"Subject: {subject}\nFrom: {sender_email}\nTo: {receiver_email}\n\n{message}"

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, email_message)
    print("Confirmation Message sent to your email.")


# Function to delete user data
def delete_user_data(user_id,record_id,menu_choice):
    try:

        if menu_choice == 1:
            confirmation = input(f"Are you sure want to delete device: {record_id}?. This Action is Irreversible (yes/no):")
            # Delete records from the services table
            if confirmation.lower() == "yes":
                cursor = db.cursor()
                cursor.execute("DELETE FROM devices WHERE device_id = %s", (record_id,))
                db.commit()
                print("Device data has been successfully deleted.")
                send_confirmation_email(user_id, True)
            else:
                print("Device Data Deletion Cancelled.")
                send_confirmation_email(user_id, False)

        elif menu_choice == 2:
            confirmation = input(f"Are you sure want to delete Service: {record_id}?. This Action is Irreversible (yes/no):")
            if confirmation.lower() == "yes":
                cursor = db.cursor()# Delete records from the devices table
                cursor.execute("DELETE FROM services WHERE device_id = %s", (record_id,))
                db.commit()
                print("Service data has been successfully deleted.")
                send_confirmation_email(user_id, True)
            else:
                print("Service Data Deletion Cancelled.")
                send_confirmation_email(user_id, False)
            
        elif menu_choice == 3:
            confirmation = input(f"Are you sure want to delete Application: {record_id}?. This Action is Irreversible (yes/no):")
            if confirmation.lower() == "yes":
                cursor = db.cursor()# Delete records from the applications table
                cursor.execute("DELETE FROM applications WHERE device_id = %s", (record_id,))
                db.commit()
                print("Application data has been successfully deleted.")
                send_confirmation_email(user_id, True)
            else:
                print("Application Data Deletion Cancelled.")
                send_confirmation_email(user_id, False)
        

        
    except mysql.connector.Error as error:
        print("Error deleting user data: ", error)
        send_confirmation_email(user_id, False)  # Send confirmation email

    finally:
        cursor.close()
        db.close()

def show_user_data(user_id,menu_choice):
    if menu_choice == 1:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM devices where user_id = %s", (user_id,))
        records = cursor.fetchall()

        if len(records) > 0:
            print("Device Records:")
            for record in records:
                print(f"Device ID: {record[0]}, User ID: {record[1]}, Device Name: {record[2]}, Device Type: {record[3]}")
        else:
            print("No Device Records found.")
            return

        record_id = input("Enter the Device ID of the record to be delete:")
        return record_id
    
    elif menu_choice == 2:
        cursor = db.cursor()
            # Delete records from the devices table
        cursor.execute("SELECT * FROM services WHERE user_id = %s", (user_id,))
        records = cursor.fetchall()

        if len(records) > 0:
            print("Service Records:")
            for record in records:
                print(f"Service ID: {record[0]}, User ID: {record[1]}, Service Name: {record[2]}, Start Date: {record[3]}, End Date: {record[4]}")
        else:
            print("No Service Records found.")

        record_id = input("Enter the Service ID of the record to be delete:")
        return record_id
        
    elif menu_choice == 3:
        cursor = db.cursor()
            # Delete records from the applications table
        cursor.execute("SELECT * FROM applications WHERE user_id = %s", (user_id,))
        records = cursor.fetchall()

        if len(records) > 0:
            print("Application Records:")
            for record in records:
                print(f"Application ID: {record[0]}, User ID: {record[1]}, Application Name: {record[2]}")
        else:
            print("No Device Records found.")
        
        record_id = input("Enter the Application ID of the record to be delete:")
        return record_id
    
        

# Function for OTP verification
def verify_otp(user_id):
    otp = generate_otp()
    

    send_otp_email(user_id, otp)  # Send OTP via email

    user_otp = int(input("Enter the OTP: "))

    if user_otp == otp:
        return True
    else:
        print("OTP verification failed.")
        return False

# Function for menu selection
def select_menu():
    print("Select the data you want to delete:")
    print("1. Devices")
    print("2. Services")
    print("3. Applications")

    choice = int(input("Enter your choice (1-3): "))
    return choice
print("-------------------WELCOME TO ITSAR SMART ELECTRIC METER------------------------")
# Prompt the user for the user ID
user_id = int(input("Enter the User ID: "))

# Check if the user exists
cursor = db.cursor()
cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
user_exists = cursor.fetchone()

if user_exists:
    email = user_exists[2]
    if verify_otp(user_id):
        print("OTP Verification Successfull.")
        # Get the menu choice from the user
        menu_choice = select_menu()
        if (menu_choice == 1):
            selected = "Device"
        elif (menu_choice == 2):
            selected = "Service"
        elif (menu_choice == 3):
            selected = "Application"


        if menu_choice >= 1 and menu_choice <=3:
            # Request for device deletion
            record_id = show_user_data(user_id,menu_choice)
            if record_id == "":
                print("Please Try Again with a Different Option from the Menu.")
                print("Terminating......")
            else:
                print(f"{selected} deletion request sent to admin.")

                # Simulate admin approval
                admin_approval = "y"

                if admin_approval.lower() == "y":
                    # Delete user data
                    delete_user_data(user_id, record_id, menu_choice)
                else:
                    print("Admin denied the request.")
                    send_confirmation_email(user_id, False)  # Send confirmation email


        else:
            print("Invalid choice.")

else:
    print("User does not exist.")

cursor.close()
db.close()

print("-------------------------------Thank You!-----------------------------             ")