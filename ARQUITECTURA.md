# Arquitectura

## Vision general

La aplicacion se disena como una herramienta de escritorio modular. Cada componente debera tener una responsabilidad clara y comunicarse mediante contratos simples para facilitar mantenimiento, pruebas y empaquetado.

## Modulos preliminares

### Interfaz

Responsable de presentar pantallas, formularios, acciones y mensajes al usuario. En una fase futura podria implementarse con PySide6.

### Datos

Responsable de leer, validar, persistir y recuperar informacion. La persistencia local probable sera SQLite, pero no se define una base operativa en esta fase.

### Logica de aplicacion

Responsable de coordinar casos de uso. No debe mezclarse con detalles de interfaz ni de almacenamiento.

### Reportes

Responsable de consultas, filtros, resumenes y exportaciones futuras.

### Documentos

Responsable de preparar documentos a partir de plantillas. Los documentos de vencimiento deberan generarse por cliente, no por poliza.

### Respaldos

Responsable de crear, verificar y recuperar respaldos. No debera borrar informacion automaticamente.

### Configuracion

Responsable de rutas locales, preferencias y parametros operativos no sensibles.

## Flujo conceptual general

```text
Usuario
  -> Interfaz
  -> Logica de aplicacion
  -> Datos / Reportes / Documentos / Respaldos
  -> Resultado visible, archivo generado o registro operativo
```

## Separacion de responsabilidades

- La interfaz no debe contener reglas de negocio complejas.
- Los modulos de datos no deben depender de la interfaz.
- La generacion de documentos no debe modificar datos operativos por si misma.
- Los respaldos deben ser operaciones explicitas y verificables.
- Cualquier eliminacion futura debe exigir confirmacion explicita.

## Estructura preliminar

```text
app/
  ui/             Futuras pantallas y componentes visuales.
  data/           Futuro acceso a datos y persistencia.
  services/       Futuros casos de uso y coordinacion.
  reports/        Futuros reportes.
  documents/      Futura generacion documental.
  backups/        Futuras rutinas de respaldo.
  config/         Futura configuracion.
```

La estructura interna de `app/` se creara solo cuando exista una fase de implementacion tecnica aprobada.
