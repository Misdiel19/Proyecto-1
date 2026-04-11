
from scipy import stats
import pandas as pd

#Reemplazar los nombres de las columnas
# Cargar el archivo
df = pd.read_csv('/Desktop/games.csv')

# Convertir los nombres de las columnas a minúsculas
df.columns = df.columns.str.lower()

# Verificar el resultado
print(df.columns)

# Convertir los datos en los tipos necesarios

# Convertir year_of_release a numérico (entero)
df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce')

# Convertir critic_score a numérico
df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce')

# Convertir user_score a numérico (maneja 'tbd' automáticamente)
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')

# Verificar los tipos de datos
df.info()

#Describe las columnas en las que los tipos de datos han sido cambiados y explica por qué.
# Guardar tipos de datos antes
dtypes_before = df.dtypes

# Conversión de tipos
df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce')
df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce')
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')

# Guardar tipos de datos después
dtypes_after = df.dtypes

# Comparar
dtypes_comparison = pd.DataFrame({
    'before': dtypes_before,
    'after': dtypes_after
})

print(dtypes_comparison)

#----Comentarios-----
#Al revisar los tipos de datos con df.info(), se observa que las columnas
#year_of_release, critic_score y user_score se encuentran en formato numérico (float64).
#Estas conversiones se realizaron previamente para permitir cálculos y análisis estadísticos.
#Al comparar los tipos de datos antes y después, no se observan cambios adicionales, ya que el 
# conjunto de datos ya había sido limpiado en pasos anteriores.

#-------------------

# Convertir 'TBD' a NaN (ya aplicado previamente)
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')

# Ver cantidad de valores ausentes por columna
df.isna().sum()

print(df.isna().sum())

#----Comentarios-----

#Los valores ausentes no se rellenaron, ya que en la mayoría de 
#los casos representan información que realmente no estaba disponible
#en el momento de la recopilación de datos. En particular, los valores
#TBD en la columna user_score indican que la puntuación aún no había 
#sido determinada, por lo que se trataron como valores nulos (NaN). 
#Rellenar estos datos podría introducir sesgos y afectar la calidad 
#del análisis, por lo que se decidió conservarlos como ausentes.

#-------------------

# Calcular las ventas totales por juego
df['total_sales'] = (
    df['na_sales'] +
    df['eu_sales'] +
    df['jp_sales'] +
    df['other_sales']
)

# Verificar el resultado
df[['name', 'total_sales']].head()

print(df[['name', 'total_sales']].head())

# Contar cuántos juegos se lanzaron por año
games_per_year = (
    df.groupby('year_of_release')['name']
    .count()
    .sort_index()
)

# Imprimir el resultado
print(games_per_year.head(10))   # primeros años
print(games_per_year.tail(10))   # últimos años

import matplotlib.pyplot as plt
# Gráfica
games_per_year.plot(kind='bar', figsize=(12, 5))
plt.title('Número de juegos lanzados por año')
plt.xlabel('Año de lanzamiento')
plt.ylabel('Cantidad de juegos')
plt.show()

#----Comentarios-----

#Al analizar la cantidad de juegos lanzados por año, se observa que los 
#primeros años del registro contienen muy pocos datos, lo que los hace 
#poco representativos. A partir de mediados de la década de 1990 y hasta 
#aproximadamente 2010 se concentra la mayor cantidad de lanzamientos, por 
#lo que este período resulta más significativo para el análisis. En los 
#años más recientes se observa una disminución en el número de juegos, 
#probablemente debido a que el conjunto de datos no está completo para esos años.

#-------------------

# Ventas totales por plataforma
sales_by_platform = (
    df.groupby('platform')['total_sales']
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_platform.head(10))

top_platforms = sales_by_platform.head(5).index
top_platforms

# Filtrar solo las plataformas más vendidas
df_top = df[df['platform'].isin(top_platforms)]

# Ventas por año y plataforma
sales_year_platform = (
    df_top.groupby(['year_of_release', 'platform'])['total_sales']
    .sum()
    .reset_index()
)

print(sales_year_platform.head())

import matplotlib.pyplot as plt

for platform in top_platforms:
    platform_data = sales_year_platform[
        sales_year_platform['platform'] == platform
    ]
    plt.plot(
        platform_data['year_of_release'],
        platform_data['total_sales'],
        label=platform
    )

plt.legend()
plt.title('Ventas anuales por plataforma')
plt.xlabel('Año de lanzamiento')
plt.ylabel('Ventas totales')
plt.show()

