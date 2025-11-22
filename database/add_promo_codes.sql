-- If promo_codes table doesn’t exist yet, create with the new columns
CREATE TABLE IF NOT EXISTS promo_codes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  amount_off_cents INT NULL,          -- NULL when using percent_off
  percent_off TINYINT NULL,           -- 1-100 when type='percent'
  type ENUM('amount','percent') NOT NULL DEFAULT 'amount',
  active TINYINT(1) NOT NULL DEFAULT 1,
  max_redemptions INT NULL,
  times_redeemed INT NOT NULL DEFAULT 0
);

