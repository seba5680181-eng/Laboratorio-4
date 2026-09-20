# ============================================================
# LABORATORIO IV - INFORMATICA II
# Resolucion de sistemas de ecuaciones lineales
# mediante la Regla de Cramer
# URL GitHub: https://github.com/seba5680181-eng/Laboratorio-4
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox


# ------------------------------------------------------------
# 1. FUNCIONES MATEMATICAS
# ------------------------------------------------------------

def determinante(matriz):
    """
    Calcula el determinante de una matriz cuadrada.

    Se utiliza expansion por cofactores.
    Esta funcion sirve para matrices de 1x1, 2x2, 3x3 y 4x4.
    """

    n = len(matriz)

    # Para determinante de una matriz 1x1.
    if n == 1:
        return matriz[0][0]

    # Para 2x2:
    # |a b|
    # |c d|  ->  ad - bc
    if n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
     # Para matrices mayores hacemos expansion por la primera fila.
    det = 0

    for columna in range(n):

        # Construimos el menor:
        # quitamos la primera fila y la columna actual.
        menor = []

        for fila in range(1, n):
            fila_menor = []

            for j in range(n):
                if j != columna:
                    fila_menor.append(matriz[fila][j])

            menor.append(fila_menor)

        # Signo del cofactor:
        # + - + -
        # - + - +
        signo = (-1) ** columna

        # Formula de expansion por cofactores.
        det += signo * matriz[0][columna] * determinante(menor)

    return det

def reemplazar_columna(matriz, vector, columna):
    """
    Crea una copia de la matriz A y reemplaza una de sus columnas
    por el vector b.

    Esto es justamente lo que necesitamos para aplicar Cramer:
        x1 = det(A1) / det(A)
        x2 = det(A2) / det(A)
        ...
    """

    # Copiamos la matriz para no modificar la matriz original.
    nueva_matriz = [fila[:] for fila in matriz]

    # Reemplazamos la columna indicada por los valores de b.
    for i in range(len(vector)):
        nueva_matriz[i][columna] = vector[i]

    return nueva_matriz


def resolver_cramer(matriz, vector):
    """
    Resuelve el sistema A*x = b mediante la Regla de Cramer.

    Devuelve:
        - la solucion x
        - el determinante de A
    """

    det_a = determinante(matriz)

    # Si det(A) = 0, no podemos dividir por det(A).
    # Ademas, el sistema no tiene una solucion unica.
    if abs(det_a) < 1e-10:
        raise ValueError(
            "El determinante de A es 0.\n"
            "La Regla de Cramer no permite obtener una solucion unica."
        )

    soluciones = []

    # Para cada incognita:
    # 1. Copiamos A.
    # 2. Reemplazamos una columna por b.
    # 3. Calculamos el nuevo determinante.
    # 4. Aplicamos xi = det(Ai) / det(A).
    for columna in range(len(matriz)):
        matriz_reemplazada = reemplazar_columna(
            matriz, vector, columna
        )

        det_ai = determinante(matriz_reemplazada)

        x = det_ai / det_a

        # Evitamos mostrar numeros como 1.9999999999999998
        # cuando en realidad el resultado matematico es 2.
        if abs(x) < 1e-10:
            x = 0.0

        soluciones.append(x)

    return soluciones, det_a

# ------------------------------------------------------------
# 2. FUNCIONES PARA LEER LOS DATOS DE LA INTERFAZ
# ------------------------------------------------------------

def obtener_datos():
    """
    Lee los valores ingresados en la GUI y arma:

        A = matriz de coeficientes
        b = vector de terminos independientes

    Solo se leen los campos correspondientes a la dimension
    seleccionada.
    """

    n = dimension.get()

    matriz = []
    vector = []

    try:
        # Recorrer las filas de A.
        for i in range(n):
            fila = []

            # Recorrer las columnas de A.
            for j in range(n):

                texto = entradas_a[i][j].get().strip()

                # No permitimos campos vacios.
                if texto == "":
                    raise ValueError(
                        f"Falta completar A[{i + 1}][{j + 1}]."
                    )

                # float permite ingresar enteros y decimales.
                valor = float(texto)

                fila.append(valor)

            matriz.append(fila)

            # Leer el termino independiente b.
            texto_b = entradas_b[i].get().strip()

            if texto_b == "":
                raise ValueError(
                    f"Falta completar b[{i + 1}]."
                )

            vector.append(float(texto_b))

        return matriz, vector

    except ValueError as error:
        # Si el error fue producido por nosotros, mostramos su mensaje.
        if str(error).startswith("Falta"):
            raise error

        # Si float() no pudo convertir el texto,
        # mostramos un mensaje mas entendible.
        raise ValueError(
            "Todos los valores deben ser numeros.\n"
            "Ejemplo: 5, -2, 3.5"
        )


