import subprocess
import time
import os
import sys

# Настройки
TARGET_IP = '8.8.8.8'          # Цель: Google Public DNS
INTERVAL_SECONDS = 30          # Интервал отправки
PING_COMMAND = ['ping', '-c', '1', TARGET_IP] # Команда: пинг, 1 пакет, на целевой IP

def run_ping_counter():
    count = 0
    pid = os.getpid()
    
    print(f"🚀 [PID: {pid}] Запуск счетчика PING...")
    print(f"   Цель: {TARGET_IP} | Интервал: {INTERVAL_SECONDS} сек.")
    print("-" * 50)

    while True:
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] === ОТСЧЕТ {count} ===")
            
            # Выполняем команду ping и захватываем вывод
            # 'capture_output=True' - захватывает stdout и stderr
            # 'text=True' - декодирует вывод как текст
            result = subprocess.run(PING_COMMAND, capture_output=True, text=True, timeout=20) 

            if result.returncode == 0:
                # Пакет отправлен и получен успешно.
                # Извлекаем время ответа (латентность) из вывода ping
                # Этот шаг может потребовать небольшой подстройки в зависимости от ОС (Linux/Windows)
                if sys.platform.startswith('linux') or sys.platform == 'darwin':
                    # Для Linux/macOS
                    time_line = [line for line in result.stdout.split('\n') if 'time=' in line]
                    latency = time_line[0].split('time=')[1].split(' ')[0] if time_line else 'N/A'
                    print(f"   ✅ СТАТУС: Успешно. Задержка (latency): {latency} мс")
                else:
                    # Для Windows, вывод может отличаться
                    print(f"   ✅ СТАТУС: Успешно (Детали: {result.stdout.strip().splitlines()[-2]})")
            else:
                # Пакет не получен (таймаут, сеть недоступна и т.п.)
                print(f"   ❌ СТАТУС: Ошибка. Пакет не получен (Код: {result.returncode})")
                
            print("-" * 50)
            
            count += 1
            # Пауза на 30 секунд
            time.sleep(INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            print(f"\n[{pid}] Процесс остановлен пользователем (Ctrl+C).")
            break
        except subprocess.TimeoutExpired:
            print(f"   ❌ СТАТУС: Ошибка. Превышен таймаут выполнения ping.")
            print("-" * 50)
            count += 1
            time.sleep(INTERVAL_SECONDS)
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            break

if __name__ == "__main__":
    run_ping_counter()
