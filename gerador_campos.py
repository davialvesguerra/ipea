from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Carregar modelo e tokenizer
modelo = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

def gerar_exemplar(nome_campo, tipo_campo):
    # Pré-processar entrada
    entrada = f"{nome_campo}, {tipo_campo}"
    inputs = tokenizer(entrada, return_tensors='pt', padding=True, truncation=True, max_length=50)

    # Gerar saída com o modelo
    output = modelo.generate(**inputs, max_length=50, num_return_sequences=1)

    # Converter tokens de saída em texto
    texto_gerado = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Pós-processar saída conforme o tipo de campo
    # dado_gerado = post_processar(texto_gerado, tipo_campo)
    
    return texto_gerado

print(gerar_exemplar("codigoCliente","long"))