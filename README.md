# Análisis físico y estadístico de las Gemínidas

Este repositorio contiene el procesamiento y análisis de observaciones de meteoros Gemínidas registradas por la **Global Meteor Network (GMN)** entre 2019 y 2025.

El proyecto estudia la asociación entre el brillo observado de los meteoros y la estructura residual de la lluvia. Esta estructura se describe mediante la separación angular respecto al radiante esperado y las desviaciones del vector de velocidad geocéntrica.

## Datos utilizados

Cada fila de la base representa una trayectoria de meteoro reconstruida a partir de observaciones realizadas desde varias estaciones.

Los archivos de GMN contienen, entre otras variables:

- Fecha y hora de observación.
- Longitud solar.
- Clasificación de la lluvia de meteoros.
- Coordenadas del radiante geocéntrico.
- Velocidad geocéntrica.
- Incertidumbres de posición y velocidad.
- Magnitud absoluta de pico.
- Altura del máximo de brillo.
- Número y nombres de las estaciones participantes.
- Indicadores de calidad geométrica y del ajuste.

La magnitud astronómica utiliza una escala inversa: los valores más negativos corresponden a meteoros más brillantes.

Los datos originales se conservan sin modificaciones. Las correcciones, selecciones y variables derivadas se almacenan en nuevas columnas y archivos procesados.

## Estructura del repositorio

```text
Investigacion/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│       ├── geminidas_v1/
│       │   └── metadata/
│       └── geminidas_modelado_v1/
│           └── metadata/
│
├── notebooks/
│   ├── 01_auditoria_y_limpieza.ipynb
│   ├── 02_integracion_multianual.ipynb
│   ├── 03_preparacion_fisica_geminidas.ipynb
│   └── 04_preparacion_modelado_geminidas.ipynb
│
├── references/
├── reports/
│   ├── figures/
│   └── tables/
│
├── src/
├── README.md
├── pyproject.toml
└── uv.lock
```

## Carpetas

### `data/raw/`

Contiene los archivos originales descargados de GMN, separados por año.

Estos archivos son la fuente primaria del proyecto y no se modifican. Cualquier limpieza o transformación se realiza sobre copias.

### `data/interim/`

Contiene productos intermedios generados durante la integración de los archivos anuales.

Su función es separar los datos originales de las bases que ya fueron homologadas, combinadas o parcialmente transformadas.

### `data/processed/geminidas_v1/`

Contiene las bases físicas generadas después de seleccionar las Gemínidas, corregir su deriva temporal y calcular las variables necesarias para estudiar el radiante y el brillo.

Incluye tres productos principales:

- **Base maestra completa:** conserva las columnas originales y todas las variables derivadas.
- **Base estándar de análisis:** contiene las variables relevantes de las 19,079 trayectorias pertenecientes a la muestra principal.
- **Base estricta de análisis:** contiene 7,040 trayectorias que también cumplen criterios adicionales de calidad.

La muestra estricta es un subconjunto de la muestra estándar. Se utiliza para comprobar si los resultados se conservan al trabajar con observaciones de mayor calidad.

### `data/processed/geminidas_modelado_v1/`

Contiene las bases preparadas específicamente para PCA y machine learning.

Incluye:

- **Base completa de modelado:** contiene todas las trayectorias y su partición temporal.
- **Base de entrenamiento:** contiene las observaciones de 2019 a 2024.
- **Base de prueba:** contiene exclusivamente las observaciones de 2025.

La base de entrenamiento contiene 12,904 trayectorias y la base de prueba contiene 6,175.

La separación por años permite evaluar si los patrones aprendidos con observaciones anteriores se mantienen en un año que no participó en el ajuste.

### Carpetas `metadata/`

Cada conjunto procesado incluye una carpeta de metadatos.

Estas carpetas contienen:

- Diccionarios de variables.
- Descripciones de las bases.
- Parámetros empleados en las transformaciones.
- Resúmenes de las particiones.
- Auditorías de consistencia.
- Verificaciones de los archivos guardados.
- Manifiestos con tamaños y hashes SHA-256.

Los metadatos permiten interpretar las columnas y verificar que los archivos compartidos no hayan sido alterados.

### `notebooks/`

Contiene el código principal del proyecto organizado en el orden en que se desarrolló el procesamiento.

Los notebooks son consecutivos: cada uno utiliza los datos o resultados generados por las etapas anteriores.

### `references/`

Contiene documentación externa necesaria para interpretar las columnas originales, principalmente el diccionario de variables de GMN.

### `reports/figures/`

