export function Alert({ message, type }: { message: string; type: 'error' | 'ok' }) {
  return <p className={`alert ${type === 'error' ? 'error' : 'ok'}`}>{message}</p>
}
