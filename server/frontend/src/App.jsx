import React, { useState, useEffect, useMemo } from 'react';

// Легка локальна SVG-заглушка замість неефективного зовнішнього сервісу
const PLACEHOLDER_IMG = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='200' viewBox='0 0 300 200'><rect width='100%' height='100%' fill='%23e2e8f0'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='16' fill='%2364748b'>Немає фото</text></svg>";

// Компонент для безпечного завантаження картинок (перехоплює 404 та помилки CDN)
function SafeImage({ src, alt, style, onClick }) {
  const [imgSrc, setImgSrc] = useState(src || PLACEHOLDER_IMG);

  useEffect(() => {
    setImgSrc(src && src !== 'Невідомо' ? src : PLACEHOLDER_IMG);
  }, [src]);

  return (
    <img
      src={imgSrc}
      alt={alt}
      style={style}
      onClick={onClick}
      onError={() => {
        if (imgSrc !== PLACEHOLDER_IMG) {
          setImgSrc(PLACEHOLDER_IMG); // Безпечна заміна при 404 помилці OLX
        }
      }}
    />
  );
}

// ==========================================
// 1. КОМПОНЕНТ ДЕТАЛЬНОГО МОДАЛЬНОГО ВІКНА
// ==========================================
function ModalDetail({ ad, onClose }) {
  if (!ad) return null;

  const allPhotosList = useMemo(() => {
    const list = [];
    const pushIfValid = (url) => {
      if (url && typeof url === 'string' && url !== 'Невідомо' && !list.includes(url)) {
        list.push(url);
      }
    };

    pushIfValid(ad.photo_url);

    const parsePhotosField = (field) => {
      if (!field) return;
      if (Array.isArray(field)) {
        field.forEach(pushIfValid);
      } else if (typeof field === 'string') {
        try {
          const parsed = JSON.parse(field);
          if (Array.isArray(parsed)) parsed.forEach(pushIfValid);
        } catch {
          field.split(',').forEach(item => pushIfValid(item.trim()));
        }
      }
    };

    parsePhotosField(ad.photos);
    parsePhotosField(ad.all_photos);

    return list.length > 0 ? list : [PLACEHOLDER_IMG];
  }, [ad]);

  const [activePhotoIdx, setActivePhotoIdx] = useState(0);

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button style={styles.closeButton} onClick={onClose}>✕</button>

        <div style={styles.header}>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '8px', flexWrap: 'wrap' }}>
            <span style={styles.typeBadge}>{(ad.item_type || 'Залізо').toUpperCase()}</span>
            {ad.pc_category && ad.pc_category !== 'uncategorized' && (
              <span style={styles.catBadge}>{ad.pc_category}</span>
            )}
            {ad.has_ban_word === 1 && (
              <span style={styles.banBadge}>⚠️ Знайдено дефект / бан-слово</span>
            )}
          </div>
          <h2 style={styles.modalTitle}>{ad.title}</h2>
          <div style={styles.priceRow}>
            <span style={styles.mainPrice}>{ad.price?.toLocaleString()} грн</span>
            {ad.seller_price_clean && ad.seller_price_clean !== ad.price && (
              <span style={styles.cleanPrice}>(Чиста ціна: {ad.seller_price_clean} грн)</span>
            )}
          </div>
        </div>

        <div style={styles.bodyGrid}>
          <div style={styles.leftCol}>
            <div style={styles.mainImageWrapper}>
              <SafeImage 
                src={allPhotosList[activePhotoIdx]} 
                alt="Фото лоту" 
                style={styles.mainImage} 
              />
              <div style={styles.photoCounter}>
                {activePhotoIdx + 1} / {allPhotosList.length}
              </div>
            </div>

            {allPhotosList.length > 1 && (
              <div style={styles.thumbGrid}>
                {allPhotosList.map((url, idx) => (
                  <SafeImage
                    key={idx}
                    src={url}
                    alt={`Мініатюра ${idx + 1}`}
                    style={{
                      ...styles.thumb,
                      borderColor: activePhotoIdx === idx ? '#2563eb' : 'transparent'
                    }}
                    onClick={() => setActivePhotoIdx(idx)}
                  />
                ))}
              </div>
            )}

            <div style={styles.card}>
              <h4 style={styles.sectionTitle}>📝 Повний опис з OLX</h4>
              <div style={styles.descriptionBox}>{ad.description || "Опис відсутній..."}</div>
            </div>
          </div>

          <div style={styles.rightCol}>
            <div style={styles.card}>
              <h4 style={styles.sectionTitle}>📈 Оцінка вартості та вигоди</h4>
              <div style={styles.dataGrid}>
                <div>
                  <span style={styles.label}>Статус угоди:</span>
                  <div style={getDealStatusStyle(ad.deal_status)}>
                    {(ad.deal_status || 'unknown').toUpperCase()}
                  </div>
                </div>
                <div>
                  <span style={styles.label}>Чиста вигода:</span>
                  <div style={{ ...styles.value, color: (ad.saving_uah || 0) > 0 ? '#16a34a' : '#dc2626' }}>
                    {ad.saving_uah ? `${ad.saving_uah > 0 ? '+' : ''}${ad.saving_uah} грн` : '0 грн'} 
                    {ad.saving_percent ? ` (${ad.saving_percent}%)` : ''}
                  </div>
                </div>
                <div>
                  <span style={styles.label}>Справедлива ціна деталей:</span>
                  <div style={styles.value}>{ad.estimated_fair_price ? `${ad.estimated_fair_price} грн` : '—'}</div>
                </div>
                <div>
                  <span style={styles.label}>Ціна конкурентів:</span>
                  <div style={styles.value}>{ad.competitor_price ? `${ad.competitor_price} грн` : '—'}</div>
                </div>
              </div>
            </div>

            <div style={styles.card}>
              <h4 style={styles.sectionTitle}>🖥️ Характеристики та Детекція</h4>
              <div style={styles.dataGrid}>
                <div>
                  <span style={styles.label}>Залізо / Сокет:</span>
                  <div style={styles.value}>{ad.component_name || '—'} {ad.socket ? `(${ad.socket})` : ''}</div>
                </div>
                <div>
                  <span style={styles.label}>Місто:</span>
                  <div style={styles.value}>📍 {ad.city || 'Не вказано'}</div>
                </div>
                <div>
                  <span style={styles.label}>Розпізнаний GPU:</span>
                  <div style={styles.value}>
                    {ad.gpu_detected || '—'} 
                    {ad.gpu_market_price ? ` (~${ad.gpu_market_price} грн)` : ''}
                  </div>
                </div>
                <div>
                  <span style={styles.label}>Розпізнаний CPU:</span>
                  <div style={styles.value}>
                    {ad.cpu_detected || '—'} 
                    {ad.cpu_market_price ? ` (~${ad.cpu_market_price} грн)` : ''}
                  </div>
                </div>
              </div>
            </div>

            <div style={styles.card}>
              <h4 style={styles.sectionTitle}>👤 Дані продавця (OLX Seller)</h4>
              <div style={styles.dataGrid}>
                <div>
                  <span style={styles.label}>Ім'я продавця:</span>
                  <div style={styles.value}>{ad.seller_name || 'Невідомо'}</div>
                </div>
                <div>
                  <span style={styles.label}>Seller ID:</span>
                  <div style={styles.value}>{ad.seller_id || '—'}</div>
                </div>
                <div>
                  <span style={styles.label}>Тип акаунту:</span>
                  <div style={styles.value}>{ad.seller_type || 'Приватна особа'}</div>
                </div>
                <div>
                  <span style={styles.label}>Рік реєстрації:</span>
                  <div style={styles.value}>{ad.seller_created_at || '—'}</div>
                </div>
                <div>
                  <span style={styles.label}>Успішні угоди:</span>
                  <div style={styles.value}>{ad.seller_successful_deals ?? '0'} шт.</div>
                </div>
                <div>
                  <span style={styles.label}>Рейтинг:</span>
                  <div style={styles.value}>{ad.seller_rating || 'Немає оцінок'}</div>
                </div>
                <div style={{ gridColumn: 'span 2' }}>
                  <span style={styles.label}>Рівень ризику:</span>
                  <div style={getRiskStyle(ad.seller_risk_score)}>
                    {(ad.seller_risk_score || 'neutral').toUpperCase()}
                  </div>
                </div>
              </div>
            </div>

            <div style={styles.cardLight}>
              <h4 style={styles.sectionTitle}>⚙️ Часові мітки та ID</h4>
              <div style={styles.dataGrid}>
                <div>
                  <span style={styles.label}>ID в БД / OLX AD ID:</span>
                  <div style={styles.smallValue}>#{ad.id} / #{ad.ad_id || '—'}</div>
                </div>
                <div>
                  <span style={styles.label}>Статус системний:</span>
                  <div style={styles.smallValue}>
                    {ad.status} {ad.deactivated_at ? `(до ${ad.deactivated_at})` : ''}
                  </div>
                </div>
                <div>
                  <span style={styles.label}>Дата публікації OLX:</span>
                  <div style={styles.smallValue}>{ad.created_at_olx || '—'}</div>
                </div>
                <div>
                  <span style={styles.label}>Останній підйом:</span>
                  <div style={styles.smallValue}>{ad.last_refresh_time || '—'}</div>
                </div>
              </div>
            </div>

            <a href={ad.url} target="_blank" rel="noreferrer" style={styles.olxLink}>
              Відкрити оригінальне оголошення на OLX ↗
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// 2. ГОЛОВНИЙ КОМПОНЕНТ ДОДАТКУ
// ==========================================
function App() {
  const [ads, setAds] = useState([]);
  const [selectedAd, setSelectedAd] = useState(null);

  const [filterCity, setFilterCity] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterMaxPrice, setFilterMaxPrice] = useState('');
  const [filterDate, setFilterDate] = useState('');
  const [filterDeal, setFilterDeal] = useState('all');

  useEffect(() => {
    fetch('http://localhost:8000/api/ads')
      .then(res => res.json())
      .then(data => setAds(data))
      .catch(err => console.error("Помилка завантаження бази:", err));
  }, []);

  // Виправлена робота WebSocket для запобігання фальшивих закриттів у React Strict Mode
  useEffect(() => {
    let ws;
    let timer;

    const connect = () => {
      ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onmessage = (event) => {
        try {
          const newAd = JSON.parse(event.data);
          setAds(prevAds => [newAd, ...prevAds]);
        } catch (e) {
          console.error("Помилка WS:", e);
        }
      };

      ws.onclose = () => {
        timer = setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      clearTimeout(timer);
      if (ws) {
        ws.onclose = null; // Скасовуємо автореконнект при розмотуванні
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
      }
    };
  }, []);

  const filteredAds = useMemo(() => {
    return ads.filter(ad => {
      const matchCity = !filterCity || (ad.city && ad.city.toLowerCase().includes(filterCity.toLowerCase()));
      const matchType = filterType === 'all' || ad.item_type === filterType;
      const matchPrice = !filterMaxPrice || (ad.price && ad.price <= parseInt(filterMaxPrice, 10));
      const matchDate = !filterDate || (ad.created_at_olx && ad.created_at_olx.toLowerCase().includes(filterDate.toLowerCase()));
      const matchDeal = filterDeal === 'all' || ad.deal_status === filterDeal;

      return matchCity && matchType && matchPrice && matchDate && matchDeal;
    });
  }, [ads, filterCity, filterType, filterMaxPrice, filterDate, filterDeal]);

  return (
    <div style={styles.appContainer}>
      <header style={styles.header}>
        <h1 style={{ margin: 0, fontSize: '24px' }}>⚡ DASHBOARD ПЕРЕКУПА</h1>
        <div style={styles.headerStats}>
          <span>Усього: <b>{ads.length}</b></span>
          <span>Показано: <b>{filteredAds.length}</b></span>
        </div>
      </header>

      <div style={styles.filterBar}>
        <input 
          type="text" 
          placeholder="Пошук за містом..." 
          value={filterCity} 
          onChange={(e) => setFilterCity(e.target.value)} 
          style={styles.input}
        />
        <select value={filterType} onChange={(e) => setFilterType(e.target.value)} style={styles.input}>
          <option value="all">Усі категорії</option>
          <option value="gpu">Відеокарти (GPU)</option>
          <option value="cpu">Процесори (CPU)</option>
          <option value="pc">Готові ПК</option>
        </select>
        <input 
          type="number" 
          placeholder="Макс. ціна (грн)" 
          value={filterMaxPrice} 
          onChange={(e) => setFilterMaxPrice(e.target.value)} 
          style={styles.input}
        />
        <input 
          type="text" 
          placeholder="Дата (напр. 11 липня)" 
          value={filterDate} 
          onChange={(e) => setFilterDate(e.target.value)} 
          style={styles.input}
        />
        <select value={filterDeal} onChange={(e) => setFilterDeal(e.target.value)} style={styles.input}>
          <option value="all">Усі угоди</option>
          <option value="super">🔥 Super Deal</option>
          <option value="good">✅ Good Deal</option>
          <option value="overpriced">❌ Overpriced</option>
        </select>
      </div>

      {filteredAds.length === 0 ? (
        <div style={styles.emptyState}>За вашим запитом нічого не знайдено 🔍</div>
      ) : (
        <div style={styles.grid}>
          {filteredAds.map((ad) => (
            <div key={ad.ad_id || ad.id} style={styles.cardItem} onClick={() => setSelectedAd(ad)}>
              <div style={styles.cardImageWrapper}>
                <SafeImage 
                  src={ad.photo_url} 
                  alt={ad.title} 
                  style={styles.cardImage} 
                />
                <span style={styles.cardCategoryBadge}>{ad.item_type?.toUpperCase()}</span>
                {ad.saving_percent > 0 && (
                  <span style={styles.cardSavingBadge}>+{ad.saving_percent}%</span>
                )}
              </div>
              <div style={styles.cardBody}>
                <h3 style={styles.cardTitle} title={ad.title}>{ad.title}</h3>
                <div style={styles.cardPrice}>{ad.price?.toLocaleString()} грн</div>
                <div style={styles.cardFooter}>
                  <span>📍 {ad.city || 'Н/Д'}</span>
                  <span>{ad.created_at_olx || ad.parsed_date}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <ModalDetail ad={selectedAd} onClose={() => setSelectedAd(null)} />
    </div>
  );
}

// ==========================================
// 3. ДОПОМІЖНІ СТИЛІ
// ==========================================
const getDealStatusStyle = (status) => {
  const base = { fontWeight: 'bold', fontSize: '12px', padding: '2px 6px', borderRadius: '4px', display: 'inline-block' };
  switch(status) {
    case 'super': return { ...base, backgroundColor: '#dcfce7', color: '#15803d' };
    case 'good': return { ...base, backgroundColor: '#e0f2fe', color: '#0369a1' };
    case 'overpriced': return { ...base, backgroundColor: '#fee2e2', color: '#b91c1c' };
    default: return { ...base, backgroundColor: '#f1f5f9', color: '#475569' };
  }
};

const getRiskStyle = (score) => {
  const base = { fontWeight: 'bold', fontSize: '12px', padding: '2px 8px', borderRadius: '4px', display: 'inline-block' };
  switch(score) {
    case 'safe': return { ...base, backgroundColor: '#dcfce7', color: '#16a34a' };
    case 'suspicious': return { ...base, backgroundColor: '#fee2e2', color: '#dc2626' };
    default: return { ...base, backgroundColor: '#fef3c7', color: '#d97706' };
  }
};

const styles = {
  appContainer: {
    padding: '24px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: '#f8fafc',
    minHeight: '100vh',
    color: '#0f172a',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  headerStats: {
    display: 'flex',
    gap: '15px',
    color: '#64748b',
    fontSize: '14px',
  },
  filterBar: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
    gap: '12px',
    marginBottom: '24px',
    backgroundColor: '#fff',
    padding: '16px',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
  },
  input: {
    padding: '10px 14px',
    borderRadius: '8px',
    border: '1px solid #cbd5e1',
    fontSize: '14px',
    outline: 'none',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
    gap: '20px',
  },
  cardItem: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    overflow: 'hidden',
    border: '1px solid #e2e8f0',
    cursor: 'pointer',
    transition: 'transform 0.15s ease',
  },
  cardImageWrapper: {
    position: 'relative',
    width: '100%',
    height: '200px',
    backgroundColor: '#f1f5f9',
  },
  cardImage: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  cardCategoryBadge: {
    position: 'absolute',
    top: '10px', left: '10px',
    backgroundColor: 'rgba(15, 23, 42, 0.8)',
    color: '#fff',
    padding: '3px 6px',
    borderRadius: '4px',
    fontSize: '10px',
    fontWeight: 'bold',
  },
  cardSavingBadge: {
    position: 'absolute',
    top: '10px', right: '10px',
    backgroundColor: '#16a34a',
    color: '#fff',
    padding: '3px 6px',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: 'bold',
  },
  cardBody: {
    padding: '14px',
  },
  cardTitle: {
    margin: '0 0 8px 0',
    fontSize: '15px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  cardPrice: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#16a34a',
    marginBottom: '10px',
  },
  cardFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '12px',
    color: '#64748b',
    borderTop: '1px solid #f1f5f9',
    paddingTop: '8px',
  },
  emptyState: {
    textAlign: 'center',
    padding: '40px',
    color: '#64748b',
  },
  overlay: {
    position: 'fixed',
    top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(15, 23, 42, 0.75)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 9999,
    padding: '20px',
  },
  modal: {
    backgroundColor: '#ffffff',
    borderRadius: '16px',
    maxWidth: '1050px',
    width: '100%',
    maxHeight: '90vh',
    overflowY: 'auto',
    padding: '24px',
    position: 'relative',
  },
  closeButton: {
    position: 'absolute',
    top: '16px', right: '16px',
    border: 'none',
    backgroundColor: '#f1f5f9',
    width: '32px', height: '32px',
    borderRadius: '50%',
    cursor: 'pointer',
    fontSize: '16px',
  },
  header: {
    borderBottom: '1px solid #e2e8f0',
    paddingBottom: '12px',
    marginBottom: '16px',
  },
  modalTitle: {
    margin: '4px 0',
    fontSize: '20px',
  },
  priceRow: {
    display: 'flex',
    alignItems: 'baseline',
    gap: '12px',
  },
  mainPrice: {
    fontSize: '24px',
    fontWeight: '800',
    color: '#16a34a',
  },
  cleanPrice: {
    fontSize: '13px',
    color: '#64748b',
  },
  typeBadge: {
    backgroundColor: '#0f172a',
    color: '#fff',
    padding: '3px 8px',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: 'bold',
  },
  catBadge: {
    backgroundColor: '#e2e8f0',
    color: '#334155',
    padding: '3px 8px',
    borderRadius: '4px',
    fontSize: '11px',
  },
  banBadge: {
    backgroundColor: '#fee2e2',
    color: '#b91c1c',
    padding: '3px 8px',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: 'bold',
  },
  bodyGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
  },
  leftCol: {
    display: 'flex',
    flexDirection: 'column',
    gap: '14px',
  },
  rightCol: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  mainImageWrapper: {
    position: 'relative',
    width: '100%',
    height: '350px',
    backgroundColor: '#0f172a',
    borderRadius: '12px',
    overflow: 'hidden',
  },
  mainImage: {
    width: '100%',
    height: '100%',
    objectFit: 'contain',
  },
  photoCounter: {
    position: 'absolute',
    bottom: '10px', right: '10px',
    backgroundColor: 'rgba(0,0,0,0.6)',
    color: '#fff',
    padding: '3px 8px',
    borderRadius: '4px',
    fontSize: '11px',
  },
  thumbGrid: {
    display: 'flex',
    gap: '8px',
    overflowX: 'auto',
  },
  thumb: {
    width: '56px',
    height: '56px',
    objectFit: 'cover',
    borderRadius: '6px',
    cursor: 'pointer',
    border: '2px solid transparent',
    backgroundColor: '#f1f5f9',
  },
  card: {
    backgroundColor: '#f8fafc',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    padding: '12px',
  },
  cardLight: {
    backgroundColor: '#ffffff',
    border: '1px dashed #cbd5e1',
    borderRadius: '8px',
    padding: '12px',
  },
  sectionTitle: {
    margin: '0 0 8px 0',
    fontSize: '13px',
    color: '#334155',
    borderBottom: '1px solid #e2e8f0',
    paddingBottom: '4px',
  },
  dataGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '8px',
  },
  label: {
    display: 'block',
    fontSize: '11px',
    color: '#64748b',
  },
  value: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#0f172a',
  },
  smallValue: {
    fontSize: '11px',
    color: '#334155',
    fontFamily: 'monospace',
  },
  descriptionBox: {
    backgroundColor: '#fff',
    border: '1px solid #e2e8f0',
    padding: '10px',
    borderRadius: '6px',
    fontSize: '12px',
    lineHeight: '1.4',
    color: '#334155',
    whiteSpace: 'pre-line',
    maxHeight: '150px',
    overflowY: 'auto',
  },
  olxLink: {
    display: 'block',
    textAlign: 'center',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    textDecoration: 'none',
    padding: '10px',
    borderRadius: '8px',
    fontWeight: 'bold',
    fontSize: '13px',
    marginTop: 'auto',
  }
};

export default App;