Está destinada a las figuras finales del PCA, los modelos y el artículo.

No contiene las gráficas exploratorias producidas durante el desarrollo, salvo que posteriormente se seleccionen como resultados definitivos.

### `reports/tables/`

Está destinada a las tablas finales de resultados, métricas, cargas del PCA y resúmenes utilizados en el artículo.

### `src/`

Está reservada para funciones reutilizables que posteriormente puedan extraerse de los notebooks.

Actualmente, la mayor parte del código se encuentra directamente en los notebooks.

### `pyproject.toml`

Define el proyecto de Python y sus dependencias principales.

### `uv.lock`

Registra las versiones exactas de las dependencias utilizadas. Su función es permitir que los integrantes trabajen con el mismo entorno y evitar diferencias causadas por versiones distintas de las bibliotecas.

## Notebooks

### `01_auditoria_y_limpieza.ipynb`

Este notebook examina la estructura de los archivos originales antes de realizar transformaciones físicas.

Revisa:

- Número de filas y columnas.
- Nombres y tipos de variables.
- Valores faltantes y no finitos.
- Registros duplicados.
- Identificadores de trayectoria.
- Códigos de lluvia.
- Variables de calidad e incertidumbre.
- Rangos de las variables físicas.

También define y valida los criterios utilizados para distinguir entre la muestra estándar y la muestra estricta.

Su resultado es una evaluación documentada de la calidad de los datos y de las observaciones que pueden utilizarse en las etapas posteriores.

### `02_integracion_multianual.ipynb`

Este notebook combina los archivos correspondientes a diciembre de 2019, 2020, 2021, 2022, 2023, 2024 y 2025.

Antes de unirlos:

- Comprueba que las columnas sean compatibles.
- Homologa nombres y tipos de datos.
- Conserva el origen de cada registro.
- Agrega la variable `source_year`.
- Revisa que no se pierdan filas.
- Comprueba los identificadores.

Su resultado es una base multianual con una fila por trayectoria y una estructura común para todos los años.

### `03_preparacion_fisica_geminidas.ipynb`

Este notebook construye las variables físicas utilizadas en el análisis.

Primero selecciona las trayectorias clasificadas como Gemínidas y genera:

- La muestra estándar.
- La muestra estricta.

Posteriormente:

- Transforma las coordenadas del radiante.
- Calcula la longitud eclíptica centrada en el Sol.
- Representa las direcciones mediante vectores unitarios.
- Modela el desplazamiento temporal del radiante.
- Modela la evolución de la velocidad geocéntrica.
- Calcula un centro esperado para cada trayectoria.
- Construye una base tangente alrededor de ese centro.
- Calcula residuos longitudinales y latitudinales.
- Calcula la distancia angular al centro esperado.
- Calcula el residuo de velocidad geocéntrica.

El notebook también prepara la información fotométrica:

- Conserva la magnitud original.
- Identifica valores fotométricos sospechosos.
- Crea una magnitud utilizable para análisis.
- Construye grupos descriptivos de brillo.
- Examina la altura del máximo de brillo.
- Revisa sesgos relacionados con año, fase solar y calidad observacional.

Finalmente, genera las bases físicas de `geminidas_v1/` y sus metadatos.

### `04_preparacion_modelado_geminidas.ipynb`

Este notebook transforma la base física en una base destinada al PCA y al modelo de clasificación.

Primero separa las observaciones en:

- Entrenamiento: 2019–2024.
- Prueba temporal: 2025.

Después vuelve a ajustar las referencias físicas utilizando exclusivamente el entrenamiento. Esto evita que las observaciones de 2025 influyan en las variables que posteriormente se utilizarán para evaluarlas.

El notebook:

- Calcula los centros esperados de entrenamiento y prueba.
- Construye los vectores observados y esperados de velocidad.
- Calcula las componentes cartesianas del vector residual.
- Verifica las normas de los vectores.
- Cuenta el número de estaciones participantes.
- Prepara las variables de calidad observacional.
- Trata los valores de incertidumbre iguales a cero.
- Define las clases de brillo.
- Marca las observaciones utilizables para PCA.
- Marca las observaciones utilizables para machine learning.
- Genera las bases de entrenamiento y prueba.

También guarda la configuración del modelado, los parámetros del centro, los diccionarios de variables y las auditorías correspondientes.

## Principales variables derivadas

