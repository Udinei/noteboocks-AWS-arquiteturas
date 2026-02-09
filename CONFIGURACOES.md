# Configurações - AWS Bedrock + Jupyter Local

Guia completo para configurar Jupyter localmente com acesso à sua conta AWS para trabalhar com Amazon Bedrock.

---

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do AWS CLI](#instalação-do-aws-cli)
3. [Configuração de Credenciais AWS](#configuração-de-credenciais-aws)
4. [Instalação de Dependências Python](#instalação-de-dependências-python)
5. [Configuração do Jupyter](#configuração-do-jupyter)
6. [Testando a Conexão](#testando-a-conexão)
7. [Executar os Notebooks](#executar-os-notebooks)
8. [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

- **Windows 10+, macOS ou Linux**
- **Python 3.8+** instalado ([Download](https://www.python.org/))
- **Conta AWS ativa** com acesso ao Amazon Bedrock
- **AWS Access Key ID e Secret Access Key** (obter no console AWS)

### Verificar versão Python

```powershell
python --version
pip --version
```

---

## Instalação do AWS CLI

### Windows (PowerShell)

```powershell
# Opção 1: pip
pip install awscli

# Opção 2: Instalador direto
# Baixar de: https://awscli.amazonaws.com/AWSCLIV2.msi
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

### macOS/Linux

```bash
pip install awscli
# ou
brew install awscli
```

### Verificar instalação

```powershell
aws --version
```

Esperado: `aws-cli/2.x.x ...`

---

## Configuração de Credenciais AWS

### Passo 1: Obter Access Key ID e Secret Access Key

1. Acesse [AWS Management Console](https://console.aws.amazon.com)
2. Vá em **IAM → Users → Seu usuário**
3. Clique na aba **Security credentials**
4. Clique **Create access key**
5. Escolha **Command Line Interface (CLI)**
6. Copie e salve com segurança:
   - **Access Key ID**
   - **Secret Access Key**

### Passo 2: Configurar com AWS CLI

```powershell
aws configure
```

Será solicitado:

```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
```

**Regiões suportadas por Bedrock (escolha uma):**
- `us-east-1` (N. Virgínia) - Recomendado
- `us-west-2` (Oregon)
- `eu-west-1` (Irlanda)
- `ap-southeast-1` (Singapura)

### Arquivo gerado

Credenciais salvas em:
- **Windows**: `C:\Users\<seu-usuario>\.aws\credentials`
- **macOS/Linux**: `~/.aws/credentials`

---

## Instalação de Dependências Python

### Criar ambiente virtual (opcional mas recomendado)

```powershell
# Criar venv
python -m venv venv

# Ativar venv
.\venv\Scripts\Activate.ps1
```

### Instalar pacotes

```powershell
pip install --upgrade pip

# Básico (Bedrock + Jupyter)
pip install boto3>=1.28.57
pip install botocore>=1.31.5
pip install jupyter

# LangChain (para Task1b)
pip install langchain
pip install langchain-aws
pip install langchain-core

# Análise de sentimento (opcional)
pip install boto3
```

### Instalar a partir de requirements.txt

Se tiver arquivo `requirements.txt` no projeto:

```powershell
pip install -r requirements.txt
```

**Exemplo de `requirements.txt`:**

```
boto3>=1.28.57
botocore>=1.31.5
jupyter>=1.0.0
langchain>=0.1.0
langchain-aws>=0.1.0
langchain-core>=0.1.0
awscli>=1.29.57
tiktoken>=0.5.0
pandas>=1.5.0
```

### Verificar instalações

```powershell
pip list | findstr "boto3|jupyter|langchain"
```

---

## Configuração do Jupyter

### 1. Gerar arquivo de configuração (opcional)

```powershell
jupyter notebook --generate-config
```

Arquivo gerado: `C:\Users\<seu-usuario>\.jupyter\jupyter_notebook_config.py`

### 2. Iniciar Jupyter

```powershell
# Da pasta do projeto
cd e:\workspace-dev-ia\noteboocks-AWS-arquiteturas

# Iniciar servidor
jupyter notebook
```

Esperado: Browser abrirá em `http://localhost:8888`

### 3. Acessar os notebooks

- `Task1a.ipynb` - Geração de texto zero-shot
- `Task1b.ipynb` - Geração com PromptTemplate (LangChain)
- Outros notebooks conforme projeto

---

## Testando a Conexão

### Verificar credenciais AWS

```powershell
aws sts get-caller-identity
```

**Retorno esperado:**

```json
{
    "UserId": "AIDAI1234567890ABCDE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/seu-usuario"
}
```

### Testar acesso ao Bedrock

No Jupyter, execute em uma célula Python:

```python
import boto3
import json

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Listar modelos disponíveis
bedrock_models = boto3.client('bedrock', region_name='us-east-1')
response = bedrock_models.list_foundation_models()

print("Modelos Bedrock disponíveis:")
for model in response['modelSummaries']:
    print(f"  - {model['modelId']}")
```

---

## Executar os Notebooks

### Task1a: Geração de Texto Zero-Shot

1. Abra `Task1a.ipynb`
2. Execute célula por célula (Shift + Enter)
3. Primeira célula: setup do boto3
4. Segundas células: definir prompt e body JSON
5. Terceira: invocar modelo Titan
6. Quarta: imprimir resposta

**Modelos suportados:**
- `amazon.titan-text-express-v1` (padrão)
- `amazon.titan-text-premier-v1:0`
- `meta.llama3-8b-instruct-v1:0`
- `anthropic.claude-3-sonnet-20240229-v1:0`

### Task1b: Geração com LangChain PromptTemplate

1. Abra `Task1b.ipynb`
2. Setup do ambiente (célula 4)
3. Importar LangChain ChatBedrock (célula 5)
4. Criar PromptTemplate (célula 7)
5. Invocar modelo com contexto (célula 9)
6. Parse e imprimir resposta (célula 10)

**Modelos recomendados para Task1b:**
- `meta.llama3-8b-instruct-v1:0` (padrão)
- `anthropic.claude-3-sonnet-20240229-v1:0`
- `amazon.titan-text-express-v1`

---

## Troubleshooting

### Erro: "AccessDeniedException"

```
AccessDeniedException: An error occurred (AccessDeniedException) when calling the InvokeModel operation
```

**Causas:**
- Usuário IAM não tem permissão em Bedrock
- Modelo não está ativado na região

**Solução:**

1. Ativar modelo no console:
   - Bedrock → Model access
   - Clicar "Manage model access"
   - Selecionar modelos desejados
   - Clique "Save changes"

2. Adicionar permissão IAM (Policy):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:GetFoundationModelAvailability",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### Erro: "ValidationException: Malformed input request"

```
ValidationException: extraneous key [textGenerationConfig] is not permitted
```

**Solução:** Use apenas `inputText` no body JSON:

```python
body = json.dumps({
    "inputText": prompt_data
})
```

Não use:
```python
body = json.dumps({
    "inputText": prompt_data,
    "textGenerationConfig": {...}  # ❌ Remove isso
})
```

### Erro: "ModuleNotFoundError: No module named 'langchain'"

```powershell
pip install langchain langchain-aws langchain-core
```

### Erro: "Unable to locate credentials"

```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solução:**

1. Verificar se `aws configure` foi executado
2. Verificar arquivo `~/.aws/credentials`:

```
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = ...
```

3. Alternativa: Use variáveis de ambiente

```powershell
$env:AWS_ACCESS_KEY_ID="AKIA..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_DEFAULT_REGION="us-east-1"
```

### Erro: "Port 8888 already in use"

```powershell
# Usar porta diferente
jupyter notebook --port 8889
```

Ou matar o processo anterior:

```powershell
# Windows
Get-Process jupyter | Stop-Process -Force

# macOS/Linux
pkill -f jupyter
```

---

## Variáveis de Ambiente Úteis

```powershell
# Windows PowerShell
$env:AWS_DEFAULT_REGION = "us-east-1"
$env:AWS_PROFILE = "default"
$env:PYTHONPATH = "e:\workspace-dev-ia"

# macOS/Linux (bash)
export AWS_DEFAULT_REGION=us-east-1
export AWS_PROFILE=default
export PYTHONPATH=/path/to/workspace
```

---

## Checklist Final

- [ ] Python 3.8+ instalado
- [ ] AWS CLI instalado e configurado (`aws configure`)
- [ ] Credenciais testadas (`aws sts get-caller-identity`)
- [ ] Modelos Bedrock ativados no console AWS
- [ ] Dependências Python instaladas (`pip install -r requirements.txt`)
- [ ] Jupyter iniciado (`jupyter notebook`)
- [ ] Notebooks Task1a e Task1b executados com sucesso
- [ ] E-mails gerados aparecem no output das células

---

## Recursos Úteis

| Recurso | URL |
|---------|-----|
| AWS Bedrock Docs | https://docs.aws.amazon.com/bedrock/ |
| Available Models | https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html |
| LangChain Docs | https://python.langchain.com/docs/ |
| boto3 Docs | https://boto3.amazonaws.com/v1/documentation/api/latest/index.html |
| AWS IAM Console | https://console.aws.amazon.com/iam/ |

---

**Última atualização:** 6 de Fevereiro de 2026  
**Versão:** 1.0  
**Autor:** Setup AWS Bedrock + Jupyter

