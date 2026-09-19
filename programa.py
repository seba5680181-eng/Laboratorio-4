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