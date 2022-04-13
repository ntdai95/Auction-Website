import pymysql.cursors
from transaction import cart

conn = pymysql.connect(
    host = "localhost",
    user="transaction",
    password="transaction",
    db="transaction",
    port = 3306
    )

cursor = conn.cursor()

init = \
"""
    DROP USER 'transaction'@'%';
    CREATE USER 'transaction'@'%' IDENTIFIED BY 'transaction';
    GRANT ALL PRIVILEGES ON transaction.* to ‘transaction’@‘%’;
"""
#cursor.execute(init)


db_order = \
"""
    CREATE TABLE `db_order` (
    `order_id` INT NOT NULL,
    `user_id` VARCHAR(256) NOT NULL,
	`item_id` VARCHAR(256) NOT NULL,
    `price` DOUBLE  NOT NULL,
	`order_time` TIMESTAMP,
	`state` VARCHAR(256) NOT NULL,
    UNIQUE(item_id)
);
"""


db_cart = \
"""
    CREATE TABLE `db_cart` (
    `user_id` VARCHAR(256) NOT NULL,
	`item_id` VARCHAR(256) NOT NULL,
    `price` DOUBLE  NOT NULL,
    `auction` BOOLEAN,
    `later` BOOLEAN
);
"""


# Execute a query
# Drop tables and create a new
cursor.execute('''DROP TABLE IF EXISTS db_cart''')
cursor.execute('''DROP TABLE IF EXISTS db_order''')

cursor.execute(db_order)
cursor.execute(db_cart)

# Create sample data
first_data = [["20201","10104", 100],["20201","10105",200],["20201","10106",300], #user wants to buy 20201 later
              ["20202","10107",405],
              ["20203","10108",600],["20203","10108",700], #'10108' is a duplicated data
              ["20204","10109",1000],["20204","10110",1000,98],["20204","10111",200.65],
              ["20205","10105", 100],["20205","10112",200]] #Multiple people wants 10105 but user 20201 buy it first
for data in first_data:
    cart()._addCart(user_id = data[0], item_id = data[1], price = data[2])

cart()._addCart(user_id = "20202", item_id = "9999",price = "10000", isAuction=True)

cart()._flip_buyLater(user_id = "20201", item_id = "10104")
cart()._flip_buyLater(user_id = "20201", item_id = "10105")
cart()._flip_buyLater(user_id = "20202", item_id = "9999")
cart()._flip_buyNow(user_id = "20201", item_id = "10105")

cart()._checkout(user_id = "20201")
cart()._checkout(user_id = "20202")
