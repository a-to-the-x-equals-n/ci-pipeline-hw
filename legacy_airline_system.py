# legacy_airline_system.py
from datetime import datetime, timedelta
from typing import Any

def dummy_function_to_force_build():
    pass


def make_entity(**fields: dict) -> dict:
    return {**fields}

# ++ -------------------------------------- METACLASS ----------------------------------
class FreezeClassConstants(type):
    def __new__(mcs: type, name: str, bases: tuple, namespace: dict) -> type:
        constants = {k for k in namespace if k.replace('_', '').isupper()}
        klass = super().__new__(mcs, name, bases, namespace)
        type.__setattr__(klass, '_immutable_attrs', constants)

        # prevent shadowing an instanced value
        def __setattr__(self, name: str, value: Any) -> None:
            # freeze constants at the INSTANCE level
            if name in self.__class__._immutable_attrs:
                raise AttributeError(f'Can\'t shadow a class level constant: \'{name}\'')
            object.__setattr__(self, name, value)
        
        # inject custom setter 
        klass.__setattr__ = __setattr__
        return klass

    def __setattr__(cls, key: str, value: Any):
        # freeze constants at the CLASS level
        if key in cls._immutable_attrs:
            raise AttributeError(f'\'{key}\' is a class level constant.')
        super().__setattr__(key, value)

# ++ -------------------------------------- FLIGHTS ----------------------------------
class FlightManager(metaclass = FreezeClassConstants):
    __slots__ = ['_flights'] # prevent shadowing class constants by using __slots__
    _AVAILABLE_SEATS = 150

    def __init__(self):
        self._flights = []
        
    @property
    def flights(self):
        return self._flights
    
    def add_flight(self, flight_number: str, origin: str, destination: str, departure_time: datetime, duration_minutes: int, aircraft_type: str) -> None:
        flight = make_entity(
            flight_number = flight_number,
            origin = origin,
            destination = destination,
            departure_time = departure_time,
            arrival_time = departure_time + timedelta(minutes = duration_minutes),
            aircraft_type = aircraft_type,
            seats_available = self.__class__._AVAILABLE_SEATS
        )
        self._flights.append(flight)
        print(f'Flight -{flight_number}- added.')

    def get_flight(self, flight_number):
        return next((f for f in self._flights if f['flight_number'] == flight_number), None)
    
    def seats(self, flight: dict):
        flight['seats_available'] -= 1
        

# ++ -------------------------------------- PASSENGERS ----------------------------------
class PassengerManager:
    def __init__(self):
        self._passengers = []

    @property
    def passengers(self):
        return self._passengers
    
    def register_passenger(self, name: str, passport_number: str) -> None:
        passenger = make_entity(
            name = name,
            passport_number = passport_number,
            registered_on = datetime.now()
        )

        self._passengers.append(passenger)
        print(f'Passenger \'{name}\' registered.')
    
    def get_passenger(self, passport_number: str):
        return next((p for p in self._passengers if p['passport_number'] == passport_number), None)

# ++ -------------------------------------- CREW ----------------------------------
class CrewManager:
    def __init__(self):
        self._crew = [] 

    @property
    def crew(self):
        return self._crew
    
    def assign_crew_member(self, name: str, role: str, flight_number: str) -> None:
        crew_member = make_entity(
            name = name,
            role = role,
            assigned_flight = flight_number
        )
        self._crew.append(crew_member)
        print(f'Crew member \'{name}\' assigned to flight: -{flight_number}-.')

    def get_crew(self, flight_number: str):
        return [c for c in self._crew if c['assigned_flight'] == flight_number]

#  -------------------------------------- BOOKING ----------------------------------
class BookingManager(metaclass = FreezeClassConstants):
    __slots__ = ['_bookings']
    _SEAT_NUMBER = 151

    def __init__(self):
        self._bookings = []     

    @property
    def bookings(self):
        return self._bookings  

    def book_flight(self, passport_number: str, flight_number: str, passengers: list, flights: list) -> None:
        # validate passenger and flight
        if not (passenger := passengers.get_passenger(passport_number)):
            return print(f'Passenger not found.')
        if not (flight := flights.get_flight(flight_number)):
            return print(f'Flight not found.')
        if flight['seats_available'] <= 0:
            return print(f'No seats available on this flight.')
            
        booking = make_entity(
            passenger = passenger,
            flight = flight,
            booking_date = datetime.now(),
            seat_number = self.__class__._SEAT_NUMBER - flight['seats_available']
        )
        flights.seats(flight)
        self.bookings.append(booking)
        print(f'Booking successful for "{passenger["name"]}" on flight -{flight["flight_number"]}-.')

    def get_booking(self, flight_number: str):
        return [b['passenger']['name'] for b in self._bookings if b['flight']['flight_number'] == flight_number]

# -------------------------------------- AIRLINE SYSTEM ----------------------------------
class AirlineSystemManager:
    def __init__(self) -> None:
        self._Flights = FlightManager()
        self._Passengers = PassengerManager()
        self._Crew = CrewManager()
        self._Bookings = BookingManager()
        
    @property
    def Flights(self):
        return self._Flights
    @property
    def Passengers(self):
        return self._Passengers
    @property
    def Crew(self):
        return self._Crew
    @property
    def Bookings(self):
        return self._Bookings
    
    def flight_summary(self, flight_number: str) -> None:
        flight = self._Flights.get_flight(flight_number)                # get the flight by number
        crew = self._Crew.get_crew(flight_number)                       # get crew and passengers assigned to this flight
        booked_passengers = self._Bookings.get_booking(flight_number)   # get crew and passengers assigned to this flight

        if not flight:
            return print('Flight not found.')
    
        # print summary info
        print(f'Flight {flight_number} from {flight["origin"]} to {flight["destination"]}:')
        print(f'Departure: {flight["departure_time"]} | Arrival: {flight["arrival_time"]}')
        print('Crew Members:')

        for c in crew:
            print(f' - {c["name"]} ({c["role"]})')
        print('Booked Passengers:')
        for name in booked_passengers:
            print(f' - {name}')


if __name__ == '__main__':

    manager = AirlineSystemManager()

    manager.Flights.add_flight('AI101', 'New York', 'London', datetime(2025, 5, 1, 18, 0), 420, 'Boeing 777')
    manager.Passengers.register_passenger('Alice Johnson', 'P1234567')
    manager.Passengers.register_passenger('Bob Lee', 'P2345678')
    manager.Crew.assign_crew_member('Captain Morgan', 'Pilot', 'AI101')
    manager.Crew.assign_crew_member('Dana Scott', 'Flight Attendant', 'AI101')
    manager.Bookings.book_flight('P1234567', 'AI101', manager.Passengers, manager.Flights)
    manager.Bookings.book_flight('P2345678', 'AI101', manager.Passengers, manager.Flights)

    manager.flight_summary('AI101')