#----Comentarios-----

#Al analizar las ventas por plataforma, se observa que cada una presenta un ciclo de vida definido.
#  Las plataformas más exitosas concentran sus ventas en un período aproximado de 7 a 10 años.

#-------------------

# Filtrar datos del período seleccionado
df_relevant = df[(df['year_of_release'] >= 2013) & (df['year_of_release'] <= 2016)]

# Verificar el resultado
print(df_relevant['year_of_release'].value_counts().sort_index())

#----Comentarios-----

#Este rango refleja las tendencias más recientes del mercado de videojuegos
#y contiene información de las plataformas activas justo antes de 2017.
#Los años anteriores presentan datos poco representativos, mientras que 
#los años más recientes están incompletos. Por ello, este período ofrece 
#un equilibrio adecuado entre relevancia y volumen de datos.

#-------------------

# Filtrar solo los años relevantes para el análisis (2013–2016)
df_relevant = df[
    (df['year_of_release'] >= 2013) &
    (df['year_of_release'] <= 2016)
].copy()

# Verificar el rango de años
print(df_relevant['year_of_release'].unique())

# Ver cuántos registros quedaron
print(df_relevant.shape)

#----Comentarios-----

#Se descartaron los datos correspondientes a juegos lanzados antes de 2013,
#ya que estos reflejan un mercado distinto al que se busca analizar. 
#Las plataformas de esos años han dejado de tener relevancia comercial 
#y no representan las tendencias cercanas a 2017. 
#Además, considerando el ciclo de vida de las plataformas, el uso de datos 
#recientes permite construir un modelo más preciso y coherente con el 
#objetivo del estudio.

#-------------------

# Ventas totales por plataforma (período relevante)
platform_sales = (
    df_relevant.groupby('platform')['total_sales']
    .sum()
    .sort_values(ascending=False)
)

print(platform_sales.head(5))

# Ventas por año y plataforma
sales_trend = (
    df_relevant.groupby(['year_of_release', 'platform'])['total_sales']
    .sum()
    .reset_index()
)

print(sales_trend.head())

platforms_to_check = ['PS4', 'XOne', 'PS3', 'X360', '3DS']

for platform in platforms_to_check:
    data = sales_trend[sales_trend['platform'] == platform]
    plt.plot(data['year_of_release'], data['total_sales'], label=platform)

plt.legend()
plt.title('Evolución de ventas por plataforma (2013–2016)')
plt.xlabel('Año')
plt.ylabel('Ventas totales')
plt.show()

#----Comentarios-----

#Durante el período 2013–2016, las plataformas líderes en ventas fueron PS4 
#y XOne, ambas pertenecientes a la generación más reciente de consolas. 
#Estas plataformas muestran una clara tendencia de crecimiento, mientras que 
#PS3 y X360 presentan una disminución sostenida en ventas, propia del final
#de su ciclo de vida. La plataforma 3DS mantiene ventas estables, lo que 
#la convierte en una opción rentable dentro de un mercado más específico.
#Por ello, PS4, XOne y 3DS se consideran las plataformas con mayor potencial
#para 2017.

#-------------------

# Preparar los datos por plataforma
platforms = df_relevant['platform'].unique()

data_to_plot = [
    df_relevant[df_relevant['platform'] == platform]['total_sales']
    for platform in platforms
]

# Crear diagrama de caja
plt.figure(figsize=(14, 6))
plt.boxplot(data_to_plot, labels=platforms, showfliers=True)
plt.xticks(rotation=45)
plt.title('Distribución de ventas globales por plataforma (2013–2016)')
plt.xlabel('Plataforma')
plt.ylabel('Ventas globales')
plt.show()

#Ventas promedio
average_sales = (
    df_relevant.groupby('platform')['total_sales']
    .mean()
    .sort_values(ascending=False)
)

print(average_sales)

#----Comentarios-----

#El diagrama de caja de las ventas globales por plataforma muestra diferencias
#significativas entre ellas. 
#Plataformas como PS4 y XOne presentan medianas y promedios de ventas más 
#altos, así como una mayor dispersión, lo que indica la presencia de juegos 
#altamente exitosos. 
#En contraste, plataformas como PS3 y X360 muestran ventas promedio más 
#bajas, reflejando su etapa de declive. 
#En general, las ventas están altamente concentradas en pocos títulos 
#exitosos, como lo evidencian los numerosos valores atípicos.

#-------------------

