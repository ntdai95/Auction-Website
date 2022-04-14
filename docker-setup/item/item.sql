DROP TABLE IF EXISTS `items`;
DROP TABLE IF EXISTS `categories`;

CREATE TABLE `items` (
    `item_id` VARCHAR(256) NOT NULL PRIMARY KEY,
    `name` VARCHAR(256),
    `auction_id` TEXT,
    `creation_date` TIMESTAMP,
    `user_id` TEXT,
    `description` TEXT,
    `categories` TEXT COMMENT '| separated',
    `counterfeit` BOOL,
    `inappropriate` BOOL,
    `price` DECIMAL(15,2) UNSIGNED,
    `sold` BOOL
);

CREATE TABLE `categories` (
    `category` VARCHAR(256) NOT NULL PRIMARY KEY,
    `created_by` TEXT,
    `blacklisted` BOOL
);

/*
INSERT INTO `categories`
VALUES ('shoes','dai',FALSE);
INSERT INTO `categories`
VALUES ('obscenity','dai',TRUE);
INSERT INTO `categories`
VALUES ('socks','dai',FALSE);
INSERT INTO `categories`
VALUES ('pens','dai',FALSE);

INSERT INTO `items`
VALUES ("100",'item0','300',NULL,'200', 'Good condition', 'shoes', FALSE, FALSE, 10000, FALSE);
INSERT INTO `items`
VALUES ("101",'item1','301',NULL,'200', 'Bad condition', 'shoes', FALSE, FALSE, 10100, FALSE);
INSERT INTO `items`
VALUES ("102",'item2','302',NULL,'201', NULL, 'obscenity', FALSE, FALSE, 10200, FALSE);
INSERT INTO `items`
VALUES ("103",'item3','303',NULL,'201', 'Nothing to say', 'obscenity', FALSE, FALSE, 10300, FALSE);
INSERT INTO `items`
VALUES ("104",'item4','304',NULL,'202', 'Old', 'socks', FALSE, FALSE, 10400, FALSE);
INSERT INTO `items`
VALUES ("105",'item5','305',NULL,'202', 'New', 'socks', FALSE, FALSE, 10500, FALSE);
INSERT INTO `items`
VALUES ("106",'item6','306',NULL,'203', 'Brand new', 'pens', FALSE, FALSE, 10600, FALSE);
INSERT INTO `items`
VALUES ("107",'item7','307',NULL,'203', 'Broken', 'pens', FALSE, FALSE, 10700, FALSE);
INSERT INTO `items`
VALUES ("108",'item8','308',NULL,'204', 'Crap', 'pens', FALSE, FALSE, 10800, TRUE);
INSERT INTO `items`
VALUES ("109",'item9','309',NULL,'So-so', 'pens', FALSE, FALSE, 10900, FALSE);
INSERT INTO `items`
VALUES ("110",'item10','310',NULL, 'Premier', 'pens',  FALSE, FALSE, 10900, FALSE);
*/
