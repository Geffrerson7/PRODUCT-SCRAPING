import os
import pandas as pd
from shutil import copyfile

# Función para buscar SKUs en los nombres de las imágenes
def buscar_skus_en_imagenes(carpeta_imagenes, df_skus, carpeta_destino):
    # Obtener la lista de SKUs del DataFrame
    skus = df_skus["SKU"].tolist()
    
    # Crear una lista para almacenar los nombres de las imágenes encontradas
    imagenes_encontradas = []
    skus_no_encontrados = skus.copy()  # Hacer una copia de la lista de SKUs
    
    # Iterar sobre los archivos en la carpeta de imágenes
    for archivo in os.listdir(carpeta_imagenes):
        # Verificar si el archivo es una imagen y tiene el formato de nombre adecuado
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg')) and '-' in archivo:
            # Obtener el SKU del nombre del archivo
            sku_archivo = archivo.split('-')[0]
            
            # Verificar si el SKU está en la lista de SKUs
            if sku_archivo in skus_no_encontrados:
                imagenes_encontradas.append(archivo)
                skus_no_encontrados.remove(sku_archivo)
                
                # Copiar la imagen a la carpeta de destino
                ruta_origen = os.path.join(carpeta_imagenes, archivo)
                ruta_destino = os.path.join(carpeta_destino, archivo)
                copyfile(ruta_origen, ruta_destino)
    
    return imagenes_encontradas, skus_no_encontrados

# Ruta de la carpeta de imágenes
carpeta_imagenes = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/total-img"

# Ruta de la carpeta destino para las imágenes encontradas
carpeta_destino = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/imagenes-encontradas"

# Cargar el archivo Excel que contiene los SKUs
archivo_excel = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/SKU-VA.xlsx"
df_skus = pd.read_excel(archivo_excel)

# Buscar los SKUs en los nombres de las imágenes
imagenes_encontradas, skus_no_encontrados = buscar_skus_en_imagenes(carpeta_imagenes, df_skus, carpeta_destino)

# Imprimir los nombres de las imágenes encontradas
print("Imágenes encontradas:")
for imagen in imagenes_encontradas:
    print(imagen)

# Crear un DataFrame con los SKUs no encontrados
df_no_encontrados = pd.DataFrame({"SKU_no_encontrado": skus_no_encontrados})

# Guardar los SKUs no encontrados en un nuevo archivo Excel
ruta_archivo_no_encontrados = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/skus_no_encontrados.xlsx"
df_no_encontrados.to_excel(ruta_archivo_no_encontrados, index=False)
print(f"Los SKUs no encontrados se han guardado en '{ruta_archivo_no_encontrados}'")

