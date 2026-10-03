"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# Mecanismos de sincronización
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.01, 0.05))
        
        sem_tarro_disponible.acquire()  # Espera si el oso está comiendo
        if not simulacion_activa:
            sem_tarro_disponible.release()
            break

        mutex.acquire()                # Entra a la sección crítica

        if tarro_miel < M:
            tarro_miel += 1
            print(f"🐝 Abeja {id_abeja} depositó miel. Tarro: {tarro_miel}/{M}")

            if tarro_miel == M:
                print(f"🐝 Abeja {id_abeja} llenó el tarro y despierta al Oso 🐻!")
                mutex.release()          # Libera mutex ANTES de despertar al oso para evitar Deadlock
                sem_oso.release()        # Despierta al oso
            else:
                mutex.release()
                sem_tarro_disponible.release()  # Habilita a la siguiente abeja
        else:
            mutex.release()
            sem_tarro_disponible.release()

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        sem_oso.acquire()  # Espera bloqueado hasta que el tarro se llene
        
        mutex.acquire()
        print(f"\n🐻 Oso despierta y se come toda la miel! ({tarros_comidos + 1}/{max_tarros})\n")
        tarro_miel = 0
        tarros_comidos += 1
        mutex.release()

        sem_tarro_disponible.release()  # Habilita a las abejas a llenar de nuevo
        time.sleep(0.05)

    # Al terminar las rondas, deshabilita la simulación y libera a las abejas bloqueadas
    simulacion_activa = False
    sem_tarro_disponible.release()

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)

    hilo_oso = threading.Thread(target=oso, args=(2,))
    hilo_oso.start()

    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        t = threading.Thread(target=abeja, args=(i + 1,))
        hilos_abejas.append(t)
        t.start()

    # Esperar a que el oso finalice sus comidas
    hilo_oso.join()

    # Esperar a que todas las abejas terminen de manera limpia
    for t in hilos_abejas:
        t.join()

    print("\n" + "=" * 60)
    print(" Simulación finalizada con éxito.")
    print("=" * 60)



    

