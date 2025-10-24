
horarios = {
    'María':  ('08', '16'),
    'Juan':   ('09', '17'),
    'Lucía':  ('07', '15'),
    'Diego':  ('10', '18'),
    # -- Empleats Extras
    'Ana':    ('08', '14'),
    'Raúl':   ('12', '20'),
}

def mostrar_registros():
    for i, (key, (entrada,salida)) in enumerate(horarios.items() , start=1):
        print("Empleado nº:"+str(i)+", Nombre: "+key+" , Horario: de "+entrada+" a "+salida)
    



def contar_entradas():
    while True:
        try:
            hora_referencia = int(input("Introduce una hora de referencia (0–23): "))
            if 0 <= hora_referencia <= 23:
                break
            else:
                print("La hora debe estar entre 0 y 23.")
        except ValueError:
            print("Por favor, introduce un número válido entre 0 y 23.")
    
    for i, (key, (entrada,salida)) in enumerate(horarios.items() , start=1):
        if int(entrada) <= hora_referencia <= int(salida):
            print("Empleado nº:"+str(i)+", Nombre: "+key+" , Horario: de "+entrada+" a "+salida)
 
def menu():
    """
    Menú principal repetitivo (bucle while) para elegir acciones:
      1) Mostrar registros
      2) Contar entradas
      3) Salir
    """
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()
 
        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")
 
 

if __name__ == '__main__':
    menu()


