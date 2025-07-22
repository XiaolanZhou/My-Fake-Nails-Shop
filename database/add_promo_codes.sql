CREATE TABLE IF NOT EXISTS promo_codes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  amount_off_cents INT NOT NULL,
  active TINYINT(1) NOT NULL DEFAULT 1,
  max_redemptions INT NULL,
  times_redeemed INT NOT NULL DEFAULT 0
); 