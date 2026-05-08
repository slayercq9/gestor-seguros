# Estándares de Columnas del Control Cartera

## Propósito

Este documento define los estándares funcionales preliminares de las columnas del `Control Cartera` para orientar la visualización, edición futura, validaciones posteriores y depuración progresiva de datos.

La fase `1.10.2` no modifica el archivo Excel, no guarda cambios, no implementa ComboBox y no aplica validaciones fuertes. Solo documenta criterios y oculta visualmente las columnas de coberturas, conservando sus valores en memoria.

## Alcance

Aplica a la lectura directa del archivo `data/input/CONTROLCARTERA_V2.xlsx` y a la GUI local del proyecto.

Incluye:

- matriz funcional de columnas principales;
- criterios de editabilidad y visibilidad;
- reglas preliminares de uso por campo;
- ocultamiento visual de coberturas;
- preparación para controles y validaciones futuras.

No incluye:

- guardado persistente;
- eliminación de datos;
- validaciones bloqueantes;
- catálogos definitivos;
- generación de vencimientos;
- exportaciones o reportes.

## Reglas Generales

- Los nombres y valores originales deben conservarse.
- Los campos que pueden contener números, identificaciones, pólizas, placas o teléfonos deben tratarse como texto cuando exista riesgo de perder ceros iniciales, guiones o letras.
- La tabla principal, el detalle y la edición deben usar columnas visibles aprobadas.
- Las columnas ocultas no deben eliminarse de los registros en memoria.
- Los cambios de edición siguen siendo solo en memoria.
- Las validaciones futuras deben advertir primero y bloquear solo cuando exista aprobación funcional.

## Matriz Resumen

| Columna | Editable | Puede quedar vacía | Tipo esperado | Control futuro | Visible tabla | Visible detalle | Visible edición | Búsqueda |
|---|---|---:|---|---|---:|---:|---:|---:|
| Nº Póliza | Con cautela | No | Texto | Campo de texto | Sí | Sí | Sí | Sí |
| Nombre del Asegurado | Sí, con cuidado | No debería | Texto | Campo de texto | Sí | Sí | Sí | Sí |
| Cédula | Con cautela | Sí | Texto | Campo de texto | Sí | Sí | Sí | Sí |
| Nº Placa / Finca | Sí | Sí | Texto | Campo de texto | Sí | Sí | Sí | Sí |
| Emisión | Sí, con cautela | No debería | Fecha | Campo de fecha | Sí | Sí | Sí | Sí |
| Vigencia | Sí | No | Categoría | ComboBox | Sí | Sí | Sí | Sí |
| DÍA | Sí | No debería | Número o texto numérico | ComboBox o selector numérico | Sí | Sí | Sí | Sí |
| MES | Sí | No debería | Número o texto numérico | ComboBox | Sí | Sí | Sí | Sí |
| AÑO | Sí | No debería | Número o texto numérico | Campo numérico o ComboBox dinámico | Sí | Sí | Sí | Sí |
| Monto Asegurado | Sí | Sí | Monto / moneda | Campo de texto numérico | Sí | Sí | Sí | Sí |
| Prima | Sí | Sí | Monto | Campo de texto numérico | Sí | Sí | Sí | Sí |
| Teléfono | Sí | Sí | Texto | Campo de texto | Sí | Sí | Sí | Sí |
| Correo | Sí | Sí | Correo / texto | Campo de texto | Sí | Sí | Sí | Sí |
| Tipo de Póliza | Sí | No debería | Categoría | ComboBox basado en catálogo real | Sí | Sí | Sí | Sí |
| Detalle | Sí | Sí | Texto largo | Área de texto multilínea | Sí | Sí | Sí | Sí |
| Columnas de coberturas | Futuro | Sí | Mixto | Ocultas por ahora | No | No | No | No |

## Detalle Funcional por Columna

### Nº Póliza

