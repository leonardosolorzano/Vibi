import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'
import { authApi, usersApi } from '../../api/services'
import { sessionService } from '../../services/session'
import type { LoginInput, User, UserCreateInput } from '../../types/api'

interface AuthContextValue {
  user: User | null
  loading: boolean
  login: (payload: LoginInput) => Promise<void>
  register: (payload: UserCreateInput) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => sessionService.getUser())
  const [loading, setLoading] = useState(false)

  const login = async (payload: LoginInput) => {
    setLoading(true)
    try {
      const loggedUser = await authApi.login(payload)
      setUser(loggedUser)
      sessionService.setUser(loggedUser)
    } finally {
      setLoading(false)
    }
  }

  const register = async (payload: UserCreateInput) => {
    setLoading(true)
    try {
      const created = await usersApi.create(payload)
      setUser(created)
      sessionService.setUser(created)
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    sessionService.clear()
  }

  const value = useMemo<AuthContextValue>(
    () => ({ user, loading, login, register, logout }),
    [user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider')
  }
  return context
}
