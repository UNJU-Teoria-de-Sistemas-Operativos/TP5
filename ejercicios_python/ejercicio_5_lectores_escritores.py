import sys
import threading
import time
import random

# Configuración UTF-8 para salida en consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# VARIABLES COMPARTIDAS Y SEMÁFOROS (Algoritmo de Courtois - Lectores/Escritores)
# ============================================================================
# mutex: controla el acceso exclusivo al contador readcounter
mutex = threading.Semaphore(1)

# sem_write: garantiza exclusión mutua para el escritor o el primer/último lector
sem_write = threading.Semaphore(1)
write = sem_write  # Alias por compatibilidad de tests

readcounter = 0

# Objeto o recurso compartido simulado (Base de Datos)
base_de_datos = {
    "version": 1,
    "contenido": "Datos iniciales consistentes del sistema operativo."
}

# Cerrojo exclusivo solo para formatear los logs en consola
print_lock = threading.Lock()

def log(msg):
    with print_lock:
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

# ============================================================================
# PROCESO LECTOR
# ============================================================================
def lector(id_lector, iteraciones=2):
    """
    Protocolo de lectura según la Diapositiva 26:
    1. Proteger readcounter con wait(mutex)
    2. Si es el primer lector (readcounter == 1), bloquear a los escritores con wait(sem_write)
    3. Liberar signal(mutex)
    4. Leer datos concurrentemente con otros lectores
    5. Proteger decremento con wait(mutex)
    6. Si es el último lector (readcounter == 0), liberar signal(sem_write)
    7. Liberar signal(mutex)
    """
    global readcounter
    for _ in range(iteraciones):
        # 1. Entrada a la sección crítica de conteo
        mutex.acquire()
        readcounter += 1
        if readcounter == 1:
            sem_write.acquire()  # El primer lector bloquea a los escritores
        mutex.release()

        # --- SECCIÓN CRÍTICA DE LECTURA (COMPARTIDA) ---
        log(f"📖 Lector {id_lector} LEYENDO datos (v{base_de_datos['version']}) | Lectores activos: {readcounter}")
        time.sleep(random.uniform(0.1, 0.3))
        log(f"✨ Lector {id_lector} terminó de leer.")

        # 2. Salida de la sección crítica de conteo
        mutex.acquire()
        readcounter -= 1
        if readcounter == 0:
            sem_write.release()  # El último lector libera a los escritores
        mutex.release()
        
        # Pausa entre iteraciones
        time.sleep(random.uniform(0.1, 0.2))

# ============================================================================
# PROCESO ESCRITOR
# ============================================================================
def escritor(id_escritor, iteraciones=2):
    """
    Protocolo de escritura según la Diapositiva 26:
    1. Solicitar acceso exclusivo con wait(sem_write)
    2. Modificar el recurso en exclusión mutua total
    3. Liberar signal(sem_write)
    """
    global base_de_datos
    for _ in range(iteraciones):
        log(f"⏳ Escritor {id_escritor} solicitando permiso para escribir...")
        
        # Adquiere el semáforo 'sem_write' para exclusión mutua total
        sem_write.acquire()

        # --- SECCIÓN CRÍTICA DE ESCRITURA (ESTRICTAMENTE EXCLUSIVA) ---
        nueva_version = base_de_datos["version"] + 1
        log(f"✍️️ [EXCLUSIÓN MUTUA] Escritor {id_escritor} MODIFICANDO la BD a versión {nueva_version}...")
        time.sleep(random.uniform(0.2, 0.4))
        base_de_datos["version"] = nueva_version
        base_de_datos["contenido"] = f"Registro actualizado por escritor {id_escritor} a las {time.strftime('%H:%M:%S')}"
        log(f"✅ Escritor {id_escritor} finalizó escritura de versión {nueva_version}.")

        # Libera el semáforo 'sem_write'
        sem_write.release()
        
        # Pausa entre iteraciones
        time.sleep(random.uniform(0.1, 0.3))

if __name__ == "__main__":
    print("=" * 70)
    print("EJERCICIO 5: Lectores y Escritores (Algoritmo de Courtois)")
    print("=" * 70)
    
    hilos = []
    
    for i in range(1, 6):
        t = threading.Thread(target=lector, args=(i,))
        hilos.append(t)
        
    for j in range(1, 3):
        t = threading.Thread(target=escritor, args=(j,))
        hilos.append(t)
        
    random.shuffle(hilos)
    for t in hilos:
        t.start()
        
    for t in hilos:
        t.join()
        
    print("\nSimulación finalizada. Estado final de la BD:", base_de_datos)