- Uso de negocio: identifica la póliza registrada en el Control Cartera.
- Ejemplos de valores: pólizas con prefijo `01`, pólizas con prefijo `02`, pólizas completamente numéricas y códigos como `AUT`, `INC`, `VG`, `FID`, `RCG`, `VTM`, `ACI`.
- Editable: con cautela.
- Puede quedar vacía: no, es obligatoria.
- Tipo de dato esperado: texto.
- Control recomendado futuro: campo de texto.
- Valores permitidos: libre, conservando formato original.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: advertir si queda vacío; detectar moneda preliminar por prefijo cuando aplique; detectar tipo preliminar por código; no bloquear valores desconocidos hasta madurar el catálogo.
- Observaciones: no convertir a número, conservar ceros iniciales, `01` indica colones, `02` indica dólares, la regla `01/02` no aplica para pólizas completamente numéricas, y estas últimas corresponden a riesgos de trabajo. `AUT` corresponde a vehículos, `INC` a incendio/casas, `VG` a vida global, `FID` a fidelidad individual, `RCG` a responsabilidad civil, `VTM` a vida colectiva y `ACI` a estudiante.

### Nombre del Asegurado

- Uso de negocio: identifica al cliente, asegurado, empresa, cooperativa, asociación o persona relacionada con la póliza.
- Ejemplos de valores: nombres personales, empresas, siglas, asociaciones o referencias operativas.
- Editable: sí, con cuidado.
- Puede quedar vacía: no debería.
- Tipo de dato esperado: texto, puede incluir números, siglas o referencias.
- Control recomendado futuro: campo de texto.
- Valores permitidos: libre.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: advertir si queda vacío; no eliminar espacios internos válidos; no forzar mayúsculas o minúsculas automáticamente.
- Observaciones: debe respetarse el nombre tal como aparece en la base.

### Cédula

- Uso de negocio: identifica al asegurado o cliente.
- Ejemplos de valores: cédula física, cédula jurídica, pasaporte o identificación extranjera.
- Editable: con cautela.
- Puede quedar vacía: sí, aunque no debería.
- Tipo de dato esperado: texto.
- Control recomendado futuro: campo de texto.
- Valores permitidos: libre.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: no convertir a número; conservar guiones, letras o caracteres especiales; no imponer un único formato nacional; advertir si queda vacía.
- Observaciones: puede contener identificaciones extranjeras.

### Nº Placa / Finca

- Uso de negocio: registra placas de vehículos o referencias de finca según el tipo de póliza.
- Ejemplos de valores: placas, referencias de finca o texto operativo.
- Editable: sí.
- Puede quedar vacía: sí.
- Tipo de dato esperado: texto.
- Control recomendado futuro: campo de texto.
- Valores permitidos: libre.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: no convertir a número; conservar letras y ceros iniciales; permitir vacío cuando la póliza no aplique a vehículo o finca.
- Observaciones: generalmente se usa para placas, pero no debe limitarse únicamente a vehículos.

### Emisión

- Uso de negocio: indica la fecha de emisión de la póliza.
- Ejemplos de valores: fechas en formato Excel o texto con formato de fecha.
- Editable: sí, con cautela.
- Puede quedar vacía: no debería, pero puede haber datos históricos incompletos.
- Tipo de dato esperado: fecha.
- Control recomendado futuro: campo de fecha.
- Valores permitidos: fecha válida.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: advertir si no tiene formato de fecha válido; no transformar automáticamente fechas ambiguas; mantener compatibilidad con el formato original del Excel; en visualización no debe mostrar hora, solo fecha.
- Observaciones: en visualización debe presentarse como fecha sin hora, preferiblemente `YYYY-MM-DD`. Esta corrección no modifica el valor original del Excel ni transforma permanentemente el dato.

### Vigencia

- Uso de negocio: indica la frecuencia, modalidad o periodicidad de la póliza.
- Ejemplos de valores: `Mensual`, `Trimestral`, `Semestral`, `Anual`, `D.M.`.
- Editable: sí.
- Puede quedar vacía: no.
- Tipo de dato esperado: categoría.
- Control recomendado futuro: ComboBox.
- Valores permitidos: `Mensual`, `Trimestral`, `Semestral`, `Anual`, `D.M.`.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: usar lista controlada; advertir si aparece un valor fuera del catálogo; no generar aviso de vencimiento para `D.M.`.
- Observaciones: `D.M.` significa deducción mensual. Estas pólizas se almacenan, pero no generan avisos.

### DÍA

