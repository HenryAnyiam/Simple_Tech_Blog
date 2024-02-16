-- Configure database to work with

-- Create Database to work with

DROP DATABASE IF EXISTS `tech_blog_db`;
CREATE DATABASE IF NOT EXISTS `tech_blog_db`;

-- Create User to work with

CREATE USER IF NOT EXISTS 'tech_blogger'@'localhost' IDENTIFIED BY 'tech_blog_pwd';

-- Grant due permissions
GRANT ALL ON `tech_blog_db`.* TO 'tech_blogger'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'tech_blogger'@'localhost';
