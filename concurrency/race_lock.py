import threading 



counter = 0
NUM_INCREMENTS = 100000
lock = threading.Lock()

def increment_counter():
    global counter
    for _ in range(NUM_INCREMENTS):
        with lock:
            counter += 1

def main():
    tasks = []
    for _ in range(10):
        tasks.append(threading.Thread(target=increment_counter))
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    print(counter)




if __name__ == "__main__":
    main()