- Uso de negocio: día de vencimiento de la póliza.
- Ejemplos de valores: `1` a `31`.
- Editable: sí.
- Puede quedar vacía: no debería si la póliza requiere vencimiento.
- Tipo de dato esperado: número entero o texto numérico.
- Control recomendado futuro: ComboBox o selector numérico.
- Valores permitidos: `1` a `31`.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: validar rango entre 1 y 31; validar coherencia con `MES` y `AÑO`; advertir si está vacío.
- Observaciones: forma parte de la fecha de vencimiento junto con `MES` y `AÑO`.

### MES

- Uso de negocio: mes de vencimiento de la póliza.
- Ejemplos de valores: `1` a `12`.
- Editable: sí.
- Puede quedar vacía: no debería si la póliza requiere vencimiento.
- Tipo de dato esperado: número entero o texto numérico.
- Control recomendado futuro: ComboBox.
- Valores permitidos: `1` a `12`.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: validar rango entre 1 y 12; eventualmente mostrar nombre del mes sin perder el número original.
- Observaciones: debe conservarse como dato útil para generar vencimientos mensuales.

### AÑO

- Uso de negocio: año de vencimiento de la póliza.
- Ejemplos de valores: `2025`, `2026`, `2027`.
- Editable: sí.
- Puede quedar vacía: no debería si la póliza requiere vencimiento.
- Tipo de dato esperado: número entero o texto numérico.
- Control recomendado futuro: campo numérico o ComboBox dinámico.
- Valores permitidos: años razonables según operación.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: validar cuatro dígitos; advertir si el año está muy antiguo o fuera de rango; validar coherencia con `DÍA` y `MES`.
- Observaciones: debe servir para calcular vencimientos y reportes futuros.

### Monto Asegurado

- Uso de negocio: indica el monto cubierto o asegurado por la póliza.
- Ejemplos de valores: montos en colones o dólares.
- Editable: sí.
- Puede quedar vacía: sí.
- Tipo de dato esperado: monto / moneda.
- Control recomendado futuro: campo de texto numérico por ahora.
- Valores permitidos: libre en esta etapa.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: permitir decimales; no perder separadores; no convertir moneda automáticamente; relacionar moneda con prefijo de póliza cuando aplique.
- Observaciones: la moneda puede inferirse por prefijo `01/02`, salvo riesgos de trabajo.

### Prima

- Uso de negocio: indica el monto de la prima asociada a la póliza.
- Ejemplos de valores: montos en colones o dólares.
- Editable: sí.
- Puede quedar vacía: sí.
- Tipo de dato esperado: monto.
- Control recomendado futuro: campo de texto numérico por ahora.
- Valores permitidos: libre en esta etapa.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: validar formato monetario; permitir decimales; evitar convertir a número si eso altera el formato; relacionar moneda con la póliza si corresponde.
- Observaciones: debe mantenerse flexible hasta entender todos los formatos reales usados.

### Teléfono

- Uso de negocio: dato de contacto del cliente o asegurado.
- Ejemplos de valores: número local, celular, varios teléfonos o notas de contacto.
- Editable: sí.
- Puede quedar vacía: sí.
- Tipo de dato esperado: texto.
- Control recomendado futuro: campo de texto.
- Valores permitidos: libre.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: advertir si contiene caracteres inusuales; permitir varios teléfonos; no convertir a número; no eliminar ceros iniciales.
- Observaciones: debe tratarse como texto porque puede incluir más de un número o anotaciones.

### Correo

- Uso de negocio: correo electrónico de contacto.
- Ejemplos de valores: `cliente@dominio.com`.
- Editable: sí.
- Puede quedar vacía: sí.
- Tipo de dato esperado: correo electrónico / texto.
- Control recomendado futuro: campo de texto.
- Valores permitidos: libre en esta etapa.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: validar formato básico de correo; permitir más de un correo si la operación lo requiere; advertir si no contiene `@` cuando se ingresa un valor.
- Observaciones: no debe bloquear el registro si está vacío.

### Tipo de Póliza

