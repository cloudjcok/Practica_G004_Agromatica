import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuración de conexión a PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "genetica_comparada",
    "user": "postgres",
    "password": "12345678"  
}

def ejecutar_analisis():
    conexion = None
    try:
        # Conectar a la base de datos
        conexion = psycopg2.connect(**DB_CONFIG)
        print("Conexión exitosa a la base de datos 'genetica_comparada'.")

        # 2. Consultar la vista comparacion_gc
        query = "SELECT especie, id_registro, longitud, porcentaje_gc FROM comparacion_gc;"
        df = pd.read_sql_query(query, conexion)
        
        print("\nResultados obtenidos desde la vista comparacion_gc:")
        print(df.to_string(index=False))

        # 3. Exportar resultados a archivo .csv
        archivo_csv = "resultados_comparacion_gc.csv"
        df.to_csv(archivo_csv, index=False, encoding="utf-8")
        print(f"\nArchivo CSV generado correctamente: {archivo_csv}")

        # 4. Generar gráfico de barras comparativo
        plt.figure(figsize=(8, 5))
        etiquetas = [f"{row['especie']}\n({row['id_registro']})" for _, row in df.iterrows()]
        valores_gc = df["porcentaje_gc"].astype(float)
        colores = ["#E69F00", "#009E73"]  # Dorado para maíz, verde para cacao

        barras = plt.bar(etiquetas, valores_gc, color=colores, width=0.45, edgecolor="black")

        # Etiquetas numéricas sobre cada barra
        for barra in barras:
            altura = barra.get_height()
            plt.text(
                barra.get_x() + barra.get_width() / 2,
                altura + 1.0,
                f"{altura:.2f}%",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold"
            )

        plt.title("Comparación del Contenido GC (%) en el Gen rbcL", fontsize=13, fontweight="bold", pad=15)
        plt.ylabel("Porcentaje de Bases GC (%)", fontsize=11)
        plt.xlabel("Especie y Código de Acceso NCBI", fontsize=11)
        plt.ylim(0, max(valores_gc) + 12)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()

        archivo_grafico = "grafico_comparacion_gc.png"
        plt.savefig(archivo_grafico, dpi=300)
        print(f"Gráfico de barras guardado como: {archivo_grafico}")
        plt.show()

    except Exception as error:
        print(f"Error durante la ejecución: {error}")
    finally:
        if conexion:
            conexion.close()
            print("Conexión a PostgreSQL cerrada.")

if __name__ == "__main__":
    ejecutar_analisis()