| Variable | Descripción |
|---|---|
| `id_fila_origen` | Identificador que permite relacionar cada fila procesada con su trayectoria de origen. |
| `source_year` | Año del archivo del que proviene la trayectoria. |
| `delta_sol_lon_deg` | Longitud solar relativa al valor de referencia utilizado para estudiar la actividad de las Gemínidas. |
| `lambda_sce_deg` | Longitud eclíptica del radiante expresada en un sistema centrado en el Sol. |
| `lambda_sce_esperada_deg` | Longitud esperada del centro de la lluvia. |
| `beta_esperada_deg` | Latitud esperada del centro de la lluvia. |
| `vgeo_esperada_km_s` | Velocidad geocéntrica esperada para la fase de actividad. |
| `residuo_lambda_coordenada_deg` | Desplazamiento longitudinal respecto al centro esperado. |
| `residuo_beta_coordenada_deg` | Desplazamiento latitudinal respecto al centro esperado. |
| `distancia_angular_centro_deg` | Separación angular entre el radiante observado y el esperado. |
| `residuo_vgeo_km_s` | Diferencia entre la rapidez observada y la esperada. |
| `delta_v_x_km_s` | Componente cartesiana \(x\) del vector residual de velocidad. |
| `delta_v_y_km_s` | Componente cartesiana \(y\) del vector residual de velocidad. |
| `delta_v_z_km_s` | Componente cartesiana \(z\) del vector residual de velocidad. |
| `norma_delta_v_km_s` | Magnitud del vector residual de velocidad. |
| `magnitud_analisis` | Magnitud de pico después de excluir valores fotométricos sospechosos. |
| `fotometria_utilizable` | Indica si la magnitud puede emplearse en el análisis. |
| `grupo_magnitud` | Grupo descriptivo de brillo asignado a la trayectoria. |
| `clase_brillo_ml` | Clase binaria utilizada por el modelo de clasificación. |
| `particion_modelado` | Indica si la fila pertenece a entrenamiento o prueba. |
| `usar_pca` | Indica si la trayectoria contiene las variables requeridas por el PCA. |
| `usar_ml` | Indica si la trayectoria puede utilizarse en el modelo de clasificación. |
| `numero_estaciones` | Número de estaciones que participaron en la reconstrucción. |
| `sigma_radiante_aprox` | Medida aproximada de la incertidumbre angular del radiante. |
| `Vgeo_sigma_modelo` | Incertidumbre de velocidad preparada para utilizarse como control en el modelo. |

La definición completa de las variables se encuentra en los diccionarios almacenados dentro de las carpetas `metadata/`.

## Archivos procesados principales

### `geminidas_v1`

```text
geminidas_base_maestra_completa_v1.parquet
geminidas_estandar_analisis_v1.parquet
geminidas_estandar_analisis_v1.csv
geminidas_estricta_analisis_v1.parquet
geminidas_estricta_analisis_v1.csv
```

La base maestra conserva todas las variables originales y derivadas. Las vistas estándar y estricta contienen una selección documentada de las columnas necesarias para los análisis físicos.

### `geminidas_modelado_v1`

```text
geminidas_modelado_completo_v1.parquet
geminidas_modelado_entrenamiento_2019_2024_v1.parquet
geminidas_modelado_entrenamiento_2019_2024_v1.csv
geminidas_modelado_prueba_2025_v1.parquet
geminidas_modelado_prueba_2025_v1.csv
```

La base completa conserva todas las trayectorias preparadas para modelado. Las otras bases separan físicamente el entrenamiento y la prueba temporal.

Los archivos Parquet son la versión principal porque conservan mejor los tipos de datos. Los archivos CSV son copias portables para inspección e intercambio.

## Estado del proyecto

Se encuentran terminadas:

- La auditoría inicial.
- La integración multianual.
- La selección de las Gemínidas.
- La preparación de coordenadas.
- La corrección de la deriva temporal.
- El cálculo de residuos físicos.
- La preparación de la magnitud.
- La auditoría de sesgos.
- La construcción de bases portables.
- La separación entre entrenamiento y prueba.
- La preparación inicial de variables para PCA y machine learning.

Se encuentran pendientes:

- La transformación del vector residual a componentes físicas locales.
- El PCA cinemático definitivo.
- El modelo de clasificación.
- La evaluación temporal con 2025.
- La generación de figuras y tablas finales.
- La redacción del artículo.

## Herramientas utilizadas

El proyecto fue desarrollado con Python y Jupyter.

Las principales bibliotecas utilizadas son:

- pandas
- NumPy
- SciPy
- Matplotlib
- seaborn
- statsmodels
- scikit-learn
- PyArrow

Las dependencias y sus versiones se encuentran definidas en `pyproject.toml` y `uv.lock`.