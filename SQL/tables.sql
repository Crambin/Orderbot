CREATE TABLE IF NOT EXISTS GuildTbl(
    GuildID     BIGINT          NOT NULL    UNIQUE      PRIMARY KEY,
    Prefix      VARCHAR(15)     NOT NULL
);

CREATE TABLE IF NOT EXISTS MarkovTbl(
    Name        VARCHAR         NOT NULL    UNIQUE      PRIMARY KEY,
    WordPairs   JSON            NOT NULL
);