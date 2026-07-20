import React, { useState, useEffect } from 'react';

function App() {
  const [ads, setAds] = useState([]); // Усі оголошення
  
  // Стейт для фільтрів
  const [filterCity, setFilterCity] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterMaxPrice, setFilterMaxPrice] = useState('');
  const [filterDate, setFilterDate] = useState('');

  // 1. Завантаження початкової бази даних через HTTP
  useEffect(() => {
    fetch('http://localhost:8000/api/ads')
      .then(res => res.json())
      .then(data => setAds(data))
      .catch(err => console.error("Помилка завантаження бази:", err));
  }, []);

  // 2. 🔥 ПІДКЛЮЧЕННЯ WEBSOCKET (Реалтайм оновлення без F5)
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      const newAd = JSON.parse(event.data);
      console.log("🔥 Прилетіло нове оголошення в реалтаймі!", newAd);
      
      // Додаємо нове оголошення на самий початок списку ads
      setAds(prevAds => [newAd, ...prevAds]);
    };

    ws.onclose = () => console.log("WebSocket закрився, пробуємо перепідключитись...");
    return () => ws.close(); // Закриваємо тунель при виході з сайту
  }, []);

  // 3. 📊 Клієнтська фільтрація масиву оголошень
  const filteredAds = ads.filter(ad => {
    const matchCity = filterCity === '' || (ad.city && ad.city.toLowerCase().includes(filterCity.toLowerCase()));
    const matchType = filterType === 'all' || ad.item_type === filterType;
    const matchPrice = filterMaxPrice === '' || ad.price <= parseInt(filterMaxPrice);
    const matchDate = filterDate === '' || (ad.created_at_olx && ad.created_at_olx.includes(filterDate));
    
    return matchCity && matchType && matchPrice && matchDate;
  });

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1> ДАШБОРД ПЕРЕКУПА (LIVE-ОНОВЛЕННЯ)</h1>
      <p>Всього в пам'яті: <b>{ads.length}</b> лотів | Відображено за фільтрами: <b>{filteredAds.length}</b></p>
      
      <hr />

      {/* 🛠️ ПАНЕЛЬ БАЗОВИХ ФІЛЬТРІВ */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
        <label>
          Фільтр міста: 
          <input 
            type="text" 
            placeholder="Наприклад: Кременчук" 
            value={filterCity} 
            onChange={(e) => setFilterCity(e.target.value)} 
          />
        </label>

        <label>
          Тип заліза: 
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
            <option value="all">Усе залізо</option>
            <option value="gpu">Відеокарти (GPU)</option>
            <option value="cpu">Процесори (CPU)</option>
            <option value="pc">Готові комп'ютери (PC)</option>
          </select>
        </label>

        <label>
          Макс. ціна (грн): 
          <input 
            type="number" 
            placeholder="До..." 
            value={filterMaxPrice} 
            onChange={(e) => setFilterMaxPrice(e.target.value)} 
          />
        </label>

        <label>
          Дата публікації: 
          <input 
            type="text" 
            placeholder="Наприклад: 11 липня" 
            value={filterDate} 
            onChange={(e) => setFilterDate(e.target.value)} 
          />
        </label>
      </div>

      <hr />

      {/* 🛍️ СПИСОК ОГОЛОШЕНЬ */}
      {filteredAds.length === 0 ? (
        <p>Нічого не знайдено за вказаними фільтрами...</p>
      ) : (
        <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th>Фото</th>
              <th>Назва лоту</th>
              <th>Категорія</th>
              <th>Ціна</th>
              <th>Місто</th>
              <th>Дата викладки</th>
              <th>Посилання</th>
            </tr>
          </thead>
          <tbody>
            {filteredAds.map((ad, index) => (
              <tr key={index}>
                <td>
                  {ad.photo_url && ad.photo_url !== 'Невідомо' ? (
                    <img src={ad.photo_url} alt="Залізо" width="80" />
                  ) : (
                    "Без фото"
                  )}
                </td>
                <td><b>{ad.title}</b></td>
                <td>{ad.item_type.toUpperCase()}</td>
                <td style={{ color: 'green', fontWeight: 'bold' }}>{ad.price} грн</td>
                <td>{ad.city}</td>
                <td>{ad.created_at_olx}</td>
                <td><a href={ad.url} target="_blank" rel="noreferrer">Відкрити OLX ↗</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;