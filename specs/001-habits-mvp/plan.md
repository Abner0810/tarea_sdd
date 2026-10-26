# Plan: habits-cli (MVP) - Habitos alimentarios


## 1. Estructura de modulos

Objetivo: cumplir RNF-3 (separacion entre logica e interfaz). Todos los nombres y mensajes en espanol.

| Modulo | Responsabilidad | RF cubiertos |
|---|---|---|
| habitos/ | Paquete principal (logica de negocio). | RF-1, RF-2, RF-3 |
| habitos/modelo.py | Entidades y validaciones del modelo. Mantiene regla de nombres unicos ignorando mayusculas/minusculas. | RF-1 |
| habitos/servicio.py | Reglas de negocio: crear habito, marcar como hecho hoy, calcular racha. Sin prints ni argumentos CLI. | RF-1, RF-2, RF-3 |
| habitos/repositorio.py | Persistencia JSON local (unico archivo). Lee/escribe de forma legible y predecible. | RNF-5 |
| cli.py | Interfaz CLI (traduce entradas/salidas/errores). Solo esta capa usa print, sys.exit y parsing de argumentos. | RF-1, RF-2, RF-3 (interfaz) |
| main.py | Punto de entrada. | N/A |
| 	ests/ | Tests unitarios para logica de negocio. | RNF-4 |
| habitos/datos/habitos.json | Archivo de persistencia (unico). | RNF-5 |

**Trazabilidad:** Todo debe trazar a RF segun principio 2 de la constitucion.
## 2. Modelo de datos JSON con un ejemplo

**Principio 5:** Unico archivo JSON local.

**Esquema (idea):**

```json
{
  "habitos": [
    {
      "id": "beber-agua",
      "nombre": "Beber agua",
      "marcas": ["2026-10-25", "2026-10-26"]
    }
  ]
}
```

**Notas:**
- `nombre` es el nombre original tal como fue creado.
- La unicidad se verifica ignorando mayusculas/minusculas (RF-1).
- Las marcas son fechas en formato `YYYY-MM-DD` registradas al marcar como hecho hoy.
- `id` o clave interna puede derivarse, pero siempre se valida unicidad por nombre normalizado.
- **RF cubiertos:** RF-1, RF-3 (persistencia de marcas). **RNF-5.**
## 3. Algoritmo de cálculo de racha en pseudocódigo

**Base:** fecha del sistema (`datetime.date.today()`) segun RF-3. La racha se mantiene hasta el ultimo dia marcado si hoy no se marco (Pregunta 4/A). La racha se reinicia si hay un salto (dias no consecutivos). **RF cubiertos:** RF-3.

**Pseudocódigo (en español):**
```text
1. Obtener fecha_hoy = fecha_actual_del_sistema()
2. Obtener lista de marcas ordenadas asc por fecha: marcas_ordenadas = sorted(habito.marcas)
3. Si marcas_ordenadas esta vacia: racha = 0; retornar racha
4. Encontrar la secuencia consecutiva mas reciente hacia atras desde la fecha mas cercana a fecha_hoy que este marcada:
   - Tomar la ultima marca L = max(marcas_ordenadas)
   - Si L < fecha_hoy - 1 dia: racha = 0 (hay salto, no hay consecutividad reciente)
   - Si L == fecha_hoy - 1 dia: contar hacia atras dias consecutivos hasta encontrar una marca faltante
   - Si L == fecha_hoy: contar hacia atras dias consecutivos hasta encontrar una marca faltante (hoy ya marcado)
5. Contar longitud de esa secuencia consecutiva: racha = numero de dias en la secuencia
6. Retornar racha

Reglas:
- "Días consecutivos" = diferencia de 1 día calendario entre marcas sucesivas hacia atras desde el punto de partida (ultimo marcado relevante)
- Si hoy no esta marcado pero ayer si y hay consecutivos antes, se cuenta hasta ayer (no se pone a 0) - CL-5
- Si hay salto (falta un dia), la racha de la secuencia mas reciente se rompe (se reinicia) 
```
## 4. Contrato de la CLI (comandos, salidas, códigos de salida)

**Principio 3:** CLI solo traduce entradas/salidas/errores. Códigos de salida son parte de interfaz. **Principio 6:** español. **RF cubiertos:** RF-1, RF-2, RF-3.

