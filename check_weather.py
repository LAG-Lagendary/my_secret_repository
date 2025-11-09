import requests
import os
import time

# --- НАСТРОЙКИ ---
API_KEY = "ВАШ_КЛЮЧ_OPenWeatherMap"
LATITUDE = "Широта_вашей_локации"    # Например: 7.00
LONGITUDE = "Долгота_вашей_локации"  # Например: 100.00
TEMP_LIMIT = 30.0                    # Критическая внешняя температура в °C
# -----------------

def get_current_temp():
    """Запрашивает текущую температуру воздуха через OpenWeatherMap API."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Вызовет ошибку для плохих статусов (4xx, 5xx)
        data = response.json()
        
        # Получаем температуру
        current_temp = data['main']['temp']
        print(f"Текущая внешняя температура: {current_temp}°C")
        return current_temp
    except Exception as e:
        print(f"Ошибка при запросе погоды: {e}")
        return None

def regulate_mining_load(current_temp):
    """Регулирует нагрузку майнинга в зависимости от температуры."""
    if current_temp is None:
        return

    # Заменяем это на ваши реальные команды из предыдущего ответа
    START_MINING_SCRIPT = "bash /path/to/start_full_mining.sh"
    REDUCE_LOAD_SCRIPT = "bash /path/to/reduce_mining_load.sh" 

    if current_temp >= TEMP_LIMIT:
        print(f"⚠️ Внешняя температура ({current_temp}°C) выше лимита ({TEMP_LIMIT}°C). Снижение нагрузки.")
        # Выполнить скрипт снижения нагрузки (например, Renice или остановка)
        os.system(REDUCE_LOAD_SCRIPT)
    else:
        print(f"✅ Внешняя температура ({current_temp}°C) в норме. Нормальная работа.")
        # Опционально: проверить и восстановить полную нагрузку
        # os.system(START_MINING_SCRIPT) 


if __name__ == "__main__":
    temp = get_current_temp()
    regulate_mining_load(temp)
