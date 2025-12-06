-- CREATE DATABASE IF NOT EXISTS visitor_mgmt;
-- use visitor_mgmt;
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'gatekeeper', 'owner') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address VARCHAR(255),
    flat_no VARCHAR(10),
    tower VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS visitors (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    tower VARCHAR(10),
    flat_no VARCHAR(10),
    added_by_role ENUM('admin', 'gatekeeper', 'owner') NOT NULL,
    status ENUM('pending', 'approved', 'declined') DEFAULT 'pending',
    owner_email VARCHAR(100),
    owner_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);