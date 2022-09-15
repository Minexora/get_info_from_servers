# Get Server İnfo 
Server bilgilerini öğrenmek için geliştirilmştir. Apiler ;
-   **/api/get_servers_info** -> server kullanım miktarları json formatında döndürülür

-   **/api/get_servers_list** -> server listesi geri döndürülür.

main.py dosyasında bulunan **get_server_list** adlı method da cihazlarınız için database sorguları yer alamaktdır. Bu sorguları kendize göre değiştirerek kullanabilirsiniz.

## Kurulum işlemleri
Kurulum için bash script aşağıdaki gibidir. 
```bash
echo "exporting Tar file..."
sleep 2
tar xzvfp /tmp/get_info_from_servers.tar.gz  --directory /

echo "cd /data/html/get_info_from_servers"
cd /data/html/get_info_from_servers

echo "creating env..."
python3.10 -m venv venv

echo "pwd"
pwd
echo "pip install"
sleep 2
venv/bin/pip install -r req.txt

echo "adding pm2"
pm2 --name get_server_info start "venv/bin/python main.py"

echo "create job  from crontab"
crontab -l > /tmp/mycron
echo "* * * * * /data/html/get_info_from_servers/venv/bin/python /data/html/get_info_from_servers/cron_methods.py" >> /tmp/mycron
crontab /tmp/mycron
rm -f /tmp/mycron 
```
## Database Bağlantısı
Database bağlantı bilgileri **.env** dosyası içerinde yer almaktadır. 
**DB_TYPE** : **mysql** ya da **postgresql** değerlerini almaktadır. 