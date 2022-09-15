from datetime import datetime
import traceback
import paramiko
import requests
from config.conf import Config


conf_cls = Config()
config = conf_cls()


def exec_cmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    return result


def split_result(result):
    lines = result.decode("utf-8").split('\n')
    result = []
    for line in lines[1:]:
        info = line.split('\t')
        if len(info) > 3:
            tmp = {
                "Used": info[0],
                "avail": info[1],
                "use_percent": info[2],
                "mounted": info[3],
            }
            result.append(tmp)
    return result


def get_server_storage_info(server):
    ip = server["ip"]
    port = server["port"]
    user = server["user"]
    passord = server["pass"]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, passord, timeout=10)

    if (server["name"] in ["emulator", "physical"]):
        cmd = "adb devices"
        result = exec_cmd(ssh, cmd)
        devices = result.decode("utf-8").split('\n')
        device_result_json = {}
        for device in devices[1:]:
            device_id = device.split('\t')[0]
            if (device_id):
                cmd = "adb -s " + device_id + " shell df -h | awk '{i = 4; for (--i; i >= 0; i--){ printf \"%s\t\",$(NF-i)} print \"\"}'"
                result = exec_cmd(ssh, cmd)
                device_result_json[device_id] = split_result(result)

        cmd = "df -h | awk '{i = 4; for (--i; i >= 0; i--){ printf \"%s\t\",$(NF-i)} print \"\"}'"
        result = exec_cmd(ssh, cmd)
        device_result_json["server"] = split_result(result)
        return device_result_json
    else:
        cmd = " df -h | awk '{i = 4; for (--i; i >= 0; i--){ printf \"%s\t\",$(NF-i)} print \"\"}'"
        result = exec_cmd(ssh, cmd)
        return split_result(result)


def get_servers_info():
    res = requests.get("http://127.0.0.1:3005/api/get_servers_list")
    servers = res.json()['servers']
    servers["backend"] = [{"ip": "10.71.1.1"}]
    for server_name, server_info in (servers).items():
        if not server_name in ["physical"]:
            for item in server_info:
                tmp_json = {
                    "ip": item['ip'],
                    "port": 22,
                    "user": "root",
                    "pass": "deneme12",
                    "name": server_name
                }
                tmp_name = "android_" + item['ip'] if server_name == "physical" and item['is_mac'] == 0 else ("mac_" + item['ip'] if server_name == "physical" and item['is_mac'] == 0 else server_name + '_' + item['ip'])

                try:
                    config["file_config"][tmp_name] = get_server_storage_info(tmp_json)
                except Exception as e:
                    traceback.print_exc()
    config["file_config"]["update_time"] = datetime.now().strftime('%H:%M %d-%m-%Y')
    conf_cls.print_json_file(config["file_config"])


if __name__ == '__main__':
    get_servers_info()
