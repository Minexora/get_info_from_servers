import os
import logging
import traceback
import mysql.connector
import psycopg2

basedir = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(
    filename=os.path.join(basedir, "server.log"),
    format="%(asctime)s - %(levelname)s - %(message)s ",
    level=logging.INFO,
)
logging.getLogger().setLevel(logging.INFO)


class Database:
    config = {}

    def __init__(self, config) -> None:
        self.config = config

    def connect_test(self):
        try:
            if str(self.config['DatabaseConnection']).lower() == 'mysql':
                connect = mysql.connector.connect(
                    host=self.config['Server'],
                    user=self.config['User'],
                    password=self.config['Pwd'],
                    database=self.config['Database']
                )
            elif str(self.config['DatabaseConnection']).lower() == 'postgresql':
                connect = psycopg2.connect(
                    host=self.config['Server'],
                    user=self.config['User'],
                    password=self.config['Pwd'],
                    database=self.config['Database']
                )
            return True
        except Exception as e:
            logging.error("Database Bağlantı Hatası: {0}".format(
                traceback.format_exc()))
            return False

    def mysql(self, command):
        try:
            connect = mysql.connector.connect(
                host=self.config['Server'],
                user=self.config['User'],
                password=self.config['Pwd'],
                database=self.config['Database']
            )
            connect.autocommit = True
            cursor = connect.cursor()
            cursor.execute(command)

            results = list()
            if 'select' in command or 'Select' in command or 'SELECT' in command:
                columns = [column[0] for column in cursor.description]

                for k in cursor.fetchall():
                    results.append(dict(zip(columns, k)))

        except Exception:
            logging.error("Database Command Runner: {0}".format(
                traceback.format_exc()))
            results = None

        return results

    def postgresql(self, command):
        try:
            connect = psycopg2.connect(
                host=self.config['Server'],
                user=self.config['User'],
                password=self.config['Pwd'],
                database=self.config['Database']
            )
            connect.autocommit = True
            cursor = connect.cursor()
            cursor.execute(command)

            results = list()
            if 'select' in command or 'Select' in command or 'SELECT' in command:
                columns = [column[0] for column in cursor.description]

                for k in cursor.fetchall():
                    results.append(dict(zip(columns, k)))

        except Exception:
            logging.error("Database Command Runner: {0}".format(
                traceback.format_exc()))
            results = None

        return results

    def exec_command(self, command):
        logging.warning("command: ", command)
        if str(self.config['DatabaseConnection']).lower() == 'mysql':
            return self.mysql(command=command)
        elif str(self.config['DatabaseConnection']).lower() == 'postgresql':
            return self.postgresql(command=command)
        else:
            logging.error('Database bağlatın yazılımı olmaması nedeniyle database bağlantısı kurulamıyor. Lütfen MySQL  veya MsSQL bağlantısı yapınız.')
