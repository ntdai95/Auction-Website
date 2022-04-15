CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    user_type TEXT,
    user_status TEXT,
    user_rating_sum INT,
    user_rating_total INT,
    watchlist_parameter TEXT,
    PRIMARY KEY (user_id)
);
