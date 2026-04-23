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
