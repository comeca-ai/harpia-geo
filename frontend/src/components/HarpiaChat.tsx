import { useEffect, useState, useCallback } from 'react'
import { ChatKit, useChatKit } from '@openai/chatkit-react'

export function HarpiaChat() {
  const [error, setError] = useState<string | null>(null)

  // Hook do ChatKit para gerenciar sessão
  const {
    clientSecret,
    isLoading,
    error: sessionError,
    refresh
  } = useChatKit({
    fetchClientSecret: async () => {
      try {
        const response = await fetch('/api/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })

        if (!response.ok) {
          throw new Error('Falha ao criar sessão')
        }

        const data = await response.json()
        return data.client_secret
      } catch (err) {
        console.error('Erro ao buscar client secret:', err)
        throw err
      }
    }
  })

  useEffect(() => {
    if (sessionError) {
      setError('Erro ao conectar. Tente novamente.')
    }
  }, [sessionError])

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full min-h-[500px]">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-harpia-blue border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-harpia-gray">Conectando ao Harpia...</p>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="flex items-center justify-center h-full min-h-[500px]">
        <div className="text-center">
          <div className="text-4xl mb-4">😕</div>
          <p className="text-harpia-red mb-4">{error}</p>
          <button
            onClick={() => {
              setError(null)
              refresh()
            }}
            className="harpia-btn-primary"
          >
            Tentar novamente
          </button>
        </div>
      </div>
    )
  }

  // ChatKit component
  return (
    <div className="h-full min-h-[500px] rounded-xl overflow-hidden border border-harpia-gray/20">
      <ChatKit
        clientSecret={clientSecret!}

        // Endpoint do backend ChatKit
        endpoint="/chatkit"

        // Tema customizado
        theme={{
          // Cores
          primaryColor: '#0066FF',
          backgroundColor: '#0F172A',
          surfaceColor: '#1E293B',
          textColor: '#F8FAFC',
          textSecondaryColor: '#94A3B8',
          borderColor: '#334155',

          // Bordas
          borderRadius: '12px',

          // Fontes
          fontFamily: 'Inter, system-ui, sans-serif',
        }}

        // Configurações
        options={{
          // Mostra indicador de typing
          showTypingIndicator: true,

          // Placeholder do input
          inputPlaceholder: 'Digite sua mensagem...',

          // Mensagem inicial (opcional - o agent envia a própria)
          // initialMessage: 'Olá! Sou o Harpia 🦅',

          // Habilita widgets
          enableWidgets: true,

          // Habilita anexos
          enableAttachments: false,

          // Habilita markdown
          enableMarkdown: true,
        }}

        // Callbacks
        onMessage={(message) => {
          console.log('Nova mensagem:', message)
        }}

        onError={(err) => {
          console.error('Erro no ChatKit:', err)
          setError('Erro na conversa. Tente novamente.')
        }}

        onWidgetAction={(action) => {
          console.log('Widget action:', action)
          // Aqui você pode tratar ações específicas dos widgets
          // Ex: action.type === 'download_pdf'
        }}
      />
    </div>
  )
}
