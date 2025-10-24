#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple






# ---------------------------------
# Variables globals
# ---------------------------------
HORA_REFERENCIA: int = 8       # Hora global per els madrugadors
INPUT_PATH: Path = Path('horarios.csv') # Fitxer d'entrada
OUTPUT_DIR: Path = Path('.')






# -----------------------------
# Classes
# -----------------------------

#clase per emmagatzemar els registres
@dataclass(frozen=True)
class RegistroHorario:
    empleado: str
    dia: str  # Nom del dia
    entrada: int  # hora entrada 0–23
    salida: int   # hora sortida 0–23

    def duracion(self) -> int:
        return self.salida - self.entrada

#classe per emmagatzemar els empleats
@dataclass
class Empleado:
    nombre: str
    registros: List[RegistroHorario] = field(default_factory=list)
#funcio per agregar un registre
    def agregar_registro(self, r: RegistroHorario) -> None:
        if r.empleado != self.nombre:
            raise ValueError("El registro no corresponde a este empleado")
        self.registros.append(r)
#funcio per calcular les hores totals
    def horas_totales(self) -> int:
        return sum(r.duracion() for r in self.registros)
#funcio per calcular els dies treballats
    def dias_trabajados(self) -> int:
        return len({r.dia for r in self.registros})
#funcio per obtenir la fila csv
    def fila_csv(self) -> Tuple[str, int, int]:
        return (self.nombre, self.dias_trabajados(), self.horas_totales())



#classe per gestionar els horaris
class GestorHorarios:
    #constructor
    def __init__(self, registros: Iterable[RegistroHorario]):
        self.registros: List[RegistroHorario] = list(registros)
        self.empleados: Dict[str, Empleado] = {}
        for r in self.registros:
            self.empleados.setdefault(r.empleado, Empleado(r.empleado)).agregar_registro(r)
#funcio per escriure el resum
    def escribir_resumen(self, ruta: Path) -> None:
        with ruta.open('w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(['empleado', 'dias_trabajados', 'horas_totales'])
            for emp in sorted(self.empleados.values(), key=lambda e: e.nombre.lower()):
                w.writerow(list(emp.fila_csv()))









# -----------------------------
# Utilitats
# -----------------------------
CAMPOS = ['nombre_empleado', 'dia', 'hora_entrada', 'hora_salida']
DIAS_ES = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

#funcio per parsejar les hores
def parse_hora(valor: str) -> int:
    """Convierte '8' o '08:00' o '16:30' en ENTERO de hora (0–23).
    Los minutos se ignoran.
    """
    v = valor.strip()
    if ':' in v:
        h = v.split(':', 1)[0]
    else:
        h = v
    hora = int(h)
    if not (0 <= hora <= 23):
        raise ValueError(f"Hora fuera de rango (0–23): {valor}")
    return hora

#funcio per normalitzar els dies
def normalizar_dia(d: str) -> str:
    """Si d es fecha YYYY-MM-DD, devuelve el nombre del día en español.
    Si ya parece ser un nombre de día, lo capitaliza correctamente.
    """
    s = d.strip()

    try:
        fecha = datetime.strptime(s, '%Y-%m-%d')
        return DIAS_ES[fecha.weekday()]
    except ValueError:
        pass

    # normalitzacio basica
    s_low = s.lower()
    mapping = {
        'lunes': 'Lunes', 'martes': 'Martes', 'miercoles': 'Miércoles', 'miércoles': 'Miércoles',
        'jueves': 'Jueves', 'viernes': 'Viernes', 'sabado': 'Sábado', 'sábado': 'Sábado',
        'domingo': 'Domingo'
    }
    return mapping.get(s_low, s)









# -----------------------------
# Lectura dels fitxers csv
# -----------------------------

#funcio per llegir els registres del csv
def leer_registros_csv(ruta: Path) -> List[RegistroHorario]:
    registros: List[RegistroHorario] = []
    with ruta.open('r', newline='', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';', quotechar='"')
        for i, fila in enumerate(lector, start=1):
            if not fila:
                continue
            if len(fila) != 4:
                raise ValueError(f"Línea {i}: se esperaban 4 columnas, llegaron {len(fila)} -> {fila}")

            nombre, dia_raw, h_entrada, h_salida = [c.strip() for c in fila]

            if i == 1 and [c.lower() for c in fila] == CAMPOS:
                continue

            try:
                entrada = parse_hora(h_entrada)
                salida = parse_hora(h_salida)
            except ValueError:
                raise ValueError(f"Línea {i}: 'hora_entrada' y 'hora_salida' deben ser horas válidas -> {fila}")

            dia = normalizar_dia(dia_raw)
            r = RegistroHorario(nombre, dia, entrada, salida)
            registros.append(r)
    return registros



# -----------------------------
# Operacions amb els registres
# -----------------------------
#funcio per construir els empleats per dia
def construir_empleados_por_dia(registros: Iterable[RegistroHorario]) -> Dict[str, Set[str]]:
    empleados_por_dia: Dict[str, Set[str]] = {}
    for r in registros:
        empleados_por_dia.setdefault(r.dia, set()).add(r.empleado)
    return empleados_por_dia

#funcio per obtenir els empleats que treballen tots els dies
def empleados_que_trabajan_en_todos_los_dias(empleados_por_dia: Dict[str, Set[str]]) -> Set[str]:
    conjuntos = list(empleados_por_dia.values())
    if not conjuntos:
        return set()
    inter = conjuntos[0].copy()
    for c in conjuntos[1:]:
        inter &= c
    return inter





# -----------------------------
# Escritura de ls fitxers csv
# -----------------------------
#funcio per escriure el resum d'hores
def escribir_resumen_horas(registros: Iterable[RegistroHorario], ruta: Path) -> None:
    horas_totales: Dict[str, int] = {}
    for r in registros:
        horas_totales.setdefault(r.empleado, 0)
        horas_totales[r.empleado] += r.duracion()

    with ruta.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['empleado', 'horas_totales'])
        for empleado, total in sorted(horas_totales.items(), key=lambda x: x[0].lower()):
            w.writerow([empleado, total])

