from abc import ABC, abstractmethod

class Car(ABC):
    def __init__(self, brand, model, color):
        self.brand = brand
        self.model = model
        self.color = color

    def info(self):
        return f"{self.brand} {self.model} ({self.color})"

    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def stop_engine(self):
        pass


class CombustionCar(Car):
    def start_engine(self):
        print(f"{self.brand} {self.model} engine started with a roar!")

    def stop_engine(self):
        print(f"{self.brand} {self.model} engine stopped.")


class ElectricCar(Car):
    def __init__(self, brand, model, color, battery_capacity):
        super().__init__(brand, model, color)
        self.battery_capacity = battery_capacity

    def start_engine(self):
        print(f"{self.brand} {self.model} engine started silently!")

    def stop_engine(self):
        print(f"{self.brand} {self.model} engine stopped.")
    
    def charge(self):
        print(f"{self.brand} {self.model} is charging. Battery capacity: {self.battery_capacity} kWh.")


if __name__ == "__main__":
    car = ElectricCar("Toyota", "Corolla", "red", 75)
    car.start_engine()
    car.stop_engine()
    car.charge()