import { Search } from "lucide-react"; // O cualquier librería de iconos

const SearchBar = () => {
  return (
    <div className="flex items-center bg-white border border-gray-300 rounded-full shadow-md hover:shadow-lg transition-shadow cursor-pointer p-2 max-w-3xl mx-auto">
      
      {/* Sección: Dónde */}
      <div className="flex flex-col px-6 py-2 hover:bg-gray-100 rounded-full flex-grow transition-colors">
        <span className="text-xs font-bold text-black">Dónde</span>
        <input 
          type="text" 
          placeholder="Explora destinos" 
          className="text-sm text-gray-500 bg-transparent outline-none placeholder-gray-500"
        />
      </div>

      {/* Divisor */}
      <div className="h-8 border-l border-gray-300"></div>

      {/* Sección: Fechas */}
      <div className="flex flex-col px-6 py-2 hover:bg-gray-100 rounded-full flex-grow transition-colors">
        <span className="text-xs font-bold text-black">Fechas</span>
        <span className="text-sm text-gray-500">Agrega fechas</span>
      </div>

      {/* Divisor */}
      <div className="h-8 border-l border-gray-300"></div>

      {/* Sección: Quién */}
      <div className="flex flex-row items-center justify-between pl-6 pr-2 py-1 hover:bg-gray-100 rounded-full flex-grow transition-colors">
        <div className="flex flex-col">
          <span className="text-xs font-bold text-black">Quién</span>
          <span className="text-sm text-gray-500">¿Cuántos?</span>
        </div>
        
        {/* Botón de búsqueda */}
        <button className="bg-[#E21C5F] hover:bg-[#D11152] text-white p-3 rounded-full transition-colors ml-4">
          <Search size={18} strokeWidth={3} />
        </button>
      </div>

    </div>
  );
};

export default SearchBar;
