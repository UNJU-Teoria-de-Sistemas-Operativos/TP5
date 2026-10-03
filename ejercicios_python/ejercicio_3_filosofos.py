"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 3: La Cena de los Filósofos (Prevención de Deadlock)
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.6 (Problema de los filósofos comensales)
"""

"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 3: La Cena de los Filósofos (Prevención de Deadlock)
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.6 (Problema de los filósofos comensales)
"""

import threading
import time
import random

NUM_FILOSOFOS = 5
# Cada tenedor está representado por un Lock (exclusión mutua)
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

# Variable para contar cuántas veces comió cada filósofo
comidas = [0] * NUM_FILOSOFOS
lock_print = threading.Lock()

def log(msg):
    with lock_print:
        print(msg)

def pensar(id):
    log(f"🤔 Filósofo {id} está pensando...")
    time.sleep(random.uniform(0.1, 0.3))

def comer(id):
    log(f"🍝 Filósofo {id} está comiendo espagueti...")
    comidas[id] += 1
    time.sleep(random.uniform(0.1, 0.3))
    log(f"✨ Filósofo {id} terminó de comer (total comidas: {comidas[id]}).")

def filosofo(id, rondas=2):
    """
    Simula el ciclo de pensar y comer de un filósofo.
    Se utiliza jerarquía de recursos (min/max en IDs de tenedores) para
    romper la condición de espera circular y evitar el Deadlock.
    """
    for _ in range(rondas):
        pensar(id)
        
        # Identificadores de los tenedores adyacentes
        tenedor_izq = id
        tenedor_der = (id + 1) % NUM_FILOSOFOS
        
        # Asignación jerárquica para romper la espera circular (menor ID primero)
        primero = min(tenedor_izq, tenedor_der)
        segundo = max(tenedor_izq, tenedor_der)

        # Adquisición segura de tenedores e invocación directa a comer(id)
        with tenedores[primero]:
            with tenedores[segundo]:
                comer(id)

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación de los Filósofos Comensales (UNJu FI)")
    print("=" * 60)
    
    hilos = []
    for i in range(NUM_FILOSOFOS):
        t = threading.Thread(target=filosofo, args=(i, 2), name=f"Filosofo-{i}")
        hilos.append(t)
        t.start()
        
    for t in hilos:
        t.join()
        
    print("=" * 60)
    print(" Resumen de Comidas:")
    for i, c in enumerate(comidas):
        print(f" - Filósofo {i}: {c} veces comió.")
        
    print(" ¡Simulación completada sin Interbloqueo (Deadlock)!")
    print("=" * 60)
