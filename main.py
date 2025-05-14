import pandas as pd
from os import path
from gurobipy import Model, GRB, quicksum
import gurobipy as gp

## encontrar J e I
BASE_CSV = "./csv"
M = 10000
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

def parse_list(cell):
    # si está vacío, lista vacía
    if cell.strip() == "":
        return []
    # split por coma, quito espacios y convierto a int
    return [int(x.strip()) for x in cell.split(",")]

def cargar_datos():
    F_i = pd.read_csv(RUTAS["F_i"],index_col=None,header=None)[0].tolist()
    c_j = pd.read_csv(RUTAS["c_j"],index_col=None,header=None)[0].tolist()
    rho_i = pd.read_csv(RUTAS["rho_i"],index_col=None,header=None)[0].tolist()
    r_i = pd.read_csv(RUTAS["r_i"],index_col=None,header=None)[0].tolist()
    b_j = pd.read_csv(RUTAS["b_j"],index_col=None,header=None)[0].tolist()
    a_ij = pd.read_csv(RUTAS["a_ij"],index_col=None,header=None).T
    P_i = pd.read_csv(
    RUTAS["P_i"],
    header=None,
    names=["raw"],
    dtype=str,           
    skip_blank_lines=False 
)
    P_i["raw"] = P_i["raw"].fillna("")
    P_i["P_i_list"] = P_i["raw"].apply(parse_list)
    P_i = P_i["P_i_list"]
    N = pd.read_csv(RUTAS["N"],index_col=None,header=None)[0][0]
    W = pd.read_csv(RUTAS["W"],index_col=None,header=None)[0][0]
    I = range(len(F_i))
    J = range(len(c_j))


    
    data ={
    "F_i":F_i ,
    "c_j": c_j,
    "rho_i":rho_i ,
    "r_i": r_i,
    "b_j": b_j,
    "a_ij": a_ij,
    "N": N,
    "W": W,
    "P_i": P_i,
    "I": I,
    "J": J
    }

    return data

    """
    Esta función debe leer los 9 archivos .csv de la instancia y devolver
    un diccionario con todos los parámetros necesarios para construir el modelo.
    """

    raise NotImplementedError("Implementa esta función para cargar los datos.")

def construir_modelo(data):
    I = data["I"]
    J = data["J"]
    a_ij = data["a_ij"]
    b_j = data["b_j"]
    P_i = data["P_i"]
    c_j = data["c_j"]
    W = data["W"]
    N = data["N"]
    r_i = data["r_i"]
    rho_i = data["rho_i"]
    F_i = data["F_i"]
    ### SETUP INICIAL ###
    model = gp.Model() # crea modelo

    # Agregamos variables
    x_i = model.addVars(I,lb=0.0, vtype=GRB.CONTINUOUS, name="x_i")
    y_j = model.addVars(J, lb=0.0, vtype=GRB.CONTINUOUS, name="y_j")
    w_i = model.addVars(I,vtype=GRB.BINARY, name="w_i")

    model.update() # actualizamos el modelo

    ### RESTRICCIONES ###
    model.addConstrs(
        ((x_i[i] <= M*w_i[i]) for i in I),
        name="R1: activacion de la binaria"
    )

    model.addConstrs(
        (quicksum(a_ij[i][j] for i in I) <= b_j[j] + y_j[j]  for j in J),
        name="R2: disponibilidad de materiales"
    )

    model.addConstrs(
        (w_i[i] + w_i[k-1] <= 1  for i in I for k in P_i[i]),
        name="R3: compatibilidad de producion de productos"
    )

    model.addConstr(
        (quicksum(y_j[j]*c_j[j] for j in J) <= W),
        name= "R4: respetar el presupuesto total para comprar materiales"
    )

    model.addConstr(
        (quicksum(w_i[i] for i in I) <= N),
        name="R5: Limite de cantidad de productos distintos producidos"
    )

    model.setObjective(
        (quicksum((r_i[i] - rho_i[i])*x_i[i] - F_i[i]*w_i[i] for i in I ) - quicksum(y_j[j]*c_j[j] for j in J)),
        GRB.MAXIMIZE
    )
    

    model.update()
    return model



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


    if model.status == GRB.INFEASIBLE:
        print('El modelo es infactible')
        model.computeIIS()
        model.write('modelo.ilp')
        return None

    elif model.status == GRB.UNBOUNDED:
        print('El modelo es no acotado')
        return None

    elif model.status == GRB.INF_OR_UNBD:
        print('El modelo es infactible o no acotado')
        return None
    
    else:
        for var in model.getVars():
            if "x_i" in var.VarName and var.X > 1e-6:
                print(f"{var.VarName}: {var.X:.2f}")
        for var in model.getVars():
            if "y_j" in var.VarName and var.X > 1e-6:
                print(f"{var.VarName}: {var.X:.2f}")
        
        for var in model.getVars():
            if "w_i" in var.VarName and var.X > 0.5:
                print(f"{var.VarName}: {int(var.X)}")

        return model.ObjVal
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
