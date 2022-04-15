DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS categories;

CREATE TABLE items (
    item_id VARCHAR(256) NOT NULL PRIMARY KEY,
    name VARCHAR(256),
    auction_id TEXT,
    creation_date TIMESTAMP,
    user_id TEXT,
    description TEXT,
    categories TEXT COMMENT '| separated',
    counterfeit BOOL,
    inappropriate BOOL,
    price DECIMAL(15,2) UNSIGNED,
    sold BOOL
);

CREATE TABLE categories (
    category VARCHAR(256) NOT NULL PRIMARY KEY,
    created_by TEXT,
    blacklisted BOOL
);