#funcio per escriure els madrugadors
def escribir_madrugadores(registros: Iterable[RegistroHorario], hora_ref: int, ruta: Path) -> None:
    madrugadores: List[Tuple[str, int]] = []
    for r in registros:
        if r.entrada < hora_ref:
            madrugadores.append((r.empleado, r.entrada))

    
    visto: Dict[str, int] = {}
    for emp, hr in madrugadores:
        visto.setdefault(emp, hr)

    with ruta.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['empleado', 'hora_entrada'])
        for emp, hr in sorted(visto.items(), key=lambda x: x[0].lower()):
            w.writerow([emp, hr])

#funcio per escriure una llista simple
def escribir_lista_simple(nombres: Iterable[str], ruta: Path, cabecera: str = 'empleado') -> None:
    with ruta.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([cabecera])
        for n in sorted(set(nombres), key=lambda s: s.lower()):
            w.writerow([n])

#funcio per escriure el resum setmanal
def escribir_resumen_semanal(registros: Iterable[RegistroHorario], ruta: Path) -> None:
    horas_totales: Dict[str, int] = {}
    dias_por_empleado: Dict[str, Set[str]] = {}

    for r in registros:
        horas_totales[r.empleado] = horas_totales.get(r.empleado, 0) + r.duracion()
        dias_por_empleado.setdefault(r.empleado, set()).add(r.dia)

    with ruta.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['empleado', 'dias_trabajados', 'horas_totales'])
        for emp in sorted(set(list(horas_totales.keys()) + list(dias_por_empleado.keys())), key=lambda s: s.lower()):
            w.writerow([emp, len(dias_por_empleado.get(emp, set())), horas_totales.get(emp, 0)])









# -----------------------------
# llogica principal 
# -----------------------------
#funcio main
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Lectura y normalizacio
    registros = leer_registros_csv(INPUT_PATH)
    print(f"Se han leído {len(registros)} registros de '{INPUT_PATH}'.")

    # construccio del diccionari dia -> empleats
    emp_por_dia = construir_empleados_por_dia(registros)
    print("Empleados por día:")
    for dia, empleados in sorted(emp_por_dia.items(), key=lambda x: x[0].lower()):
        print(f"  {dia}: {sorted(empleados, key=str.lower)}")

    # empleats que treballen tots els dies
    en_todos = empleados_que_trabajan_en_todos_los_dias(emp_por_dia)
    print(f"Empleados que trabajaron en TODOS los días del CSV: {sorted(en_todos, key=str.lower)}")

    # resum d'hores totals
    escribir_resumen_horas(registros, OUTPUT_DIR / 'resumen_horarios.csv')
    print(f"Generado: {OUTPUT_DIR / 'resumen_horarios.csv'}")

    # madrugadors (entrada < HORA_REFERENCIA)
    escribir_madrugadores(registros, HORA_REFERENCIA, OUTPUT_DIR / 'madrugadores.csv')
    print(f"Generado: {OUTPUT_DIR / 'madrugadores.csv'} (HORA_REFERENCIA={HORA_REFERENCIA})")

    # empleats que treballen Lunes i Viernes
    lunes = emp_por_dia.get('Lunes', set())
    viernes = emp_por_dia.get('Viernes', set())
    inter_lu_vi = lunes & viernes
    print(f"Empleados que trabajaron Lunes y Viernes: {sorted(inter_lu_vi, key=str.lower)}")
    escribir_lista_simple(inter_lu_vi, OUTPUT_DIR / 'en_dos_dias.csv')
    print(f"Generado: {OUTPUT_DIR / 'en_dos_dias.csv'}")

    # empleats que treballen dissabte pero NO diumenge
    sabado = emp_por_dia.get('Sábado', set()) | emp_por_dia.get('Sabado', set())
    domingo = emp_por_dia.get('Domingo', set())
    exclusivos_sabado = sabado - domingo  # diferencia
    print(f"Empleados que trabajaron Sábado pero NO Domingo: {sorted(exclusivos_sabado, key=str.lower)}")
    escribir_lista_simple(exclusivos_sabado, OUTPUT_DIR / 'exclusivos_sabado.csv')
    print(f"Generado: {OUTPUT_DIR / 'exclusivos_sabado.csv'}")

    # resum setmanal (dies treballats + hores totals)
    escribir_resumen_semanal(registros, OUTPUT_DIR / 'resumen_semanal.csv')
    print(f"Generado: {OUTPUT_DIR / 'resumen_semanal.csv'}")

    # filtracio empleats que treballen >= 6h en totes les jornades
    empleados = {r.empleado for r in registros}
    cumple_6h: Set[str] = set()
    for emp in empleados:
        regs_emp = [r for r in registros if r.empleado == emp]
        if regs_emp and all(r.duracion() >= 6 for r in regs_emp):
            cumple_6h.add(emp)
    print(f"Empleados que trabajan ≥ 6h en TODAS sus jornadas: {sorted(cumple_6h, key=str.lower)}")

    # dissenys de classes
    gestor = GestorHorarios(registros)
    gestor.escribir_resumen(OUTPUT_DIR / 'resumen_clases.csv')
    print(f"Generado: {OUTPUT_DIR / 'resumen_clases.csv'}")


if __name__ == '__main__':
    main()
