# Especificacion: habits-cli (MVP) - Habitos alimentarios


## Contexto y objetivo

CLI para registrar habitos alimentarios y calcular rachas de dias consecutivos. Proyecto educativo para mantener un desarrollador junior. El tema es distinto a rutinas de gimnasio.


## Usuarios

Persona que desea llevar seguimiento de habitos alimentarios (beber agua, comer fruta, cocinar en casa, etc.).


## Historias de usuario

- HU-1: Como usuario, quiero crear un habito alimentario para poder darle seguimiento.
- HU-2: Como usuario, quiero marcar mi habito como hecho hoy para registrar mi progreso.
- HU-3: Como usuario, quiero listar mis habitos con su racha de dias consecutivos para ver mi constancia.


## Requisitos funcionales (RF)

### RF-1: Crear habito
**Descripcion:** El usuario debe poder crear un habito alimentario.
**Criterios de aceptacion en notacion EARS en espanol:**
- CUANDO el usuario cree un habito con un nombre valido, EL sistema DEBERA registrar el habito.
- CUANDO el usuario cree un habito con un nombre vacio o solo espacios, EL sistema DEBERA rechazarlo con un mensaje de error.
- CUANDO el usuario cree un habito con un nombre que ya existe ignorando mayusculas/minusculas, EL sistema DEBERA rechazarlo con un mensaje de error.

### RF-2: Marcar habito como hecho hoy
**Descripcion:** El usuario debe poder marcar un habito como hecho en la fecha actual.
**Criterios de aceptacion en notacion EARS en espanol:**
- CUANDO el usuario marque como hecho un habito existente que no ha sido marcado hoy, EL sistema DEBERA registrar la marca para la fecha actual.
- CUANDO el usuario marque como hecho un habito ya marcado hoy, EL sistema DEBERA rechazarlo con un mensaje de error.
- CUANDO el usuario marque como hecho un habito que no existe, EL sistema DEBERA rechazarlo con un mensaje de error y salir con codigo distinto a 0.

### RF-3: Listar habitos con racha
**Descripcion:** El usuario debe poder listar todos los habitos con su racha de dias consecutivos.
**Criterios de aceptacion en notacion EARS en espanol:**
- CUANDO el usuario liste los habitos, EL sistema DEBERA mostrar cada habito con su racha de dias consecutivos.
- SI un habito no ha sido marcado hoy pero fue marcado ayer y hay dias consecutivos anteriores, EL sistema DEBERA mantener la racha contando hasta el ultimo dia marcado.
- CUANDO se liste un habito que no existe, EL sistema DEBERA rechazarlo con un mensaje de error y salir con codigo distinto a 0.
- PARA calcular la racha, EL sistema DEBERA usar la fecha del sistema (datetime.date.today()).


## Requisitos no funcionales

- RNF-1: Debe seguir los principios de docs/constitution.md.
- RNF-2: Debe usar unica y exclusivamente Python con biblioteca estandar.
- RNF-3: Debe haber separacion entre logica de negocio e interfaz CLI.
- RNF-4: Los mensajes al usuario y el codigo deben estar en espanol.
- RNF-5: Persistencia en un unico archivo JSON local.

## Casos limite

- CL-1: Nombre con solo espacios debe rechazarse.
- CL-2: Nombres duplicados ignorando mayusculas/minusculas deben rechazarse.
- CL-3: Marcar dos veces el mismo habito el mismo dia debe rechazar con error.
- CL-4: Marcar/listar un habito inexistente debe dar error y codigo distinto a 0.
- CL-5: Racha se mantiene hasta ultimo dia marcado si hoy no se marco.

## Fuera de alcance

- FO-1: Interfaz grafica.
- FO-2: Base de datos.
- FO-3: Dependencias externas.
- FO-4: Recordatorios o notificaciones.
- FO-5: Estadisticas avanzadas mas alla de racha.

## Criterios de finalizacion

- CF-1: Los tres comandos (crear, marcar hecho hoy, listar) funcionan segun los RF.
- CF-2: Los criterios de aceptacion se cumplen.
- CF-3: Se respeta la constitucion.

## Dudas abiertas marcadas como [NECESITA ACLARACION]

- DA-1: [NECESITA ACLARACION] ¿Debe permitirse eliminar habitos en este MVP? (Fuera segun FO, pero aclarar)
- DA-2: [NECESITA ACLARACION] ¿Que formato exacto debe tener la salida al listar (solo texto)? (Se deja flexible para el plan)
