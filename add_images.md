# Adding Images to Your Website

## How to Add Your Images

1. **Place your images in the `client/public/images/` directory**
   - Supported formats: JPG, PNG, GIF, WebP
   - Recommended size: 400x400 pixels or larger
   - File naming: Use descriptive names like `rose-quartz.jpg`, `galaxy-glam.jpg`, etc.

2. **Update the database with your actual image filenames**
   ```sql
   -- Example: If you have a file called "my-nail-art.jpg"
   UPDATE products 
   SET image_url = '/images/my-nail-art.jpg' 
   WHERE name = 'Rose Quartz Set';
   ```

3. **Image file naming convention:**
   - Use lowercase letters
   - Separate words with hyphens: `rose-quartz.jpg`
   - Avoid spaces and special characters
   - Keep names descriptive but short

## Current Expected Images:
- `rose-quartz.jpg` - Rose Quartz Set
- `galaxy-glam.jpg` - Galaxy Glam
- `sunset-ombre.jpg` - Sunset Ombre
- `french-classic.jpg` - French Classic
- `neon-pop.jpg` - Neon Pop
- `matte-black.jpg` - Matte Black

## Alternative: Using External Image URLs
If you prefer to use external image hosting (like Imgur, Cloudinary, etc.):
```sql
UPDATE products 
SET image_url = 'https://your-image-hosting.com/image.jpg' 
WHERE name = 'Product Name';
```

## Testing Your Images
After adding images, restart your development server and check that the images load correctly in your React app. 