import time
import random
from threading import Thread

products_finished = set() # set to keep track of finished products


class Product:
    def __init__(self, name, machine_list=[], worker_list=[]):
        self.name = name
        self.machines = [0, 1, 2, 3, 4, 5] # machines the product needs to go through
        self.worker = None
        self.machine_list = machine_list # List of all available machines
        self.worker_list = worker_list # List of all available workers

    def __str__(self):
        return f'{self.name} - {self.machines}'

    # Function to find the next machine and worker to work on this product (the worker is chosen randomly)
    def next_machine(self, machine_list):
        global products_finished
        random.shuffle(machine_list) # Randomly shuffle the list of machines
        random.shuffle(self.worker_list) # Randomly shuffle the list of workers
        while True:
            for mach in machine_list:
                if (len(self.machines) != 0) and (mach.number == self.machines[0]) and mach.available == True:
                    for worker in self.worker_list:
                        if (worker.available == True) and (mach.number in worker.skills):
                            self.worker = worker
                            worker.available = False
                            mach.add_product(self) # Assign this product to the machine
                            break
                    break
            if len(self.machines) == 0:
                products_finished.add(self) # Add the finished product to the final set
                break


class Worker:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills # List of skills this worker possesses
        self.available = True # Worker's availability status

    def __str__(self):
        return self.name


class Machine:

    def __init__(self, number, duration, machine_name=''):
        self.number = number
        self.duration = duration
        self.current_worker = []
        self.slot = []
        self.start_time = time.perf_counter()
        self.waitlist = []
        self.machine_name = machine_name
        self.available = True # Machine's availability status

    def __str__(self):
        return f'Machine {self.number} - {self.slot} - {self.current_worker}'
        
    # Function to add a product to the machine
    def add_product(self, Product):

        if self.available == True:
            self.available = False
            self.slot.append(Product)

            elapsed_time = time.perf_counter() - self.start_time
            print(
                f'[{elapsed_time:.6f}min]{Product.worker} is working in {Product.name} on machine {self.number} - {self.machine_name}')

            self.finish_product(Product)

    # Function to simulate product finishing after the duration of the process of the machine
    def finish_product(self, Product):
        time.sleep(self.duration)
        elapsed_time = time.perf_counter() - self.start_time
        prod = self.slot.pop(0)
        self.available = True
        Product.worker.available = True
        prod.machines.remove(self.number)
        prod.next_machine(prod.machine_list)


if __name__ == '__main__':
    # Create a list of machines
    m1 = Machine(0, 2.5, 'Corte 1')
    m2 = Machine(1, 1, 'Marcacao 1')
    m3 = Machine(2, 2, 'Furacao 1')
    m4 = Machine(3, 3.5, 'Dobra 1')
    m5 = Machine(4, 1.5, 'Polimento 1')
    m6 = Machine(5, 4, 'Pintura 1')
    m7 = Machine(0, 2.5, 'Corte 2')
    m8 = Machine(1, 1, 'Marcacao 2')
    m9 = Machine(2, 2, 'Furacao 2')
    m10 = Machine(3, 3.5, 'Dobra 2')
    m11 = Machine(4, 1.5, 'Polimento 2')
    m12 = Machine(5, 4, 'Pintura 2')

    machine_list = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
    
    # Create a list of workers
    luis = Worker('Luis', [0, 1, 2, 3, 5])
    paula = Worker('Paula', [0, 1, 2, 4, 5])
    carlos = Worker('Carlos', [0, 2, 3, 4, 5])
    vera = Worker('Vera',  [0, 1, 2, 4, 5])

    worker_list = [luis, paula, carlos, vera]

    # Create a list of product instances
    instanceNames = ['produto'+str(i) for i in range(1, 100)]
    holder = [Product(name=name, machine_list=machine_list,
                      worker_list=worker_list) for name in instanceNames]
    
    # Create threads to simulate product processing
    threads = [Thread(target=prod.next_machine, args=(machine_list,))
               for prod in holder]

    # Start and join threads
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Calculate and print the elapsed time and the number of finished products
    elapsed_time = time.perf_counter() - m1.start_time
    print(
        f'Production finished in [{elapsed_time:.6f}min]\n{len(products_finished)} finished')
