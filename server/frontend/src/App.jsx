import React, { useState, useEffect, useRef } from 'react';

function App() {
  const [ads, setAds] = useState([]);

  // 🛠️ Стейт для фільтрів
  const [filterTitle, setFilterTitle] = useState('');
  const [filterCity, setFilterCity] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterMinPrice, setFilterMinPrice] = useState('');
  const [filterMaxPrice, setFilterMaxPrice] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');

  // 📜 Стейт для пагінації / Нескінченного скролу
  const [visibleCount, setVisibleCount] = useState(50);
  const loaderRef = useRef(null);

  // 👁️ Стейт для модального вікна деталей лоту
  const [selectedAd, setSelectedAd] = useState(null);
  const [showPriceAnalysis, setShowPriceAnalysis] = useState(false);

  // 1. Завантаження початкової бази даних через HTTP
  useEffect(() => {
    fetch('http://localhost:8000/api/ads')
      .then(res => res.json())
      .then(data => setAds(data))
      .catch(err => console.error("Помилка завантаження бази:", err));
  }, []);

  // 2. 🔥 ПІДКЛЮЧЕННЯ WEBSOCKET (З розумною дедуплікацією)
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = (event) => {
      const newAd = JSON.parse(event.data);
      setAds(prevAds => {
        const exists = prevAds.some(ad => ad.id === newAd.id);
        if (exists) {
          return prevAds.map(ad => ad.id === newAd.id ? { ...ad, ...newAd } : ad);
        }
        return [newAd, ...prevAds];
      });
    };

    ws.onclose = () => console.log("WebSocket закрився...");
    return () => ws.close();
  }, []);

  // 3. 📊 Клієнтська фільтрація
  const filteredAds = ads.filter(ad => {
    const matchTitle = filterTitle === '' || (ad.title && ad.title.toLowerCase().includes(filterTitle.toLowerCase()));
    const matchCity = filterCity === '' || (ad.city && ad.city.toLowerCase().includes(filterCity.toLowerCase()));
    const matchType = filterType === 'all' || ad.item_type === filterType;
    
    const priceCleaned = String(ad.price || '').replace(/\s+/g, '').replace(/[^0-9]/g, '');
    const priceNum = parseInt(priceCleaned, 10) || 0;
    
    const matchMinPrice = filterMinPrice === '' || priceNum >= parseInt(filterMinPrice, 10);
    const matchMaxPrice = filterMaxPrice === '' || priceNum <= parseInt(filterMaxPrice, 10);
    const adRisk = ad.seller_risk ? ad.seller_risk.toLowerCase() : 'neutral';
    const matchRisk = filterRisk === 'all' || adRisk === filterRisk;
    
    return matchTitle && matchCity && matchType && matchMinPrice && matchMaxPrice && matchRisk;
  });

  // 4. Скидання ліміту видимих лотів при зміні фільтрів
  useEffect(() => {
    setVisibleCount(50);
  }, [filterTitle, filterCity, filterType, filterMinPrice, filterMaxPrice, filterRisk]);

  // 5. 🕵️‍♂️ Розумний тригер скролу (Intersection Observer API)
  useEffect(() => {
    const currentLoader = loaderRef.current;
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        setVisibleCount(prevCount => prevCount + 50);
      }
    }, { threshold: 1.0 });

    if (currentLoader) {
      observer.observe(currentLoader);
    }

    return () => {
      if (currentLoader) observer.unobserve(currentLoader);
    };
  }, [filteredAds]); 

  const adsToDisplay = filteredAds.slice(0, visibleCount);

  const getRiskStyle = (risk) => {
    const cleanRisk = risk ? risk.toLowerCase() : '';
    if (cleanRisk === 'safe') return { backgroundColor: '#d4edda', color: '#155724', padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold' };
    if (cleanRisk === 'suspicious') return { backgroundColor: '#f8d7da', color: '#721c24', padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold' };
    return { backgroundColor: '#fff3cd', color: '#856404', padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold' };
  };

  const openModal = (ad) => {
    setSelectedAd(ad);
    setShowPriceAnalysis(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#f4f6f9', minHeight: '100vh', textAlign: 'left' }}>
      <h1 style={{ color: '#1e293b' }}>⚙️ HARDWARE INTELLIGENCE PRO DASHBOARD</h1>
      <p style={{ color: '#64748b' }}>
        Всього в пам'яті: <b>{ads.length}</b> лотів | 
        Знайдено за фільтрами: <b>{filteredAds.length}</b> | 
        Відображено на екрані: <b>{Math.min(visibleCount, filteredAds.length)}</b>
      </p>
      
      <hr style={{ borderColor: '#cbd5e1' }} />

      {/* 🛠️ ПАНЕЛЬ ФІЛЬТРІВ */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '15px', flexWrap: 'wrap', backgroundColor: '#fff', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
        <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', fontSize: '13px', color: '#475569' }}>
          <b>Пошук назви:</b>
          <input type="text" placeholder="RTX 3060..." value={filterTitle} onChange={(e) => setFilterTitle(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1' }} />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', fontSize: '13px', color: '#475569' }}>
          <b>Місто:</b>
          <input type="text" placeholder="Франківськ" value={filterCity} onChange={(e) => setFilterCity(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1' }} />
        </label>

        {/* 🔥 РОЗШИРЕНИЙ ФІЛЬТР КАТЕГОРІЙ */}
        <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', fontSize: '13px', color: '#475569' }}>
          <b>Тип заліза:</b>
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1' }}>
            <option value="all">Усе залізо</option>
            <option value="gpu">GPU (Відеокарти)</option>
            <option value="cpu">CPU (Процесори)</option>
            <option value="pc">PC (Готові ПК)</option>
            <option value="mb">MB (Материнські плати)</option>
            <option value="psu">PSU (Блоки живлення)</option>
            <option value="ssd">SSD накопичувачі</option>
            <option value="hdd">HDD диски</option>
          </select>
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', fontSize: '13px', color: '#475569' }}>
          <b>Ціна від:</b>
          <input type="number" placeholder="Від" value={filterMinPrice} onChange={(e) => setFilterMinPrice(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1', width: '90px' }} />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', fontSize: '13px', color: '#475569' }}>
          <b>Ціна до:</b>
          <input type="number" placeholder="До" value={filterMaxPrice} onChange={(e) => setFilterMaxPrice(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1', width: '90px' }} />
        </label>

        <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', fontSize: '13px', color: '#475569' }}>
          <b>Аудит продавця:</b>
          <select value={filterRisk} onChange={(e) => setFilterRisk(e.target.value)} style={{ padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1' }}>
            <option value="all">Усі</option>
            <option value="safe">🟢 SAFE</option>
            <option value="neutral">🟡 NEUTRAL</option>
            <option value="suspicious">🔴 SUSPICIOUS</option>
          </select>
        </label>
      </div>

      {/* 🛍️ ТАБЛИЦЯ ОГОЛОШЕНЬ */}
      <table border="0" cellPadding="12" style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#fff', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 2px 5px rgba(0,0,0,0.05)' }}>
        <thead>
          <tr style={{ backgroundColor: '#f1f5f9', borderBottom: '2px solid #e2e8f0' }}>
            <th>Фото</th>
            <th>Назва лоту (Клік для деталей)</th>
            <th>Категорія</th>
            <th>Ціна</th>
            <th>Місто</th>
            <th>Надійність</th>
            <th>Дія</th>
          </tr>
        </thead>
        <tbody>
          {adsToDisplay.map((ad) => (
            <tr key={ad.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
              <td>
                {ad.photo_url && ad.photo_url !== 'Невідомо' ? (
                  <img src={ad.photo_url} alt="Залізо" width="55" style={{ borderRadius: '6px' }} />
                ) : ("Ні")}
              </td>
              <td style={{ cursor: 'pointer', color: '#3b82f6', fontWeight: '600' }} onClick={() => openModal(ad)}>
                {ad.title}
              </td>
              <td>
                <span style={{ fontSize: '11px', fontWeight: 'bold', backgroundColor: '#eff6ff', color: '#1d4ed8', padding: '3px 6px', borderRadius: '4px' }}>
                  {ad.item_type?.toUpperCase()}
                </span>
              </td>
              <td style={{ color: '#16a34a', fontWeight: 'bold' }}>
                {Number(ad.price).toLocaleString('uk-UA')} грн
              </td>
              <td>{ad.city || "Невідомо"}</td>
              <td><span style={getRiskStyle(ad.seller_risk)}>{ad.seller_risk?.toUpperCase()}</span></td>
              <td><a href={ad.url} target="_blank" rel="noreferrer" style={{ padding: '5px 10px', backgroundColor: '#f1f5f9', borderRadius: '4px', textDecoration: 'none', color: '#334155', fontSize: '12px', fontWeight: '500' }}>OLX ↗</a></td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* МАРКЕР НЕКІНЧЕННОГО СКРОЛУ */}
      {filteredAds.length > visibleCount && (
        <div ref={loaderRef} style={{ height: '40px', display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px 0', color: '#64748b', fontSize: '14px', fontWeight: 'bold' }}>
          ⏳ Завантаження наступних лотів заліза...
        </div>
      )}

      {/* 👁️ МОДАЛЬНЕ ВІКНО */}
      {selectedAd && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', backgroundColor: 'rgba(15, 23, 42, 0.4)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div style={{ width: '1000px', height: '880px', backgroundColor: '#f8fafc', borderRadius: '16px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)', display: 'flex', position: 'relative', overflow: 'hidden', fontFamily: 'sans-serif' }}>
            
            <button onClick={() => setSelectedAd(null)} style={{ position: 'absolute', top: '15px', right: '15px', zIndex: 11, border: 'none', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '50%', width: '32px', height: '32px', cursor: 'pointer', fontWeight: 'bold', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              ✕
            </button>

            {/* ЛІВА ЧАСТИНА: Фото + Основне + Опис */}
            <div style={{ flex: 1, padding: '25px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px', borderRight: '1px solid #e2e8f0' }}>
              <h2 style={{ margin: 0, fontSize: '20px', color: '#0f172a' }}>📑 Деталі оголошення</h2>
              
              <div style={{ width: '100%', height: '450px', backgroundColor: '#0f172a', borderRadius: '12px', display: 'flex', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
                {selectedAd.photo_url && selectedAd.photo_url !== 'Невідомо' ? (
                  <img src={selectedAd.photo_url} alt="Залізо" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                ) : (
                  <b style={{ color: '#94a3b8' }}>Фото відсутнє</b>
                )}
              </div>

              <div style={{ backgroundColor: '#ffffff', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
                <h3 style={{ margin: '0 0 15px 0', fontSize: '16px', color: '#1e293b', borderBottom: '2px solid #f1f5f9', paddingBottom: '8px' }}>📋 Основні параметри</h3>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div style={{ backgroundColor: '#f8fafc', padding: '12px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '20px' }}>🏷️</span>
                    <div>
                      <small style={{ color: '#64748b', display: 'block', fontSize: '11px' }}>Назва лоту</small>
                      <b style={{ color: '#334155', fontSize: '13px' }}>{selectedAd.title}</b>
                    </div>
                  </div>
                  <div style={{ backgroundColor: '#f8fafc', padding: '12px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '20px' }}>💰</span>
                    <div>
                      <small style={{ color: '#64748b', display: 'block', fontSize: '11px' }}>Ціна продажу</small>
                      <b style={{ color: '#16a34a', fontSize: '14px' }}>{Number(selectedAd.price).toLocaleString('uk-UA')} грн</b>
                    </div>
                  </div>
                  <div style={{ backgroundColor: '#f8fafc', padding: '12px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '20px' }}>📍</span>
                    <div>
                      <small style={{ color: '#64748b', display: 'block', fontSize: '11px' }}>Локація ринку</small>
                      <b style={{ color: '#334155', fontSize: '13px' }}>{selectedAd.city || "Невідомо"}</b>
                    </div>
                  </div>
                  <div style={{ backgroundColor: '#f8fafc', padding: '12px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '20px' }}>⚡</span>
                    <div>
                      <small style={{ color: '#64748b', display: 'block', fontSize: '11px' }}>Категорія товару</small>
                      <b style={{ color: '#1d4ed8', fontSize: '13px' }}>{selectedAd.item_type ? selectedAd.item_type.toUpperCase() : "UNKNOWN"}</b>
                    </div>
                  </div>
                </div>
              </div>

              <div style={{ backgroundColor: '#ffffff', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0', textAlign: 'left' }}>
                <h3 style={{ margin: '0 0 10px 0', fontSize: '15px', color: '#1e293b' }}>📄 Текст опису з OLX</h3>
                <p style={{ margin: 0, fontSize: '13px', color: '#334155', lineHeight: '1.5', whiteSpace: 'pre-line', maxHeight: '180px', overflowY: 'auto', backgroundColor: '#f8fafc', padding: '12px', borderRadius: '8px' }}>
                  {selectedAd.description || "Текстовий опис комплектуючих відсутній."}
                </p>
              </div>
            </div>

            {/* ПРАВА ЧАСТИНА: Продавець + Кнопка аналізу ціни */}
            <div style={{ width: '340px', backgroundColor: '#ffffff', padding: '25px', display: 'flex', flexDirection: 'column', gap: '20px', boxShadow: '-2px 0 10px rgba(0,0,0,0.02)' }}>
              <div style={{ backgroundColor: '#f8fafc', border: '1px solid #e2e8f0', padding: '18px', borderRadius: '12px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <h3 style={{ margin: 0, fontSize: '16px', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px' }}>👤 Контакти продавця</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '12px' }}>
                  <div><span style={{ color: '#64748b' }}>Ім'я на OLX:</span> <b style={{ color: '#1e293b', float: 'right' }}>{selectedAd.seller_name || "Невідомо"}</b></div>
                  <div><span style={{ color: '#64748b' }}>Справжніх угод:</span> <b style={{ color: '#1e293b', float: 'right' }}>{selectedAd.seller_successful_deals} шт.</b></div>
                  <div><span style={{ color: '#64748b' }}>Рейтинг аккаунта:</span> <b style={{ color: '#1e293b', float: 'right' }}>{selectedAd.seller_rating}</b></div>
                  <div><span style={{ color: '#64748b' }}>Рік реєстрації:</span> <b style={{ color: '#1e293b', float: 'right' }}>{selectedAd.seller_created_at || "Чистий"} р.</b></div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
                    <span style={{ color: '#64748b' }}>Аудит системи:</span>
                    <span style={getRiskStyle(selectedAd.seller_risk)}>{selectedAd.seller_risk ? selectedAd.seller_risk.toUpperCase() : 'NEUTRAL'}</span>
                  </div>
                </div>
                <a href={selectedAd.url} target="_blank" rel="noreferrer" style={{ display: 'block', textAlign: 'center', padding: '10px', backgroundColor: '#0f172a', color: '#ffffff', borderRadius: '8px', textDecoration: 'none', fontSize: '13px', fontWeight: 'bold', marginTop: '5px' }}>
                  Відкрити оригінал лоту ↗
                </a>
              </div>

              {/* 🔥 КНОПКА ТА БЛОК АНАЛІЗУ ЦІНИ (ВИПРАВЛЕНО) */}
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <button 
                  onClick={() => setShowPriceAnalysis(!showPriceAnalysis)} 
                  style={{ 
                    width: '100%', 
                    padding: '12px', 
                    backgroundColor: '#2563eb', 
                    color: '#ffffff', 
                    border: 'none', 
                    borderRadius: '8px', 
                    fontSize: '13px', 
                    fontWeight: 'bold', 
                    cursor: 'pointer' 
                  }}
                >
                  {showPriceAnalysis ? "📊 Сховати аналіз ціни" : "📊 Показати аналіз ціни заліза"}
                </button>

                {showPriceAnalysis && (
                  <div style={{ backgroundColor: '#f0fdf4', border: '1px solid #bbf7d0', padding: '15px', borderRadius: '12px', fontSize: '12px', display: 'flex', flexDirection: 'column', gap: '8px', textAlign: 'left' }}>
                    <h4 style={{ margin: '0 0 6px 0', color: '#166534', fontSize: '13px' }}>📋 Аналітика маржі комплектуючих:</h4>
                    
                    <div style={{ borderBottom: '1px dashed #d1fae5', paddingBottom: '6px', display: 'flex', justifyContent: 'space-between' }}>
                      <span>⚖️ Собівартість деталей:</span>
                      <b>
                        {selectedAd.estimated_fair_price !== null && selectedAd.estimated_fair_price !== undefined
                          ? `${Number(selectedAd.estimated_fair_price).toLocaleString('uk-UA')} грн`
                          : "Не обраховано"}
                      </b>
                    </div>

                    <div style={{ borderBottom: '1px dashed #d1fae5', paddingBottom: '6px', display: 'flex', justifyContent: 'space-between' }}>
                      <span>🥊 Ринок конкурентів:</span>
                      <b>
                        {selectedAd.competitor_price !== null && selectedAd.competitor_price !== undefined
                          ? `${Number(selectedAd.competitor_price).toLocaleString('uk-UA')} грн`
                          : "Унікальна"}
                      </b>
                    </div>

                    {selectedAd.saving_uah !== null && selectedAd.saving_uah !== undefined ? (
                      <div style={{ 
                        fontWeight: 'bold', 
                        color: selectedAd.saving_uah >= 0 ? '#166534' : '#991b1b', 
                        marginTop: '6px', 
                        fontSize: '12px', 
                        backgroundColor: selectedAd.saving_uah >= 0 ? '#dcfce7' : '#fee2e2', 
                        padding: '8px', 
                        borderRadius: '6px', 
                        textAlign: 'center' 
                      }}>
                        {selectedAd.saving_uah >= 0 
                          ? `🔥 Профіт: +${Number(selectedAd.saving_uah).toLocaleString('uk-UA')} грн (${selectedAd.saving_percent}%)` 
                          : `❌ Оверпрайс: ${Number(selectedAd.saving_uah).toLocaleString('uk-UA')} грн (${selectedAd.saving_percent}%)`}
                      </div>
                    ) : (
                      <div style={{ color: '#64748b', fontSize: '11px', textAlign: 'center', marginTop: '4px' }}>
                        ⏳ Оцінку маржі ще не проведено
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

export default App;