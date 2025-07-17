USE my1stwebsite;

-- Add status column to existing orders table
ALTER TABLE orders 
ADD COLUMN status ENUM('unpaid', 'processing', 'shipped', 'review') NOT NULL DEFAULT 'unpaid';

-- Update some existing orders to have different statuses for testing
UPDATE orders SET status = 'processing' WHERE id % 3 = 0;
UPDATE orders SET status = 'shipped' WHERE id % 3 = 1;
UPDATE orders SET status = 'review' WHERE id % 3 = 2; 