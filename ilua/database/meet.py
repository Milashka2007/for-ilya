import sqlite3

class Database1:
    def __init__(self,db_file):
        self.connection=sqlite3.connect(db_file)
        self.cursor=self.connection.cursor()

    def add_name_meet(self, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `meet` (`nickname`) VALUES(?)",(name,))

    def add_date_meet(self, name, date):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS meet(
                           date VARCHAR (60),
                           time VARCHAR (60),
                           nickname VARCHAR (60),
                           zapis VARCHAR (60),
                           client VARCHAR (60));
                        """)
            return self.cursor.execute("UPDATE `meet` SET `date` =? WHERE `nickname`=?",(date, name,))

    def add_time_meet(self, name, time):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `time` =? WHERE `nickname`=?",(time, name,))

    def rename_meet(self, name, name_new):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `nickname` =? WHERE `nickname`=?",(name_new, name,))

    def delete_meet(self, name):
        with self.connection:
            return self.cursor.execute("DELETE FROM `meet` WHERE `nickname`=?",(name,))

    def name_meet(self):
        with self.connection:
            x=self.cursor.execute("SELECT * FROM `meet`")
            meet=[]
            for meets in x:
                meet.append(meets[4])
                meet.append(meets[2])
                meet.append(meets[1])
                meet.append(meets[0])
            return meet

    def name_meet1(self):
        with self.connection:
            x=self.cursor.execute("SELECT * FROM `meet`")
            meet=[]
            for meets in x:
                meet.append(meets[3])
                meet.append(meets[2])
                meet.append(meets[1])
                meet.append(meets[0])
            return meet

    def meet_exists(self, chose):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `meet` WHERE `nickname` =?", (chose,)).fetchall()
            return bool(len(result))

    def add_zapis_meet(self, status, name):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `zapis` =? WHERE `nickname`=?",(status, name,))

    def add_client_meet(self, status, name):
        with self.connection:
            return self.cursor.execute("UPDATE `meet` SET `client` =? WHERE `nickname`=?",(status, name,))

    def client_exists(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `meet`")
            client=[]
            for clients in result:
                client.append(clients[4])
            return client

    def meet_by_client(self, name):
        with self.connection:
            result= self.cursor.execute("SELECT `nickname` FROM `meet` WHERE `client`=?",(name,))
            for row in result:
                name = str(row[0])
            return name

