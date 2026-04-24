# Mapa Origen a Canonico

## Proposito

Documentar, de forma segura y abstracta, como se espera que el workbook operativo alimente el dataset canonico interno.

Este documento no usa ejemplos reales ni valores sensibles. Solo describe mapeos estructurales, transformaciones y estado de validacion.

## Reglas de seguridad

- No incluir muestras reales de filas.
- No incluir catalogos reconstruidos desde datos sensibles.
- No incluir nombres reales, identificaciones, polizas completas, placas ni texto libre real.
- Usar nombre de columna original solo cuando ya sea conocido documentalmente y no implique exponer datos de fila.
- Si una columna real no esta confirmada o su encabezado es incierto, usar alias tecnico seguro.

## Convenciones

### Estado

- `confirmado`: la procedencia es consistente con auditoria y reglas conocidas.
- `preliminar`: la procedencia parece probable, pero requiere validacion humana.
- `pendiente de validacion`: no hay suficiente certeza para implementacion.

### Transformacion esperada

- `copia`: traslado directo desde origen.
- `normalizacion`: reexpresion controlada del dato original.
- `consolidacion`: union de varios campos de origen.
- `derivacion`: calculo desde reglas aprobadas.
- `revision manual`: requiere criterio humano u operacional.

## Mapeo estructural tentativo

| Origen estructural | Alias tecnico | Entidad destino | Campo canonico | Tipo | Sensible | Editable futuro | Transformacion esperada | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nombre de cliente o asegurado | ORIG_CLIENTE_NOMBRE | Cliente | nombre_original | Original | Si | No | copia | preliminar |
| Tipo de identificacion | ORIG_CLIENTE_TIPO_ID | Cliente | tipo_identificacion_normalizado | Normalizado | Si | No | normalizacion | preliminar |
| Identificacion | ORIG_CLIENTE_ID | Cliente | identificacion_original | Original | Si | No | copia | confirmado |
| Identificacion | ORIG_CLIENTE_ID | Cliente | identificacion_normalizada | Normalizado | Si | No | normalizacion | preliminar |
| Telefono | ORIG_CLIENTE_TELEFONO | Cliente | telefono_original | Original | Si | No | copia | preliminar |
| Correo | ORIG_CLIENTE_CORREO | Cliente | correo_original | Original | Si | No | copia | preliminar |
| Direccion | ORIG_CLIENTE_DIRECCION | Cliente | direccion_original | Original | Si | No | copia | preliminar |
| Numero de Poliza | ORIG_POLIZA_NUMERO | Poliza | numero_poliza_original | Original | Si | No | copia | confirmado |
| Numero de Poliza | ORIG_POLIZA_NUMERO | Poliza | numero_poliza_normalizado | Normalizado | Si | No | normalizacion | preliminar |
| Tipo de seguro | ORIG_POLIZA_TIPO | Poliza | tipo_seguro_original | Original | No | No | copia | preliminar |
| Aseguradora | ORIG_POLIZA_ASEGURADORA | Poliza | aseguradora_original | Original | No | No | copia | preliminar |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Poliza | vigencia_original | Original | No | No | copia | confirmado |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Poliza | frecuencia_normalizada | Normalizado | No | No | normalizacion | preliminar |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Poliza | frecuencia_observada | Derivado | No | No | derivacion | confirmado |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Poliza | es_dm | Derivado | No | No | derivacion | confirmado |
| Numero de Poliza | ORIG_POLIZA_NUMERO | Poliza | moneda_normalizada | Derivado | No | No | derivacion | preliminar |
| Numero de Poliza | ORIG_POLIZA_NUMERO | Poliza | es_riesgo_trabajo_probable | Derivado | No | No | derivacion | preliminar |
| Numero de Placa / Finca | ORIG_POLIZA_PLACA_FINCA | Poliza | numero_placa_finca_original | Original | Si | No | copia | confirmado |
| detalle | ORIG_POLIZA_DETALLE | Poliza | detalle_original | Original | Si | No | copia | confirmado |
| Dia de vencimiento | ORIG_VENC_DIA | Vencimiento | dia_vencimiento_original | Original | No | No | copia | preliminar |
| Mes de vencimiento | ORIG_VENC_MES | Vencimiento | mes_vencimiento_original | Original | No | No | copia | preliminar |
| Ano de vencimiento | ORIG_VENC_ANO | Vencimiento | ano_vencimiento_original | Original | No | No | copia | preliminar |
| Fecha de vencimiento | ORIG_VENC_FECHA | Vencimiento | fecha_vencimiento_original | Original | No | No | copia | preliminar |
| Dia, mes y ano | ORIG_VENC_PARTES | Vencimiento | fecha_vencimiento_normalizada | Derivado | No | No | consolidacion | preliminar |
| Vigencia o frecuencia | ORIG_POLIZA_VIGENCIA | Poliza | genera_aviso | Derivado | No | No | derivacion | pendiente de validacion |
| detalle | ORIG_POLIZA_DETALLE | Relacion Cliente-Poliza | relacion_detectada_desde_detalle | Derivado | No | No | revision manual | preliminar |
| Hoja de origen | META_HOJA_ORIGEN | Metadatos Operativos | hoja_origen | Operativo | No | No | copia | confirmado |
| Columna de origen | META_COLUMNA_ORIGEN | Metadatos Operativos | columna_origen | Operativo | No | No | copia | confirmado |
| Fila de origen | META_FILA_ORIGEN | Metadatos Operativos | fila_origen | Operativo | No | No | copia | preliminar |

## Zonas de mayor cuidado

### detalle

- Puede mezclar texto libre y relaciones entre polizas.
- Debe mapearse como original sensible.
- Su interpretacion futura no debe automatizarse sin validacion.

### Numero de Poliza

- Sirve como origen de numero original.
- Tambien alimenta clasificaciones derivadas de moneda y riesgo del trabajo probable.
- Su uso como clave unica aun no debe asumirse.

### Fecha de vencimiento

- Puede existir como fecha unica o como dia, mes y ano.
- El canonicado debe soportar ambas formas sin perder trazabilidad del origen.

### Identificacion

- El origen debe preservarse tal como viene.
- La normalizacion futura no debe sobrescribir el valor original.

## Regla de convivencia workbook -> canonico

- El workbook sigue siendo la fuente operativa principal.
- El dataset canonico se disena para lectura, normalizacion y trazabilidad.
- Ningun mapeo de esta fase implica cambiar o renombrar columnas del workbook.
- Las exportaciones futuras deberan alinearse al formato mejorado sin eliminar la referencia al origen.
