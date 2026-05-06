# Mapa Origen a Canonico

## Proposito

Documentar, de forma segura y abstracta, como se espera que el workbook operativo alimente el dataset canónico interno.

Este documento no usa ejemplos reales ni valores sensibles. Solo describe mapeos estructurales, transformaciones y estado de validación.

## Reglas de seguridad

- No incluir muestras reales de filas.
- No incluir catalogos reconstruidos desde datos sensibles.
- No incluir nombres reales, identificaciones, pólizas completas, placas ni texto libre real.
- Usar nombre de columna original solo cuando ya sea conocido documentalmente y no implique exponer datos de fila.
- Si una columna real no está confirmada o su encabezado es incierto, usar alias técnico seguro.

## Convenciones

### Estado

- `confirmado`: la procedencia es consistente con auditoría y reglas conocidas.
- `preliminar`: la procedencia parece probable, pero requiere validación humana.
- `pendiente de validacion`: no hay suficiente certeza para implementación.

### Transformacion esperada

- `copia`: traslado directo desde origen.
- `normalizacion`: reexpresion controlada del dato original.
- `consolidacion`: union de varios campos de origen.
- `derivacion`: calculo desde reglas aprobadas.
- `revision manual`: requiere criterio humano u operaciónal.

## Mapeo estructural tentativo

| Origen estructural | Alias técnico | Entidad destino | Campo canónico | Tipo | Sensible | Editable futuro | Transformacion esperada | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nombre de cliente o asegurado | ORIG_CLIENTE_NOMBRE | Cliente | nombre_original | Original | Si | No | copia | preliminar |
| Tipo de identificación | ORIG_CLIENTE_TIPO_ID | Cliente | tipo_identificacion_normalizado | Normalizado | Si | No | normalización | preliminar |
| Identificacion | ORIG_CLIENTE_ID | Cliente | identificacion_original | Original | Si | No | copia | confirmado |
| Identificacion | ORIG_CLIENTE_ID | Cliente | identificacion_normalizada | Normalizado | Si | No | normalización | preliminar |
| Telefono | ORIG_CLIENTE_TELEFONO | Cliente | telefono_original | Original | Si | No | copia | preliminar |
| Correo | ORIG_CLIENTE_CORREO | Cliente | correo_original | Original | Si | No | copia | preliminar |
| Direccion | ORIG_CLIENTE_DIRECCION | Cliente | direccion_original | Original | Si | No | copia | preliminar |
| Número de Póliza | ORIG_POLIZA_NUMERO | Póliza | numero_poliza_original | Original | Si | No | copia | confirmado |
| Número de Póliza | ORIG_POLIZA_NUMERO | Póliza | numero_poliza_normalizado | Normalizado | Si | No | normalización | preliminar |
| Tipo de seguro | ORIG_POLIZA_TIPO | Póliza | tipo_seguro_original | Original | No | No | copia | preliminar |
| Aseguradora | ORIG_POLIZA_ASEGURADORA | Póliza | aseguradora_original | Original | No | No | copia | preliminar |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Póliza | vigencia_original | Original | No | No | copia | confirmado |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Póliza | frecuencia_normalizada | Normalizado | No | No | normalización | preliminar |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Póliza | frecuencia_observada | Derivado | No | No | derivacion | confirmado |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Póliza | es_dm | Derivado | No | No | derivacion | confirmado |
| Número de Póliza | ORIG_POLIZA_NUMERO | Póliza | moneda_normalizada | Derivado | No | No | derivacion | preliminar |
| Número de Póliza | ORIG_POLIZA_NUMERO | Póliza | es_riesgo_trabajo_probable | Derivado | No | No | derivacion | preliminar |
| Número de Placa / Finca | ORIG_POLIZA_PLACA_FINCA | Póliza | numero_placa_finca_original | Original | Si | No | copia | confirmado |
| detalle | ORIG_POLIZA_DETALLE | Póliza | detalle_original | Original | Si | No | copia | confirmado |
| Día de vencimiento | ORIG_VENC_DIA | Vencimiento | día_vencimiento_original | Original | No | No | copia | preliminar |
| Mes de vencimiento | ORIG_VENC_MES | Vencimiento | mes_vencimiento_original | Original | No | No | copia | preliminar |
| Ano de vencimiento | ORIG_VENC_ANO | Vencimiento | ano_vencimiento_original | Original | No | No | copia | preliminar |
| Fecha de vencimiento | ORIG_VENC_FECHA | Vencimiento | fecha_vencimiento_original | Original | No | No | copia | preliminar |
| Día, mes y año | ORIG_VENC_PARTES | Vencimiento | fecha_vencimiento_normalizada | Derivado | No | No | consolidación | preliminar |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Póliza | genera_aviso | Derivado | No | No | derivacion | pendiente de validación |
| detalle | ORIG_POLIZA_DETALLE | Relacion Cliente-Póliza | relacion_detectada_desde_detalle | Derivado | No | No | revisión manual | preliminar |
| Hoja de origen | META_HOJA_ORIGEN | Metadatos Operativos | hoja_origen | Operativo | No | No | copia | confirmado |
| Columna de origen | META_COLUMNA_ORIGEN | Metadatos Operativos | columna_origen | Operativo | No | No | copia | confirmado |
| Fila de origen | META_FILA_ORIGEN | Metadatos Operativos | fila_origen | Operativo | No | No | copia | preliminar |

## Zonas de mayor cuidado

### detalle

- Puede mezclar texto libre y relaciones entre pólizas.
- Debe mapearse como original sensible.
- Su interpretacion futura no debe automatizarse sin validación.

### Número de Póliza

- Sirve como origen de número original.
- Tambien alimenta clasificaciones derivadas de moneda y riesgo del trabajo probable.
- Su uso como clave única aún no debe asumirse.

### Fecha de vencimiento

- Puede existir como fecha única o como día, mes y año.
- El canonicado debe soportar ambas formas sin perder trazabilidad del origen.

### Identificacion

- El origen debe preservarse tal como viene.
- La normalización futura no debe sobrescribir el valor original.

## Regla de convivencia workbook -> canónico

- El workbook sigue siendo la fuente operativa principal.
- El dataset canónico se diseña para lectura, normalización y trazabilidad.
- Ningun mapeo de esta fase implica cambiar o renombrar columnas del workbook.
- Las exportaciones futuras deberán alinearse al formato mejorado sin eliminar la referencia al origen.
