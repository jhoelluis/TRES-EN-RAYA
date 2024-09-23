import tkinter as tk
from tkinter import messagebox
import random

VACIO = None
X = 'X'
O = 'O'

def estado_inicial():
    return [[VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO]]

def Jugador(S):
    x_cont, o_cont = 0, 0
    for fila in S:
        x_cont += fila.count(X)
        o_cont += fila.count(O)
    
    if o_cont < x_cont:
        return O
    return X

def Acciones(S):
    acciones = []
    for i in range(3):
        for j in range(3):
            if S[i][j] == VACIO:
                acciones.append((i, j))
    return acciones

def Resultado(S, a):
    i, j = a
    nuevo_estado = [fila[:] for fila in S]
    jugador = Jugador(S)
    nuevo_estado[i][j] = jugador
    return nuevo_estado

def verificar_ganador(S):
    lineas = [
        [S[0][0], S[0][1], S[0][2]],  # Fila 1
        [S[1][0], S[1][1], S[1][2]],  # Fila 2
        [S[2][0], S[2][1], S[2][2]],  # Fila 3
        [S[0][0], S[1][0], S[2][0]],  # Columna 1
        [S[0][1], S[1][1], S[2][1]],  # Columna 2
        [S[0][2], S[1][2], S[2][2]],  # Columna 3
        [S[0][0], S[1][1], S[2][2]],  # Diagonal 1
        [S[0][2], S[1][1], S[2][0]]   # Diagonal 2
    ]
    
    for linea in lineas:
        if linea[0] is not None and linea[0] == linea[1] == linea[2]:
            return linea[0]
    return None

def es_terminal(S):
    if verificar_ganador(S) or not Acciones(S):
        return True
    return False

def utilidad(S):
    ganador = verificar_ganador(S)
    if ganador == X:
        return 1
    elif ganador == O:
        return -1
    return 0

def minimax(S):
    if es_terminal(S):
        return None, utilidad(S)
    
    jugador_actual = Jugador(S)
    
    if jugador_actual == X:
        mejor_valor = -float('inf')
        mejor_movimiento = None
        for movimiento in Acciones(S):
            nuevo_estado = Resultado(S, movimiento)
            _, valor = minimax(nuevo_estado)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
        return mejor_movimiento, mejor_valor
    
    else:
        mejor_valor = float('inf')
        mejor_movimiento = None
        for movimiento in Acciones(S):
            nuevo_estado = Resultado(S, movimiento)
            _, valor = minimax(nuevo_estado)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
        return mejor_movimiento, mejor_valor

