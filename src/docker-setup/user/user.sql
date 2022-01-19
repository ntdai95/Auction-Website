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

INSERT INTO user (username,password,email,user_type,user_status,user_rating_sum,user_rating_total,watchlist_parameter)
VALUES ("dai",'admin','ngotandai95@gmail.com','admin','active',0,0,'');

INSERT INTO user (username,password,email,user_type,user_status,user_rating_sum,user_rating_total,watchlist_parameter)
VALUES ("kasyap",'admin','skmnktl@gmail.com','admin','active',0,0,'');
INSERT INTO user (username,password,email,user_type,user_status,user_rating_sum,user_rating_total,watchlist_parameter)
VALUES ("notadmin",'pass','x@gmail.com','user','active',0,0,'');
