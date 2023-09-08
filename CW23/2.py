from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class TemperatureDisplay(Observer):
    def update(self, temperature, humidity):
        print(f"Temperature Display: Temperature is {temperature}°C")


class HumidityDisplay(Observer):
    def update(self, temperature, humidity):
        print(f"Humidity Display: Humidity is {humidity}%")


class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = 0
        self._humidity = 0

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._temperature, self._humidity)

    def set_measurements(self, temperature, humidity):
        self._temperature = temperature
        self._humidity = humidity
        self.notify_observers()


if __name__ == "__main__":
    weather_station = WeatherStation()
    temp_display = TemperatureDisplay()
    humidity_display = HumidityDisplay()

    weather_station.register_observer(temp_display)
    weather_station.register_observer(humidity_display)

    weather_station.set_measurements(25, 60)
    weather_station.set_measurements(30, 55)
