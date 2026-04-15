import { useState } from 'react';
import { Umbrella, Mountain, Trees, Palmtree, Tent, Waves } from 'lucide-react';
import CategoryItem from '../common/CategoryItem';

const CATEGORIES_DATA = [
  { id: 'beach', label: 'Playa', icon: Umbrella },
  { id: 'mountain', label: 'Montañas', icon: Mountain },
  { id: 'amazon', label: 'Amazonía', icon: Trees },
  { id: 'tropical', label: 'Trópico', icon: Palmtree },
  { id: 'camping', label: 'Camping', icon: Tent },
  { id: 'lake', label: 'Lagos', icon: Waves },
];

const CategoriesBar = () => {
  // Estado para saber cuál está seleccionada (por defecto la primera)
  const [selectedCategory, setSelectedCategory] = useState(CATEGORIES_DATA[0].id);

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-4 mt-6">
      {/* Contenedor con scroll horizontal para pantallas pequeñas */}
      <div className="flex flex-row items-center justify-start md:justify-center gap-6 overflow-x-auto no-scrollbar pb-2">

        {/* 2. El "reciclaje": Mapeamos el array para crear los componentes */}
        {CATEGORIES_DATA.map((category) => {
          const IconComponent = category.icon; // Extraemos el icono
          return (
            <CategoryItem
              key={category.id}
              label={category.label}
              Icon={IconComponent}
              isSelected={selectedCategory === category.id}
              onClick={() => setSelectedCategory(category.id)}
            />
          );
        })}
      </div>
    </div>
  );
};

export default CategoriesBar;
