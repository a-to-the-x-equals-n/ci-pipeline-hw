from datetime import datetime, timedelta

class AirlineSystemManager:
    def __init__(self):
        self.flights = []
        self.passengers = []
        self.bookings = []
        self.crew_members = []

    def add_flight(self, flight_number, origin, destination, departure_time, duration_minutes, aircraft_type):
        flight = {
            'flight_number': flight_number,
            'origin': origin,
            'destination': destination,
            'departure_time': departure_time,
            'arrival_time': departure_time + timedelta(minutes=duration_minutes),
            'aircraft_type': aircraft_type,
            'seats_available': 150
        }
        self.flights.append(flight)
        print(f"Flight {flight_number} added.")

    def register_passenger(self, name, passport_number):
        passenger = {
            'name': name,
            'passport_number': passport_number,
            'registered_on': datetime.now()
        }
        self.passengers.append(passenger)
        print(f"Passenger '{name}' registered.")

    def assign_crew_member(self, name, role, flight_number):
        crew = {
            'name': name,
            'role': role,
            'assigned_flight': flight_number
        }
        self.crew_members.append(crew)
        print(f"Crew member '{name}' assigned to flight {flight_number}.")

    def book_flight(self, passport_number, flight_number):
        passenger = next((p for p in self.passengers if p['passport_number'] == passport_number), None)
        flight = next((f for f in self.flights if f['flight_number'] == flight_number), None)

        if not passenger:
            print("Passenger not found.")
            return
        if not flight:
            print("Flight not found.")
            return
        if flight['seats_available'] <= 0:
            print("No seats available on this flight.")
            return

        booking = {
            'passenger': passenger,
            'flight': flight,
            'booking_date': datetime.now(),
            'seat_number': 151 - flight['seats_available']
        }
        flight['seats_available'] -= 1
        self.bookings.append(booking)
        print(f"Booking successful for {passenger['name']} on flight {flight['flight_number']}.")

    def flight_summary(self, flight_number):
        flight = next((f for f in self.flights if f['flight_number'] == flight_number), None)
        if not flight:
            print("Flight not found.")
            return

        crew = [c for c in self.crew_members if c['assigned_flight'] == flight_number]
        booked_passengers = [b['passenger']['name'] for b in self.bookings if b['flight']['flight_number'] == flight_number]

        print(f"Flight {flight_number} from {flight['origin']} to {flight['destination']}:")
        print(f"Departure: {flight['departure_time']} | Arrival: {flight['arrival_time']}")
        print("Crew Members:")
        for c in crew:
            print(f" - {c['name']} ({c['role']})")
        print("Booked Passengers:")
        for name in booked_passengers:
            print(f" - {name}")

if __name__ == '__main__':
    manager = AirlineSystemManager()
    manager.add_flight("AI101", "New York", "London", datetime(2025, 5, 1, 18, 0), 420, "Boeing 777")
    manager.register_passenger("Alice Johnson", "P1234567")
    manager.register_passenger("Bob Lee", "P2345678")
    manager.assign_crew_member("Captain Morgan", "Pilot", "AI101")
    manager.assign_crew_member("Dana Scott", "Flight Attendant", "AI101")
    manager.book_flight("P1234567", "AI101")
    manager.book_flight("P2345678", "AI101")
    manager.flight_summary("AI101")