ps4_data = df_relevant[df_relevant['platform'] == 'PS4']


#Reseñas de usuarios vs ventas globales
plt.figure(figsize=(8, 5))
plt.scatter(ps4_data['user_score'], ps4_data['total_sales'], alpha=0.6)
plt.title('Reseñas de usuarios vs Ventas globales (PS4)')
plt.xlabel('Puntuación de usuarios')
plt.ylabel('Ventas globales')
plt.show()

#Reseñas de usuarios vs ventas globales
plt.figure(figsize=(8, 5))
plt.scatter(ps4_data['critic_score'], ps4_data['total_sales'], alpha=0.6)
plt.title('Reseñas de críticos vs Ventas globales (PS4)')
plt.xlabel('Puntuación de críticos')
plt.ylabel('Ventas globales')
plt.show()

#Correlación con reseñas de usuarios
user_corr = ps4_data['user_score'].corr(ps4_data['total_sales'])
print('Correlación usuarios vs ventas:', user_corr)

#Correlación con reseñas de críticos
critic_corr = ps4_data['critic_score'].corr(ps4_data['total_sales'])
print('Correlación críticos vs ventas:', critic_corr)

#----Comentarios-----

#El análisis de la plataforma PS4 muestra que existe una relación débil
#entre las reseñas (tanto de usuarios como de críticos) y las ventas globales.
#Aunque los juegos mejor calificados tienden a vender ligeramente más, 
#la dispersión en los datos indica que las reseñas no determinan por sí 
#solas el éxito comercial. 
#Factores como la franquicia, el marketing y la popularidad previa influyen 
#de manera importante en las ventas.

#-------------------

#Identificar juegos que salen en varias plataformas
# Juegos que aparecen en más de una plataforma
multi_platform_games = (
    df_relevant
    .groupby('name')['platform']
    .nunique()
    .reset_index()
)

multi_platform_games = multi_platform_games[multi_platform_games['platform'] > 1]
multi_platform_games.head()

#Filtrar los datos solo para esos juegos
multi_games_data = df_relevant[df_relevant['name'].isin(multi_platform_games['name'])]

#Comparar ventas por plataforma
sales_by_platform = (
    multi_games_data
    .groupby('platform')['total_sales']
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_platform)

sales_by_platform.plot(kind='bar', figsize=(12, 5))
plt.title('Ventas totales de los mismos juegos por plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Ventas globales')
plt.show()

#----Comentarios-----

#Al comparar las ventas de los mismos juegos en distintas plataformas, se
#observa que el desempeño comercial varía considerablemente. 
#Esto indica que, aunque las reseñas se mantienen constantes para un mismo 
#título, factores como la popularidad de la plataforma y su base de usuarios 
#tienen un impacto mucho mayor en las ventas. 
#Las plataformas líderes concentran la mayor parte de las ventas incluso
#cuando los juegos están disponibles en sistemas menos populares.

#-------------------

# Cantidad de juegos por género
games_by_genre = df_relevant['genre'].value_counts()

print(games_by_genre)

games_by_genre.plot(kind='bar', figsize=(10, 5))
plt.title('Cantidad de juegos por género')
plt.xlabel('Género')
plt.ylabel('Número de juegos')
plt.show()

#Ventas totales por género
sales_by_genre = (
    df_relevant
    .groupby('genre')['total_sales']
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_genre)

sales_by_genre.plot(kind='bar', figsize=(10, 5))
plt.title('Ventas totales por género')
plt.xlabel('Género')
plt.ylabel('Ventas globales')
plt.show()

#Ventas promedio por género
avg_sales_by_genre = (
    df_relevant
    .groupby('genre')['total_sales']
    .mean()
    .sort_values(ascending=False)
)

print(avg_sales_by_genre)

#----Comentarios-----

#El análisis de la distribución de juegos por género muestra que los géneros
#de acción, disparos y deportes concentran las mayores ventas totales y 
#promedio, lo que indica una alta demanda del mercado. 
#En contraste, géneros como rompecabezas y estrategia presentan ventas
#significativamente menores, lo que sugiere que están dirigidos a audiencias
#más específicas. 
#Por lo tanto, los géneros con mayor éxito comercial suelen ser aquellos
#orientados al entretenimiento masivo.

#-------------------

