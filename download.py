import pandas as pd
import requests
import os
from PIL import Image
from io import BytesIO

# Función para descargar y procesar una imagen de una URL y guardarla en formato JPG
def procesar_imagen(url, sku, carpeta_destino):
    enlaces_separados = url.split(',')  # Dividir los enlaces por la coma
    for i, enlace in enumerate(enlaces_separados, start=1):
        nombre_archivo = f"{sku}-{i}.jpg"  # Nombre del archivo será SKU-i.jpg
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)  # Construir la ruta completa del archivo
        
        try:
            respuesta = requests.get(enlace.strip())  # Eliminar posibles espacios en blanco
            if respuesta.ok:
                imagen = Image.open(BytesIO(respuesta.content))
                imagen = imagen.convert("RGB")  # Convertir la imagen a formato RGB
                imagen = imagen.resize((1000, 1000))  # Redimensionar la imagen a 1000x1000
                imagen.save(ruta_archivo, "JPEG", quality=95)  # Guardar la imagen en formato JPEG con calidad del 95
                print(f"Imagen guardada: {ruta_archivo}")
            else:
                print(f"Error al descargar la imagen {enlace}: {respuesta.status_code}")
        except Exception as e:
            print(f"Error al procesar la imagen {enlace}: {e}")

# Cargar el archivo Excel
archivo_excel = "enlaces_imagenes_y_sku.xlsx"  # Asumiendo que el archivo está en el mismo directorio que el script
df = pd.read_excel(archivo_excel)

# Carpeta donde se guardarán las imágenes
carpeta_destino = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/imagenes"
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# List to store SKUs with empty image links
skus_sin_imagen = []

# Iterar sobre las filas del DataFrame
for index, fila in df.iterrows():
    enlaces_imagen = fila['link']
    sku = fila['SKU']
    if pd.isna(enlaces_imagen) or enlaces_imagen.strip() == "":
        skus_sin_imagen.append(sku)
    else:
        procesar_imagen(enlaces_imagen, sku, carpeta_destino)

# Guardar los SKUs sin imagen en un nuevo archivo Excel
df_sin_imagen = pd.DataFrame({'SKU': skus_sin_imagen})
df_sin_imagen.to_excel('skus_sin_imagen.xlsx', index=False)

print("¡Proceso completado!")
