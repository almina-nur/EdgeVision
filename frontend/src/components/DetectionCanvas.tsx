/**
 * EdgeVision - Tespit Çizim Bileşeni
 * 
 * Yüklenen görüntüyü bir HTML5 Canvas üzerine çizer.
 * Modelden gelen sınırlayıcı kutuları (bounding boxes) ve sınıf etiketlerini
 * görüntünün üzerine yerleştirir.
 */
import { useEffect, useRef } from 'react';
import type { Prediction } from '../App';

interface Props {
  imageUrl: string;
  prediction: Prediction | null;
}

// Sınıflara göre kutu renkleri
const CLASS_COLORS: Record<string, string> = {
  pedestrian: '#ef4444', people: '#f97316', bicycle: '#eab308',
  car: '#22c55e', van: '#14b8a6', truck: '#3b82f6',
  tricycle: '#8b5cf6', 'awning-tricycle': '#ec4899',
  bus: '#f43f5e', motor: '#06b6d4',
};

export default function DetectionCanvas({ imageUrl, prediction }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.onload = () => {
      // Canvas boyutunu görüntü boyutuna eşitle
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      if (!prediction) return;

      // Çizgi kalınlığı ve yazı boyutu (görüntü boyutuna göre dinamik)
      ctx.lineWidth = Math.max(2, img.width / 400);
      ctx.font = `${Math.max(12, img.width / 60)}px sans-serif`;

      // Her tespit için kutu ve etiket çiz
      for (const det of prediction.detections) {
        const [x, y, w, h] = det.bbox;
        const color = CLASS_COLORS[det.class_name] || '#ffffff';
        
        // Sınırlayıcı kutuyu çiz
        ctx.strokeStyle = color;
        ctx.strokeRect(x, y, w, h);

        // Etiket arka planı
        const label = `${det.class_name} %${(det.confidence * 100).toFixed(0)}`;
        const textWidth = ctx.measureText(label).width;
        ctx.fillStyle = color;
        ctx.fillRect(x, y - 20, textWidth + 8, 20);

        // Etiket metni
        ctx.fillStyle = '#000';
        ctx.fillText(label, x + 4, y - 5);
      }
    };
    img.src = imageUrl;
  }, [imageUrl, prediction]);

  return <canvas ref={canvasRef} style={{ maxWidth: '100%', marginTop: 16, borderRadius: 8 }} />;
}
