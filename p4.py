import cv2
import os
import qrcode
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Read the image
img = cv2.imread("LockPic.jpg")

# User inputs for the message and password
msg = input("Enter your message:")
password = input("Enter a password")

# Encrypt the message
encrypted_msg = cipher_suite.encrypt(msg.encode())

# Save the key to a file for later decryption
with open('key.key', 'wb') as key_file:
    key_file.write(key)

# Dictionaries for encoding and decoding
d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

# Encode the encrypted message into the image
m = 0
n = 0
z = 0

for i in range(len(encrypted_msg)):
    img[n, m, z] = encrypted_msg[i]
    n += 1
    m += 1
    z = (z + 1) % 3

# Save the encoded image
cv2.imwrite("EncryptedImage.jpg", img)
os.system("start EncryptedImage.jpg")

# Ask the user if they want to generate a QR code
choice = input("Do you want to generate a QR code for the encrypted message? (yes/no): ").strip().lower()

if choice == "yes":
    # Generate the QR code for the encrypted message
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_msg.decode('utf-8'))
    qr.make(fit=True)

    # Create an image of the QR code
    qr_img = qr.make_image(fill="black", back_color="white")

    # Save the QR code image
    qr_img.save("QRCode.png")
    os.system("start QRCode.png")

# Decrypt the message from the QR code
if choice == "yes":
    scanned_encrypted_msg = input("Enter the scanned encrypted message from QR code: ")

    # Decode the message with a passcode
    pas = input("Enter your passcode for Decryption")
    if password == pas:
        decrypted_msg = cipher_suite.decrypt(scanned_encrypted_msg.encode('utf-8'))
        print("Decryption message:", decrypted_msg.decode('utf-8'))
    else:
        print("Wrong passcode, You aren't authorized")
else:
    # Message decoding from the image
    message = b""
    n = 0
    m = 0
    z = 0

    pas = input("Enter your passcode for Decryption")
    if password == pas:
        for i in range(len(encrypted_msg)):
            message += bytes([img[n, m, z]])
            n += 1
            m += 1
            z = (z + 1) % 3

        # Decrypt the message
        decrypted_msg = cipher_suite.decrypt(message)
        print("Decryption message:", decrypted_msg.decode('utf-8'))
    else:
        print("Wrong passcode, You aren't authorized")
