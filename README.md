# Brillo y estructura residual de las Gemínidas

Análisis físico, análisis de componentes principales (PCA) y modelado predictivo del brillo observado de meteoros Gemínidas utilizando datos de **Global Meteor Network (GMN)** de diciembre de 2019 a 2025.

El proyecto estudia si la dispersión angular del radiante y la cinemática residual contienen información asociada con el brillo observado, después de corregir la evolución temporal de la lluvia y considerar la calidad de las observaciones.

## Estado del proyecto

El pipeline principal está compuesto por siete notebooks auditados para ejecutarse secuencialmente:

```text
01 → 02 → 03 → 04 → 05 → 06 → 07
```

Los archivos originales de datos, las bases procesadas y los resultados generados no se almacenan en Git. Se reconstruyen localmente mediante los notebooks.

---

## 1. Requisitos

Se recomienda tener instalado:

- Git
- `uv`
- VS Code con soporte para Jupyter, o Jupyter Lab

El proyecto utiliza **Python 3.13**.

Las dependencias están definidas en:

```text
pyproject.toml
uv.lock
```

No es necesario instalar manualmente cada librería.

---

## 2. Clonar el repositorio

```bash
git clone https://github.com/AlexBytes-23/Investigacion_geminidas.git
cd Investigacion_geminidas
```

---

## 3. Instalar `uv`

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Comprobar la instalación:

```bash
uv --version
```

---

## 4. Preparar el entorno

Desde la raíz del repositorio:

```bash
uv python install 3.13
uv sync --frozen
```

El entorno virtual queda en:

```text
.venv/
```

Comprobar que las dependencias principales funcionan:

```bash
uv run python -c "import numpy, pandas, pyarrow, sklearn, statsmodels, matplotlib, joblib; print('Entorno OK')"
```

Comprobar la versión de Python:

```bash
uv run python --version
```

El proyecto está preparado para Python 3.13.

---

## 5. Descargar los datos originales de GMN

Los archivos originales no se almacenan en Git debido a su tamaño.

Fuente oficial:

https://globalmeteornetwork.org/data/traj_summary_data/monthly/

Descargar los siguientes siete archivos **sin cambiar sus nombres**:

```text
traj_summary_monthly_201912.txt
traj_summary_monthly_202012.txt
traj_summary_monthly_202112.txt
traj_summary_monthly_202212.txt
traj_summary_monthly_202312.txt
traj_summary_monthly_202412.txt
traj_summary_monthly_202512.txt
```

Colocarlos en:

```text
data/raw/
```

La estructura debe verse así:

```text
data/
├── raw/
│   ├── traj_summary_monthly_201912.txt
│   ├── traj_summary_monthly_202012.txt
│   ├── traj_summary_monthly_202112.txt
│   ├── traj_summary_monthly_202212.txt
│   ├── traj_summary_monthly_202312.txt
│   ├── traj_summary_monthly_202412.txt
│   └── traj_summary_monthly_202512.txt
├── interim/
└── processed/
```

### Integridad de los datos

GMN puede actualizar archivos históricos.

El archivo:

```text
references/manifiesto_datos_gmn.csv
```

contiene el nombre, tamaño y SHA-256 de los siete archivos utilizados en la ejecución auditada del proyecto.

Una descarga posterior puede permitir ejecutar correctamente el pipeline sin ser necesariamente idéntica byte por byte a la utilizada para obtener los resultados originales.

---

## 6. Ejecutar los notebooks

Los notebooks deben ejecutarse en orden.

Para una ejecución reproducible:

1. Seleccionar como kernel el Python de `.venv`.
2. Reiniciar el kernel.
3. Ejecutar todas las celdas desde el inicio.
4. No continuar al siguiente notebook si aparece un error.

### 01 — Auditoría inicial y criterios de calidad

```text
notebooks/01_auditoria_y_limpieza.ipynb
```

Examina diciembre de 2019 para comprender la estructura de los datos GMN, revisar incertidumbres, detectar problemas de calidad y justificar los criterios utilizados posteriormente.

Es un notebook diagnóstico: no produce directamente la entrada del notebook 02.

### 02 — Integración multianual

```text
notebooks/02_integracion_multianual.ipynb
```

Carga y homogeneiza los archivos de diciembre de 2019 a 2025.

Genera la base multianual:

```text
data/interim/gmn_diciembre_2019_2025.parquet
```

### 03 — Preparación física de las Gemínidas

```text
notebooks/03_preparacion_fisica_geminidas.ipynb
```

Selecciona las Gemínidas y desarrolla el análisis físico descriptivo.

Incluye:

- coordenadas relativas al Sol;
- fase solar;
- deriva del radiante y de la velocidad;
- construcción del centro descriptivo;
- residuos angulares;
- análisis de la fotometría;
- calidad observacional;
- relación entre brillo y dispersión.

Genera:

```text
data/processed/geminidas_v1/
```

### 04 — Preparación para PCA y aprendizaje automático

