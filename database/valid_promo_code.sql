-- Add new columns safely
ALTER TABLE promo_codes
  ADD COLUMN IF NOT EXISTS percent_off TINYINT NULL;

ALTER TABLE promo_codes
  ADD COLUMN IF NOT EXISTS type ENUM('amount','percent') NOT NULL DEFAULT 'amount';

ALTER TABLE promo_codes
  MODIFY COLUMN amount_off_cents INT NULL;

-- Insert test promo codes
INSERT IGNORE INTO promo_codes (code, amount_off_cents, type)
VALUES ('SAVE7', 700, 'amount');

INSERT IGNORE INTO promo_codes (code, percent_off, type)
VALUES ('SAVE15', 15, 'percent');

INSERT IGNORE INTO promo_codes (code, percent_off, type, max_redemptions)
VALUES ('20PERCENT', 20, 'percent', 100);
