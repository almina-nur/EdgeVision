/**
 * EdgeVision - Ana Uygulama Bileşeni
 * 
 * Bu bileşen, uygulamanın genel düzenini ve sekme (tab) sistemini yönetir.
 * İki ana sekme bulunur:
 * 1. Görüntü Tespiti: Kullanıcının görüntü yükleyip tespit yapmasını sağlar.
 * 2. Benchmark & Analiz: Model performans metriklerini ve grafikleri gösterir.
 */
import { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import DetectionCanvas from './components/DetectionCanvas';
import Stats from './components/Stats';

// Tespit edilen tek bir nesnenin veri yapısı
export interface Detection {
  bbox: [number, number, number, number]; // [x, y, genişlik, yükseklik]
  class_id: number;
  class_name: string;
  confidence: number;
}

// API'den dönen tahmin yanıtının veri yapısı
export interface Prediction {
  detections: Detection[];
  inference_ms: number;
  image_width: number;
  image_height: number;
  model: string;
}

function App() {
  // Bileşen durumları (State)
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'detect' | 'stats'>('detect');

  // Kullanıcı yeni bir görüntü seçtiğinde çalışır
  const handleImageSelected = (file: File) => {
    setImageFile(file);
    setImageUrl(URL.createObjectURL(file));
    setPrediction(null);
    setError('');
  };

  // "Tespit Et" butonuna basıldığında API'ye istek atar
  const handlePredict = async () => {
    if (!imageFile) return;
    setLoading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      
      const res = await fetch('/api/predict', { method: 'POST', body: formData });
      if (!res.ok) throw new Error(`Sunucu Hatası: HTTP ${res.status}`);
      
      const data = await res.json();
      setPrediction(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Bilinmeyen bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 24 }}>
      {/* Başlık Bölümü */}
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>EdgeVision</h1>
        <p style={{ color: '#94a3b8', margin: '4px 0 0' }}>
          İHA görüntülerinde edge-optimize YOLO nesne tespiti
        </p>
      </header>

      {/* Sekme (Tab) Butonları */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        <button
          onClick={() => setActiveTab('detect')}
          style={{
            padding: '10px 20px',
            background: activeTab === 'detect' ? '#3b82f6' : '#1e293b',
            color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer',
            fontWeight: activeTab === 'detect' ? 'bold' : 'normal',
          }}
        >
          Görüntü Tespiti
        </button>
        <button
          onClick={() => setActiveTab('stats')}
          style={{
            padding: '10px 20px',
            background: activeTab === 'stats' ? '#3b82f6' : '#1e293b',
            color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer',
            fontWeight: activeTab === 'stats' ? 'bold' : 'normal',
          }}
        >
          Benchmark ve Analiz
        </button>
      </div>

      {/* 1. SEKME: Görüntü Tespiti */}
      {activeTab === 'detect' && (
        <>
          <ImageUploader onImageSelected={handleImageSelected} />

          {imageUrl && (
            <div style={{ marginTop: 16 }}>
              <button onClick={handlePredict} disabled={loading} style={{
                padding: '10px 20px', background: loading ? '#475569' : '#3b82f6',
                color: 'white', border: 'none', borderRadius: 6,
                cursor: loading ? 'not-allowed' : 'pointer', fontSize: 14,
              }}>
                {loading ? 'Tespit ediliyor...' : 'Tespit Et'}
              </button>
            </div>
          )}

          {error && (
            <div style={{ marginTop: 12, padding: 12, background: '#7f1d1d', borderRadius: 6 }}>
              Hata: {error}
            </div>
          )}

          {imageUrl && <DetectionCanvas imageUrl={imageUrl} prediction={prediction} />}

          {prediction && (
            <div style={{ marginTop: 16, padding: 16, background: '#1e293b', borderRadius: 8 }}>
              <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
                <div><strong>Model:</strong> {prediction.model}</div>
                <div><strong>Çıkarım:</strong> {prediction.inference_ms} ms</div>
                <div><strong>Tespit:</strong> {prediction.detections.length} nesne</div>
                <div><strong>Boyut:</strong> {prediction.image_width} x {prediction.image_height}</div>
              </div>
            </div>
          )}
        </>
      )}

      {/* 2. SEKME: Benchmark ve Analiz */}
      {activeTab === 'stats' && <Stats />}
    </div>
  );
}

export default App;
