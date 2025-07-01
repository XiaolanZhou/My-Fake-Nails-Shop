CREATE DATABASE IF NOT EXISTS my1stwebsite;
USE my1stwebsite;

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

-- Insert sample products
INSERT IGNORE INTO products (name, description, price, image_url) VALUES
('Rose Quartz Set', 'Elegant pink marble design with glossy finish.', 19.99, 'https://example.com/images/rose-quartz.jpg'),
('Galaxy Glam', 'Black base with holographic glitter tips.', 22.50, 'https://example.com/images/galaxy-glam.jpg'),
('Sunset Ombre', 'Gradient from coral to soft yellow.', 18.00, 'https://example.com/images/sunset-ombre.jpg'),
('French Classic', 'Timeless French tips with a subtle pink base.', 15.99, 'https://example.com/images/french-classic.jpg'),
('Neon Pop', 'Bold neon colors perfect for summer.', 20.00, 'https://example.com/images/neon-pop.jpg'),
('Matte Black', 'Chic and edgy matte black set.', 17.50, 'https://example.com/images/matte-black.jpg');