class TresEnRaya:
    def __init__(self, root, vs_ia=False, dificultad="fácil"):
        self.root = root
        self.vs_ia = vs_ia
        self.dificultad = dificultad
        self.root.title("Tres en Raya")
        self.root.configure(bg="#e0f7fa")  # Color de fondo
        self.tablero = estado_inicial()
        self.botones = [[None for _ in range(3)] for _ in range(3)]
        self.label_turno = tk.Label(self.root, text="Turno de R", font=('Helvetica', 24), bg="#e0f7fa")
        self.label_turno.grid(row=0, column=0, columnspan=3, pady=10)
        self.crear_tablero()
        self.jugador_actual = X

    def crear_tablero(self):
        for i in range(3):
            for j in range(3):
                boton = tk.Button(self.root, text="", width=5, height=2, font=('Helvetica', 36, 'bold'),
                                   command=lambda i=i, j=j: self.hacer_movimiento(i, j), bg="#ffffff", fg="#000000",
                                   borderwidth=5, relief="raised")
                boton.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")
                self.botones[i][j] = boton
        # Expandir filas y columnas
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def hacer_movimiento(self, i, j):
        if self.tablero[i][j] is VACIO and not es_terminal(self.tablero):
            self.tablero = Resultado(self.tablero, (i, j))
            self.actualizar_botones()

            if es_terminal(self.tablero):
                self.mostrar_ganador()
            else:
                self.jugador_actual = Jugador(self.tablero)
                self.actualizar_label_turno()
                
                if self.vs_ia and self.jugador_actual == O:
                    self.movimiento_ia()

    def movimiento_ia(self):
        if self.dificultad == "fácil":
            self.movimiento_ia_fácil()
        elif self.dificultad == "intermedio":
            self.movimiento_ia_intermedio()
        else:
            movimiento, _ = minimax(self.tablero)  
            if movimiento:
                self.tablero = Resultado(self.tablero, movimiento)
                self.actualizar_botones()
                if es_terminal(self.tablero):
                    self.mostrar_ganador()
                else:
                    self.jugador_actual = Jugador(self.tablero)
                    self.actualizar_label_turno()

    def movimiento_ia_fácil(self):
        if random.random() < 0.8:  # 80% de éxito
            movimiento = random.choice(Acciones(self.tablero))
        else:
            movimiento = random.choice(Acciones(self.tablero)) 
        self.tablero = Resultado(self.tablero, movimiento)
        self.actualizar_botones()
        if es_terminal(self.tablero):
            self.mostrar_ganador()
        else:
            self.jugador_actual = Jugador(self.tablero)
            self.actualizar_label_turno()

    def movimiento_ia_intermedio(self):
        if random.random() < 0.5: 
            movimiento, _ = minimax(self.tablero)
        else:
            movimiento = random.choice(Acciones(self.tablero))  
        if movimiento:
            self.tablero = Resultado(self.tablero, movimiento)

        self.actualizar_botones()
        if es_terminal(self.tablero):
            self.mostrar_ganador()
        else:
            self.jugador_actual = Jugador(self.tablero)
            self.actualizar_label_turno()

    def actualizar_botones(self):
        for i in range(3):
            for j in range(3):
                texto = self.tablero[i][j] if self.tablero[i][j] else ""
                if texto == X:
                    color = "blue"
                    bg_color = "#aeeeee"
                elif texto == O:
                    color = "red"
                    bg_color = "#ffcccb"
                else:
                    color = "black"
                    bg_color = "#ffffff"
                
                self.botones[i][j].config(text=texto, fg=color, bg=bg_color)

    def actualizar_label_turno(self):
        self.label_turno.config(text=f"Turno de {self.jugador_actual}")

    def mostrar_ganador(self):
        ganador = verificar_ganador(self.tablero)
        if ganador:
            if ganador == X:
                messagebox.showinfo("🎉 Fin del juego", "¡El jugador R (🟦) ha ganado! 🎉")
            else:
                messagebox.showinfo("🎉 Fin del juego", "¡El jugador J (🟥) ha ganado! 🎉")
        else:
            messagebox.showinfo("🤝 Fin del juego", "¡Es un empate! 🤝")
        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.tablero = estado_inicial()
        self.actualizar_botones()
        self.jugador_actual = X
        self.actualizar_label_turno()

class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Tres en Raya")
        self.root.configure(bg="#b2ebf2")  
        self.label = tk.Label(self.root, text="Elige una opción", font=('Helvetica', 24), bg="#b2ebf2")
        self.label.pack(pady=20)

        self.boton_ia = tk.Button(self.root, text="Jugar contra IA", command=self.seleccionar_dificultad, bg="#ffffff", font=('Helvetica', 18))
        self.boton_ia.pack(pady=10)

        self.boton_amigos = tk.Button(self.root, text="Jugar con amigos", command=self.iniciar_juego_con_amigos, bg="#ffffff", font=('Helvetica', 18))
        self.boton_amigos.pack(pady=10)

    def seleccionar_dificultad(self):
        self.limpiar_menu()
        self.label_dificultad = tk.Label(self.root, text="Selecciona la dificultad", font=('Helvetica', 20), bg="#b2ebf2")
        self.label_dificultad.pack(pady=20)

        self.boton_facil = tk.Button(self.root, text="Fácil", command=lambda: self.iniciar_juego("fácil"), bg="#ffffff", font=('Helvetica', 16))
        self.boton_facil.pack(pady=5)

        self.boton_intermedio = tk.Button(self.root, text="Intermedio", command=lambda: self.iniciar_juego("intermedio"), bg="#ffffff", font=('Helvetica', 16))
        self.boton_intermedio.pack(pady=5)

        self.boton_dificil = tk.Button(self.root, text="Difícil", command=lambda: self.iniciar_juego("difícil"), bg="#ffffff", font=('Helvetica', 16))
        self.boton_dificil.pack(pady=5)

    def iniciar_juego(self, dificultad):
        self.root.destroy()  # Cierra el menú
        nueva_ventana = tk.Tk()
        juego = TresEnRaya(nueva_ventana, vs_ia=True, dificultad=dificultad)
        nueva_ventana.mainloop()

    def iniciar_juego_con_amigos(self):
        self.root.destroy()  # Cierra el menú
        nueva_ventana = tk.Tk()
        juego = TresEnRaya(nueva_ventana, vs_ia=False)
        nueva_ventana.mainloop()

    def limpiar_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
