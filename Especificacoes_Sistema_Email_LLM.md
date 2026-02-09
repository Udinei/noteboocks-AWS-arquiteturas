# Especificações para o Cenário Real: Sistema de Geração de E-mails Personalizados com LLM

## Contexto do Cenário

**Ator**: Bob, gerente de atendimento ao cliente na UmaEmpresa

**Objetivo**: Gerar e-mails de desculpas personalizados e otimistas para clientes insatisfeitos, recuperando sua confiança através de respostas adaptadas ao sentimento expresso em suas reclamações.

---

## 1. Arquitetura Geral

```
Sistema de Análise de Sentimento + Geração de E-mails Personalizados
├── Coleta de Dados
├── Processamento e Análise
├── Geração com LLM
└── Gerenciamento e Entrega
```

---

## 2. Componentes Técnicos (AWS)

### 2.1 Entrada de Dados

- **Amazon S3**: Armazenar e-mails dos clientes insatisfeitos
- **Amazon DynamoDB**: Banco de dados para perfil de clientes
- **Amazon SES** ou **SNS**: Para gerenciar comunicações

### 2.2 Análise de Sentimento

- **Amazon Comprehend**: Análise automática de sentimento dos e-mails recebidos
  - Classificar: Negativo, Neutro, Positivo
  - Extrair: Entidades (produtos, serviços mencionados)
  - Detectar: Idiomas

### 2.3 Processamento com LLM

- **Amazon Bedrock**: Acesso a modelos como Claude, GPT
- **AWS Lambda**: Funções serverless para orquestração
- **Amazon SageMaker**: Opcional, para fine-tuning de modelos específicos

### 2.4 Armazenamento

- **RDS (PostgreSQL)**: Histórico de interações e templates
- **S3**: Backup de e-mails gerados
- **ElastiCache**: Cache de templates frequentes

---

## 3. Fluxo de Dados

```
E-mail do Cliente
      ↓
[Amazon Comprehend] → Análise de Sentimento
      ↓
[Lambda Function] → Extração de contexto
      ↓
[Amazon Bedrock] → Prompt otimizado + Geração
      ↓
[SES/SNS] → Envio personalizado
      ↓
[DynamoDB] → Log e confirmação
```

---

## 4. Especificações de Entrada (Input)

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **email_cliente** | String | `cliente@example.com` |
| **texto_reclamacao** | Text | Conteúdo da reclamação |
| **nivel_sentimento** | Float (0-1) | 0.15 (muito negativo) |
| **categoria_problema** | String | "Entrega", "Qualidade", "Suporte" |
| **cliente_id** | String | "CLI-00123456" |
| **historico_interacoes** | JSON | Compras, retornos anteriores |
| **data_reclamacao** | DateTime | 2026-01-30T08:00:00Z |

---

## 5. Especificações de Saída (Output)

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **email_gerado** | Text | Resposta personalizada completa |
| **tom** | String | "Empático", "Formal", "Amigável" |
| **ofertas_compensacao** | JSON | `{"cupom": "15%", "frete_gratis": true}` |
| **confianca_modelo** | Float (0-1) | 0.92 |
| **timestamp_geracao** | DateTime | 2026-01-30T10:30:00Z |
| **status** | String | "pronto_envio", "requer_revisao" |

---

## 6. Prompts de Exemplo para o LLM

### Prompt Base

```
Você é Bob, gerente de atendimento ao cliente na UmaEmpresa.

INFORMAÇÕES DO CLIENTE:
- Nome: [NOME_CLIENTE]
- ID: [CLIENTE_ID]
- Histórico: [HISTÓRICO]

RECLAMAÇÃO RECEBIDA:
"[TEXTO_RECLAMACAO]"

ANÁLISE DE SENTIMENTO: [NIVEL_SENTIMENTO] (0-1)
CATEGORIA DO PROBLEMA: [CATEGORIA]

TAREFA:
Gere um e-mail de desculpas personalizado que:
1. Reconheça o problema específico mencionado
2. Peça desculpas sinceras e genuínas
3. Explique o que será feito para resolver
4. Ofereça compensação apropriada: [OFERTAS]
5. Mantenha tom [TOM] e otimista
6. Máximo 250 palavras
7. Assinado por "Bob, Gerente de Atendimento ao Cliente"

Gere somente o corpo do e-mail.
```

### Exemplos de Tons por Sentimento

- **Muito Negativo (0-0.3)**: Mais empático, reconhecer frustração
- **Negativo (0.3-0.5)**: Equilibrado entre empatia e ação
- **Neutro (0.5-0.7)**: Profissional e informativo
- **Positivo (0.7-1.0)**: Agradecimento e reforço

