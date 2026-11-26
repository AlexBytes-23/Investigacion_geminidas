# Brillo, radiante y velocidad de las Gemínidas

Proyecto F1009 basado en trayectorias de la **Global Meteor Network (GMN)** de diciembre de 2019 a 2025.

El proyecto estudia cómo se relaciona el brillo observado de las Gemínidas con su estructura angular y cinemática residual. El análisis incluye preparación física de las trayectorias, PCA, modelos de clasificación y una evaluación temporal con 2025.

> **Estado actual:** el repositorio está en auditoría final. Los notebooks 01–03 ya se están limpiando para ejecución reproducible; 04–07 todavía deben pasar la misma revisión. Para probar la instalación y el flujo de datos, por ahora se recomienda ejecutar 01 → 02 → 03.

---

## 1. Qué necesitas

Para trabajar con el repositorio se recomienda:

- Git.
- `uv` para instalar Python y las dependencias.
- Un editor con soporte para Jupyter, como VS Code, o Jupyter Lab.

No es necesario instalar Python manualmente si se usa `uv`: `uv` puede instalar Python 3.13 para el proyecto.

El proyecto utiliza el entorno definido en:

- `pyproject.toml`
- `uv.lock`

No instales las librerías una por una con `pip` salvo que estés modificando deliberadamente el entorno del proyecto.

---

## 2. Obtener el repositorio

### Con Git

```bash
git clone https://github.com/AlexBytes-23/Investigacion_geminidas.git
cd Investigacion_geminidas
```

También se puede descargar el repositorio como ZIP desde GitHub y descomprimirlo en una carpeta local.

Conviene trabajar en una carpeta local normal, por ejemplo `Documents/` o `Proyectos/`. Evita mover los notebooks fuera del repositorio porque las rutas del proyecto están diseñadas para trabajar con esta estructura.

---

## 3. Instalar `uv`

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Cierra y vuelve a abrir la terminal si `uv` no aparece inmediatamente.

Comprueba la instalación:

```powershell
uv --version
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Después:

```bash
uv --version
```

---

## 4. Crear el entorno del proyecto

Desde la raíz del repositorio:

```bash
uv python install 3.13
uv venv --python 3.13
uv sync --frozen
```

Esto crea el entorno virtual del proyecto en:

```text
.venv/
```

Para comprobar que las librerías principales se importan correctamente:

```bash
uv run python -c "import numpy, pandas, pyarrow, sklearn, statsmodels, matplotlib, joblib; print('Entorno OK')"
```

Si aparece:

```text
Entorno OK
```

el entorno básico está listo.

---

## 5. Descargar los datos de GMN

Los archivos de datos originales **no se guardan en Git** porque son grandes.

Fuente oficial:

https://globalmeteornetwork.org/data/traj_summary_data/monthly/

Descarga los siguientes siete archivos sin cambiarles el nombre:

```text
traj_summary_monthly_201912.txt
traj_summary_monthly_202012.txt
traj_summary_monthly_202112.txt
traj_summary_monthly_202212.txt
traj_summary_monthly_202312.txt
traj_summary_monthly_202412.txt
traj_summary_monthly_202512.txt
```

Como referencia, los archivos publicados actualmente tienen tamaños aproximados de 10, 16, 29, 41, 60, 79 y 105 MB, respectivamente. Los tamaños pueden cambiar si GMN actualiza los archivos históricos.

Crea esta carpeta dentro del repositorio:

```text
data/
└── raw/
```

y coloca ahí los siete archivos:

```text
Investigacion_geminidas/
├── data/
│   └── raw/
│       ├── traj_summary_monthly_201912.txt
│       ├── traj_summary_monthly_202012.txt
│       ├── traj_summary_monthly_202112.txt
│       ├── traj_summary_monthly_202212.txt
│       ├── traj_summary_monthly_202312.txt
│       ├── traj_summary_monthly_202412.txt
│       └── traj_summary_monthly_202512.txt
├── notebooks/
├── reports/
├── src/
├── pyproject.toml
└── uv.lock
```

### Nota de reproducibilidad

GMN puede actualizar archivos históricos. Por eso una descarga nueva permite probar el pipeline, pero no garantiza por sí sola obtener exactamente los mismos conteos y resultados de una ejecución anterior.

Antes de cerrar la versión final del proyecto se añadirá un manifiesto de integridad con los archivos o huellas SHA-256 correspondientes al conjunto utilizado para los resultados definitivos.

---

## 6. Abrir los notebooks

### Opción A: VS Code

Abre **la carpeta completa del repositorio**, no un notebook aislado.

En VS Code selecciona como kernel de Jupyter el Python del entorno `.venv`.

En Windows normalmente será:

```text
.venv\Scripts\python.exe
```

En macOS / Linux:

```text
.venv/bin/python
```

### Opción B: Jupyter Lab

Desde la raíz del repositorio:

```bash
uv run jupyter lab
```

---

## 7. Orden de los notebooks

El proyecto está organizado en siete notebooks.

### 01 — Auditoría inicial y criterios de calidad

```text
notebooks/01_auditoria_y_limpieza.ipynb
```

Usa diciembre de 2019 como caso diagnóstico para entender la estructura de GMN, revisar calidad y estudiar los criterios que se aplicarán después.

No genera un archivo necesario para el notebook 02. Su papel es metodológico y diagnóstico.

### 02 — Integración multianual

```text
notebooks/02_integracion_multianual.ipynb
```

Carga los siete diciembres de 2019–2025, homogeneiza los datos, aplica los criterios de calidad y genera:

```text
data/interim/gmn_diciembre_2019_2025.parquet
```

El notebook 03 depende de este archivo.

### 03 — Preparación física de las Gemínidas

```text
notebooks/03_preparacion_fisica_geminidas.ipynb
```

Selecciona las Gemínidas, construye coordenadas relativas al Sol, estudia la deriva del radiante y de la velocidad, calcula el centro descriptivo y los residuos físicos, prepara la fotometría y analiza posibles sesgos observacionales.

Genera la carpeta:

```text
data/processed/geminidas_v1/
```

### 04 — Preparación para PCA y aprendizaje automático

```text
notebooks/04_preparacion_modelado_pca_ml.ipynb
```

Separa 2019–2024 de 2025, aprende una referencia física exclusivamente con 2019–2024 y construye las componentes locales de velocidad residual.

Genera:

```text
data/processed/geminidas_modelado_v2/
```

### 05 — PCA

```text
notebooks/05_pca.ipynb
```

Ajusta el PCA con las trayectorias de entrenamiento y describe cómo se organiza la variación de las tres componentes de velocidad residual.

### 06 — Modelos de clasificación

```text
notebooks/06_modelo_ml_geminidas.ipynb
```

Compara modelos de control y modelos con información cinemática usando validación temporal interna sobre 2019–2024. Después ajusta y guarda los modelos finales previos a 2025.

### 07 — Evaluación temporal de 2025

```text
notebooks/07_evaluacion_2025.ipynb
```

Carga los modelos congelados y evalúa su rendimiento sobre 2025. Guarda predicciones, métricas y figuras.

---

## 8. Flujo de archivos

```text
GMN 2019–2025
      │
      ▼
