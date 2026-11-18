/**
 * EdgeVision - Görüntü Yükleyici Bileşeni
 * 
 * Kullanıcının bilgisayarından bir görüntü seçmesini sağlar.
 * Seçilen dosyayı üst bileşene (App.tsx) iletir.
 */
import { ChangeEvent } from 'react';

interface Props {
  onImageSelected: (file: File) => void;
}

export default function ImageUploader({ onImageSelected }: Props) {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelected(file);
    }
  };

  return (
    <div style={{
      border: '2px dashed #334155', borderRadius: 8, padding: 32,
      textAlign: 'center', background: '#1e293b',
    }}>
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleChange} 
        id="file-input" 
        style={{ display: 'none' }} 
      />
      <label htmlFor="file-input" style={{ cursor: 'pointer', color: '#60a5fa', fontSize: 16 }}>
        Bir görüntü seçmek için tıklayın
      </label>
    </div>
  );
}