---

## 7. Requisitos de Segurança

### Criptografia
- **Em trânsito**: TLS 1.2+
- **Em repouso**: AWS KMS com chaves gerenciadas

### Controle de Acesso
- **IAM Roles**: Princípio de mínimo privilégio
- **VPC**: Isolamento de rede para dados sensíveis

### Auditoria e Conformidade
- **CloudTrail**: Rastrear todas as mudanças
- **CloudWatch Logs**: Monitoramento de eventos
- **LGPD/GDPR**: Conformidade com proteção de dados
  - Direito ao esquecimento: Política de retenção de 12 meses
  - Consentimento: Registro de consentimento antes do envio

---

## 8. Métricas e Monitoramento

| Métrica | Alvo | Descrição |
|---------|------|-----------|
| **Taxa de Sucesso** | > 95% | E-mails gerados sem erro |
| **Latência Média** | < 5s | Tempo de geração completa |
| **Taxa de Entrega** | > 98% | E-mails entregues com sucesso |
| **Satisfação Pós-Resposta** | > 80% | Feedback positivo do cliente |
| **Taxa de Retenção** | Crescimento | % de clientes que permanecem |
| **Custo por E-mail** | < $0.05 | Otimização de recursos |

### Dashboard CloudWatch
- Gráficos em tempo real de throughput
- Alertas para erros ou latência alta
- Análise de sentimento dos e-mails gerados

---

## 9. Escalabilidade

### Volume Esperado
- **Ambiente de Teste**: 10 e-mails/dia (~300/mês)
- **Produção Inicial**: 250 e-mails/dia
- **Produção Pico**: 500 e-mails/dia
- **Crescimento**: 20-30% ao trimestre

### Configuração de Infraestrutura
**Ambiente de Teste (10 e-mails/dia):**
- **Lambda**: Concorrência reservada de 1-2 (suficiente para testes)
- **RDS**: Instância t3.micro (camada gratuita/baixo custo)
- **DynamoDB**: On-demand com limites mínimos
- **S3**: Bucket único sem particionamento

**Produção (250-500 e-mails/dia):**
- **Lambda**: Concorrência reservada de 10-50
- **RDS**: Single-AZ (escalável para Multi-AZ)
- **DynamoDB**: Auto-scaling com limites conservadores
- **S3**: Particionamento por data/cliente

### Custo Estimado (Mensal)
**Ambiente de Teste (10 e-mails/dia):**
- **Bedrock (LLM)**: $20-40
- **Lambda + Compute**: $5-10
- **Armazenamento**: $1-5
- **Outras APIs (Comprehend, SES)**: $5-15
- **Total Testes**: $31-70/mês

**Produção (250-500 e-mails/dia):**
- **Bedrock (LLM)**: $400-800
- **Lambda + Compute**: $100-200
- **Armazenamento**: $50-100
- **Outras APIs**: $100-200
- **Total Produção**: $650-1.300/mês

---

## 10. Fluxo de Implementação

### Fase 1: MVP (2 semanas)
- Setup básico de Lambda + Comprehend
- Integração com um modelo LLM
- E-mails gerados manualmente revisados

### Fase 2: Automação (3 semanas)
- Integração SES para envio automático
- Dashboard de monitoramento
- Templates parametrizados

### Fase 3: Otimização (2 semanas)
- Fine-tuning de prompts
- Análise de feedback de clientes
- Escalabilidade e performance

### Fase 4: Produção (Ongoing)
- Monitoramento 24/7
- Melhorias contínuas
- A/B testing de respostas

---

## 11. Casos de Uso Específicos

### Caso 1: Atraso na Entrega
```
Sentimento: Muito Negativo (0.1)
Compensação: Frete grátis na próxima compra + 10% desconto
Tom: Empático e solucionador
```

### Caso 2: Qualidade do Produto Inferior
```
Sentimento: Negativo (0.35)
Compensação: Reembolso + 15% desconto
Tom: Reconhecedor e comprometido
```

### Caso 3: Demora no Suporte
```
Sentimento: Negativo (0.4)
Compensação: Atendimento prioritário + 5% desconto
Tom: Profissional e atencioso
```

---

## 12. Próximos Passos

1. [ ] Criar infraestrutura AWS base
2. [ ] Configurar políticas de IAM
3. [ ] Implementar Lambda function prototipo
4. [ ] Testar com 100 e-mails piloto
5. [ ] Ajustar prompts baseado em feedback
6. [ ] Deploy em produção com alertas
7. [ ] Monitorar métricas e iterar

---

**Documento criado em**: 30 de Janeiro de 2026  
**Versão**: 1.0
