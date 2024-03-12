import logging

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import time 
import pandas as pd


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.chat_data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    await context.bot.send_photo(update.effective_chat.id,photo='https://thispersondoesnotexist.com/')


async def gerar_questao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    data = pd.read_csv('dados_cru.csv')
    data_respondido = pd.read_csv('dados_respondidos.csv')
    
    if(context.args):
        topico = 'tópico ' + context.args[0]
        data = data[data['topico'] == topico]
        data_respondido = data_respondido[data_respondido['topico'] == topico]

    qtd_questao = str(data.shape[0] - data_respondido.shape[0])
    dados = data.sample()

    while(True):
        if(dados['id'].to_list()[0] not in data_respondido['id'].to_list()):
            break
        
        dados = data.sample()
    

    context.user_data['id'] = dados['id'].to_list()[0]
    context.user_data['topico'] = dados['topico'].to_list()[0]
    context.user_data['tema'] = dados['tema'].to_list()[0]
    context.user_data['enunciado'] = dados['enunciado'].to_list()[0]
    context.user_data['resposta_certa'] = dados['resposta_certa'].to_list()[0]
    context.user_data['explicacao'] = dados['explicacao'].to_list()[0]

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Faltam {qtd_questao} questões desse tópico a serem respondidas!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=context.user_data['enunciado'])


async def mostrar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['resposta_user'] = context.args[0]
    context.user_data['dificuldade'] = context.args[1]
    context.user_data['ano'] = time.localtime()[0]
    context.user_data['mes'] = time.localtime()[1]
    context.user_data['dia'] = time.localtime()[2]

    resposta = " ".join([context.user_data['resposta_certa'], context.user_data['explicacao']])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)
       
async def salvar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # https://www.dio.me/articles/desvendando-o-potencial-do-duckdb-uma-introducao-que-vai-turbinar-suas-analises-de-dados

    dados = {
         'id': context.user_data['id'] ,
         'topico': context.user_data['topico'] ,
         'tema': context.user_data['tema'],
         'enunciado': context.user_data['enunciado'],
         'resposta_certa': context.user_data['resposta_certa'],
         'explicacao': context.user_data['explicacao'],
         'resposta_user': context.user_data['resposta_user'],
         'ano': context.user_data['ano'],
         'mes': context.user_data['mes'],
         'dia': context.user_data['dia'],
         'dificuldade': context.user_data['dificuldade']
         }
    

    data = pd.read_csv('dados_respondidos.csv')
    dados = pd.DataFrame(dados, index=[0])

    data = pd.concat([data, dados])

    dados_respondidos_hoje = data[(data['mes'] == time.localtime()[1])*(data['dia'] == time.localtime()[2])]
    qtd_dados_respondidos_hoje = dados_respondidos_hoje.shape[0]

    data.to_csv('dados_respondidos.csv', index=False)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Os dados foram salvos!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Você respondeu um total de {qtd_dados_respondidos_hoje} questões hoje.")

def main():
    """Função principal que define o bot."""
    # Token fornecido pelo BotFather
    TOKEN = TELEGRAM_API_KEY


    # Obter o dispatcher para registrar os manipuladores
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    echo_handler = CommandHandler('echo', echo)
    gerar_questao_handler = CommandHandler('questao', gerar_questao)
    mostrar_resposta_handler = CommandHandler('resposta', mostrar_resposta)
    salvar_resposta_handler = CommandHandler('salvar', salvar_resposta)

    # Diferentes manipuladores para diferentes comandos
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(gerar_questao_handler)
    application.add_handler(mostrar_resposta_handler)
    application.add_handler(salvar_resposta_handler)

    application.run_polling()
    


if __name__ == '__main__':
    main()
