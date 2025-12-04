-- PostgreSQL Schema for My Fake Nails Shop

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    rating DECIMAL(3, 2) DEFAULT 0.0,
    rating_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart items table
CREATE TABLE IF NOT EXISTS cart_items (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    product_id INT REFERENCES products(id) ON DELETE SET NULL,
    quantity INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product ratings table
CREATE TABLE IF NOT EXISTS product_ratings (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    UNIQUE (product_id, user_id)
);

-- Promo codes table
CREATE TABLE IF NOT EXISTS promo_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    amount_off_cents INT,
    percent_off SMALLINT,
    type VARCHAR(10) DEFAULT 'amount' CHECK (type IN ('amount', 'percent')),
    active BOOLEAN DEFAULT true,
    max_redemptions INT,
    times_redeemed INT DEFAULT 0
);

-- Insert sample products with Vercel Blob URLs
INSERT INTO products (name, description, price, image_url) VALUES
('Rose Quartz Set', 'Beautiful rose quartz nail set with elegant pink tones', 19.99, 'https://hthaottxeeqjyffd.public.blob.vercel-storage.com/uploads/rose-quartz-set-DbqtA26x3Uz2W5xxJJ1yLHo5XJNkFO.png'),
('Galaxy Glam', 'Stunning galaxy themed nails with cosmic sparkle', 24.99, 'https://hthaottxeeqjyffd.public.blob.vercel-storage.com/uploads/galaxy-glam-7wjRWUN45hpi67oTbfgE0A5LyomSZc.png'),
('Sunset Ombre', 'Beautiful sunset gradient nails in warm tones', 22.50, 'https://hthaottxeeqjyffd.public.blob.vercel-storage.com/uploads/sunset-ombre-02mLd4LwtUwlmAlzCTkAqpA0J7mGLp.png'),
('French Classic', 'Timeless French manicure set for elegant style', 18.00, 'https://hthaottxeeqjyffd.public.blob.vercel-storage.com/uploads/french-classic-QEd11bjgbewUFIFquUelsDSjn7kEYV.png'),
('Neon Pop', 'Vibrant neon nail collection for bold looks', 20.00, 'https://hthaottxeeqjyffd.public.blob.vercel-storage.com/uploads/neon-pop-2q4YW70uugEFqB7tI2aIrLp1u1LQo0.png'),
('Matte Black', 'Sleek matte black nails for sophisticated style', 17.50, 'https://hthaottxeeqjyffd.public.blob.vercel-storage.com/uploads/matte-black-NWJz6cRTUyJogBrUrue4eId99T5ILl.png')
ON CONFLICT DO NOTHING;

-- Insert sample promo codes
INSERT INTO promo_codes (code, amount_off_cents, type) VALUES ('SAVE7', 700, 'amount')
ON CONFLICT DO NOTHING;
INSERT INTO promo_codes (code, percent_off, type) VALUES ('SAVE15', 15, 'percent')
ON CONFLICT DO NOTHING;
