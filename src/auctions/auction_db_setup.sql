Drop DATABASE if EXISTS auctions;
CREATE DATABASE auctions;
USE auctions;

DROP TABLE IF EXISTS auctions, bids;
CREATE TABLE auctions (
    auction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    auction_type varchar(40),
    item_id varchar(40),
    user_id INT,
    auction_status varchar(6),
    auction_start timestamp,
    auction_end timestamp,
    winning_bid varchar(40)
);

CREATE TABLE bids (
    bid_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    bid_price decimal(10,2),
    user_id int,
    auction_id varchar(40) REFERENCES auctions(auction_id),
    bid_timestamp timestamp
);

-- INSERT INTO auctions (
--     "abc123",
--     "FB",
--     "item_apple_123abc",
--      "on",
--      CURRENT_TIMESTAMP,
--      CURRENT_TIMESTAMP,
--      NULL);

-- INSERT INTO auctions (
--     "abc124",
--     "FB",
--     "item_android_0001",
--      "on",
--      CURRENT_TIMESTAMP,
--      CURRENT_TIMESTAMP,
--      NULL);
-- INSERT INTO auctions (
--     "abc125",
--     "FB",
--     "item_android_0002",
--      "on",
--      CURRENT_TIMESTAMP,
--      CURRENT_TIMESTAMP,
--      NULL);
-- INSERT INTO auctions (
--     "abc126",
--     "FB",
--     "item_apple_123abd",
--      "on",
--      CURRENT_TIMESTAMP,
--      CURRENT_TIMESTAMP,
--      NULL);
