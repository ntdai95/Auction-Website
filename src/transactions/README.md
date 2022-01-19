** INSTRUCTION:  

**Setup  
  
docker run --name=transaction -e MYSQL_ROOT_PASSWORD=transaction -p 3306:3306 -d mysql:latest  
  
(In case 3306 is already used error):  
    sudo pkill mysqld  
    sudo pkill mysql  
  
docker exec -it transaction mysql -uroot -ptransaction  
(Change -uroot to -utransaction from the second run)  
  
CREATE USER 'transaction'@'%' IDENTIFIED BY 'transaction';  
  
GRANT ALL PRIVILEGES ON transaction.* to ‘transaction’@‘%’;  
  
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'transaction';  
  
CREATE DATABASE transaction;  
  
USE DATABASE;  
  
  
**Run  
  
Run Create.py first. It will initialize the database and seeds some mock data in both db_cart and db_order.  

