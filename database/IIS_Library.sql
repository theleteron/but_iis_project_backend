
DROP TABLE IF EXISTS `Book loan`;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS `Publication-Order table`;
DROP TABLE IF EXISTS `order`;
DROP TABLE IF EXISTS `Library opening hours`;
DROP TABLE IF EXISTS Hash;
DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS Publication;
DROP TABLE IF EXISTS Library;

CREATE TABLE Library (
    ID INT AUTO_INCREMENT NOT NULL,
    Name VARCHAR (50) UNIQUE NOT NULL,
    City VARCHAR (50) NOT NULL,
    `Zip code` INT (6) NOT NULL,
    Street VARCHAR (50) NOT NULL,
    Description VARCHAR (255),
    PRIMARY KEY (ID)
);

CREATE TABLE `Library opening hours` (
    ID INT AUTO_INCREMENT NOT NULL,
    `Library ID` INT,
    Day INT(1) NOT NULL,
    `Open time` TIME,
    `Close time` TIME,
    PRIMARY KEY (ID),
    FOREIGN KEY (`Library ID`) REFERENCES Library(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `User` (
    ID INT AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Surname VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    `Zip code` INT(6) NOT NULL,
    Street VARCHAR(50) NOT NULL,
    Email VARCHAR(50) UNIQUE,
    Phone INT(9) UNIQUE,
    Position SET('Unregistered_user', 'Registered_user', 'Administrator', 'Librarian', 'Distributor')
        NOT NULL DEFAULT('Unregistered_user'),
    `Working at` INT,
    PRIMARY KEY (ID),
    FOREIGN KEY (`Working at`) REFERENCES Library(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Hash (
    ID INT AUTO_INCREMENT,
    `User ID` INT NOT NULL,
    Hash VARCHAR(20) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (`User ID`) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Publication (
    ID INT AUTO_INCREMENT,
    Name VARCHAR(50) UNIQUE NOT NULL,
    Series VARCHAR(50),
    Synopsis VARCHAR(255),
    `Author/s` VARCHAR(50) NOT NULL,
    Language VARCHAR(20) NOT NULL,
    ISBN DECIMAL(20,0) NOT NULL,
    `Date of publication` DATE,
    Publisher VARCHAR(50),
    Genre VARCHAR(50),
    Pages INT(4),
    Tags VARCHAR(255),
    Rating INT(3),
    PRIMARY KEY (ID)
);

CREATE TABLE Book (
    ID INT AUTO_INCREMENT,
    `Publication ID` INT,
    `Library ID` INT,
    `Condition` SET('New', 'Used', 'Damaged', 'Disposed'),
    Section INT(3),
    PRIMARY KEY (ID),
    FOREIGN KEY (`Library ID`) REFERENCES Library(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Publication ID`) REFERENCES Publication(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Order` (
    ID INT AUTO_INCREMENT,
    `Library ID` INT NOT NULL,
    `User ID` INT NOT NULL,
    `Date of order` DATE,
    Delivered BOOL DEFAULT 0,
    Price NUMERIC(10,2),
    PRIMARY KEY (ID),
    FOREIGN KEY (`Library ID`) REFERENCES Library(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`User ID`) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Publication-Order table` (
    `Order ID` INT,
    `Publication ID` INT,
    `Number of books` INT(4) NOT NULL ,
    `Price per book` NUMERIC(6,2) NOT NULL,
    FOREIGN KEY (`Order ID`) REFERENCES `Order`(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Publication ID`) REFERENCES Publication(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Book loan` (
    ID INT AUTO_INCREMENT,
    `From` DATE NOT NULL,
    `To` DATE NOT NULL,
    Extension DATE,
    Fine INT,
    Loans INT NOT NULL,
    Receives INT,
    Creates INT NOT NULL,
    `Book 1` INT,
    `Book 2` INT,
    `Book 3` INT,
    `Book 4` INT,
    `Book 5` INT,
    PRIMARY KEY (ID),
    FOREIGN KEY (Loans) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (Receives) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (Creates) REFERENCES User(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Book 1`) REFERENCES Book(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Book 2`) REFERENCES Book(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Book 3`) REFERENCES Book(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Book 4`) REFERENCES Book(ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`Book 5`) REFERENCES Book(ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Library VALUES (1,'Library_01','Brno',60200,'Beethovenova 10','Our first Library');
INSERT INTO Library(Name, City, `Zip code`, Street, Description) VALUES ('Library_02','Breclav',69002,'U splavu 4','Our second Library');
INSERT INTO Library(Name, City, `Zip code`, Street) VALUES ('Library_03','Brno',60200,'Buresova 16');

INSERT INTO Publication(name, series, synopsis, `author/s`, language, isbn, `date of publication`, publisher, genre, pages, tags, rating)
    VALUES ('The Fellowship of the Ring', 'The Lord of the Rings', 'The first volume in J.R.R. Tolkien\'s epic adventure THE LORD OF THE RINGS One Ring to rule them all, One Ring to find them, One Ring to bring them all and in the darkness bind them' , 'J.R.R. Tolkien', 'EN', 9780547928210, DATE '2009-04-20', 'HarperCollins', 'Fantasy' , 433, 'lotr, middleearth, thehobbit, jrrtolkien, hobbit, gandalf, aragorn, legolas, sauron, frodo, elves, elf, gondor, gimli, gollum, mordor, mirkwood', 87);
INSERT INTO Publication(name, series, synopsis, `author/s`, language, isbn, `date of publication`, publisher, genre, pages, tags, rating)
    VALUES ('The Two Towers', 'The Lord of the Rings', 'The awesome conclusion to The Lord of the Rings—the greatest fantasy epic of all time—which began in The Fellowship of the Ring and The Two Towers.' , 'J.R.R. Tolkien', 'EN', 9780547952024, DATE '2009-04-20', 'HarperCollins ', 'Fantasy' , 352, 'lotr, middleearth, thehobbit, jrrtolkien, hobbit, gandalf, aragorn, legolas, sauron, frodo, elves, elf, gondor, gimli, gollum, mordor, mirkwood', 93);
INSERT INTO Publication(name, `author/s`, language, isbn) VALUES ('Karanténa s moderním fotrem', 'Dominik Landsman', 'CZ',9788024945798);

INSERT INTO `User`(name, surname, city, `zip code`, street, email, phone, position) VALUES('Maria', 'Johanson', 'Brno', 60200, 'Antoninska 15', 'M.ria@gmail.com', 234567890, 'Registered_user');
INSERT INTO `User`(name, surname, city, `zip code`, street, email, phone) VALUES('Lucas', 'Green', 'Brno', 60200, 'Antoninska 13', 'LucasG@gmail.com', 123456789);
INSERT INTO `User`(name, surname, city, `zip code`, street, phone, position, `working at`) VALUES('Petr', 'Salajka', 'Breclav', 69003, 'Lidicka 36', 345678901, 'Librarian', 2);
INSERT INTO `User`(name, surname, city, `zip code`, street, email, position, `working at`) VALUES('Aneta', 'Pecharova', 'Breclav', 69001, '17. Listopadu 1', 'AnetPechar@seznam.cz', 'Administrator', 2);
INSERT INTO `User`(name, surname, city, `zip code`, street, position, `working at`) VALUES('Thomas', 'Smith', 'Brno', 60203, 'Hlinky 99', 'Librarian', 3);

INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (1, 1, '9:00:00', '12:00:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (1, 2, '9:00:00', '15:30:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (1, 3, '9:00:00', '15:30:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (1, 4, '9:00:00', '15:30:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (1, 5, '9:00:00', '12:00:00');

INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (2, 1, '9:00:00', '12:00:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (2, 2, '9:00:00', '16:00:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (2, 3, '9:00:00', '12:00:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (2, 4, '9:00:00', '16:00:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (2, 5, '9:00:00', '12:00:00');

INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (3, 2, '10:00:00', '14:00:00');
INSERT INTO `Library opening hours`(`library id`, day, `open time`, `close time`) VALUES (3, 3, '10:00:00', '14:00:00');

INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 1, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 1, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 1, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 1, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 1, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 1, 'new');

INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (3, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (3, 2, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (3, 2, 'new');

INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (1, 3, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (2, 3, 'new');
INSERT INTO Book(`publication id`, `library id`, `condition`) VALUES (3, 3, 'new');

INSERT INTO `Book loan`(`from`, `to`, loans, creates, `book 1`) VALUES (DATE '2021-10-28', DATE '2021-11-28', 3, 1, 1);
INSERT INTO `Book loan`(`from`, `to`, loans, creates, `book 1`, `Book 2`) VALUES (DATE '2021-10-28', DATE '2021-11-28', 3, 1, 3, 5);


#DROP TABLE IF EXISTS `Book loan`;
#DROP TABLE IF EXISTS Book;
#DROP TABLE IF EXISTS `Publication-Order table`;
#DROP TABLE IF EXISTS `order`;
#DROP TABLE IF EXISTS `Library opening hours`;
#DROP TABLE IF EXISTS Hash;
#DROP TABLE IF EXISTS `User`;
#DROP TABLE IF EXISTS Publication;
#DROP TABLE IF EXISTS Library;
