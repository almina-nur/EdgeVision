/**
 * EdgeVision - İstatistik ve Analiz Bileşeni
 * 
 * Backend'deki /stats endpoint'inden verileri çeker ve tablolar halinde gösterir.
 * Benchmark sonuçları, edge simülasyonu ve sınıf bazlı analizleri içerir.
 */
import { useEffect, useState } from 'react';

interface BenchmarkRow {
  model: string;
  size_mb?: number;
  fps: number;
  latency_avg_ms: number;
  latency_p95_ms?: number;
}

interface ClassRow {
  class: string;
  mAP50: number;
  size_group: string;
  instances: number;
}

interface StatsData {
  benchmark?: BenchmarkRow[];
  edge_benchmark?: BenchmarkRow[];
  class_analysis?: ClassRow[];
}

export default function Stats() {
  const [data, setData] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetch('/api/stats')
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d) => setData(d))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 24 }}>Veriler yükleniyor...</div>;
  if (error) return <div style={{ padding: 24, color: '#ef4444' }}>Hata: {error}</div>;
  if (!data) return <div style={{ padding: 24 }}>Veri bulunamadı.</div>;

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Benchmark ve Analiz</h2>

      {/* Edge Benchmark Tablosu */}
      {data.edge_benchmark && data.edge_benchmark.length > 0 && (
        <section style={{ marginTop: 32 }}>
          <h3>Edge Simülasyonu (1 CPU Thread)</h3>
          <p style={{ color: '#94a3b8', fontSize: 14 }}>
            Gerçek uç cihaz senaryosunu simüle etmek için işlemci 1 çekirdeğe sınırlandırılmıştır.
          </p>
          <table style={{ width: '100%', borderCollapse: 'collapse', background: '#1e293b', borderRadius: 8 }}>
            <thead>
              <tr style={{ background: '#334155' }}>
                <th style={{ padding: 12, textAlign: 'left' }}>Model</th>
                <th style={{ padding: 12 }}>FPS</th>
                <th style={{ padding: 12 }}>Ortalama Gecikme (ms)</th>
                <th style={{ padding: 12 }}>P95 Gecikme (ms)</th>
              </tr>
            </thead>
            <tbody>
              {data.edge_benchmark.map((r, i) => (
                <tr key={i} style={{ borderTop: '1px solid #334155' }}>
                  <td style={{ padding: 12 }}>{r.model}</td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.fps.toFixed(2)}</td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.latency_avg_ms.toFixed(1)}</td>
                  <td style={{ padding: 12, textAlign: 'center', color: (r.latency_p95_ms ?? 0) > 500 ? '#ef4444' : '#10b981' }}>
                    {r.latency_p95_ms?.toFixed(1) ?? '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {/* Normal Benchmark Tablosu */}
      {data.benchmark && data.benchmark.length > 0 && (
        <section style={{ marginTop: 32 }}>
          <h3>Normal CPU Benchmark</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse', background: '#1e293b', borderRadius: 8 }}>
            <thead>
              <tr style={{ background: '#334155' }}>
                <th style={{ padding: 12, textAlign: 'left' }}>Model</th>
                <th style={{ padding: 12 }}>Boyut (MB)</th>
                <th style={{ padding: 12 }}>FPS</th>
                <th style={{ padding: 12 }}>Ortalama Gecikme (ms)</th>
              </tr>
            </thead>
            <tbody>
              {data.benchmark.map((r, i) => (
                <tr key={i} style={{ borderTop: '1px solid #334155' }}>
                  <td style={{ padding: 12 }}>{r.model}</td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.size_mb?.toFixed(2) ?? '-'}</td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.fps.toFixed(2)}</td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.latency_avg_ms.toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {/* Sınıf Analizi Tablosu */}
      {data.class_analysis && data.class_analysis.length > 0 && (
        <section style={{ marginTop: 32 }}>
          <h3>Sınıf Bazında Doğruluk (Küçük Nesne Analizi)</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse', background: '#1e293b', borderRadius: 8 }}>
            <thead>
              <tr style={{ background: '#334155' }}>
                <th style={{ padding: 12, textAlign: 'left' }}>Sınıf</th>
                <th style={{ padding: 12 }}>Boyut Grubu</th>
                <th style={{ padding: 12 }}>mAP50</th>
                <th style={{ padding: 12 }}>Örnek Sayısı</th>
              </tr>
            </thead>
            <tbody>
              {data.class_analysis.map((r, i) => (
                <tr key={i} style={{ borderTop: '1px solid #334155' }}>
                  <td style={{ padding: 12 }}>{r.class}</td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.size_group}</td>
                  <td style={{
                    padding: 12, textAlign: 'center', fontWeight: 'bold',
                    color: r.mAP50 < 0.15 ? '#ef4444' : r.mAP50 > 0.5 ? '#10b981' : '#eab308',
                  }}>
                    {r.mAP50.toFixed(3)}
                  </td>
                  <td style={{ padding: 12, textAlign: 'center' }}>{r.instances}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}
