# Programa para registrar empleados y analizar horarios de entrada y salida

# Validación de número de empleados
while True:
    try:
        num_empleados = int(input("¿Cuántos empleados vas a introducir? "))
        if num_empleados <= 0:
            print("El número de empleados debe ser positivo.")
            continue
        break
    except ValueError:
        print("Por favor, introduce un número válido.")

# Validación de hora de referencia
while True:
    try:
        hora_referencia = int(input("Introduce una hora de referencia (0–23): "))
        if 0 <= hora_referencia <= 23:
            break
        else:
            print("La hora debe estar entre 0 y 23.")
    except ValueError:
        print("Por favor, introduce un número válido entre 0 y 23.")

contador_entradas = 0
salida_mas_temprana = 24 
empleado_salida_temprana = None


contador = 0
while contador < num_empleados:
    print(f"\nEmpleado {contador + 1}:")
    nombre = input("Nombre del empleado: ")

    try:
        hora_entrada = int(input("Hora de entrada (0–23): "))
        hora_salida = int(input("Hora de salida (0–23): "))

        if not (0 <= hora_entrada <= 23 and 0 <= hora_salida <= 23):
            print("Las horas deben estar entre 0 y 23. Intenta de nuevo.")
            continue
        if hora_salida <= hora_entrada:
            print("La hora de salida debe ser mayor que la de entrada. Intenta de nuevo.")
            continue

   
        if hora_entrada <= hora_referencia:
            contador_entradas += 1

 
        if hora_salida < salida_mas_temprana:
            salida_mas_temprana = hora_salida
            empleado_salida_temprana = nombre

        contador += 1  

    except ValueError:
        print("Debes introducir valores numéricos para las horas.")


print("\n--- RESULTADOS ---")
print(f"Empleados que entraron antes o a la hora de referencia ({hora_referencia}): {contador_entradas}")

if empleado_salida_temprana is not None:
    print(f"El empleado que salió más temprano fue {empleado_salida_temprana} a las {salida_mas_temprana}h.")
else:
    print("No se ha registrado ninguna salida válida.")
