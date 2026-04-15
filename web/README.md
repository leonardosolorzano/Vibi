src/
├── assets/          # Archivos estáticos (tu logo de Vibi, imágenes por defecto, íconos)
├── components/      # Componentes pequeños y reutilizables (botones, inputs, tarjetas)
│   ├── common/      # (Ej: Button.jsx, Modal.jsx)
│   └── layout/      # (Ej: Navbar.jsx, Footer.jsx, SearchBar.jsx)
├── layouts/         # Estructuras de página o "plantillas"
│   └── MainLayout.jsx 
├── pages/           # Vistas completas de tu aplicación (cada una es una ruta)
│   ├── Home.jsx
│   ├── PropertyDetails.jsx
│   ├── SearchResults.jsx
│   └── Profile.jsx
├── services/        # Toda la comunicación con tu API de FastAPI
│   ├── api.js       # Configuración base de Axios
│   └── properties.js# Funciones para pedir alojamientos (getProperties, getPropertyById)
├── hooks/           # Custom hooks (Ej: useAuth.js, useFetch.js)
├── utils/           # Funciones de ayuda (Ej: formatCurrency.js, formatDate.js)
├── App.jsx          # Configuración de tus rutas (React Router)
└── main.jsx         # Punto de entrada de la aplicación