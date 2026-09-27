# Task 5: Parking Lot
# Build a thread-safe ParkingLot using threading.Condition.
# State
# The class should maintain:
# capacity
# Number of currently occupied spaces
# A threading.Condition
# Methods
# Implement:
# enter(car_id)
# If the parking lot is full, the car must wait.
# Once a space is available, the car enters.
# Print that the car entered.
# Wake up a waiting thread that might now be able to proceed.
# leave(car_id)
# The car leaves.
# Decrease the number of occupied spaces.
# Print that the car left.
# Wake up a waiting car.
# Concurrency setup
# Create:
# A parking lot with capacity 3
# 8 car threads
# Each car should:
# Enter the parking lot
# Stay for a random/brief amount of time using time.sleep()
# Leave
# Restrictions
# Use only:
# threading.Thread
# threading.Condition
# time.sleep()
# Don't use Semaphore, queue.Queue, or executors.

import threading 
import time 
import random 

class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity 
        self.cars = set()
        self.cond = threading.Condition()

    def enter(self, car_id):
        with self.cond:
            while len(self.cars)>= self.capacity:
                print(f"Car {car_id} is waiting to enter the parking lot")
                self.cond.wait() 
            self.cars.add(car_id)
            print(f"Car {car_id} entered the parking lot")
            self.cond.notify_all()

    def leave(self, car_id):
        with self.cond:
            self.cars.remove(car_id)
            print(f"Car {car_id} left the parking lot")
            self.cond.notify_all() 

def enter_and_leave(lot, car):
    lot.enter(car)
    time.sleep(random.random())
    lot.leave(car)


def main():

    lot = ParkingLot(capacity=3)
    tasks = []
    for i in range(8):
        tasks.append(threading.Thread(target=enter_and_leave, args=(lot, i)))
    
    for task in tasks:
        task.start()
    
    for task in tasks:
        task.join()

    

if __name__ == "__main__":
    main()
    