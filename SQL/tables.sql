CREATE TABLE IF NOT EXISTS GuildTbl(
    GuildID     BIGINT          NOT NULL    UNIQUE      PRIMARY KEY,
    Prefix      VARCHAR(15)     NOT NULL
);

CREATE TABLE IF NOT EXISTS MarkovTbl(
    Name        VARCHAR         NOT NULL    UNIQUE      PRIMARY KEY,
    WordPairs   JSON            NOT NULL
);

CREATE TABLE IF NOT EXISTS UserTbl(
    UserID      BIGINT         NOT NULL    UNIQUE      PRIMARY KEY,
    DisplayName VARCHAR        NOT NULL,
    Balance     INT            NOT NULL    DEFAULT     0,
    Birthday    DATE
);