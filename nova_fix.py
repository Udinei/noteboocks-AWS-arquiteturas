# Correção para Amazon Nova
import json
import boto3

# Configuração
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

prompt_data = """
Command: Write an email from Bob, Customer Service Manager, AnyCompany to the customer "John Doe" 
who provided negative feedback on the service provided by our customer support 
engineer"""

# Formato correto para Amazon Nova
body = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": [{"text": prompt_data}]
        }
    ],
    "inferenceConfig": {
        "maxTokens": 1000,
        "temperature": 0.7
    }
})

modelId = 'amazon.nova-lite-v1:0'
accept = 'application/json'
contentType = 'application/json'

try:
    response = bedrock_client.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    # Formato correto para Nova
    outputText = response_body['output']['message']['content'][0]['text']
    print(outputText)
    
except Exception as e:
    print(f"Erro: {e}")