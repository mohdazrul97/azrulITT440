import socket
import sys
import hashlib
import pyAesCrypt
import re
import datetime
import datetime


def create_user_file():
    fullname = ""
    gender = ""

    fullname = input("Enter your fullname:")
    fullname = fullname.upper()
    if re.search(r'\bBIN\b', fullname):
        name_split = fullname.split("BIN")  # currently for malay user only
    elif re.search(r'\bBIN\b', fullname):
        name_split = fullname.split("BINTI")
    elif re.search(r'\bAL\b', fullname):
        name_split = fullname.split("AL")  # currently for non-malay user only
    elif re.search(r'\bAP\b', fullname):
        name_split = fullname.split("AP")  
   
    print(f"First name: {name_split[0]}")
    print(f"Last name :{name_split[1]}")




    ic = int(input("Enter your ic number: "))
    ic = str(ic)
    gamename = input("Insert Your Game's Name:")
    nadult = int(input("Enter number of adults:"))
    nchild = int(input("Enter number of children:"))
    nsencitizen = int(input("Enter number of senior citizen:"))

    price_nadult = 15
    price_nchild = 10
    price_nsencitizen = 5

    totalp       = (nadult*price_nadult)+(nchild*price_nchild)+(nsencitizen*price_nsencitizen)

    date = input("Enter date to play a game:")

    male_num = ("1", "3", "5", "7", "9")
    if ic.endswith(male_num):
        gender = "Male"
    else:
        gender = "Female"
    print(gender)

    bornyear = ic[0:2]
    bornmonth = ic[2:4]
    bornday = ic[4:6]

    now = datetime.datetime.now()

    print(f"year {bornyear} , month {bornmonth}, day{bornday} ")

    filename = fullname.title() + ".txt"

    month = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November",12:"December"}

    bornmonth = month.get(int(bornmonth)) # get key

    f = open(filename, 'w')
    f.write(f"Customer Details of Scream Park: \n")
    f.write(f"First name: {name_split[0]}\n")
    f.write(f"Last name: {name_split[1]}\n")
    f.write(f"IC Number of customer: {ic}\n")
    f.write(f"Customer's Gender: {gender}\n")
    f.write(f"Age: {now.year - int(bornyear)-1900}\n")
    f.write(f"Customer's Born Year: {int(bornyear) + 1900}\n")
    f.write(f"Customer's Born Month: {bornmonth}\n")
    f.write(f"Customer's Born Day: {bornday}\n")
    f.write(f"\n")
    f.write(f"Theme's Park Ticket Details: \n")
    f.write(f"Game's Name: {gamename}\n")
    f.write(f"No. of Adults: {nadult}\n")
    f.write(f"No. of Children: {nchild}\n")
    f.write(f"No. of Senior Citizen: {nsencitizen}\n")
    f.write(f"Total Price to Pay: RM {totalp}\n")
    f.write(f"Your date to play a game: {date}\n")
    now = datetime.datetime.now()
    f.write(f"Your Date Booked: {now}\n")


def hashmd5(filename):  # hash md5
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read()
    hasher.update(buf)
    print(f"Hash from local : {hasher.hexdigest()}")
    hash_from_server = s.recv(1024).decode()
    print(f"Hash from server: {hash_from_server}")
    if hash_from_server != hasher.hexdigest():
        print("Hash value not same, file may be edited...")
    else:
        print("Hash value same with server")


def decrypt_file(filename):
    bufferSize = 64 * 1024
    password = "password"
    filename_aes = filename.replace(".aes", " ")
    # encrypt
    pyAesCrypt.decryptFile(filename, filename_aes, password, bufferSize)


def encrypt_file(filename):
    # encryption/decryption buffer size - 64K
    bufferSize = 64 * 1024
    password = "password"
    filename_aes = filename + ".aes"
    # encrypt
    pyAesCrypt.encryptFile(filename, filename_aes, password, bufferSize)


def download(file_download):
    f = open(file_download, 'w')
    data = s.recv(1024)
    f.write(data.decode())
    f.close()


def upload(filename):
    filename = filename + ".txt"
    f = open(filename, "r")
    bf = f.read().encode()  # read file content
    s.send(bf)
    print("File uploaded to server...")


def menu():
    print(30 * "X", "AZRUL SCREAM---THEME PARK TICKETING SYSTEM", 30 * "X")
    print("1. To Upload Ticket of Scream Park")
    print("2. To Download Ticket of Scream Park")
    print("3. To Hash Ticketof Scream Park")
    print("4. To Encrypt Ticket of Scream Park")
    print("5. To Decrypt Ticket of Scream Park")
    print("6. To Booking Ticket of Scream Park")
    print("7. Exit")
    print(80 * "X")
    choice = (input("Please Insert Your Details Correctly by press [1-7]:  "))

    while True:

        if(choice == "1"):
            s.send(choice.encode())
            filename = input("Enter filename to be upload: ")
            s.send(filename.encode())
            upload(filename)
        elif(choice == "2"):
            s.send(choice.encode())
            file_download = input("Enter filename to download:  ")
            s.send(file_download.encode())
            download(file_download)
        elif(choice == "3"):
            s.send(choice.encode())
            filename = input("Enter filename to hash with server: ")
            s.send(filename.encode())
            hashmd5(filename)
        elif(choice == "4"):
            filename = input("Enter filename to be encrypt")
            encrypt_file(filename)
            print("File encrypted...")
        elif(choice == "5"):
            filename = input("Enter filename to be decrypt")
            decrypt_file(filename)
            print("File decrypted...")
        elif(choice == "6"):
            create_user_file()
        elif (choice == "7"):
            exit(0)
        else:
            print("Invalid input")
            choice = 0
            menu()
        choice = 0
        menu()


host = str(sys.argv[1])
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    menu()

    # ask the client whether he/she wants to continue
    ans = input('\nDo you want to continue(y/n) :')
    if ans == 'y':
        continue
    else:
        break
# close the connection
s.close()
