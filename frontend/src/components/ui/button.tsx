import type { ButtonHTMLAttributes } from 'react'

type Variant = 'primary' | 'secondary' | 'ghost' | 'danger'

const stylesByVariant: Record<Variant, string> = {
  primary: 'bg-gradient-to-r from-orange-500 to-red-500 text-white hover:from-orange-600 hover:to-red-600 shadow-lg hover:shadow-xl',
  secondary: 'bg-neutral-900 text-white hover:bg-neutral-800 shadow-md',
  ghost: 'border-2 border-orange-400 bg-white text-orange-600 hover:bg-orange-50 hover:border-orange-500',
  danger: 'bg-red-600 text-white hover:bg-red-700 shadow-lg hover:shadow-xl',
}

export function Button({
  variant = 'primary',
  className = '',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={`rounded-xl px-4 py-2.5 text-sm font-semibold transition duration-200 disabled:cursor-not-allowed disabled:opacity-60 ${stylesByVariant[variant]} ${className}`}
      {...props}
    />
  )
}
