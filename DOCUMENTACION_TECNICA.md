# Documentacion Tecnica

## Objetivos tecnicos

- Mantener una arquitectura modular y escalable.
- Preparar el proyecto para una aplicacion de escritorio en Python.
- Facilitar distribucion portable y, posteriormente, instalador.
- Separar interfaz, persistencia, reglas de negocio, documentos, reportes y respaldos.
- Documentar decisiones, supuestos y riesgos desde el inicio.

## Principios de diseno

- Implementar por fases pequenas y revisables.
- Evitar dependencias hasta que exista una necesidad concreta.
- No introducir logica de negocio definitiva sin datos reales o validacion previa.
- No borrar informacion automaticamente.
- Requerir confirmacion explicita para cualquier eliminacion futura.
- Mantener trazabilidad sobre cambios relevantes.
- Priorizar codigo claro sobre abstracciones prematuras.

## Estrategia incremental

El proyecto avanzara por versiones. Cada version debera definir alcance, entregables, pruebas y documentacion actualizada.

Fases tentativas:

1. Base documental y estructura del repositorio.
2. Esqueleto tecnico de la aplicacion.
3. Modelo de datos preliminar con muestras controladas.
4. Prototipo de interfaz.
5. Importacion validada desde Excel real.
6. Persistencia local.
7. Documentos de vencimiento por cliente.
8. Reportes, respaldos y empaquetado.

## Versionado

El proyecto usa versionado `X.Y.Z`.

- `X` version mayor: cambios estructurales, incompatibles o que redefinen el producto.
- `Y` version menor: nuevas fases, modulos, capacidades o avances funcionales revisables.
- `Z` parche: correcciones acotadas, ajustes documentales menores, mantenimiento o mejoras sin cambio de alcance.

Antes de publicar una version se debe confirmar que el alcance este documentado, que los archivos relevantes hayan sido actualizados y que las pruebas o revisiones aplicables esten registradas.

## Estandar de commits

Los commits deben ser pequenos, revisables y describir una intencion clara. Se recomienda usar un prefijo de tipo:

- `docs`: cambios de documentacion.
- `chore`: mantenimiento sin cambio funcional.
- `feat`: nueva capacidad funcional futura.
- `fix`: correccion de comportamiento futuro.
- `test`: pruebas.
- `refactor`: cambio interno sin cambio esperado de comportamiento.

Ejemplos:

```text
docs: actualizar politica de datos confidenciales
docs: documentar reglas preliminares de polizas
chore: ajustar gitignore para archivos locales
feat: agregar esqueleto de modulo de clientes
test: cubrir validacion de monedas de poliza
```

Cada commit debe evitar mezclar temas no relacionados.

## Estrategia de ramas

La estrategia inicial sera simple:

- `main`: rama estable y revisable.
- `codex/<descripcion>`: ramas de trabajo asistido.
- `feature/<descripcion>`: nuevas capacidades funcionales.
- `docs/<descripcion>`: cambios documentales amplios.
- `fix/<descripcion>`: correcciones acotadas.

Las ramas deben tener nombres cortos, descriptivos y en minusculas, usando guiones cuando sea necesario.

## Criterios de release

Una release debe cumplir, segun aplique:

- version definida en formato `X.Y.Z`;
- entrada actualizada en `CHANGELOG.md`;
- notas de release en `docs/releases/` cuando exista entregable;
- documentacion de usuario actualizada si cambia el uso del sistema;
- documentacion tecnica actualizada si cambia arquitectura, dependencias o reglas;
- pruebas o revisiones registradas;
- confirmacion de que no se incluyen datos reales confidenciales.

Las notas de release deben indicar alcance, cambios principales, limitaciones conocidas, instrucciones de revision y riesgos pendientes.

## Lineamientos de mantenimiento

- Mantener `README.md`, `MANUAL_USUARIO.md` y documentos tecnicos sincronizados con cada version.
- Registrar cambios relevantes en `CHANGELOG.md`.
- Documentar supuestos cuando falte informacion.
- Agregar pruebas cuando exista codigo ejecutable.
- Evitar mezclar cambios funcionales con refactorizaciones no relacionadas.

## Lineamientos de modularidad

La futura aplicacion debera separar responsabilidades:

- interfaz de usuario;
- acceso a datos;
- modelos y validaciones;
- logica de aplicacion;
- generacion de reportes;
- generacion de documentos;
- respaldo y recuperacion;
- utilidades compartidas.

La estructura exacta de paquetes se definira cuando inicie la implementacion tecnica.

## Documentacion del codigo principal

Cuando exista codigo principal, debe quedar documentado de forma suficiente para facilitar mantenimiento:

