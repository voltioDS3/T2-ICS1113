import pandas as pd
from os import path
from gurobipy import Model, GRB
import gurobipy as gp

## encontrar J e I
BASE_CSV = "./csv"
RUTAS = {
    "F_i": path.join(BASE_CSV, "costo_fijo.csv"),
    "c_j": path.join(BASE_CSV, "costo_material.csv"),
    "rho_i": path.join(BASE_CSV, "costo_variable.csv"),
    "r_i": path.join(BASE_CSV, "ingreso_por_unidad.csv"),
    "b_j": path.join(BASE_CSV, "material_disponible.csv"),
    "a_ij": path.join(BASE_CSV, "material_requerido.csv"),
    "N": path.join(BASE_CSV, "maximo_productos.csv"),
    "W": path.join(BASE_CSV, "presupuesto_materiales.csv"),
    "P_i": path.join(BASE_CSV, "productos_prohibidos.csv"),
}
def cargar_datos():
    F_i = pd.read_csv(RUTAS["F_i"],index_col=None,header=None)[0].tolist()
    c_j = pd.read_csv(RUTAS["c_j"],index_col=None,header=None)[0].tolist()
    rho_i = pd.read_csv(RUTAS["rho_i"],index_col=None,header=None)[0].tolist()
    r_i = pd.read_csv(RUTAS["r_i"],index_col=None,header=None)[0].tolist()
    b_j = pd.read_csv(RUTAS["b_j"],index_col=None,header=None)[0].tolist()
    # a_ij = pd.read_csv(RUTAS["a_ij"],index_col=None,header=None)[0].tolist()
    P_i = pd.read_csv(RUTAS["P_i"],index_col=None,header=None)[0].tolist()

    I = len(F_i)
    J = len(c_j)
    data ={

    }




    """
    Esta función debe leer los 9 archivos .csv de la instancia y devolver
    un diccionario con todos los parámetros necesarios para construir el modelo.
    """

    raise NotImplementedError("Implementa esta función para cargar los datos.")

def construir_modelo(data):
    I = data["I"]
    J = data["J"]

    model = gp.Model() # crea modelo
    x_i = model.addVars(I,lb=0.0, vtype=GRB.CONTINUOUS, name="x_i")
    y_j = model.addvars(J, lb=0.0, vtype=GRB.CONTINUOUS, name="y_j")
    w_i = model.addVars(I,vtype=GRB.BINARY, name="w_i")

    model.update()
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
