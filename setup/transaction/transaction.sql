CREATE TABLE db_order (
    order_id INT NOT NULL,
    user_id VARCHAR(256) NOT NULL,
	item_id VARCHAR(256) NOT NULL,
    price DOUBLE,
	order_time TIMESTAMP,
	order_status VARCHAR(256) NOT NULL,
    UNIQUE(item_id)
);

CREATE TABLE db_cart (
	item_id VARCHAR(256) NOT NULL,
    user_id VARCHAR(256) NOT NULL,
    price DOUBLE,
    auction BOOLEAN,
    later BOOLEAN,
    UNIQUE KEY (user_id, item_id)
);
