import type { User } from '../types/api'

const SESSION_KEY = 'vibi_user'

export const sessionService = {
  getUser(): User | null {
    const raw = localStorage.getItem(SESSION_KEY)
    if (!raw) return null
    try {
      return JSON.parse(raw) as User
    } catch {
      localStorage.removeItem(SESSION_KEY)
      return null
    }
  },
  setUser(user: User) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(user))
  },
  clear() {
    localStorage.removeItem(SESSION_KEY)
  },
}
