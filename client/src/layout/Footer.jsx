import React from 'react';

const Footer = () => (
  <footer className="mt-16 bg-gradient-to-t from-white/80 to-transparent border-t border-pink-100">
    <div className="max-w-6xl mx-auto px-4 lg:px-8 py-8 text-center text-sm text-gray-500">
      <p>© {new Date().getFullYear()} PHEW Nails. All rights reserved.</p>
      <p className="mt-2 text-xs uppercase tracking-[0.2em] text-pink-400">Made with sparkle &amp; care</p>
    </div>
  </footer>
);

export default Footer;
