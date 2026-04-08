import os
from pymongo import MongoClient
import bcrypt
from datetime import datetime
import config

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[config.DB_NAME]
            self.users = self.db[config.DB_USERS_COLLECTION]
            self.chats = self.db[config.DB_CHAT_COLLECTION]
            
            # Create indexes
            self.users.create_index("email", unique=True)
            self.chats.create_index("user_id")
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.db = None
            self.users = None
            self.chats = None

    def is_connected(self):
        return self.db is not None

    def create_user(self, name, email, password, education_level, interests="None"):
        if not self.is_connected():
            return False, "Database not connected"
            
        if self.users.find_one({"email": email}):
            return False, "User with this email already exists"

        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "education_level": education_level,
            "interests": interests,
            "created_at": datetime.utcnow()
        }

        try:
            result = self.users.insert_one(user_data)
            return True, str(result.inserted_id)
        except Exception as e:
            return False, str(e)

    def authenticate_user(self, email, password):
        if not self.is_connected():
            return False, "Database not connected", None

        user = self.users.find_one({"email": email})
        if not user:
            return False, "Invalid email or password", None

        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Remove password from returned user object
            user.pop('password', None)
            user['_id'] = str(user['_id']) # Convert ObjectId to string for session state
            return True, "Authentication successful", user
        
        return False, "Invalid email or password", None
        
    def get_user_by_email(self, email):
        if not self.is_connected():
            return None
        user = self.users.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
            user.pop('password', None)
        return user
        
    def save_chat_message(self, user_id, role, content, session_id="legacy"):
        if not self.is_connected():
            return False
            
        chat_data = {
            "user_id": user_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        try:
            self.chats.insert_one(chat_data)
            return True
        except Exception as e:
            print(f"Error saving chat: {e}")
            return False
            
    def get_chat_history(self, user_id, session_id="legacy", limit=50):
        if not self.is_connected():
            return []
            
        query = {"user_id": user_id}
        if session_id:
            query["session_id"] = session_id
            
        chats = self.chats.find(query).sort("timestamp", 1).limit(limit)
        return [{"role": chat["role"], "content": chat["content"]} for chat in chats]

    def get_chat_sessions(self, user_id):
        """Returns a list of conversation threads for a user."""
        if not self.is_connected():
            return []
            
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$sort": {"timestamp": 1}},
            {"$group": {
                "_id": "$session_id",
                "first_message": {"$first": "$content"},
                "last_timestamp": {"$last": "$timestamp"}
            }},
            {"$sort": {"last_timestamp": -1}}
        ]
        
        try:
            sessions = list(self.chats.aggregate(pipeline))
            return sessions
        except Exception as e:
            print(f"Error fetching chat sessions: {e}")
            return []

    def clear_chat_history(self, user_id):
        if not self.is_connected():
            return False
        try:
            self.chats.delete_many({"user_id": user_id})
            return True
        except Exception as e:
            print(f"Error clearing chat: {e}")
            return False

    def update_user_profile(self, user_id, update_fields):
        if not self.is_connected():
            return False, "Database not connected"
        from bson import ObjectId
        try:
            self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_fields}
            )
            return True, "Profile updated successfully"
        except Exception as e:
            return False, str(e)


# Create a singleton instance
db = Database()