```text
notebooks/04_preparacion_modelado_pca_ml.ipynb
```

Separa temporalmente los datos:

```text
2019–2024 → desarrollo
2025      → prueba
```

La referencia física utilizada para el modelado se ajusta únicamente con 2019–2024.

Después se construye el vector residual de velocidad y se proyecta sobre una base física local formada por tres componentes:

```text
paralela
lambda
beta
```

Genera:

```text
data/processed/geminidas_modelado_v2/
```

con las bases de entrenamiento y prueba.

### 05 — Análisis de componentes principales

```text
notebooks/05_pca.ipynb
```

Ajusta un PCA utilizando las tres componentes locales de velocidad residual de 2019–2024.

El brillo no interviene en la construcción de los ejes PCA. Después del ajuste se compara cómo se distribuyen los distintos grupos de brillo sobre esos mismos ejes.

Las tablas y figuras generadas se guardan en:

```text
reports/tables/
reports/figures/
```

### 06 — Desarrollo y selección de modelos

```text
notebooks/06_modelo_ml_geminidas.ipynb
```

Utiliza únicamente información de 2019–2024.

Compara siete modelos mediante validación temporal creciente, incluyendo:

- modelo de control;
- cinemática local lineal;
- cinemática local cuadrática;
- modelos reducidos mediante PCA.

Después selecciona y ajusta los modelos finales con todo el periodo 2019–2024.

Genera:

```text
configs/protocolo_ml_pre2025.json
reports/models/modelos_pre2025.joblib
```

El protocolo registra las decisiones metodológicas previas a la evaluación de 2025 e incluye la huella SHA-256 del archivo de modelos.

### 07 — Evaluación temporal de 2025

```text
notebooks/07_evaluacion_2025.ipynb
```

Carga el protocolo y los modelos congelados y evalúa la partición reservada de 2025.

No reajusta modelos ni transformaciones utilizando 2025.

Calcula:

- ROC-AUC;
- Average Precision;
- exactitud balanceada;
- análisis de sensibilidad;
- matrices de confusión;
- bootstrap pareado de las diferencias;
- dependencia temporal por noche;
- coeficientes del modelo principal.

También genera las figuras finales de evaluación.

---

## 7. Flujo principal de datos

```text
Archivos GMN 2019–2025
        │
        ▼
data/raw/
        │
        ▼
02 Integración multianual
        │
        ▼
data/interim/gmn_diciembre_2019_2025.parquet
        │
        ▼
03 Preparación física
        │
        ▼
data/processed/geminidas_v1/
        │
        ▼
04 Preparación de modelado
        │
        ▼
data/processed/geminidas_modelado_v2/
        │
        ├──────────► 05 PCA
        │
        └──────────► 06 Desarrollo ML
                          │
                          ▼
                   modelos pre-2025
                          │
                          ▼
                   07 Evaluación 2025
```

El notebook 01 aparece al inicio porque documenta y justifica los criterios utilizados posteriormente, aunque no genera directamente la entrada del notebook 02.

---

## 8. Resultados generados

Los productos del análisis se escriben localmente en:

```text
reports/
├── figures/
├── models/
└── tables/
```

Estos archivos no se almacenan normalmente en Git porque pueden regenerarse ejecutando el pipeline.

Entre los productos se encuentran:

- parámetros y puntuaciones del PCA;
- tablas de validación interna;
- estabilidad de coeficientes;
- predicciones individuales de 2025;
- métricas externas;
- intervalos bootstrap;
- matrices de confusión;
- curvas ROC;
- curvas precisión–exhaustividad;
- manifiestos de integridad.

---

## 9. Estructura del repositorio

```text
configs/        configuración metodológica
data/raw/       archivos originales de GMN
data/interim/   productos intermedios
data/processed/ bases derivadas del proyecto
notebooks/      pipeline principal 01–07
references/     documentación y manifiestos de datos
reports/        resultados generados
src/            funciones reutilizables
```

Los datos y resultados generados están excluidos mediante `.gitignore`.

---

## 10. Reproducibilidad

Para comprobar el pipeline desde una instalación nueva:

1. Clonar el repositorio.
2. Ejecutar `uv sync --frozen`.
3. Colocar únicamente los siete archivos originales de GMN en `data/raw/`.
4. Verificar, si se desea una reproducción exacta, sus SHA-256 contra `references/manifiesto_datos_gmn.csv`.
5. Ejecutar los notebooks 01 → 07 en orden.

Durante esta prueba no deben reutilizarse bases procesadas, modelos ni resultados obtenidos en otra instalación.

---

## 11. Fuente de los datos

Global Meteor Network:

https://globalmeteornetwork.org/

Archivos mensuales de trayectorias:

https://globalmeteornetwork.org/data/traj_summary_data/monthly/

Descripción de las columnas utilizadas:

```text
references/GMN_orbit_data_columns.pdf
```

Los datos de Global Meteor Network deben citarse conforme a las condiciones de atribución correspondientes.