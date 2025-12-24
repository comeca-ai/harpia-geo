import { useEffect, useState } from 'react'
import { HarpiaChat } from './HarpiaChat'

export function ChatPage() {
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    // Simula carregamento inicial
    const timer = setTimeout(() => setIsReady(true), 500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col">
      {/* Header da página */}
      <div className="bg-harpia-dark border-b border-harpia-gray/20 py-4">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-harpia-blue/20 rounded-full flex items-center justify-center">
              <span className="text-xl">🦅</span>
            </div>
            <div>
              <h1 className="font-semibold">Harpia</h1>
              <p className="text-sm text-harpia-gray">Assistente de GEO</p>
            </div>
            <div className="ml-auto flex items-center gap-2">
              <span className="w-2 h-2 bg-harpia-green rounded-full animate-pulse" />
              <span className="text-sm text-harpia-gray">Online</span>
            </div>
          </div>
        </div>
      </div>

      {/* Área do Chat */}
      <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-6">
        {isReady ? (
          <HarpiaChat />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-16 h-16 border-4 border-harpia-blue border-t-transparent rounded-full animate-spin mx-auto mb-4" />
              <p className="text-harpia-gray">Conectando ao Harpia...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
