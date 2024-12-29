 
import tkinter as tk
from tkinter import messagebox
import random
import time
import twilio 
from twilio.rest import Client

# Global variables for OTP and expiry time
otp_generated = None
otp_expiry_time = None

# Twilio credentials
account_sid = 'AC49babd6c3b86ba72ecb4a89a4d4f2c44'
auth_token = '5ca9c853410f81c87cf6ec15ec05a3f7'
twilio_phone_number = '+1 218 520 9744'

def generate_otp():
    global otp_generated, otp_expiry_time
    otp_generated = random.randint(100000, 999999)
    otp_expiry_time = time.time() + 120  # Set expiry for 2 minutes

# Function to send OTP via SMS
def send_otp():
    global otp_generated
    generate_otp()
    client = Client(account_sid, auth_token)
    
    # Replace with the user's phone number
    user_phone_number = entry_phone.get()
    try:
        message = client.messages.create(
            body=f"Your OTP is: {otp_generated}",
            from_=twilio_phone_number,
            to=user_phone_number
        )
        messagebox.showinfo("OTP Sent", f"OTP sent to {user_phone_number}.")
        print(f"Sent message: {message.sid}")  # For debugging purposes
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

# Function to verify the OTP entered by the user
def verify_otp():
    global otp_generated, otp_expiry_time
    user_input = entry_otp.get()
    
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter the OTP.")
        return
    
    try:
        user_input = int(user_input)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric OTP.")
        return
    
    if time.time() > otp_expiry_time:
        messagebox.showerror("Expired OTP", "The OTP has expired.")
        return
    
    if user_input == otp_generated:
        messagebox.showinfo("Success", "OTP Verified Successfully!")
    else:
        messagebox.showerror("Verification Failed", "Incorrect OTP. Please try again.")

root = tk.Tk()
root.title("OTP Verification System")
root.geometry("400x300")

# Create and place widgets
label_phone = tk.Label(root, text="Enter your phone number:")
label_phone.pack(pady=10)

entry_phone = tk.Entry(root)
entry_phone.pack(pady=10)

button_send = tk.Button(root, text="Send OTP", command=send_otp)
button_send.pack(pady=5)

label_otp = tk.Label(root, text="Enter the OTP:")
label_otp.pack(pady=10)

entry_otp = tk.Entry(root)
entry_otp.pack(pady=10)

button_verify = tk.Button(root, text="Verify OTP", command=verify_otp)
button_verify.pack(pady=5)


root.mainloop()