# 📚 API Reference - AgriSense

Referência rápida das principais APIs do sistema.

## 🌱 Sensores

### SoilSensor

```python
sensor = SoilSensor("SOIL_001", (-25.4284, -49.2733), 5)
sensor.start()
data = sensor.read_all()  # moisture, ph, nitrogen, phosphorus, potassium

weather = WeatherSensor("WEATHER_001", (-25.4284, -49.2733), 934.6)
weather.start()
data = weather.read_all()  # temperature, humidity, pressure, wind, etc

WeatherSensor

pythonweather = WeatherSensor("WEATHER_001", (-25.4284, -49.2733), 934.6)
weather.start()
data = weather.read_all()  # temperature, humidity, pressure, wind, etc
```

GPSSensor
pythongps = GPSSensor("GPS_001", (-25.4284, -49.2733), 'RTK')
gps.start()
coords = gps.get_coordinates() # (lat, lon)

🚜 Atuadores
IrrigationSystem
pythonirrigation = IrrigationSystem("IRR_001", zones=4, max_flow_rate=100.0)
irrigation.start(IrrigationMode.AUTOMATIC)
irrigation.irrigate_zone(1, duration_minutes=20.0)

FertilizerSystem
pythonfertilizer = FertilizerSystem("FERT_001", tank_capacity=500.0)
fertilizer.load_fertilizer(FertilizerType.NPK_15_15_15, 300.0)
fertilizer.start()
fertilizer.set_application_rate(80.0)
result = fertilizer.apply(area=5.0)

📡 Protocolos
CANProtocol
pythoncan = CANProtocol("CAN0", CANBaudRate.RATE_250K, 0x17)
can.start()
can.send_sensor_data('temperature', 25.5)
can.send_actuator_command('irrigation', 'start')

ISOBUSSimulator
pythonisobus = ISOBUSSimulator("ISOBUS0")
isobus.start()
isobus.add_device("Trator", 0x00)
isobus.connect_task_controller()
isobus.start_task("Pulverização", {'area': 50.0})

🛠️ Utilitários
DataGenerator
pythonsoil_data = DataGenerator.generate_soil_data(num_samples=200, hours=48)
weather_data = DataGenerator.generate_weather_data(num_samples=200)

AgriLogger
pythonlogger = AgriLogger("AgriSense")
logger.info("Sistema iniciado")
logger.log_irrigation(zone=1, duration=30.0, volume=1350.0)
