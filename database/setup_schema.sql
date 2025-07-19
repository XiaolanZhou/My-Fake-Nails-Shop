CREATE DATABASE IF NOT EXISTS my1stwebsite;

USE my1stwebsite;

-- DROP TABLE IF EXISTS cart_items;
-- DROP TABLE IF EXISTS orders;
-- DROP TABLE IF EXISTS products;


-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description TEXT,
    price DECIMAL(10, 2),
    image_url VARCHAR(500)
);

-- Create the cart_items table
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    product_id INT,
    quantity INT,
    status ENUM('unpaid', 'processing', 'shipped', 'review') NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email   VARCHAR(255) UNIQUE NOT NULL,
    phone   VARCHAR(32) NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    points INT NOT NULL DEFAULT 0
);


-- Insert sample products
INSERT IGNORE INTO products (name, description, price, image_url) VALUES
('Rose Quartz Set', 'Elegant pink marble design with glossy finish.', 19.99, '/uploads/rose-quartz-set.png'),
('Galaxy Glam', 'Black base with holographic glitter tips.', 22.50, '/uploads/galaxy-glam.png'),
('Sunset Ombre', 'Gradient from coral to soft yellow.', 18.00, '/uploads/sunset-ombre.png'),
('French Classic', 'Timeless French tips with a subtle pink base.', 15.99, '/uploads/french-classic.png'),
('Neon Pop', 'Bold neon colors perfect for summer.', 20.00, '/uploads/neon-pop.png'),
('Matte Black', 'Chic and edgy matte black set.', 17.50, '/uploads/matte-black.png');