- Uso de negocio: clasifica la póliza según su tipo o ramo.
- Ejemplos de valores: auto, incendio, vida, riesgos de trabajo u otros tipos usados en la cartera.
- Editable: sí.
- Puede quedar vacía: no debería, pero puede haber registros incompletos.
- Tipo de dato esperado: categoría.
- Control recomendado futuro: ComboBox basado en catálogo real.
- Valores permitidos: pendiente de definir con base en valores reales.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: crear catálogo de tipos de póliza; advertir si el valor no existe en catálogo; no bloquear valores nuevos hasta que el catálogo esté maduro.
- Observaciones: antes de cerrar una lista de valores conviene revisar los tipos reales existentes. Los tipos pueden inferirse por códigos de pólizas como `AUT`, `ACI`, `INC`, entre otros.

### Detalle

- Uso de negocio: campo libre para observaciones, notas o referencias entre pólizas.
- Ejemplos de valores: anotaciones sobre dueño, relación entre pólizas u observaciones comerciales.
- Editable: sí.
- Puede quedar vacía: sí.
- Tipo de dato esperado: texto largo.
- Control recomendado futuro: área de texto multilínea.
- Valores permitidos: libre.
- Visible en tabla: sí.
- Visible en detalle: sí.
- Visible en edición: sí.
- Búsqueda: sí.
- Validaciones futuras: no aplicar validaciones rígidas; permitir saltos de línea si se decide soportarlos; evitar borrar contenido accidentalmente.
- Observaciones: es importante para contexto operativo y relación entre pólizas de un mismo dueño.

### Columnas de coberturas

- Uso de negocio: representan tipos de cobertura asociados a algunas pólizas.
- Ejemplos de valores: marcadores, textos o montos pendientes de depuración específica.
- Editable: sí en el futuro; de momento ocultas.
- Puede quedar vacía: sí.
- Tipo de dato esperado: mixto / pendiente de depuración.
- Control recomendado futuro: ocultas por ahora.
- Valores permitidos: pendiente.
- Visible en tabla: no.
- Visible en detalle: no.
- Visible en edición: no.
- Búsqueda: no.
- Validaciones futuras: fase específica de depuración de coberturas.
- Observaciones: no deben eliminarse. Se conservan en memoria para futuras exportaciones o depuración, pero se ocultan en tabla, detalle y edición porque actualmente no aportan valor operativo inmediato.

## Reglas de Ocultamiento de Coberturas

En `1.10.2`, las columnas cuyo encabezado contenga la palabra `cobertura` se ocultan visualmente.

Reglas:

- no se muestran en la tabla principal;
- no se muestran en `Detalle del registro`;
- no se muestran en `Editar registro`;
- no aparecen en el selector `Buscar en`;
- no son editables por ahora;
- no generan entradas de bitácora porque no se editan;
- no se eliminan de los datos cargados en memoria;
- no se eliminan del Excel;
- no se guardan cambios.

Si una columna no tiene encabezado confiable, no debe ocultarse automáticamente salvo que exista una regla aprobada que la clasifique como cobertura.

## Preparación para Validaciones Futuras

Las validaciones futuras deberán iniciar como advertencias no bloqueantes. Las prioridades recomendadas son:

- campos obligatorios vacíos;
- conservación de formato textual para pólizas, cédulas, teléfonos y placas;
- coherencia de fecha entre `DÍA`, `MES` y `AÑO`;
- catálogo controlado de `Vigencia`;
- catálogo progresivo de `Tipo de Póliza`;
- revisión específica de coberturas.

## Preparación para Controles por Campo

Controles sugeridos para fases posteriores:

- campos de texto para póliza, nombre, cédula, placa/finca, teléfono y correo;
- ComboBox para `Vigencia`;
- ComboBox o selector numérico para `DÍA` y `MES`;
- campo numérico o ComboBox dinámico para `AÑO`;
- área multilínea para `Detalle`;
- controles específicos de coberturas solo después de depuración funcional.

## Decisiones Abiertas

- Catálogo definitivo de tipos de póliza.
- Tratamiento visual de monedas CRC/USD.
- Estrategia de validación para correos múltiples o teléfonos múltiples.
- Diseño futuro de coberturas.
- Política de guardado seguro y exportación.

## Límite de la Fase 1.10.2

Esta fase no implementa ComboBox, validaciones fuertes, guardado persistente, exportación, eliminación de datos, vencimientos ni DOCX.
