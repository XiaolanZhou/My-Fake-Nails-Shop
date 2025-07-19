-- 1) add the column
ALTER TABLE orders
  ADD COLUMN user_id INT NULL AFTER id;
  ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id); 