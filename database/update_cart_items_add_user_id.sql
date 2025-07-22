-- Add user_id column to cart_items and set existing rows to NULL
ALTER TABLE cart_items
  ADD COLUMN user_id INT NULL,
  ADD FOREIGN KEY (user_id) REFERENCES users(id); 