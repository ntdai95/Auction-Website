CREATE TABLE watchlist (
    user_id INT,
    item_id VARCHAR(256),
    watchlist_id TEXT,
    lastNotified DATETIME,
    PRIMARY KEY(user_id, item_id)
);
