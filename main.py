from crypt import methods
from flask import Flask, jsonify
from flask_cors import CORS
from config.conf import Config
from database import Database, logging


app = Flask(__name__)
CORS(app)

conf_cls = Config()
config = conf_cls()


@app.route('/api/get_servers_info', methods=['GET'])
def get_servers_info():
    global config
    config = conf_cls()
    return jsonify({"res": config['file_config']}), 200


@app.route('/api/get_servers_list', methods=['GET'])
def get_server_list_api():
    servers = get_server_list()
    return jsonify({"servers": servers}), 200


def get_connection_str():
    return {
        "DatabaseConnection": config['env_config']['DB_TYPE'],
        "User": config['env_config']['DB_USER'],
        "Pwd": config['env_config']['DB_PASS'],
        "Server": config['env_config']['DB_HOST'],
        "Port": config['env_config']['DB_PORT'],
        "Database": config['env_config']['DB_NAME']
    }


def _create_db_connection():
    con_str = get_connection_str()
    db = Database(con_str)
    if db.connect_test():
        return db
    else:
        return None


def get_server_list():
    server_list = {}
    # physical servers
    query = "select pds.ip, pds.is_mac from physical_device_servers pds"
    server_list["physical"] = app.db.exec_command(command=query)
    
    # emulator servers
    query = "select ip from dynamic_tools where dynamic_tool_id  > 0"
    server_list["emulator"] = app.db.exec_command(command=query)
    
    # static servers
    query = "select ip from static_tools WHERE static_tool_id  > 0"
    server_list["static"] = app.db.exec_command(command=query)



    # server_list.append({
    #     "ip": "11.17.1.50", "port": 22, "user": "root", "pass": "deneme12", "name": "backend"
    # })
    # server_list.append({
    #     "ip": "172.16.101.36", "port": 22, "user": "ubuntu36", "pass": "deneme12", "name": "emulator"
    # })
    return server_list


if __name__ == "__main__":
    app.db = _create_db_connection()
    if app.db is not None:
        app.run(
            host=config['env_config']['FLASK_HOST'],
            port=config['env_config']['FLASK_PORT']
        )
    else:
        logging.error('Could not connect to database !')