- modulos con proposito claro;
- funciones publicas con nombres descriptivos;
- comentarios breves en bloques complejos o decisiones no evidentes;
- docstrings cuando una funcion, clase o modulo tenga contrato relevante;
- referencias a reglas de negocio solo cuando hayan sido aprobadas y documentadas.

No se deben agregar comentarios decorativos ni duplicar lo que el codigo ya expresa claramente.

## Calidad textual de futura GUI

Cuando exista interfaz grafica, todo texto visible debe revisarse antes de cada entrega:

- ortografia en espanol;
- consistencia de terminos;
- mensajes claros y accionables;
- uso consistente de moneda, fechas e identificadores;
- confirmaciones explicitas antes de operaciones destructivas;
- respeto por los nombres originales de registros cuando se muestren datos importados.

## Politica de datos confidenciales

La base real es confidencial y no debe subirse a GitHub. Los archivos reales deben mantenerse en rutas locales excluidas por `.gitignore`, como `data/input/`, `data/output/` y `data/backups/`.

No se deben publicar nombres reales, identificaciones, telefonos, correos, placas, fincas, numeros de poliza, archivos originales ni capturas con datos sensibles.

## Politica de anonimizacion para pruebas

Las pruebas podran usar datos ficticios o anonimizados. Una copia anonimizada debe:

- reemplazar nombres reales por nombres ficticios;
- reemplazar identificaciones, telefonos y correos;
- reemplazar placas, fincas y numeros de poliza;
- conservar estructuras de columnas y formatos utiles para pruebas;
- marcarse claramente como muestra o dato ficticio;
- evitar cualquier dato que permita reconstruir informacion real.

La anonimizacion debe preservar patrones tecnicos necesarios para probar el sistema, sin conservar datos sensibles reales.

## Auditoria local segura de Excel

La auditoria local de la base confidencial se ejecuta mediante `scripts/auditar_base_local.py`.

El script:

- recibe una ruta de entrada y una ruta de salida;
- abre el workbook en modo de lectura;
- no modifica el Excel original;
- detecta hojas, dimensiones y encabezados reales sin renombrarlos;
- estima la hoja principal por volumen de datos y encabezados;
- calcula completitud por columna;
- resume categorias de vigencia/frecuencia como conteos;
- clasifica patrones de numero de poliza sin mostrar valores completos;
- detecta campos separados de dia, mes y ano de vencimiento;
- revisa presencia de columnas candidatas de `detalle` y placa/finca;
- genera reportes locales en `data/output/auditoria/`.

Los reportes de auditoria pueden incluir nombres originales de columnas, conteos y categorias controladas. No deben incluir muestras de filas, nombres reales, identificaciones, polizas completas, placas, fincas ni anotaciones reales.

Las reglas detectadas por esta auditoria siguen siendo preliminares hasta que sean revisadas y aprobadas.

## Reglas conocidas no implementadas

Las siguientes reglas se documentan para analisis futuro, pero no deben implementarse todavia como validaciones rigidas:

- Las vigencias `D.M.` significan deduccion mensual.
- Las polizas con vigencia `D.M.` no generan avisos, pero si deben almacenarse.
- Ademas de `D.M.` o deduccion mensual, pueden observarse frecuencias mensuales, trimestrales, semestrales y anuales.
- Las frecuencias observadas deben contarse y documentarse antes de convertirse en reglas funcionales.
- Las polizas que inician en `01` corresponden preliminarmente a colones.
- Las polizas que inician en `02` corresponden preliminarmente a dolares.
- La regla de prefijo `01`/`02` no aplica a riesgos del trabajo, identificados preliminarmente como polizas cuyo numero es completamente numerico.
- Los formatos de identificacion pueden incluir cedula fisica, cedula juridica, pasaporte o identificacion de extranjero.
- `Nº Placa / Finca` usualmente contiene numeros de placa de vehiculos.
- La fecha de vencimiento puede venir separada en dia, mes y ano.
- La columna `detalle` se usa para anotaciones o para relacionar polizas de un mismo dueno.

## Decisiones tecnicas iniciales

- Lenguaje base: Python.
- GUI probable: PySide6.
- Persistencia local probable: SQLite.
- Excel probable: openpyxl y/o pandas.
- DOCX probable: python-docx.
- Pruebas probables: pytest.
- Empaquetado probable: PyInstaller.

Estas decisiones son preliminares y podran ajustarse con evidencia tecnica.

## Riesgos iniciales

- La base real en Excel todavia no esta disponible.
- Las reglas de negocio no estan completamente definidas.
- La estructura final de datos podria cambiar al revisar datos reales.
- La generacion documental dependera de plantillas y criterios aun pendientes.
