import sqlite3
class Database:
    def __init__(self,db_file):
        self.connection=sqlite3.connect(db_file)
        self.cursor=self.connection.cursor()
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES(?)",(user_id,))


    def user_exists(self,user_id):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY,
               user_id  NOT NULL,
               nickname VARCHAR (60),
               signup VARCHAR DEFAULT setnickname);
            """)
            result=self.cursor.execute("SELECT * FROM `users` WHERE `user_id` =?",(user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self,user_id,nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` =? WHERE `user_id`=?",(nickname,user_id,))

    def change_nickname(self,new_nickname , old_nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `client` =? WHERE `client`=?",(new_nickname,old_nickname,))

    def get_signup(self, user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchall()
            for row in result:
                signup=str(row[0])
            return signup

    def set_signup(self,user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` =? WHERE `user_id`=?",(signup,user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchall()
            for row in result:
                nickname=str(row[0])
            return nickname

    def zapis_meet(self, user_name, chose):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `client` =? WHERE `nickname`=?",(chose, user_name,))

    def get_meet(self, name):
        with self.connection:
            result=self.cursor.execute("SELECT `client` FROM `meet` WHERE `nickname` = ?",(name,)).fetchall()
            for row in result:
                meet=str(row[0])
            return meet

    def update_zapis(self, nickname, null):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `client` =? WHERE `nickname`=?",(null, nickname,))

    def time_zapis(self, name):
        with self.connection:
            result= self.cursor.execute("SELECT `time` FROM `meet` WHERE `nickname`=?",(name,))
            for row in result:
                time = str(row[0])
            return time
    def date_zapis(self, name):
        with self.connection:
            result= self.cursor.execute("SELECT `date` FROM `meet` WHERE `nickname`=?",(name,))
            for row in result:
                date = str(row[0])
            return date

    def zapis_for_registration(self, name):
        with self.connection:
            result=self.cursor.execute("SELECT `zapis` FROM `meet` WHERE `nickname` = ?",(name,)).fetchall()
            for row in result:
                zapis=str(row[0])
            return zapis
