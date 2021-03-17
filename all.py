"""
Roadmap:
Add more eligibility criteria
Enable data updation
Testing with real hardware
Add support for other biometric traits
Caching by region
Code cleanup
Encrpytion on remote database
-----
Add GUI
"""
import pyrebase
import datetime
#note: random is only to simulate fingerprint scanner inaccuracy
import random
import serverinfo



firebaseConfig = serverinfo.ourServer

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database();

def findAge(born):
    # age = age.split['/']
    #date is in form of dd/mm/yyyy
    #datetime.date takes input in form of yyyy, dd, mm
    born = datetime.datetime.strptime(born, '%d/%m/%Y')
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getFingerprint(param):
    if param == 'load':
        #Temporary operations:
        temp_id = input("Scan your finger please: ")
        users = db.get()
        fingerprints = users.val().keys()
        if temp_id not in fingerprints: #If match was not found
            identity = {'fingerprint_ID': None}
            return identity
        else: #If match is found
            identity = users.val()[temp_id]
            identity['fingerprint_ID'] = temp_id
        # identity = users[users]
        failure = random.randint(1,10) #accuracy is 90%
        if failure == 1:
            identity['fingerprint_ID'] = 'TRY_AGAIN'
        return identity

    elif param == 'store':
        #Temporary operations
        temp_id = input("Scan your finger please: ")
        return temp_id

def push_data(fingerprint_ID, name, id_no, dob, address):
    #create the data object:
    data = {
        "NAME":name,
        "ID":id_no,
        "DOB":dob,
        "ADDRESS":address
    }

    db.child(fingerprint_ID).set(data)

def register():
    while True:
        print("----------")
        print("Registration process:")
        name = input("Enter name: ")
        id_no = input("Enter id number: ")
        dob = input("Enter date of birth in dd/mm/yyyy: ")
        address = input("Enter your address: ")

        fingerprint_ID = getFingerprint('store')

        print("Confirm data:\n")
        print(f"Name: {name}\nID number: {id_no}\nDate of birth: {dob}\nAddresss: {address}")
        ok = input("IS EVERYTHING OK? y/n   ")
        if ok == 'y':
            push_data(fingerprint_ID, name, id_no, dob, address)
        else:
            continue
        again = input("Registration complete. Register another candidate? y/n   ")
        if again == 'y':
            continue
        else:
            break

def validate():
    print("----------")
    print("Validation process")
    #Here, identity is a dict
    while True:
        identity = getFingerprint('load')
        if identity['fingerprint_ID'] == 'TRY_AGAIN':
            print("Oops, finger not registered, please try again")
            continue
        elif identity['fingerprint_ID'] is not None:
            eligible = True
            #Add more validation factors here:
            #age:
            age = findAge(identity['DOB'])
            eligible = eligible and (age >= 18)
            break
        else:
            eligible = 'NA'
            break
    if eligible == True:
        print(f"{identity['NAME']} is eligible for voting!")
    elif eligible == 'NA':
        print("User not registered!")
    else:
        print(f"{identity['NAME']} is ineligible for voting!")



# users = db.get()
# print(users.val().keys())
# print(f"Age for dob 29/07/1999 is {findAge('29/07/1999')}")
print("Welcome to the biometric identification and verification system!")
while True:
    choice = input("Do you want to register/validate/quit? r/v/q:  ")
    if choice == 'r':
        register()
    elif choice == 'v':
        validate()
    else:
        break
# print(db.child('1010').child('ADDRESS').get().val())