| Comando (idea) | Acción | Éxito (salida) | Errores | Código salida |
|---|---|---|---|---|
| `crear <nombre>` | Crear hábito alimentario (RF-1). Validar nombre no vacío/solo espacios, unicidad ignorando mayúsculas/minúsculas. | Mensaje en español confirmando creación (ej. "Hábito creado: ...") | Nombre vacío/espacios -> error; duplicado (ignorando mayúsculas/minúsculas) -> error | 0 en éxito, distinto a 0 en error |
| `marcar <nombre>` | Marcar como hecho hoy (RF-2). Fecha = `date.today()`. | Mensaje en español confirmando marca (ej. "Marcado como hecho hoy: ...") | Ya marcado hoy -> error; hábito inexistente -> error | 0 en éxito, distinto a 0 en error |
| `listar` o `listar [<nombre>]` | Listar hábitos con racha (RF-3). Si se pasa nombre, se valida existencia (RF-2/RF-3) y se lista ese hábito o da error. Si es listado global, comportamiento por definir detalles pero debe cubrir lista vacía. | Para cada hábito: mostrar nombre y racha de días consecutivos. Formato flexible para plan pero en español. | Si se especifica un nombre y no existe -> error y código distinto a 0. | 0 en éxito, distinto a 0 en error |

**Notas:** Los mensajes son en español. Los códigos de salida distintos a 0 en errores corresponden a la interfaz CLI.
## 5. Decisiones técnicas justificadas (y su alternativa descartada)

| Decisión | Justificación | Alternativa descartada | RF/RNF |
|---|---|---|---|
| **Solo biblioteca estándar de Python** | Cumple RNF-2 y simplicidad (constitución 1). Sin dependencias externas. | Usar `click`/`typer`/`rich` | RNF-2 |
| **Separación lógica/interfaz (servicio.py vs cli.py)** | Cumple constitución 3 y facilita tests unitarios de reglas de negocio. | Mezclar lógica con `print`/`argparse` en un solo archivo | RNF-3 |
| **Persistencia en único archivo JSON** | Cumple constitución 5, legible, predecible, sin BD. | SQLite/archivos CSV/binarios | RNF-5 |
| **Unicidad ignorando mayúsculas/minúsculas** | Respuesta pregunta 1. | Case-sensitive | RF-1 |
| **Rechazar marcar dos veces el mismo día** | Respuesta pregunta 2 (A). | Ignorar silenciosamente | RF-2 |
| **Usar `datetime.date.today()`** | Respuesta pregunta 3 (A). | Fecha manual configurable | RF-3 |
| **Racha hasta último marcado si hoy no marcado** | Respuesta pregunta 4 (A). | Poner a 0 si hoy no marcado | RF-3, CL-5 |
| **Rechazar nombre vacío/solo espacios** | Respuesta pregunta 5. | Aceptar o normalizar a vacío | RF-1 |
| **Error + código distinto a 0 si no existe** | Respuesta pregunta 6 (A). | Crear automáticamente o ignorar | RF-2, RF-3 |

**Trazabilidad:** Cada decisión se vincula a RF o RNF.
## 6. Estrategia de tests

**Principio 4:** Reglas de negocio cubiertas por tests verificables. **RNF-3:** Tests enfocan lógica (servicio/modelo), no solo CLI. Todo en español.

| Tipo de test | Qué cubre | RF/RNF |
|---|---|---|
| **Unitarios (modelo/validaciones)** | Nombre vacío/solo espacios -> error; unicidad ignorando mayúsculas/minúsculas. | RF-1 |
| **Unitarios (servicio - crear)** | Crear hábito válido se registra; duplicado rechazado. | RF-1 |
| **Unitarios (servicio - marcar)** | Marcar hoy registra marca; marcar dos veces mismo día -> error; hábito inexistente -> error. | RF-2 |
| **Unitarios (servicio - racha)** | Cálculo con fecha base `date.today()` (mockear fecha para tests); racha mantiene hasta último marcado si hoy no marcado; racha se reinicia tras salto; racha 0 si sin marcas o roto. | RF-3, CL-5 |
| **Unitarios (repositorio/persistencia)** | Guardar/cargar JSON único, legible. | RNF-5 |
| **Integración mínima (CLI)** | Traduce errores a mensajes en español y códigos de salida distintos a 0. Verifica separación lógica/interfaz. | RF-1,RF-2,RF-3, RNF-3 |

**Notas:** Usar `unittest.mock` para simular `datetime.date.today()` si es necesario. Sin dependencias externas (constitución 1).
