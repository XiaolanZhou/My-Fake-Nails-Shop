-- Table to store individual ratings
CREATE TABLE IF NOT EXISTS product_ratings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  user_id INT NOT NULL,
  rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  UNIQUE KEY uniq_product_user (product_id, user_id),
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Add aggregate columns to products
ALTER TABLE products
  ADD COLUMN rating DECIMAL(3,2) NOT NULL DEFAULT 0.0,
  ADD COLUMN rating_count INT NOT NULL DEFAULT 0; 