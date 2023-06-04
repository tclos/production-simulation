import time
import random
from threading import Thread

products_finished = set()


class Product:
    def __init__(self, name, machine_list=[], worker_list=[]):
        self.name = name
        self.machines = [0, 1, 2, 3, 4, 5]
        self.worker = None
        self.machine_list = machine_list
        self.worker_list = worker_list

    def __str__(self):
        return f'{self.name} - {self.machines}'

    def next_machine(self, machine_list):
        global products_finished
        random.shuffle(machine_list)
        random.shuffle(self.worker_list)
        while True:
            for mach in machine_list:
                if (len(self.machines) != 0) and (mach.number == self.machines[0]) and mach.available == True:
                    for worker in self.worker_list:
                        if (worker.available == True) and (mach.number in worker.skills):
                            self.worker = worker
                            worker.available = False
                            mach.add_product(self)
                            break
                    break
            if len(self.machines) == 0:
                products_finished.add(self)
                break


class Worker:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.available = True

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
        self.available = True

    def __str__(self):
        return f'Machine {self.number} - {self.slot} - {self.current_worker}'

    def add_product(self, Product):

        if self.available == True:
            self.available = False
            self.slot.append(Product)

            elapsed_time = time.perf_counter() - self.start_time
            print(
                f'[{elapsed_time:.6f}min]{Product.worker} esta trabalhando no {Product.name} na maquina {self.number} - {self.machine_name}')

            self.finish_product(Product)

    def finish_product(self, Product):
        time.sleep(self.duration)
        elapsed_time = time.perf_counter() - self.start_time
        prod = self.slot.pop(0)
        self.available = True
        Product.worker.available = True
        prod.machines.remove(self.number)
        prod.next_machine(prod.machine_list)


if __name__ == '__main__':

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

    luis = Worker('Luis', [0, 1, 2, 3, 5])
    paula = Worker('Paula', [0, 1, 2, 4, 5])
    carlos = Worker('Carlos', [0, 2, 3, 4, 5])
    vera = Worker('Vera',  [0, 1, 2, 4, 5])

    worker_list = [luis, paula, carlos, vera]

    instanceNames = ['produto'+str(i) for i in range(1, 100)]
    holder = [Product(name=name, machine_list=machine_list,
                      worker_list=worker_list) for name in instanceNames]

    threads = [Thread(target=prod.next_machine, args=(machine_list,))
               for prod in holder]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    elapsed_time = time.perf_counter() - m1.start_time
    print(
        f'Producao terminada em [{elapsed_time:.6f}min]\n{len(products_finished)} finalizados')