# Cinco plataformas principales por región
top_na_platforms = (
    df_relevant.groupby('platform')['na_sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

top_eu_platforms = (
    df_relevant.groupby('platform')['eu_sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

top_jp_platforms = (
    df_relevant.groupby('platform')['jp_sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("Top NA:\n", top_na_platforms, "\n")
print("Top UE:\n", top_eu_platforms, "\n")
print("Top JP:\n", top_jp_platforms)

# Cinco géneros por región
top_na_genres = (
    df_relevant.groupby('genre')['na_sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

top_eu_genres = (
    df_relevant.groupby('genre')['eu_sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

top_jp_genres = (
    df_relevant.groupby('genre')['jp_sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("Top NA géneros:\n", top_na_genres, "\n")
print("Top UE géneros:\n", top_eu_genres, "\n")
print("Top JP géneros:\n", top_jp_genres)

# Ventas por clasificación ESRB en cada región
rating_na = (
    df_relevant.groupby('rating')['na_sales']
    .sum()
    .sort_values(ascending=False)
)

rating_eu = (
    df_relevant.groupby('rating')['eu_sales']
    .sum()
    .sort_values(ascending=False)
)

rating_jp = (
    df_relevant.groupby('rating')['jp_sales']
    .sum()
    .sort_values(ascending=False)
)

print("NA ESRB:\n", rating_na, "\n")
print("UE ESRB:\n", rating_eu, "\n")
print("JP ESRB:\n", rating_jp)

#----Comentarios-----

#El análisis regional muestra diferencias claras en preferencias de plataformas,
#géneros y clasificaciones. 
#Mientras que Norteamérica y Europa presentan comportamientos similares,
#Japón destaca por su preferencia por plataformas y géneros de origen local.
#Asimismo, las clasificaciones ESRB influyen significativamente en las ventas
#en NA y UE, pero tienen un impacto limitado en el mercado japonés.

#-------------------

# Filtrar calificaciones de usuarios para Xbox One
xone_scores = df[
    (df['platform'] == 'XOne') & (df['user_score'].notna())
]['user_score']

# Filtrar calificaciones de usuarios para PC
pc_scores = df[
    (df['platform'] == 'PC') & (df['user_score'].notna())
]['user_score']

# Ver tamaños de muestra
print("Xbox One n =", len(xone_scores))
print("PC n =", len(pc_scores))

alpha = 0.05

t_stat, p_value = stats.ttest_ind(
    xone_scores,
    pc_scores,
    equal_var=False
)

print("Estadístico t:", t_stat)
print("p-value:", p_value)

if p_value < alpha:
    print("Rechazamos la hipótesis nula")
else:
    print("No rechazamos la hipótesis nula")

#----Comentarios-----

#Dado que el valor p es menor al nivel de significancia del 5 %, se 
#rechaza la hipótesis nula. 
#Por lo tanto, se concluye que las calificaciones promedio de los 
#usuarios para las plataformas Xbox One y PC presentan una diferencia 
#estadísticamente significativa.

#-------------------

# Calificaciones de usuarios para Acción
action_scores = df[
    (df['genre'] == 'Action') & (df['user_score'].notna())
]['user_score']

# Calificaciones de usuarios para Deportes
sports_scores = df[
    (df['genre'] == 'Sports') & (df['user_score'].notna())
]['user_score']

# Tamaño de las muestras
print("Action n =", len(action_scores))
print("Sports n =", len(sports_scores))

# Calificaciones de usuarios para Acción
action_scores = df[
    (df['genre'] == 'Action') & (df['user_score'].notna())
]['user_score']

# Calificaciones de usuarios para Deportes
sports_scores = df[
    (df['genre'] == 'Sports') & (df['user_score'].notna())
]['user_score']

# Tamaño de las muestras
print("Action n =", len(action_scores))
print("Sports n =", len(sports_scores))

t_stat, p_value = stats.ttest_ind(
    action_scores,
    sports_scores,
    equal_var=False
)

print("Estadístico t:", t_stat)
print("p-value:", p_value)

if p_value < alpha:
    print("Se rechaza la hipótesis nula (H0).")
    print("Las calificaciones promedio de los usuarios son diferentes.")
else:
    print("No se rechaza la hipótesis nula (H0).")
    print("No hay evidencia suficiente de que las calificaciones promedio sean diferentes.")

#----Comentarios-----

#Dado que el valor p es mayor que el nivel de significancia del 5 %, 
#no se rechaza la hipótesis nula. 
#Por lo tanto, no se encontraron diferencias estadísticamente significativas
#entre las calificaciones promedio de los usuarios para los 
#géneros Acción y Deportes.

#-------------------

