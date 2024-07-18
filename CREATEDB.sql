-- -----------------------------------------------------
-- Table USERS
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Users (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  mail TEXT NOT NULL,
  hashPass TEXT NOT NULL,
  dateRegistered DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table Projects
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Projects (
  ProjectID INTEGER PRIMARY KEY AUTOINCREMENT,
  projectName TEXT NULL,
  projectDescription TEXT NULL,
  projectLink TEXT NULL,
  projectStars INTEGER NULL
);

-- -----------------------------------------------------
-- Table Favourites
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Favourites (
  UserID INTEGER NOT NULL ,
  ProjectID INTEGER NOT NULL,
  favouriteDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (UserID, ProjectID),
  FOREIGN KEY (UserID) REFERENCES USERS (ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  FOREIGN KEY (ProjectID) REFERENCES Projects (ProjectID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table Posts
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Posts (
  PostID INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  postText TEXT NOT NULL,
  UserID INTEGER NOT NULL,
  postDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES USERS (ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table Notes
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Notes (
  NoteID INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  noteText TEXT NOT NULL,
  UserID INTEGER NOT NULL,
  noteDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES USERS (ID)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
