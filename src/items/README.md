 # DOCKER MYSQL:
https://medium.com/swlh/how-to-connect-to-mysql-docker-from-python-application-on-macos-mojave-32c7834e5afa

 Name: items-ms-datastore
 Login: root@items-ms-datastore: tseitems

 # CREATED DOCKER USING:
 docker run --name=items-ms-datastore --env="MYSQL_ROOT_PASSWORD=tseitems" -p 3306:3306 -d mysql:latest

 # EXEC INTO MYSQL:
 docker exec -it items-ms-datastore mysql -uroot -ptseitems

 # create service account and password
 CREATE USER 'items-ms'@'%' IDENTIFIED BY 'items-ms';
 GRANT ALL PRIVILEGES ON items_ms_datastore.* to 'items-ms'@'%';


