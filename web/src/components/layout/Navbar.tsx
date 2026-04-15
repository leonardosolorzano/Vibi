import logo from "../../assets/main-logo-vibi.png";
import { Menu, UserCircle, Globe } from "lucide-react";

const Navbar = () => {
  return (
    // header con sticky para que se quede anclado arriba al hacer scroll
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200">
      
      {/* Contenedor centralizado para alinear con el resto del contenido */}
      <div className="flex items-center justify-between max-w-7xl mx-auto px-4 sm:px-6 h-20">
        
        {/* Izquierda: Logo */}
        <div className="flex-shrink-0 flex items-center cursor-pointer transition-transform hover:scale-105">
          <img 
            src={logo} 
            alt="Vibi Logo" 
            className="h-10 w-auto" // Ajusta el 'h-10' según qué tan grande quieras el logo
          />
        </div>

        {/* Centro: Enlaces principales (Ocultos en pantallas muy pequeñas) */}
        <nav className="hidden md:flex items-center gap-8">
          <a href="#" className="text-sm text-gray-500 hover:text-black font-semibold transition-colors">
            Explorar
          </a>
          <a href="#" className="text-sm text-gray-500 hover:text-black font-semibold transition-colors">
            Guardados
          </a>
          <a href="#" className="text-sm text-gray-500 hover:text-black font-semibold transition-colors">
            Viajes
          </a>
        </nav>

        {/* Derecha: Acciones y Perfil de Usuario */}
        <div className="flex items-center gap-1 sm:gap-2">
          
          {/* Llamado a la acción (Opcional, estilo Airbnb) */}
          <a href="#" className="hidden lg:block text-sm font-semibold text-gray-700 hover:bg-gray-100 px-4 py-2 rounded-full transition-colors">
            Pon tu espacio en Vibi
          </a>
          
          {/* Icono de idioma/región */}
          <button className="hidden sm:flex items-center justify-center p-2.5 hover:bg-gray-100 rounded-full transition-colors text-gray-700">
            <Globe size={18} strokeWidth={2} />
          </button>

          {/* Menú de Usuario (Cápsula interactiva) */}
          <div className="flex items-center gap-3 border border-gray-300 rounded-full p-1.5 pl-3 ml-2 hover:shadow-md transition-shadow cursor-pointer bg-white">
            <Menu size={18} strokeWidth={2} className="text-gray-600" />
            
            {/* Si el usuario no está logueado, mostramos el icono genérico. 
                Luego podrás reemplazarlo por su foto de perfil. */}
            <UserCircle size={32} strokeWidth={1} className="text-gray-500 fill-gray-100" />
          </div>

        </div>
      </div>
    </header>
  );
};

export default Navbar;
