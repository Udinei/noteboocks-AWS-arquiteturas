# Especificação AWS - Sistema de Resposta Automática para Atendimento ao Cliente

## Cenário
Sistema para gerar e-mails de resposta personalizados para clientes insatisfeitos, utilizando análise de sentimento e geração de texto otimista.

## Arquitetura AWS

### Serviços Principais
- **Amazon SageMaker**: Hospedagem e inferência do modelo LLM
- **Amazon Bedrock**: Modelos de fundação para geração de texto
- **Amazon S3**: Armazenamento de dados e modelos
- **AWS Lambda**: Processamento serverless
- **Amazon SES**: Envio de e-mails

### Especificações Técnicas

#### SageMaker
- **Instância**: ml.t3.medium (para testes mínimos)
- **Endpoint**: Real-time inference
- **Modelo**: Claude 3 Haiku via Bedrock ou modelo fine-tuned

#### Processamento
- **Input**: E-mail do cliente + análise de sentimento
- **Output**: E-mail de resposta personalizado
- **Volume**: Mínimo para testes (< 100 e-mails/mês)

#### Custos Estimados (Teste)
- SageMaker Endpoint: ~$30-50/mês
- Bedrock (Claude): ~$0.25 por 1K tokens
- Lambda: Camada gratuita
- SES: $0.10 por 1K e-mails

### Fluxo de Dados
1. Recebimento do e-mail do cliente
2. Análise de sentimento (negativo/neutro/positivo)
3. Geração de resposta via LLM
4. Personalização baseada no contexto
5. Envio automático via SES

### Requisitos Mínimos
- Região: us-east-1 ou us-west-2
- IAM roles configuradas
- VPC endpoints (opcional para segurança)
- Monitoramento via CloudWatch