# ------------------------------------------------------------
# 3. FUNCIONES DE LOS BOTONES
# ------------------------------------------------------------

def calcular():
    """
    Funcion ejecutada cuando se presiona el boton "Calcular".
    """

    try:
        # Obtenemos A y b desde los campos de la GUI.
        matriz, vector = obtener_datos()

        # Aplicamos la Regla de Cramer.
        soluciones, det_a = resolver_cramer(matriz, vector)

        # Mostramos cada componente del vector x.
        for i in range(4):
            if i < len(soluciones):
                entradas_x[i].delete(0, tk.END)
                entradas_x[i].insert(0, formatear_numero(soluciones[i]))
            else:
                entradas_x[i].delete(0, tk.END)

        # Tambien mostramos el determinante calculado.
        entrada_determinante.delete(0, tk.END)
        entrada_determinante.insert(0, formatear_numero(det_a))

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def calcular_determinante():
    """
    Funcion ejecutada cuando se presiona "Calcular det.".
    Calcula solamente det(A).
    """

    try:
        matriz, vector = obtener_datos()

        det_a = determinante(matriz)

        entrada_determinante.delete(0, tk.END)
        entrada_determinante.insert(0, formatear_numero(det_a))

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def borrar_valores():
    """
    Borra todos los valores de A, b, x y el determinante.
    """

    # Borramos los valores de la matriz A.
    for i in range(4):
        for j in range(4):
            entradas_a[i][j].delete(0, tk.END)

    # Borramos b y x.
    for i in range(4):
        entradas_b[i].delete(0, tk.END)
        entradas_x[i].delete(0, tk.END)

    # Borramos el determinante.
    entrada_determinante.delete(0, tk.END)

    # Volvemos a actualizar el estado de los campos.
    actualizar_dimension()


def actualizar_dimension():
    """
    Activa solamente los campos correspondientes a la dimension
    seleccionada.

    Ejemplo:
        2x2 -> usa A[1..2][1..2], b[1..2], x[1..2]
        3x3 -> usa A[1..3][1..3], b[1..3], x[1..3]
        4x4 -> usa todos los campos.
    """

    n = dimension.get()

    for i in range(4):
        for j in range(4):

            if i < n and j < n:
                # Campo utilizado por el sistema.
                entradas_a[i][j].configure(state="normal")
            else:
                # Campo fuera de la dimension seleccionada.
                entradas_a[i][j].delete(0, tk.END)
                entradas_a[i][j].configure(state="disabled")

        # Campos b y x.
        if i < n:
            entradas_b[i].configure(state="normal")
            entradas_x[i].configure(state="normal")
        else:
            entradas_b[i].delete(0, tk.END)
            entradas_x[i].delete(0, tk.END)

            entradas_b[i].configure(state="disabled")
            entradas_x[i].configure(state="disabled")


def formatear_numero(numero):
    """
    Convierte un numero a texto de forma mas prolija.

    Por ejemplo:
        2.0 -> "2"
        2.5 -> "2.5"
    """

    if abs(numero - round(numero)) < 1e-10:
        return str(int(round(numero)))

    return f"{numero:.6f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------
# 4. CREACION DE LA VENTANA PRINCIPAL
# ------------------------------------------------------------

ventana = tk.Tk()

ventana.title(
    "Resolución de sistemas de ecuaciones lineales mediante la Regla de Cramer"
)

ventana.geometry("720x620")
ventana.resizable(False, False)


# ------------------------------------------------------------
# 5. TITULO
# ------------------------------------------------------------

titulo = ttk.Label(
    ventana,
    text="Resolución de sistemas de ecuaciones lineales",
    font=("Arial", 16, "bold")
)

titulo.pack(pady=(15, 3))

subtitulo = ttk.Label(
    ventana,
    text="mediante la Regla de Cramer",
    font=("Arial", 12)
)

subtitulo.pack(pady=(0, 15))


# ------------------------------------------------------------
# 6. VARIABLE PARA ELEGIR LA DIMENSION
# ------------------------------------------------------------

# Comenzamos con 3x3, igual que en la imagen del enunciado.
dimension = tk.IntVar(value=3)


# ------------------------------------------------------------
# 7. FRAME PRINCIPAL
# ------------------------------------------------------------

