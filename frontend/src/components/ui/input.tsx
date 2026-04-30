import type { InputHTMLAttributes } from 'react'

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className="w-full rounded-xl border-2 border-gray-200 bg-white px-4 py-2.5 text-sm text-neutral-900 outline-none transition placeholder:text-gray-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 hover:border-gray-300"
      {...props}
    />
  )
}
