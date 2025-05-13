import pandas as pd
from gurobipy import Model, GRB

def cargar_datos():
    """
    Esta función debe leer los 9 archivos .csv de la instancia y devolver
    un diccionario con todos los parámetros necesarios para construir el modelo.
    """
    raise NotImplementedError("Implementa esta función para cargar los datos.")

def construir_modelo(data):
    """
    Esta función debe construir el modelo de optimización utilizando Gurobi
    y los datos provistos en el diccionario `data`.
    """
    raise NotImplementedError("Implementa esta función para construir el modelo.")

def resolver_modelo(model):
    """
    Esta función debe llamar al solver de Gurobi para resolver el modelo.
    """
    model.optimize()
    return model

def imprimir_resultados(model):
    """
    Esta función debe imprimir de forma clara el valor óptimo (con su unidad)
    y la cantidad de productos producidos de cada tipo.
    """
    raise NotImplementedError("Implementa esta función para imprimir los resultados.")

def main():
    data = cargar_datos()
    model = construir_modelo(data)
    resultado = resolver_modelo(model)
    imprimir_resultados(resultado)

if __name__ == "__main__":
    main()