frame_principal = ttk.Frame(ventana, padding=10)
frame_principal.pack()


# ------------------------------------------------------------
# 8. SELECCION DE DIMENSION
# ------------------------------------------------------------

frame_dimension = ttk.LabelFrame(
    frame_principal,
    text="Dimensión",
    padding=10
)

frame_dimension.grid(
    row=0,
    column=0,
    rowspan=4,
    padx=(0, 30),
    sticky="n"
)


# Creamos las opciones 2x2, 3x3 y 4x4.
for valor in (2, 3, 4):
    ttk.Radiobutton(
        frame_dimension,
        text=f"{valor} x {valor}",
        variable=dimension,
        value=valor,
        command=actualizar_dimension
    ).pack(anchor="w", pady=5)


# ------------------------------------------------------------
# 9. ENCABEZADOS DE LAS MATRICES
# ------------------------------------------------------------

# Etiqueta A.
ttk.Label(
    frame_principal,
    text="A",
    font=("Arial", 12, "bold")
).grid(row=0, column=2, columnspan=4, pady=(0, 5))

# Etiqueta b.
ttk.Label(
    frame_principal,
    text="b",
    font=("Arial", 12, "bold")
).grid(row=0, column=6, padx=8)

# Etiqueta x.
ttk.Label(
    frame_principal,
    text="x",
    font=("Arial", 12, "bold")
).grid(row=0, column=7, padx=8)


# ------------------------------------------------------------
# 10. CREACION DE LOS CAMPOS
# ------------------------------------------------------------

# Estas listas guardan las cajas de texto.
# De esta forma podemos acceder luego a cada valor.
entradas_a = []
entradas_b = []
entradas_x = []

for i in range(4):

    # Lista para la fila i de la matriz A.
    fila_entradas = []

    # Numero de fila de A.
    ttk.Label(
        frame_principal,
        text=str(i)
    ).grid((row=i + 1)+1, column=1, padx=5)

    for j in range(4):

        # Numero de columna de A.
        if i == 0:
            ttk.Label(
                frame_principal,
                text=str(j)
            ).grid(row=0, column=j + 2, padx=2)

        # Campo de entrada de A.
        entrada = ttk.Entry(
            frame_principal,
            width=7,
            justify="center"
        )

        entrada.grid(
            row=(i + 1)+1,
            column=j + 2,
            padx=2,
            pady=3
        )

        fila_entradas.append(entrada)

    entradas_a.append(fila_entradas)

    # Campo del vector b.
    entrada_b = ttk.Entry(
        frame_principal,
        width=7,
        justify="center"
    )

    entrada_b.grid(
        row=i + 1,
        column=6,
        padx=8,
        pady=3
    )

    entradas_b.append(entrada_b)

    # Campo del vector x.
    entrada_x = ttk.Entry(
        frame_principal,
        width=7,
        justify="center"
    )

    entrada_x.grid(
        row=i + 1,
        column=7,
        padx=8,
        pady=3
    )

    entradas_x.append(entrada_x)


# ------------------------------------------------------------
# 11. TEXTO DE AYUDA
# ------------------------------------------------------------

ayuda = ttk.Label(
    ventana,
    text=(
        "Ayuda: el sistema de ecuaciones permite calcular A·x = b\n"
        "Se deben cargar los valores de A y b y luego\n"
        "al calcular, se obtienen los valores del vector x."
    ),
    justify="center"
)

ayuda.pack(pady=20)


# ------------------------------------------------------------
# 12. BOTONES
# ------------------------------------------------------------

frame_botones = ttk.Frame(ventana)
frame_botones.pack(pady=5)

boton_borrar = ttk.Button(
    frame_botones,
    text="Borrar valores",
    command=borrar_valores
)

boton_borrar.grid(row=0, column=0, padx=8)

boton_calcular = ttk.Button(
    frame_botones,
    text="Calcular",
    command=calcular
)

boton_calcular.grid(row=0, column=1, padx=8)


# ------------------------------------------------------------
# 13. DETERMINANTE
# ------------------------------------------------------------

frame_det = ttk.Frame(ventana)
frame_det.pack(pady=15)

ttk.Label(
    frame_det,
    text="Determinante:"
).grid(row=0, column=0, padx=5)

entrada_determinante = ttk.Entry(
    frame_det,
    width=12,
    justify="center"
)

entrada_determinante.grid(row=0, column=1, padx=8)

boton_determinante = ttk.Button(
    frame_det,
    text="Calcular det.",
    command=calcular_determinante
)

boton_determinante.grid(row=0, column=2, padx=8)
