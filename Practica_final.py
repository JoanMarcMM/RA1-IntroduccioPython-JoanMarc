#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica final:
Característique clau:
- Menú 
- Llegeix i escriu csv
- Utilitza tipus de variables basics i estructures de dades
- Classes propies
- Utilitza datetime.
- Gestio d arxius i validacions de dades

Estructura q segueixen els csv:
- clientes.csv: id, nombre, email, fecha_alta (YYYY-MM-DD)
- eventos.csv:  id, nombre, fecha_evento (YYYY-MM-DD), categoria, precio (float)
- ventas.csv:   id, cliente_id, evento_id, fecha_venta (YYYY-MM-DD), importe (float)
"""

from __future__ import annotations
import csv
import os
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Dict, Tuple, Optional, Set
import re





# ---------------------------
# Validacions varies
# ---------------------------

FECHA_FMT = "%Y-%m-%d"  # Formato de fecha estándar para CSV

#funcio per parejar la data amb datetime

def parse_fecha(fecha_str: str) -> date:
    """Parsea una fecha en formato YYYY-MM-DD y devuelve datetime.date.
    Lanza ValueError si no cumple el formato.
    """
    return datetime.strptime(fecha_str, FECHA_FMT).date()


#funcio per validar el email amb match de regex
def validar_email(email: str) -> bool:
    """Validación simple de email (no exhaustiva)."""
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(patron, email) is not None














# ---------------------------
# Clasess
# ---------------------------
#Clase client
@dataclass
class Cliente:
    id: int
    nombre: str
    email: str
    fecha_alta: date

#Te dues funcions, una per calcular l'antiguedad en dies i l'altra per mostrar la info del client
    def antiguedad_dias(self) -> int:
        """Días desde la fecha de alta hasta hoy."""
        return (date.today() - self.fecha_alta).days

    def __str__(self) -> str:
        return f"Cliente({self.id}) {self.nombre} <{self.email}> — alta: {self.fecha_alta.isoformat()} ({self.antiguedad_dias()} días)"

    __repr__ = __str__



#clase evento
@dataclass
class Evento:
    id: int
    nombre: str
    fecha_evento: date
    categoria: str
    precio: float
#te dos funcions, una per calcular els dies fins l'event i l'altra per mostrar la info de l'event
    def dias_hasta_evento(self) -> int:
        """Días desde hoy hasta la fecha del evento (negativo si ya pasó)."""
        return (self.fecha_evento - date.today()).days

    def __str__(self) -> str:
        return (
            f"Evento({self.id}) {self.nombre} — {self.categoria} — fecha: {self.fecha_evento.isoformat()} "
            f"(en {self.dias_hasta_evento()} días) — precio: {self.precio:.2f}€"
        )

    __repr__ = __str__



#classe venta
@dataclass
class Venta:
    id: int
    cliente_id: int
    evento_id: int
    fecha_venta: date
    importe: float
#te una funcio per mostrar la info de la venta
    def __str__(self) -> str:
        return (
            f"Venta({self.id}) cliente={self.cliente_id} evento={self.evento_id} "
            f"fecha={self.fecha_venta.isoformat()} importe={self.importe:.2f}€"
        )

    __repr__ = __str__










# ------------------------------------
# Contenedor de datos en memoria (tablas)
# ------------------------------------

class BD:
    """Estructura de datos en memoria y utilidades de acceso/índices."""

    def __init__(self):
        # Llistes q utilitzo
        self.clientes: List[Cliente] = []
        self.eventos: List[Evento] = []
        self.ventas: List[Venta] = []

        # index er id per accedir mes rapid
        self.idx_clientes: Dict[int, Cliente] = {}
        self.idx_eventos: Dict[int, Evento] = {}
        self.idx_ventas: Dict[int, Venta] = {}

        # Rutes dels arxius CSV
        self.dir_data = os.path.join("data")
        self.f_clientes = os.path.join(self.dir_data, "clientes.csv")
        self.f_eventos = os.path.join(self.dir_data, "eventos.csv")
        self.f_ventas = os.path.join(self.dir_data, "ventas.csv")

        # aixo garantitza que el directori data existeixi
        os.makedirs(self.dir_data, exist_ok=True)












    # ---------------------------
    # Cargar dades
    # ---------------------------
    #funcio per cargar les dades, aquesta funcio crida a les tres altre funcions per cargar cada csv
    def cargar_datos(self) -> None:
        """Llegeix els 3 CSV i carrega les dades a memòria. Si hi ha algun q no esta avisa per terminaol"""
        self._leer_clientes()
        self._leer_eventos()
        self._leer_ventas()
        print("\nCarga completada.")


#funcio per cargar els clients
    def _leer_clientes(self):
        #neteja les llistes i els indexs
        self.clientes.clear(); self.idx_clientes.clear()
        try:
            #llegeix el csv
            with open(self.f_clientes, newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    try:
                        c = Cliente(
                            id=int(row['id']),
                            nombre=row['nombre'].strip(),
                            email=row['email'].strip(),
                            fecha_alta=parse_fecha(row['fecha_alta'].strip()),
                        )
                        self.clientes.append(c)
                        self.idx_clientes[c.id] = c
                    except Exception as e:
                        print(f"[clientes.csv] Fila inválida omitida: {row} — Error: {e}")
        except FileNotFoundError:
            print("[clientes.csv] No encontrado. La tabla de clientes se inicializa vacía.")


#funci o per cargar els events
    def _leer_eventos(self):
        #neteja les llistes i els indexs
        self.eventos.clear(); self.idx_eventos.clear()
        try:
            #llegeix el csv
            with open(self.f_eventos, newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    try:
                        e = Evento(
                            id=int(row['id']),
                            nombre=row['nombre'].strip(),
                            fecha_evento=parse_fecha(row['fecha_evento'].strip()),
                            categoria=row['categoria'].strip(),
                            precio=float(row['precio']),
                        )
                        self.eventos.append(e)
                        self.idx_eventos[e.id] = e
                    except Exception as e:
                        print(f"[eventos.csv] Fila inválida omitida: {row} — Error: {e}")
        except FileNotFoundError:
            print("[eventos.csv] No encontrado. La tabla de eventos se inicializa vacía.")


#funcio per cargar les ventes
    def _leer_ventas(self):
        #neteja les llistes i els indexs
        self.ventas.clear(); self.idx_ventas.clear()
        try:
            #llegeix el csv
            with open(self.f_ventas, newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    try:
                        v = Venta(
                            id=int(row['id']),
                            cliente_id=int(row['cliente_id']),
                            evento_id=int(row['evento_id']),
                            fecha_venta=parse_fecha(row['fecha_venta'].strip()),
                            importe=float(row['importe']),
                        )
                        self.ventas.append(v)
                        self.idx_ventas[v.id] = v
                    except Exception as e:
                        print(f"[ventas.csv] ila inválida omitida: {row} — Error: {e}")
        except FileNotFoundError:
            print("[ventas.csv] No encontrado. La tabla de ventas se inicializa vacía.")









    # ---------------------------
    # Guardar dades
    # ---------------------------
#funcio per guardar els clients
    def guardar_clientes(self) -> None:
        with open(self.f_clientes, 'w', newline='', encoding='utf-8') as fh:
            campos = ['id', 'nombre', 'email', 'fecha_alta']
            writer = csv.DictWriter(fh, fieldnames=campos)
            writer.writeheader()
            for c in self.clientes:
                writer.writerow({
                    'id': c.id,
                    'nombre': c.nombre,
                    'email': c.email,
                    'fecha_alta': c.fecha_alta.isoformat(),
                })

#funcio per exportar l'informe on surten els totals per event i ingressos
    def exportar_informe(self) -> None:
        ruta = os.path.join(self.dir_data, 'informe_resumen.csv')
        # Calculamos un dict: evento_id -> {nombre, num_ventas, total}
        resumen: Dict[int, Dict[str, object]] = {}
        for v in self.ventas:
            ev = self.idx_eventos.get(v.evento_id)
            if not ev:
                # Aixo es per si hi ha vendes d'esdeveniments que no existeix
                nombre = f"Evento {v.evento_id} (desconocido)"
            else:
                nombre = ev.nombre
            item = resumen.setdefault(v.evento_id, {'evento_id': v.evento_id, 'evento_nombre': nombre, 'num_ventas': 0, 'total_ingresos': 0.0})
            item['num_ventas'] = int(item['num_ventas']) + 1
            item['total_ingresos'] = float(item['total_ingresos']) + float(v.importe)

        with open(ruta, 'w', newline='', encoding='utf-8') as fh:
            campos = ['evento_id', 'evento_nombre', 'num_ventas', 'total_ingresos']
            writer = csv.DictWriter(fh, fieldnames=campos)
            writer.writeheader()
            for _, item in sorted(resumen.items()):
                writer.writerow(item)

        print(f"\n📄 Informe exportado en: {ruta}")




    # ---------------------------
    # Operacions diverses
    # ---------------------------
#funcio per generar un nou id per a les taules
    def generar_nuevo_id(self, tabla: str) -> int:
        if tabla == 'clientes':
            existentes = set(self.idx_clientes.keys())
        elif tabla == 'eventos':
            existentes = set(self.idx_eventos.keys())
        elif tabla == 'ventas':
            existentes = set(self.idx_ventas.keys())
        else:
            raise ValueError("Tabla desconocida para ID")
        return (max(existentes) + 1) if existentes else 1



#funcio per fer print de les taules
    def listar(self, tabla: str) -> None:
        """Imprime de forma formateada la tabla indicada."""
        tabla = tabla.lower()
        if tabla == 'clientes':
            print("\n=== CLIENTES ===")
            for c in self.clientes:
                print(c)
            print(f"Total: {len(self.clientes)}")
        elif tabla == 'eventos':
            print("\n=== EVENTOS ===")
            for e in sorted(self.eventos, key=lambda x: x.fecha_evento):
                print(e)
            print(f"Total: {len(self.eventos)}")
        elif tabla == 'ventas':
            print("\n=== VENTAS ===")
            for v in self.ventas:
                print(v)
            print(f"Total: {len(self.ventas)}")
        else:
            print("Tabla no reconocida. Usa: clientes | eventos | ventas")


#funcio per donar d'alta un nou client
    def alta_cliente(self) -> None:
        """Pide datos por input(), valida y guarda incrementalmente en CSV."""
        print("\n-- Alta de cliente --")
        nombre = input("Nombre: ").strip()
        email = input("Email: ").strip()
        if not validar_email(email):
            print("Email no válido. Operación cancelada.")
            return
        fecha_str = input("Fecha de alta (YYYY-MM-DD): ").strip()
        try:
            fecha = parse_fecha(fecha_str)
        except ValueError:
            print("Formato de fecha incorrecto. Usa YYYY-MM-DD.")
            return
        # Verificar si el email ja existex
        if any(c.email.lower() == email.lower() for c in self.clientes):
            print("Ya existe un cliente con ese email.")
            return

        nuevo_id = self.generar_nuevo_id('clientes')
        c = Cliente(id=nuevo_id, nombre=nombre, email=email, fecha_alta=fecha)
        self.clientes.append(c)
        self.idx_clientes[c.id] = c

        self.guardar_clientes()
        print(f"Cliente creado: {c}")


#funcio per filtrar les ventes per rang de dates
    def filtrar_ventas_por_rango(self) -> List[Venta]:
        """Solicita dos fechas al usuario, valida e imprime las ventas en el rango (inclusive).
        Devuelve la lista filtrada por si se quiere reutilizar.
        """
        print("\n-- Filtro de ventas por rango de fechas --")
        ini_str = input("Fecha inicio (YYYY-MM-DD): ").strip()
        fin_str = input("Fecha fin (YYYY-MM-DD): ").strip()
        try:
            f_ini = parse_fecha(ini_str)
            f_fin = parse_fecha(fin_str)
        except ValueError:
            print("Alguna de las fechas es inválida. Usa YYYY-MM-DD.")
            return []
        if f_ini > f_fin:
            print("La fecha de inicio no puede ser posterior a la fecha fin.")
            return []

        filtradas = [v for v in self.ventas if f_ini <= v.fecha_venta <= f_fin]

        print(f"\nVentas entre {f_ini.isoformat()} y {f_fin.isoformat()} (ambas inclusive):")
        total = 0.0
        for v in filtradas:
            print(v)
            total += v.importe
        print(f"Total ventas encontradas: {len(filtradas)} — Ingresos: {total:.2f}€")
        return filtradas


#funcio per mostrar les estadistiques
    def estadisticas(self) -> None:
        """Muestra métricas generales solicitadas:
        - Ingresos totales
        - Ingresos por evento (dict)
        - Set de categorías existentes
        - Días hasta el evento más próximo
        - Tupla (min, max, media) de precios de eventos
        """
        print("\n=== ESTADÍSTICAS ===")

        # Ingressos totals , sumem l'import de totes les ventes
        ingresos_totales = sum(v.importe for v in self.ventas)
        print(f"Ingresos totales: {ingresos_totales:.2f}€")

        # Ingressos per event , sumem l'import per cada event
        ingresos_por_evento: Dict[int, float] = {}
        for v in self.ventas:
            ingresos_por_evento[v.evento_id] = ingresos_por_evento.get(v.evento_id, 0.0) + v.importe
        print("Ingresos por evento (evento_id -> total €):")
        for ev_id, total in sorted(ingresos_por_evento.items()):
            nombre = self.idx_eventos.get(ev_id).nombre if ev_id in self.idx_eventos else f"Evento {ev_id} (desconocido)"
            print(f"  {ev_id} - {nombre}: {total:.2f}€")

        # Fem print del set de categories
        categorias: Set[str] = {e.categoria for e in self.eventos}
        print(f"Categorías: {categorias}")

        # dies fins l'event mes proper
        futuros = [e for e in self.eventos if e.fecha_evento >= date.today()]
        if futuros:
            dias_min = min(e.dias_hasta_evento() for e in futuros)
            print(f"Días hasta el evento más próximo: {dias_min}")
        else:
            print("Días hasta el evento más próximo: n/d (no hay eventos futuros)")

        # Indiquem min, max, mitja de preus dels events
        if self.eventos:
            precios = [e.precio for e in self.eventos]
            min_p, max_p = min(precios), max(precios)
            media_p = sum(precios) / len(precios)
            resumen_precios: Tuple[float, float, float] = (min_p, max_p, media_p)
            print(f"Precios de eventos (min, max, media): {resumen_precios}")
        else:
            print("Precios de eventos (min, max, media): n/d")


# ---------------------------
# Menu
# ---------------------------
#funcio per mostrar el menu
def mostrar_menu() -> None:
    print(
        """
=========================
 Gestion Eventos
=========================
1) Cargar CSV
2) Listar tabla (clientes | eventos | ventas)
3) Alta de cliente
4) Filtro de ventas por rango de fechas
5) Estadísticas
6) Exportar informe (totales por evento)
7) Salir
"""
    )

#funcio per demanar l'opcio
def pedir_opcion() -> str:
    return input("Elige una opción (1-7): ").strip()

#funcio per demanar quina taula listar
def input_listar() -> str:
    return input("¿Qué tabla quieres listar? (clientes/eventos/ventas): ").strip().lower()




# ---------------------------
# Función principal (bucle app)
# ---------------------------
#MAIN
def main():
    bd = BD()
    bd.cargar_datos()

    while True:
        mostrar_menu()
        op = pedir_opcion()

        if op == '1':
            bd.cargar_datos()
        elif op == '2':
            bd.listar(input_listar())
        elif op == '3':
            bd.alta_cliente()
        elif op == '4':
            bd.filtrar_ventas_por_rango()
        elif op == '5':
            bd.estadisticas()
        elif op == '6':
            bd.exportar_informe()
        elif op == '7':
            print("\nCerrando programa")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == '__main__':
    main()