data/raw/
      │
      ▼
02_integracion_multianual
      │
      ▼
data/interim/gmn_diciembre_2019_2025.parquet
      │
      ▼
03_preparacion_fisica_geminidas
      │
      ▼
data/processed/geminidas_v1/
      │
      ▼
04_preparacion_modelado_pca_ml
      │
      ▼
data/processed/geminidas_modelado_v2/
      │
      ├──────────────► 05_pca
      │
      └──────────────► 06_modelo_ml_geminidas
                              │
                              ▼
                    modelos pre-2025
                              │
                              ▼
                    07_evaluacion_2025
```

El notebook 01 queda al inicio porque documenta y justifica la preparación, aunque no produce directamente el archivo de entrada del 02.

---

## 9. Primera prueba recomendada

Mientras continúa la auditoría final del repositorio, prueba primero:

```text
01 → 02 → 03
```

Para cada notebook:

1. Reinicia el kernel.
2. Ejecuta **Run All** desde la primera celda.
3. No ejecutes celdas fuera de orden.
4. Si aparece un error, no continúes con el siguiente notebook.
5. Conserva el mensaje completo del error.

Después del notebook 02 debe existir:

```text
data/interim/gmn_diciembre_2019_2025.parquet
```

Después del notebook 03 debe existir:

```text
data/processed/geminidas_v1/
```

Cuando 04–07 terminen su auditoría, esta misma prueba se ampliará a la cadena completa.

---

## 10. Carpetas principales

```text
configs/       configuración metodológica
data/raw/      datos originales descargados de GMN
data/interim/  productos intermedios
data/processed/ bases derivadas del proyecto
notebooks/     análisis principal
references/    documentación de las variables GMN
reports/       tablas, figuras y modelos generados
src/           funciones reutilizables
```

Los directorios de datos están excluidos de Git mediante `.gitignore`.

---

## 11. Qué no hacer

- No renombres los archivos mensuales de GMN.
- No combines manualmente entrenamiento y 2025 para ajustar modelos.
- No ejecutes los notebooks en orden arbitrario.
- No sobrescribas los archivos originales en `data/raw/`.
- No uses `pip install` para cambiar dependencias sin actualizar deliberadamente `pyproject.toml` y `uv.lock`.
- No interpretes los archivos guardados en `reports/` como entradas originales: son productos del análisis.

---

## 12. Fuente de los datos

Global Meteor Network:

https://globalmeteornetwork.org/

Datos mensuales de trayectorias:

https://globalmeteornetwork.org/data/traj_summary_data/monthly/

Descripción de columnas:

```text
references/GMN_orbit_data_columns.pdf
```

Los datos orbitales de GMN se publican bajo licencia CC BY 4.0. Debe citarse la fuente correspondiente en cualquier trabajo derivado.
