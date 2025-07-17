import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

export default function ProductDetails() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5001/api/products/${id}`)
      .then(res => res.json())
      .then(data => {
        setProduct(data);
        setSelectedImage(data.image_url); // Use main image by default
      })
      .catch(console.error);
  }, [id]);

  if (!product) return <div>Loading...</div>;

  const images = product.images || [product.image_url];

  return (
    <div className="max-w-6xl mx-auto p-8 bg-white rounded-lg shadow flex flex-col md:flex-row gap-8">
      {/* Left: Images */}
      <div className="flex flex-col md:flex-row gap-6 w-full md:w-1/2">
        {/* Thumbnails */}
        <div className="flex md:flex-col gap-2">
          {images.map((img, idx) => (
            <img
              key={idx}
              src={img}
              alt={`Thumbnail ${idx + 1}`}
              className={`w-16 h-16 object-cover rounded cursor-pointer border-2 ${selectedImage === img ? 'border-pink-500' : 'border-transparent'}`}
              onClick={() => setSelectedImage(img)}
            />
          ))}
        </div>
        {/* Main Image */}
        <div className="flex-1 flex items-center justify-center">
          <img src={selectedImage} alt={product.name} className="max-h-[400px] w-auto object-contain rounded" />
        </div>
      </div>

      {/* Right: Product Info */}
      <div className="flex-1 flex flex-col gap-4">
        <h1 className="text-2xl font-bold">{product.name}</h1>
        <div className="text-lg text-red-600 font-bold">${product.price}</div>
        <div className="text-gray-700">{product.description}</div>
        {/* Example options (customize as needed) */}
        <div className="mt-4">
          <label className="block font-semibold mb-1">Options</label>
          <select className="border rounded p-2 w-full">
            <option>Default Option</option>
            {/* Add more options here */}
          </select>
        </div>
        <button className="mt-6 bg-pink-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-pink-700 transition">
          Add to Cart
        </button>
      </div>
    </div>
  );
}
