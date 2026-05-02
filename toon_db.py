import os
import toon

class ToonDB:
    def __init__(self, filename="data.toon"):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            self.save_data({
                "users": {},
                "quotes": []
            })

    def get_data(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return {"users": {}, "quotes": []}
            try:
                return toon.decode(content)
            except Exception as e:
                print(f"Error decoding TOON: {e}")
                return {"users": {}, "quotes": []}

    def save_data(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            encoded = toon.encode(data)
            f.write(encoded)

    def get_user(self, username):
        data = self.get_data()
        return data["users"].get(username)

    def create_user(self, username, password, is_guest=False):
        data = self.get_data()
        if username in data["users"]:
            return False
        data["users"][username] = {
            "password": password,
            "is_guest": is_guest
        }
        self.save_data(data)
        return True

    def add_quote(self, text, author, added_by, date_str):
        data = self.get_data()
        import uuid
        quote_id = str(uuid.uuid4())
        data["quotes"].append({
            "id": quote_id,
            "text": text,
            "author": author,
            "added_by": added_by,
            "date": date_str,
            "likes": [],
            "comments": []
        })
        self.save_data(data)
        return quote_id

    def get_all_quotes(self):
        data = self.get_data()
        for q in data["quotes"]:
            if "comments" not in q:
                q["comments"] = []
        # Sort by date descending implicitly if we just reverse the list
        return list(reversed(data["quotes"]))

    def toggle_like(self, quote_id, username):
        data = self.get_data()
        for q in data["quotes"]:
            if q["id"] == quote_id:
                if q["added_by"] == username:
                    return "error_self_like", len(q["likes"])
                if username in q["likes"]:
                    q["likes"].remove(username)
                    status = "unliked"
                else:
                    q["likes"].append(username)
                    status = "liked"
                self.save_data(data)
                return status, len(q["likes"])
        return "error", 0

    def add_comment(self, quote_id, text, username, date_str):
        data = self.get_data()
        for q in data["quotes"]:
            if q["id"] == quote_id:
                if "comments" not in q:
                    q["comments"] = []
                import uuid
                comment_id = str(uuid.uuid4())
                q["comments"].append({
                    "id": comment_id,
                    "text": text,
                    "added_by": username,
                    "date": date_str
                })
                self.save_data(data)
                return comment_id
        return None
