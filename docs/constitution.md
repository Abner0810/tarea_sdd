# Constitución de habits-cli

1. **Simplicidad del stack**: Únicamente Python con biblioteca estándar. Sin dependencias externas para el MVP.
2. **Relación entre spec y código**: Toda implementación debe trazar a un requisito funcional (RF-x) de la especificación. Si no hay RF, no se implementa.
3. **Separación entre lógica e interfaz**: La lógica de negocio (hábitos y cálculo de rachas) debe estar aislada de la interfaz CLI. La CLI solo debe traducir entradas, salidas y errores.
4. **Política de tests**: Las reglas de negocio deben estar cubiertas por tests verificables. Ningún cambio en lógica sin su correspondiente validación por tests.
5. **Persistencia de datos**: Los datos se guardarán en un único archivo JSON local, legible, predecible y sin necesidad de una base de datos.
6. **Idioma del código y los mensajes**: Código, identificadores, comentarios y mensajes al usuario deben estar en español.
