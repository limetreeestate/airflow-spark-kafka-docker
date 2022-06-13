CREATE DATABASE IF NOT EXISTS nimbus;

USE nimbus;

CREATE TABLE IF NOT EXISTS stage1 (
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    address1 VARCHAR(100),
    city VARCHAR(100),
    postcode VARCHAR(100),
    decision VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS stage2 (
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    address1 VARCHAR(100),
    city VARCHAR(100),
    postcode VARCHAR(100),
    decision VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS duplicates (
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    duplicateCount int
);

CREATE TABLE IF NOT EXISTS decision (
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    decision VARCHAR(100),
    isGoodDecision BOOlEAN
);

CREATE TABLE IF NOT EXISTS stage3 (
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    address1 VARCHAR(100),
    city VARCHAR(100),
    postcode VARCHAR(100),
    decision VARCHAR(100),
    isGoodDecision BOOlEAN
);