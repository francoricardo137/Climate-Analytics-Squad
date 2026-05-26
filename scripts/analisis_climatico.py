import pandas as pd
import matplotlib.pyplot as plt
import os

# esto lo hice para el tp de organizacion empresarial
# analisis de datos climaticos, escenario A

print("=== Script de análisis climático ===\n")

# rutas relativas como pide la consigna
datos_path = "../datos/"
resultados_path = "../resultados/"

# busco si hay algun csv en la carpeta datos
archivos = os.listdir(datos_path)
csv_files = [f for f in archivos if f.endswith('.csv')]

if len(csv_files) == 0:
    print("❌ No se encontró ningún archivo CSV en la carpeta /datos")
    print("Por favor, subí un dataset a la carpeta /datos")
    exit()
else:
    archivo_csv = csv_files[0]
    print(f"📂 Leyendo archivo: {archivo_csv}")

# cargo los datos
df = pd.read_csv(os.path.join(datos_path, archivo_csv))
print(f"✅ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas\n")

# muestro las columnas para saber con que estoy trabajando
print("📋 Columnas disponibles:")
print(df.columns.tolist())
print("\n")

# trato de adivinar cual es la columna de temperatura y cual la de año
# porque no se como se llama exactamente en cada dataset
temp_col = None
year_col = None

for col in df.columns:
    col_lower = col.lower()
    if 'temp' in col_lower or 'temperature' in col_lower:
        temp_col = col
    if 'year' in col_lower or 'date' in col_lower:
        year_col = col

# si no encuentra temperatura, agarra la primera columna numerica que encuentre
if temp_col is None:
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        temp_col = numeric_cols[0]
        print(f"⚠️ Usando '{temp_col}' como columna de temperatura")

if year_col is None:
    year_col = df.columns[0]
    print(f"⚠️ Usando '{year_col}' como columna de año/tiempo")

# calculo los indicadores que pide el tp
print(f"\n📊 Calculando indicadores usando:")
print(f"   Temperatura: {temp_col}")
print(f"   Año/tiempo: {year_col}")

temp_promedio = df[temp_col].mean()
temp_max = df[temp_col].max()
temp_min = df[temp_col].min()

print(f"\n🌡️ RESULTADOS:")
print(f"   Temperatura promedio: {temp_promedio:.2f}")
print(f"   Temperatura máxima: {temp_max:.2f}")
print(f"   Temperatura mínima: {temp_min:.2f}")

# genero el grafico que pide la consigna
plt.figure(figsize=(12, 6))
plt.plot(df[year_col], df[temp_col], marker='o', linestyle='-', linewidth=1, markersize=3)
plt.title('Evolución de Temperatura', fontsize=14)
plt.xlabel(year_col, fontsize=12)
plt.ylabel(temp_col, fontsize=12)
plt.grid(True, alpha=0.3)

# guardo el grafico en la carpeta resultados
os.makedirs(resultados_path, exist_ok=True)
plt.savefig(os.path.join(resultados_path, 'grafico_temperatura.png'), dpi=150)
plt.close()
print(f"\n📈 Gráfico guardado en: {resultados_path}grafico_temperatura.png")

# guardo un resumen en txt para entregar
with open(os.path.join(resultados_path, 'resumen.txt'), 'w', encoding='utf-8') as f:
    f.write("=== RESUMEN ANÁLISIS CLIMÁTICO ===\n\n")
    f.write(f"Archivo analizado: {archivo_csv}\n")
    f.write(f"Columna de temperatura: {temp_col}\n")
    f.write(f"Columna temporal: {year_col}\n\n")
    f.write(f"Temperatura promedio: {temp_promedio:.2f}\n")
    f.write(f"Temperatura máxima: {temp_max:.2f}\n")
    f.write(f"Temperatura mínima: {temp_min:.2f}\n")

print(f"📝 Resumen guardado en: {resultados_path}resumen.txt")
print("\n=== FIN DEL ANÁLISIS ===")
