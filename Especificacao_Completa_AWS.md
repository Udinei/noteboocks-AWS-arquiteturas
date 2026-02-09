# Especificação Completa: Sistema de E-mails Personalizados com LLM - AWS

## Cenário
**Ator**: Bob, gerente de atendimento ao cliente na UmaEmpresa  
**Objetivo**: Gerar e-mails de desculpas personalizados para clientes insatisfeitos usando análise de sentimento e LLM, com foco em testes mínimos e ambiente pago AWS.

---

## Arquitetura AWS

### Serviços Principais
- **Amazon Bedrock**: Modelos Claude 3 Haiku para geração de texto
- **Amazon Comprehend**: Análise de sentimento automática
- **AWS Lambda**: Processamento serverless e orquestração
- **Amazon S3**: Armazenamento de e-mails e dados
- **Amazon SES**: Envio de e-mails personalizados
- **Amazon DynamoDB**: Perfis de clientes e histórico
- **Amazon CloudWatch**: Monitoramento e alertas

### Fluxo de Dados
```
E-mail Cliente → Comprehend (Sentimento) → Lambda (Processamento) → 
Bedrock (Geração) → SES (Envio) → DynamoDB (Log)
```

---

## Especificações Técnicas

### Entrada (Input)
| Campo | Tipo | Exemplo |
|-------|------|---------|
| email_cliente | String | cliente@example.com |
| texto_reclamacao | Text | Conteúdo da reclamação |
| nivel_sentimento | Float (0-1) | 0.15 (muito negativo) |
| categoria_problema | String | "Entrega", "Qualidade", "Suporte" |
| cliente_id | String | CLI-00123456 |

### Saída (Output)
| Campo | Tipo | Exemplo |
|-------|------|---------|
| email_gerado | Text | Resposta personalizada |
| tom | String | "Empático", "Formal" |
| ofertas_compensacao | JSON | {"cupom": "15%"} |
| confianca_modelo | Float (0-1) | 0.92 |
| status | String | "pronto_envio" |

---

## Configuração para Testes Mínimos

### Instâncias e Recursos
- **Lambda**: 512MB RAM, timeout 30s
- **DynamoDB**: On-demand, capacidade mínima
- **S3**: Bucket único, classe Standard
- **Bedrock**: Claude 3 Haiku (mais econômico)
- **Região**: us-east-1 (menor custo)

### Volume de Teste
- **Máximo**: 100 e-mails/mês
- **Latência**: < 5 segundos por e-mail
- **Taxa de sucesso**: > 95%

---

## Custos Estimados (Ambiente de Teste)

| Serviço | Custo Mensal |
|---------|--------------|
| Bedrock (Claude 3 Haiku) | $20-30 |
| Lambda (processamento) | $5-10 |
| Comprehend (análise) | $10-15 |
| SES (envio) | $1-5 |
| DynamoDB | $2-5 |
| S3 + CloudWatch | $1-3 |
| **Total** | **$39-68/mês** |

---

## Prompt Template para LLM

```
Você é Bob, gerente de atendimento da UmaEmpresa.

CLIENTE: [NOME_CLIENTE]
RECLAMAÇÃO: "[TEXTO_RECLAMACAO]"
SENTIMENTO: [NIVEL_SENTIMENTO] (0-1)
CATEGORIA: [CATEGORIA]

Gere e-mail de desculpas que:
1. Reconheça o problema específico
2. Peça desculpas sinceras
3. Ofereça solução: [OFERTAS]
4. Tom [TOM] e otimista
5. Máximo 200 palavras
6. Assinado: "Bob, Gerente de Atendimento"
```

---

## Implementação Mínima

### Fase 1: Setup Básico (1 semana)
- Criar funções Lambda
- Configurar Bedrock e Comprehend
- Integração básica S3 + DynamoDB

### Fase 2: Testes (1 semana)
- Processar 50 e-mails de teste
- Ajustar prompts baseado em resultados
- Configurar monitoramento CloudWatch

### Fase 3: Produção Limitada (1 semana)
- Integração SES para envio automático
- Dashboard de métricas
- Alertas para falhas

---

## Segurança e Conformidade

### Criptografia
- **Em trânsito**: TLS 1.2+
- **Em repouso**: AWS KMS

### Controle de Acesso
- **IAM**: Princípio de mínimo privilégio
- **VPC**: Opcional para testes

### Retenção de Dados
- **E-mails**: 12 meses (LGPD)
- **Logs**: 90 dias
- **Métricas**: 1 ano

---

## Métricas de Sucesso

| Métrica | Meta |
|---------|------|
| Taxa de geração | > 95% |
| Latência média | < 5s |
| Custo por e-mail | < $0.50 |
| Satisfação cliente | > 80% |

---

## Próximos Passos

1. [ ] Setup conta AWS e IAM roles
2. [ ] Implementar Lambda de processamento
3. [ ] Configurar Bedrock com Claude 3 Haiku
4. [ ] Testar com 10 e-mails piloto
5. [ ] Ajustar prompts e parâmetros
6. [ ] Deploy produção com 100 e-mails/mês
7. [ ] Monitorar custos e performance

---

**Versão**: 1.0 - Especificação Unificada  
**Data**: Janeiro 2026