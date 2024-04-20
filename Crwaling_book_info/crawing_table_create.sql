

CREATE TABLE Books (
    bookID INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(255),
    publishing DATE,
    rating DECIMAL(3, 1),
    review INT,
    sales INT,
    price DECIMAL(10, 2),
    ranking INT,
    ranking_weeks INT
);