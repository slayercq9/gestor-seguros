# AGENTS.md

Reglas para trabajar en este repositorio:

- Mantener cambios pequenos, claros y alineados al alcance de la fase.
- Priorizar una arquitectura modular y escalable.
- No introducir dependencias sin necesidad validada.
- No implementar reglas de negocio definitivas sin datos reales o aprobacion explicita.
- No borrar informacion automaticamente.
- Cualquier futura eliminacion debe requerir confirmacion explicita.
- No exponer datos confidenciales en codigo, documentacion, capturas, commits o ejemplos.
- No subir a GitHub la base real ni archivos sensibles derivados.
- Usar solo datos ficticios o anonimizados para pruebas y ejemplos.
- Respetar los nombres originales de registros para analisis interno, sin exponerlos en reportes si pueden ser datos reales.
- Mantener distincion explicita entre campos originales, canonicos, derivados, operativos y sensibles.
- Usar identificadores seguros de columna cuando un encabezado no sea confiable.
- Preferir artefactos temporales autocontenidos en pruebas antes que salidas persistentes dentro del proyecto.
- Documentar o comentar el codigo principal cuando la intencion no sea evidente.
- Revisar ortografia y consistencia de textos cuando se trabaje en GUI.
- Documentar supuestos de forma conservadora cuando falte informacion.
- Mantener actualizados `README.md`, `CHANGELOG.md` y documentos en `docs/proyecto/`.
- Agregar pruebas cuando exista codigo ejecutable.
- No romper comportamiento existente ni reestructurar archivos sin razon clara.
