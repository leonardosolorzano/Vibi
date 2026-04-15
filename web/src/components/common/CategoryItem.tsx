interface CategoryItemProps {
  label: string;
  Icon: React.ComponentType<{ size: number; strokeWidth: number }>;
  isSelected: boolean;
  onClick: () => void;
}

const CategoryItem = ({ label, Icon, isSelected, onClick }: CategoryItemProps) => {
  return (
    <div 
      onClick={onClick}
      className={`flex flex-col items-center justify-center gap-2 min-w-[80px] p-2 cursor-pointer transition-all duration-200 border-b-2 
      ${isSelected 
        ? 'border-[#E21C5F] text-[#E21C5F]' // Color de tu marca Vibi si está seleccionado
        : 'border-transparent text-gray-500 hover:text-black hover:border-gray-300'
      }`}
    >
      <Icon size={24} strokeWidth={2} />
      <span className="text-xs font-semibold whitespace-nowrap">{label}</span>
    </div>
  );
};

export default CategoryItem;