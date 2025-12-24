import { Link } from 'react-router-dom'

export function HomePage() {
  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-harpia-blue/10 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-harpia-yellow/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-harpia-dark border border-harpia-gray/30 rounded-full mb-8">
            <span className="w-2 h-2 bg-harpia-green rounded-full animate-pulse" />
            <span className="text-sm text-harpia-gray">GEO - A nova fronteira do marketing</span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-7xl font-bold mb-6 leading-tight">
            Você posta. Posta. Posta.
            <br />
            <span className="harpia-gradient-text">E ninguém vê.</span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl text-harpia-gray max-w-3xl mx-auto mb-8">
            Enquanto você luta pelo algoritmo do Instagram, seus clientes estão perguntando
            para o <span className="text-white font-semibold">ChatGPT</span> quem contratar.
            <br />
            <span className="text-harpia-yellow">A pergunta é: a IA está recomendando você?</span>
          </p>

          {/* CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/chat" className="harpia-btn-primary text-lg px-8 py-4 animate-pulse-glow">
              🔍 Descobrir se a IA me conhece
            </Link>
            <a href="#como-funciona" className="harpia-btn-secondary text-lg px-8 py-4">
              Como funciona?
            </a>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-harpia-blue">800%</div>
              <div className="text-sm text-harpia-gray">Crescimento de tráfego LLM</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-harpia-yellow">48%</div>
              <div className="text-sm text-harpia-gray">Executivos preferem IA ao Google</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-harpia-green">2027</div>
              <div className="text-sm text-harpia-gray">LLMs superam o Google</div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20 bg-harpia-dark/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">
            O jogo mudou. <span className="text-harpia-red">Você não percebeu.</span>
          </h2>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* O que você faz */}
            <div className="harpia-card">
              <div className="text-2xl mb-4">❌</div>
              <h3 className="text-xl font-semibold mb-4 text-harpia-red">O que você faz</h3>
              <ul className="space-y-3 text-harpia-gray">
                <li>• Posta todo dia no Instagram</li>
                <li>• Luta por likes e seguidores</li>
                <li>• Gasta horas em legendas</li>
                <li>• Paga por anúncios caros</li>
              </ul>
            </div>

            {/* O que deveria fazer */}
            <div className="harpia-card border-harpia-green/50">
              <div className="text-2xl mb-4">✅</div>
              <h3 className="text-xl font-semibold mb-4 text-harpia-green">O que deveria fazer</h3>
              <ul className="space-y-3 text-harpia-gray">
                <li>• Ser citado quando a IA responde</li>
                <li>• Aparecer em recomendações de ChatGPT</li>
                <li>• Otimizar para ser A RESPOSTA</li>
                <li>• Ter clientes que chegam prontos</li>
              </ul>
            </div>
          </div>

          <p className="text-center text-xl mt-12 text-harpia-gray">
            <span className="text-white font-semibold">Posts viram pó em 24h.</span>
            <br />
            Recomendações de IA geram clientes <span className="text-harpia-green">todo dia</span>.
          </p>
        </div>
      </section>

      {/* How it Works */}
      <section id="como-funciona" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4">
            Como o <span className="harpia-gradient-text">Harpia</span> funciona
          </h2>
          <p className="text-harpia-gray text-center mb-12">
            3 passos. Sem complicação.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="harpia-card text-center">
              <div className="w-16 h-16 bg-harpia-blue/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">🔍</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">1. Diagnóstico</h3>
              <p className="text-harpia-gray">
                Descobrimos se (e como) a IA fala de você hoje. Analisamos seu site e presença online.
              </p>
            </div>

            <div className="harpia-card text-center">
              <div className="w-16 h-16 bg-harpia-yellow/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">⚡</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">2. Otimização</h3>
              <p className="text-harpia-gray">
                Geramos 20 prompts otimizados e dicas de conteúdo para você aparecer nas respostas.
              </p>
            </div>

            <div className="harpia-card text-center">
              <div className="w-16 h-16 bg-harpia-green/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl">📈</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">3. Monitoramento</h3>
              <p className="text-harpia-gray">
                Acompanhamos sua visibilidade em todas as IAs. Você foca no seu negócio.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 bg-gradient-to-b from-harpia-dark to-harpia-darker">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">
            A IA está recomendando você?
          </h2>
          <p className="text-harpia-gray mb-8">
            Descubra agora. Grátis. Sem compromisso.
          </p>
          <Link to="/chat" className="harpia-btn-primary text-lg px-8 py-4">
            🦅 Fazer Diagnóstico Grátis
          </Link>
          <p className="text-harpia-gray text-sm mt-4">
            Sem cartão de crédito • Resultado em 2 minutos
          </p>
        </div>
      </section>
    </div>
  )
}
