import { useState } from 'react'

// Mock data para demonstração
const mockAnalises = [
  {
    id: '1',
    empresa: 'Datarisk',
    site: 'datarisk.io',
    score: 65,
    totalPrompts: 20,
    createdAt: '2024-12-20',
    status: 'completed'
  },
  {
    id: '2',
    empresa: 'TechSolutions',
    site: 'techsolutions.com.br',
    score: 35,
    totalPrompts: 20,
    createdAt: '2024-12-19',
    status: 'completed'
  },
  {
    id: '3',
    empresa: 'Minha Loja',
    site: 'minhaloja.com',
    score: 10,
    totalPrompts: 20,
    createdAt: '2024-12-18',
    status: 'completed'
  }
]

export function DashboardPage() {
  const [analises] = useState(mockAnalises)

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-harpia-green'
    if (score >= 50) return 'text-harpia-yellow'
    if (score >= 20) return 'text-orange-500'
    return 'text-harpia-red'
  }

  const getScoreEmoji = (score: number) => {
    if (score >= 80) return '🟢'
    if (score >= 50) return '🟡'
    if (score >= 20) return '🟠'
    return '🔴'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excelente'
    if (score >= 50) return 'Bom'
    if (score >= 20) return 'Regular'
    return 'Crítico'
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-harpia-gray">Acompanhe suas análises de visibilidade</p>
        </div>
        <a href="/chat" className="harpia-btn-primary">
          + Nova Análise
        </a>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="harpia-card">
          <div className="text-harpia-gray text-sm mb-1">Total de Análises</div>
          <div className="text-3xl font-bold">{analises.length}</div>
        </div>
        <div className="harpia-card">
          <div className="text-harpia-gray text-sm mb-1">Score Médio</div>
          <div className="text-3xl font-bold text-harpia-yellow">
            {Math.round(analises.reduce((acc, a) => acc + a.score, 0) / analises.length)}%
          </div>
        </div>
        <div className="harpia-card">
          <div className="text-harpia-gray text-sm mb-1">Prompts Gerados</div>
          <div className="text-3xl font-bold text-harpia-blue">
            {analises.reduce((acc, a) => acc + a.totalPrompts, 0)}
          </div>
        </div>
        <div className="harpia-card">
          <div className="text-harpia-gray text-sm mb-1">Plano Atual</div>
          <div className="text-xl font-bold text-harpia-green">Free</div>
          <a href="#upgrade" className="text-harpia-blue text-sm hover:underline">
            Fazer upgrade →
          </a>
        </div>
      </div>

      {/* Tabela de Análises */}
      <div className="harpia-card">
        <h2 className="text-lg font-semibold mb-4">Análises Recentes</h2>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-harpia-gray/20">
                <th className="text-left py-3 px-4 text-harpia-gray font-medium">Empresa</th>
                <th className="text-left py-3 px-4 text-harpia-gray font-medium">Site</th>
                <th className="text-left py-3 px-4 text-harpia-gray font-medium">Score</th>
                <th className="text-left py-3 px-4 text-harpia-gray font-medium">Status</th>
                <th className="text-left py-3 px-4 text-harpia-gray font-medium">Data</th>
                <th className="text-left py-3 px-4 text-harpia-gray font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              {analises.map((analise) => (
                <tr key={analise.id} className="border-b border-harpia-gray/10 hover:bg-harpia-dark/50">
                  <td className="py-4 px-4">
                    <div className="font-medium">{analise.empresa}</div>
                  </td>
                  <td className="py-4 px-4">
                    <a
                      href={`https://${analise.site}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-harpia-blue hover:underline"
                    >
                      {analise.site}
                    </a>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <span>{getScoreEmoji(analise.score)}</span>
                      <span className={`font-bold ${getScoreColor(analise.score)}`}>
                        {analise.score}%
                      </span>
                      <span className="text-harpia-gray text-sm">
                        ({getScoreLabel(analise.score)})
                      </span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className="px-2 py-1 bg-harpia-green/20 text-harpia-green rounded-full text-sm">
                      Concluído
                    </span>
                  </td>
                  <td className="py-4 px-4 text-harpia-gray">
                    {analise.createdAt}
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <button className="text-harpia-blue hover:underline text-sm">
                        Ver Prompts
                      </button>
                      <button className="text-harpia-gray hover:text-white text-sm">
                        Retestar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {analises.length === 0 && (
          <div className="text-center py-12">
            <div className="text-4xl mb-4">🦅</div>
            <p className="text-harpia-gray mb-4">Nenhuma análise ainda</p>
            <a href="/chat" className="harpia-btn-primary">
              Fazer primeira análise
            </a>
          </div>
        )}
      </div>

      {/* Upgrade CTA */}
      <div className="harpia-card mt-8 bg-gradient-to-r from-harpia-blue/10 to-harpia-yellow/10 border-harpia-blue/30">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold mb-2">
              🚀 Quer monitoramento contínuo?
            </h3>
            <p className="text-harpia-gray">
              Upgrade para o plano Pro e acompanhe sua visibilidade em tempo real.
            </p>
          </div>
          <button className="harpia-btn-primary">
            Ver Planos
          </button>
        </div>
      </div>
    </div>
  )
}
