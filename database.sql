-- Tạo cơ sở dữ liệu
CREATE DATABASE IF NOT EXISTS dacs1_realestate;
USE dacs1_realestate;

-- Bảng Người dùng (Customer, Seller, Admin)
CREATE TABLE users (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       username VARCHAR(50) NOT NULL UNIQUE,
                       password_hash VARCHAR(255) NOT NULL,
                       role ENUM('CUSTOMER', 'SELLER', 'ADMIN') DEFAULT 'CUSTOMER',
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Bất động sản
CREATE TABLE properties (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            seller_id INT,
                            title VARCHAR(255) NOT NULL,
                            area FLOAT NOT NULL, -- Diện tích (m2)
                            bedrooms INT NOT NULL, -- Số phòng ngủ
                            location_code INT NOT NULL, -- Mã khu vực (để AI dễ tính toán)
                            price DECIMAL(15, 2), -- Giá bán thực tế
                            status ENUM('AVAILABLE', 'SOLD', 'RENTED') DEFAULT 'AVAILABLE',
                            FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- Thêm dữ liệu mẫu
INSERT INTO users (username, password_hash, role) VALUES ('seller01', 'hash123', 'SELLER');
INSERT INTO properties (seller_id, title, area, bedrooms, location_code, price)
VALUES (1, 'Nhà phố Hải Châu', 75.5, 3, 1, 3500000000);