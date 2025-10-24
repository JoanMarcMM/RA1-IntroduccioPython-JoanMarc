# Faig import de json
import json



#FUNCIONS RELACIONADES AMB LES HORES
#funcio que demana una hora que el tranforma en int i verifica si esta entre 0 i 23
def validar_hora(valor_str: str) -> int:
    valor = int(valor_str)  
    if 0 <= valor <= 23:
        return valor
    raise ValueError("La hora debe estar entre 0 y 23.")
#funcio que demana un minut que el tranforma en int i verifica si esta entre 0 i 59
def validar_minuto(valor_str: str) -> int:
    valor = int(valor_str)  
    if 0 <= valor <= 59:
        return valor
    raise ValueError("Los minutos deben estar entre 0 y 59.")







#FUNCIOS RELACIONADES AMB JSON
#funcio per llegir el json
def leerHorarios():
    with open('horarios.json', 'r') as file:
        global horarios
        horarios = json.load(file)




#funcio per escriure en el json
def guardarHorarios():
    with open('horarios.json', 'w') as file:
        json.dump(horarios, file, indent=4)






#FUNCIONS FUNCIONAMENT PROGRAMA
#funcio per recorre el diccionari horaris i imprimir cada empleat
def mostrar_registros():
    for i, (key, (entrada, salida)) in enumerate(horarios.items(), start=0):
        print(f"Empleado nº:{i}, Nombre: {key} , Horario: de {entrada} a {salida}")




#funcio que demana una hora de referencia i fa print dels empleats que estan treballant a aquesta hora
def contar_entradas():
    while True:
        try:
            hora_referencia = validar_hora(input("Introduce una hora de referencia (0–23): ").strip())
            minuto_referencia = validar_minuto(input("Introduce un minuto de referencia (0–59): ").strip())
            break
        except ValueError as e:
            print(e)

    for i, (key, (entrada, salida)) in enumerate(horarios.items(), start=1):
        #faig split de entrada i sortida per separar hores i minuts
        hora_entrada, minuto_entrada = map(int, entrada.split(':'))
        hora_salida, minuto_salida = map(int, salida.split(':'))
        if (hora_entrada < hora_referencia < hora_salida) or (hora_entrada == hora_referencia and minuto_entrada <= minuto_referencia) or (hora_salida == hora_referencia and minuto_salida >= minuto_referencia):
            print(f"Empleado nº:{i}, Nombre: {key} , Horario: de {entrada} a {salida}")




#funcio per afegir un empleat demanant nom hora entrada i hora sortida
def añadir_empleado():
    nombre = input("Nombre del empleado: ").strip()
    while True:
        try:
            print("Hora de entrada (0–23): ")
            hora_entrada = validar_hora(input("Introduce una hora de entrada (0–23): ").strip())
            minuto_entrada = validar_hora(input("Introduce un minuto de entrada (0–59): ").strip())
            hora_salida  = validar_hora(input("Introduce una hora de salida (0–23): ").strip())
            minuto_salida = validar_hora(input("Introduce un minuto de salida (0–59): ").strip())
            if hora_salida <= hora_entrada:
                print("La hora de salida debe ser mayor que la de entrada. Intenta de nuevo.")
                continue
            if hora_salida == hora_entrada and minuto_salida <= minuto_entrada:
                print("El minuto de salida debe ser mayor que el de entrada. Intenta de nuevo.")
                continue
            break
        except ValueError as e:
            print(e)
    entrada = f"{hora_entrada:02}:{minuto_entrada:02}"
    salida = f"{hora_salida:02}:{minuto_salida:02}"
    horarios[nombre] = (entrada, salida)
    print(f"Empleado {nombre} añadido con horario de {entrada} a {salida}.")




#funcio menu que ensenya el menu i demana la opcio al ususari
def menu():
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Añadir empleado")
        print("4) Salir")
        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            añadir_empleado()
        elif opcion == '4':
            # al cerrar el programa guardamos los cambios en el json
            guardarHorarios()
            print("Cerrando programa")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")

if __name__ == '__main__':
    leerHorarios()
    menu() 
