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


