# for user authentication (multi user)

import json
import os
import bcrypt  #external package for password verification

USER_DB_PATH = os.path.join(os.path.dirname(__file__), "user_db.json")

def load_users():
    if not os.path.exists(USER_DB_PATH):
        
        return {}
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=2)



def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {"password": hashed_pw}
    save_users(users)
    return True, "Registration successful."



def authenticate_user(username, password):
    users = load_users()


    if username not in users:
        return False
    hashed = users[username]["password"].encode()
    return bcrypt.checkpw(password.encode(), hashed)
