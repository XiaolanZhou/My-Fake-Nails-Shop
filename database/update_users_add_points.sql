-- database/update_users_add_points.sql
ALTER TABLE users
  ADD COLUMN points INT NOT NULL DEFAULT 0; 