import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port in ports:
    print(f"Porta: {port.device}")
    print(f"Descrição: {port.description}")
    print(f"ID: {port.hwid}")
    print(f'Fabricante: {port.manufacturer}')
    print(f"Produto: {port.product}")
    print(f"serial: {port.serial_number}")
    print("-" * 40)
    print(f"{port}")