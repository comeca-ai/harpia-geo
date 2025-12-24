# 🦅 Harpia - Plataforma GEO

> Fazemos a IA recomendar você.

Harpia é uma plataforma de **Generative Engine Optimization (GEO)** que ajuda empresas brasileiras a serem recomendadas por IAs como ChatGPT, Gemini e Perplexity.

## 📋 Funcionalidades

- **Diagnóstico de Visibilidade**: Analisa se as IAs conhecem sua empresa
- **Geração de Prompts**: Cria 20 prompts otimizados para seu nicho
- **Teste em LLMs**: Verifica se você é mencionado nas respostas
- **Dashboard**: Acompanha sua visibilidade ao longo do tempo

## 🏗️ Arquitetura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│     Backend     │────▶│    Supabase     │
│  React + Vite   │     │ FastAPI+ChatKit │     │  PostgreSQL     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   OpenAI API    │
                        │  Agents + GPT   │
                        └─────────────────┘
```

## 🚀 Quick Start

### 1. Clone e configure

```bash
cd apps/harpia

# Backend
cd backend
cp .env.example .env
# Edite .env com suas API keys
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Configure as variáveis de ambiente

```env
# backend/.env
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
FIRECRAWL_API_KEY=fc-...
SERPER_API_KEY=...
GOOGLE_API_KEY=...
```

### 3. Rode o projeto

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Com Docker

```bash
docker-compose up
```

## 📁 Estrutura

```
harpia/
├── backend/
│   ├── main.py              # FastAPI + ChatKitServer
│   ├── agents/
│   │   └── harpia_agent.py  # Agent principal
│   ├── tools/
│   │   ├── diagnostico.py   # Análise de empresa
│   │   ├── prompts.py       # Geração de prompts
│   │   └── testar_llm.py    # Teste de visibilidade
│   ├── widgets/
│   │   ├── forms.py         # Formulários
│   │   ├── resultado.py     # Cards de resultado
│   │   └── prompts_list.py  # Lista de prompts
│   └── store/
│       └── supabase_store.py # Persistência
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   └── components/
│   │       ├── Layout.tsx
│   │       ├── HomePage.tsx
│   │       ├── ChatPage.tsx
│   │       ├── HarpiaChat.tsx
│   │       └── DashboardPage.tsx
│   └── styles/
│       └── globals.css
│
├── docker-compose.yml
└── README.md
```

## 🎨 Design System

### Cores
- **Azul**: `#0066FF` - Primary
- **Amarelo**: `#FFCC00` - Accent
- **Verde**: `#10B981` - Success
- **Vermelho**: `#EF4444` - Error
- **Dark**: `#0F172A` - Background

### Componentes
- Cards com bordas sutis e hover effects
- Gradientes para textos importantes
- Animações suaves de glow e pulse

## 🔌 APIs Utilizadas

| API | Uso | Custo Estimado |
|-----|-----|----------------|
| OpenAI GPT-4 | Geração de prompts | ~$0.06/análise |
| Firecrawl | Scraping de sites | ~$0.02/análise |
| Serper | Web search | ~$0.01/análise |
| Google Gemini | Teste de visibilidade | ~$0.01/teste |

**Custo total por análise:** ~$0.10

## 📊 Modelo de Dados (Supabase)

```sql
-- Threads de chat
CREATE TABLE threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR,
  user_id UUID REFERENCES users,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Análises de empresas
CREATE TABLE analises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID REFERENCES threads,
  empresa VARCHAR NOT NULL,
  site VARCHAR NOT NULL,
  dados JSONB,
  status VARCHAR DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Prompts gerados
CREATE TABLE prompts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analise_id UUID REFERENCES analises,
  ordem INTEGER,
  texto TEXT NOT NULL,
  categoria VARCHAR,
  intent VARCHAR,
  persona VARCHAR,
  formato_esperado VARCHAR
);

-- Testes de visibilidade
CREATE TABLE testes_visibilidade (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analise_id UUID REFERENCES analises,
  score_geral DECIMAL,
  resultados JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 🛣️ Roadmap

- [x] MVP: Diagnóstico + Geração de Prompts
- [ ] Teste automático em LLMs
- [ ] Dashboard com histórico
- [ ] Planos pagos (Stripe)
- [ ] API pública
- [ ] White-label para agências

## 📝 Licença

Proprietário - Harpia © 2024

---

**🦅 Harpia** - Fazendo a IA recomendar você.
