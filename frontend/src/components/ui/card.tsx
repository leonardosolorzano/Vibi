import type { ReactNode } from 'react'

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <article className={`rounded-3xl border border-orange-100 bg-white p-6 shadow-lg hover:shadow-xl transition-shadow duration-300 ${className}`}>
      {children}
    </article>
  )
}
