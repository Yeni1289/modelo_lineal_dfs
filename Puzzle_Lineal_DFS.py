"""Puzzle lineal con busqueda en profundidad (DFS) + interfaz Streamlit."""

import streamlit as st


class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos
        self.padre = padre
        self.hijos = []

    def get_datos(self):
        return self.datos

    def get_padre(self):
        return self.padre

    def set_hijos(self, hijos):
        self.hijos = hijos

    def en_lista(self, lista_nodos):
        for n in lista_nodos:
            if n.get_datos() == self.datos:
                return True
        return False


def buscar_solucion_DFS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop()
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo, len(nodos_visitados)

        dato_nodo = nodo.get_datos()

        # Operador izquierdo
        hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izquierdo = Nodo(hijo, nodo)

        # Operador derecho
        hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_derecho = Nodo(hijo, nodo)

        # Operador central
        hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_central = Nodo(hijo, nodo)

        hijos = [hijo_izquierdo, hijo_derecho, hijo_central]
        for hijo_nodo in hijos:
            if not hijo_nodo.en_lista(nodos_visitados) and not hijo_nodo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_nodo)

        nodo.set_hijos(hijos)

    return None, len(nodos_visitados)


def reconstruir_camino(nodo_solucion):
    if nodo_solucion is None:
        return []

    resultado = []
    nodo = nodo_solucion
    while nodo is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.reverse()
    return resultado


def parsear_estado(texto):
    partes = [x.strip() for x in texto.split(",")]
    if len(partes) != 4:
        raise ValueError("Debes ingresar exactamente 4 numeros separados por coma.")

    estado = [int(x) for x in partes]
    if sorted(estado) != [1, 2, 3, 4]:
        raise ValueError("Solo se permiten los numeros 1,2,3,4 sin repetir.")

    return estado


def estado_a_texto(estado):
    return " | ".join(str(x) for x in estado)


def app():
    st.set_page_config(page_title="Puzzle Lineal DFS", page_icon="🧩", layout="centered")

    st.markdown(
        """
        <style>
            .main {background: linear-gradient(180deg, #f7f8fb 0%, #eef2ff 100%);} 
            .bloque {
                background: white;
                border: 1px solid #dbe1f0;
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 10px;
                box-shadow: 0 2px 6px rgba(20, 30, 60, 0.05);
            }
            .paso {
                font-size: 14px;
                color: #334155;
                margin-bottom: 4px;
            }
            .estado {
                font-size: 20px;
                font-weight: 700;
                letter-spacing: 1px;
                color: #0f172a;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Puzzle lineal con DFS")
    st.caption("Version simple e interactiva")

    with st.sidebar:
        st.subheader("Instrucciones")
        st.write("Ingresa 4 numeros separados por coma usando solo 1,2,3,4.")
        st.write("Ejemplo: 4,2,3,1")

    col1, col2 = st.columns(2)
    with col1:
        estado_inicial_txt = st.text_input("Estado inicial", "4,2,3,1")
    with col2:
        estado_meta_txt = st.text_input("Estado meta", "1,2,3,4")

    if st.button("Resolver con DFS"):
        try:
            estado_inicial = parsear_estado(estado_inicial_txt)
            estado_meta = parsear_estado(estado_meta_txt)
        except ValueError as e:
            st.error(str(e))
            return

        nodo_solucion, visitados = buscar_solucion_DFS(estado_inicial, estado_meta)
        camino = reconstruir_camino(nodo_solucion)

        if not camino:
            st.warning("No se encontro solucion.")
            return

        st.success("Solucion encontrada.")
        m1, m2 = st.columns(2)
        m1.metric("Nodos visitados", visitados)
        m2.metric("Pasos", len(camino) - 1)

        st.subheader("Ruta de solucion")
        for i, estado in enumerate(camino):
            st.markdown(
                f"""
                <div class="bloque">
                    <div class="paso">Paso {i}</div>
                    <div class="estado">{estado_a_texto(estado)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    app()