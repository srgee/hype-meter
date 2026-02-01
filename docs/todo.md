@ 🚀 Plan de Implementación: Hypemeter

Este plan divide el desarrollo en pasos atómicos. Cada tarea debe completarse y verificarse antes de pasar a la siguiente para garantizar la integridad del sistema.

## Fase 1: Cimientos y Configuración (Foundations)

    [x] Inicialización del entorno: Configurar el proyecto con uv, crear pyproject.toml y establecer la estructura de directorios (apps/, config/).

    [x] Base de Datos y Core: Crear apps.core.models.TimestampedModel como clase base abstracta.

    [x] App de Tópicos: Crear la aplicación apps.topics y definir el modelo Topic con campos para el score, nombre e historial (JSON).

    [x] 1.5 Verificación de Persistencia: Realizar migraciones y registrar el modelo en el Admin de Django para pruebas manuales.

## Fase 2: El Motor de Hype (Logic & Service Layer)

    [ ] 2.1 Definición de Interfaces: Crear la estructura en apps.ingestion para los proveedores de datos (Google, News, Social).

    [ ] 2.2 Motor de Hype (Mock): Crear el servicio HypeEngine en apps.topics.services que devuelva datos simulados para validar el flujo sin depender de APIs externas.

    [ ] 2.3 Lógica de Caché (TTL): Implementar la regla de negocio: "Si el dato existe y tiene < 24 horas, no volver a consultar APIs".

    [ ] 2.4 Tests Unitarios de Lógica: Verificar que el motor respeta la caché y calcula correctamente los umbrales de estado (Viral/Neutral/Dead).

## Fase 3: Ingestión de Datos Reales (Data Providers)

    [ ] 3.1 Integración Google Trends: Implementar el proveedor para medir el interés de búsqueda (50% del peso).

    [ ] 3.2 Integración NewsAPI: Implementar el proveedor de volumen de noticias (20% del peso).

    [ ] 3.3 Integración Bluesky: Implementar el proveedor de conversación social (30% del peso).

    [ ] 3.4 Algoritmo de Normalización: Desarrollar la función que unifica las tres fuentes en una escala de 0 a 100.

    [ ] 3.5 Conexión de Capas: Sustituir los datos "mock" del HypeEngine por las llamadas reales a los proveedores de ingestión.

## Fase 4: Interfaz de Usuario e Interactividad (Frontend & HTMX)

    [ ] 4.1 Layout y Estilos: Configurar base.html con Tailwind CSS y HTMX.

    [ ] 4.2 Vista de Búsqueda: Crear la Home con una barra de búsqueda centrada y limpia.

    [ ] 4.3 Estados de Carga: Implementar hx-indicator para mostrar una animación de "Analizando..." mientras el servidor procesa las APIs.

    [ ] 4.4 Partial de Resultados: Diseñar el fragmento HTML que devuelve el servidor con el score y el label dinámico de estado.

## Fase 5: Análisis Visual y Comparativas (Data Visualization)

    [ ] 5.1 Integración de Gráficos: Configurar Chart.js para renderizar el historial de 7 días almacenado en el JSON del modelo.

    [ ] 5.2 Lógica de Peer-Comparison: Desarrollar la función que busque tópicos relacionados o de referencia para dar contexto al score.

    [ ] 5.3 UI de Comparativa: Mostrar los tópicos relacionados como elementos interactivos bajo el score principal.

    [ ] 5.4 Optimización Móvil: Asegurar que el gráfico y la interfaz sean 100% responsivos.

## Fase 6: Resiliencia y Despliegue (Robustness)

    [ ] 6.1 Gestión de Fallos de API: Implementar un sistema de degradación graciosa (si una API falla, calcular con las restantes o usar caché antigua).

    [ ] 6.2 Rate Limiting: Añadir protección contra abusos en el buscador (limitar peticiones por IP).

    [ ] 6.3 Sanitización: Reforzar la limpieza de entradas para evitar inyecciones o términos malformados en las APIs.

    [ ] 6.4 Configuración de Producción: Configurar WhiteNoise para estáticos y preparar el entorno para Gunicorn/Uvicorn.