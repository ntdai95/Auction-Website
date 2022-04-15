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
