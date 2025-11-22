import { useEffect, useRef } from 'react';

export default function PetalCanvas() {
  const ref = useRef(null);

  useEffect(() => {
    const canvas = ref.current;
    const ctx = canvas.getContext('2d');
    const resize = () => {
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize(); window.addEventListener('resize', resize);

    const TOTAL = 100;
    const petals = [];
    const img = new Image();
    img.src = 'https://djjjk9bjm164h.cloudfront.net/petal.png';
    img.onload = () => {
      for (let i = 0; i < TOTAL; i++) petals.push(new Petal());
      requestAnimationFrame(render);
    };

    let mouseX = 0;
    const move = e => { mouseX = (e.clientX || e.touches?.[0]?.clientX || 0) / window.innerWidth; };
    window.addEventListener('mousemove', move);
    window.addEventListener('touchmove', move);

    function Petal() {
      this.reset = () => {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height * 2 - canvas.height;
        this.w = 25 + Math.random() * 15;
        this.h = 20 + Math.random() * 10;
        this.opacity = this.w / 40;
        this.flip = Math.random();
        this.xSpeed = 1.5 + Math.random() * 2;   // 1.5 – 3.5 px / frame
        this.ySpeed = 1 + Math.random() * 1;     // 1 – 2   px / frame
        this.flipSpeed = Math.random() * 0.01;
      };
      this.reset();
      this.draw = () => {
        if (this.y > canvas.height || this.x > canvas.width) this.reset();
        ctx.globalAlpha = this.opacity;
        ctx.drawImage(
          img,
          this.x,
          this.y,
          this.w * (0.6 + Math.abs(Math.cos(this.flip)) / 3),
          this.h * (0.8 + Math.abs(Math.sin(this.flip)) / 5)
        );
      };
      this.update = () => {
        this.x += this.xSpeed + mouseX * 0.5   // gentle sway instead of burst
        this.y += this.ySpeed + mouseX * 0.2
        this.flip += this.flipSpeed;
        this.draw();
      };
    }

    function render() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      petals.forEach(p => p.update());
      requestAnimationFrame(render);
    }

    return () => {
      window.removeEventListener('resize', resize);
      window.removeEventListener('mousemove', move);
      window.removeEventListener('touchmove', move);
    };
  }, []);

  return <canvas id="petal-canvas" ref={ref}></canvas>;
}