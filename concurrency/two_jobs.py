import threading 
import time

def download_a():
    time.sleep(5)
    print("A done")

def download_b():
    time.sleep(2)
    print("B done")

def main():

    a = threading.Thread(target=download_a)
    b = threading.Thread(target=download_b)

    start = time.perf_counter()
    a.start()
    b.start()
    a.join()
    b.join()
    print(f"All done! in {time.perf_counter() - start}s")
    

if __name__ == "__main__":
    main()