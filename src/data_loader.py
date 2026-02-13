import pandas as pd

def load_and_clean_data(filepath):
    """
    Завантажує дані, автоматично визначає роздільник та проводить глибоку очистку
    для забезпечення стабільної роботи інтерактивних елементів дашборду.
    """
    try:
        # 1. Завантаження з автоматичним визначенням роздільника (кома, крапка з комою, табуляція)
        df = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8')
        
        # 2. Очищення назв колонок (видалення пробілів на початку та в кінці)
        df.columns = [col.strip() for col in df.columns]
        
        # 3. Очищення текстових колонок (Country, Segment, Product_Name, Customer_ID)
        # Це гарантує, що "USA " та "USA" будуть сприйматися як одна країна
        text_cols = ['Country', 'Segment', 'Product_Name', 'Customer_ID']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # 4. Очищення числових колонок
        # Видаляємо пробіли, нерозривні пробіли (\xa0) та знаки валют. 
        # Замінюємо кому на крапку для десяткових значень.
        numeric_cols = ['Units Sold', 'Sales', 'Profit']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str)
                    .str.replace(r'[\s\xa0\$]', '', regex=True)
                    .str.replace(',', '.', regex=False)
                )
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 5. Обробка дати
        # dayfirst=True забезпечує правильне зчитування європейського формату (ДД.ММ.РРРР)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
            
        # Видаляємо рядки, де дата не зчиталася (якщо такі є)
        df = df.dropna(subset=['Date'])
        
        # Сортуємо за датою для коректної побудови часових графіків
        df = df.sort_values('Date')
            
        return df

    except Exception as e:
        # Вивід помилки в консоль для діагностики
        print(f"CRITICAL ERROR in data_loader: {e}")
        return None