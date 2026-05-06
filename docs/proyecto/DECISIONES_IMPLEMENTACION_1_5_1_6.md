# Decisiones Implementacion 1.5.0 y 1.6.0

## Proposito

Listar las decisiones que deben quedar aprobadas antes de pasar a implementación técnica en `1.5.0` y `1.6.0`.

## Decisiones bloqueantes

### 1. Unidad canónica principal

Debe quedar aprobado el rol de:

- cliente;
- póliza;
- vencimiento;
- relación cliente-póliza;
- metadatos operativos.

### 2. Regla de autoridad

Debe quedar definido:

- que campos seguirán siendo reflejo fiel del origen;
- que campos podrán tener valor propio dentro de la app;
- en que momento un dato operativo editable dejaria de depender exclusivamente del workbook.

### 3. Política de IDs internos

Debe definirse:

- como se identificaran clientes, pólizas y vencimientos internamente;
- como se evitara depender solo de nombres o texto libre;
- como se mantendra trazabilidad con el origen sin exponer PII.

### 4. Tratamiento de duplicados y relaciones

Debe quedar aprobado:

- como manejar una persona con multiples pólizas;
- como interpretar `detalle` cuando sugiera relación entre pólizas;
- como tratar conflicto entre nombre, identificación y número de póliza;
- como distinguir casos que requieren revisión manual.

### 5. Política de normalización

Debe definirse para:

- frecuencia;
- moneda;
- fechas;
- identificaciones;
- placas o finca;
- número de póliza para clasificación técnica.

### 6. Política de sensibilidad

Debe quedar decidido:

- que puede mostrarse en interfaz;
- que puede salir en reportes locales;
- que debe permanecer solo en entorno controlado;
- que no debe aparecer nunca en documentación ni artefactos versionados.

### 7. Criterio de edición futura

Debe quedar definido:

- que campos serán solo lectura;
- que campos admitiran correccion operativa;
- que campos requeriran historial o trazabilidad;
- que campos nunca se deberán sobrescribir sobre el origen.

### 8. Límites por versión futura

#### 1.5.0

Debe enfocarse en:

- modelo interno;
- definicion técnica de entidades;
- capa preliminar de lectura y normalización;
- persistencia o contratos técnicos mínimos, si ya estén aprobados.

#### 1.6.0

Debe enfocarse en:

- primeros flujos controlados sobre dataset canónico;
- validaciones de integridad iniciales;
- soporte operativo sin reemplazar aún el workbook salvo decision explícita posterior.

## Decisiones cerradas en 1.5.0

- El paquete base de la aplicación se llama `app`.
- El entry point técnico oficial es `python -m app`.
- La configuración se centraliza en `app/config/`.
- Rutas, logging y excepciones técnicas viven en `app/core/`.
- Los contratos preliminares del dataset canónico viven en `app/domain/`.
- `app/services/` contiene solo servicios técnicos no funcionales en esta fase.
- No se crean paquetes de GUI, lectura funcional, persistencia, reportes, documentos ni respaldos hasta una fase aprobada.
- La versión `1.5.0` usa solo libreria esténdar de Python.

## Decisiones pendientes para 1.6.0

- Confirmar si se crea `app/ingest/` para lectura controlada del workbook o si se mantiene como contrato abstracto una fase más.
- Definir política inicial de IDs internos para cliente, póliza y vencimiento.
- Definir alcance exacto de la primera lectura no intrusiva del workbook.
- Confirmar si los contratos canónicos se separan por entidad o permanecen en un módulo central.
- Confirmar si SQLite entra en `1.6.0` o se pospone.

## Riesgos a monitorear antes de implementar

- ambigüedades de encabezados o significado real de columnas;
- exceso de rigidez del modelo canónico;
- pérdida de trazabilidad entre origen y app;
- interpretacion apresurada de `detalle`;
- falsa unicidad de identificación o número de póliza;
- mezcla entre campos originales, corregidos y derivados sin distincion clara.

## Criterio de salida de 1.4.0

La fase `1.4.0` estara lista cuando estas decisiones queden documentadas y revisables, aúnque todavía no esten implementadas en código funcional.
