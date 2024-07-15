import paramiko
import logging
import re

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


import logging
import psycopg2
from psycopg2 import Error
import os
# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


#Подключаемся по ssh
host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=username, password=password, port=port)


#PSYCOP2 
params = {
    "dbname": os.getenv('DB_DATABASE'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT')
}
TOKEN = os.getenv('TOKEN')


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'findPhoneNumbers'




def getEmails(update: Update, context):
    
    conn = psycopg2.connect(**params) # подключение к бд
    cur = conn.cursor() # создаем курсор
    
    # Выполнение SQL-запроса
    cur.execute("SELECT * FROM email;")

    # Получение всех результатов запроса
    rows = cur.fetchall()

    update.message.reply_text(rows)
    

def getPhone(update: Update, context):

    conn = psycopg2.connect(**params) # подключение к бд
    cur = conn.cursor() # создаем курсор

    # Выполнение SQL-запроса
    cur.execute("SELECT * FROM phone;")

    # Получение всех результатов запроса
    rows = cur.fetchall()

    update.message.reply_text(rows)
    

def findPhoneNumbers(update: Update, context):
    user_input = update.message.text

    phoneNumRegex = re.compile(r'(?:\+7|8|7)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}')

    phoneNumberList = phoneNumRegex.findall(user_input)

    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены!')
        return

    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'

    update.message.reply_text(phoneNumbers)

    update.message.reply_text('Введите "y" для сохранения найденных номеров телефонов в базу данных или "n" для отмены:')

    context.user_data['found_list'] = phoneNumberList

    return 'savePhoneNumbersCommand'

def savePhoneCommand(update: Update, context):
    user_input = update.effective_message.text.lower()

    if user_input == 'y':
        found_list = context.user_data['found_list']

        try:
            conn = psycopg2.connect(**params)

            cur = conn.cursor()

            for phone_number in found_list:
                cur.execute("INSERT INTO phone (phone_number) VALUES (%s)", (phone_number,))

            conn.commit()

            update.message.reply_text('Данные успешно записаны в базу данных.')

        except (Exception, psycopg2.Error) as error:
            update.message.reply_text(f'Произошла ошибка при записи данных в базу данных: {error}')

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    elif user_input == 'n':
        update.message.reply_text('Запись данных отменена.')

    return ConversationHandler.END


def getreleaseCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('lsb_release -a') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    release_info = data.decode("utf-8")  # декодируем данные в строку

    response = "Информация о выпуске Linux:\n"
    lines = release_info.split("\n")  # разделяем строки
    for line in lines:
        if len(line) > 0:
            response += f"- {line}\n"  # добавляем каждую строку с префиксом "-" для удобства чтения

    update.message.reply_text(response)  # отправляем красиво отформатированный текст
    

def getUnameCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('uname -a') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getUptimeCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('uptime') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getDfCommand(update: Update, context):
    stdin, stdout, stderr = client.exec_command('df') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info) 

def getFreeCommand(update: Update, context): #free
    stdin, stdout, stderr = client.exec_command('free') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getMpstatCommand(update: Update, context): #mpstat
    stdin, stdout, stderr = client.exec_command('mpstat') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getrepllogs(update: Update, context):
    stdin, stdout, stderr = client.exec_command("cat /var/log/postgresql/postgresql-15-main.log | grep replication | head -n 10") #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getWCommand(update: Update, context): #w
    stdin, stdout, stderr = client.exec_command('w') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getLastCommand(update: Update, context): #Последние 10 авторизаций LAST
    stdin, stdout, stderr = client.exec_command('last -n 10') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getCritCommand(update: Update, context): #Последние 10 авторизаций LAST
    stdin, stdout, stderr = client.exec_command('journalctl -p crit -n 5') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getPsCommand(update: Update, context): #Процессы
    stdin, stdout, stderr = client.exec_command('ps auxf | head') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def getSsCommand(update: Update, context): #Порты
    stdin, stdout, stderr = client.exec_command('ss -tlu') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def AptListCommand(update: Update, context):
    update.message.reply_text('Напишите название, если вам нужен определенный пакет, иначе напишите нет')

    return 'get_apt_list'

def get_apt_list (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий нет или гназвание

    Conditions = 'нет' 
    if Conditions.upper() == user_input.upper(): # провека
        stdin, stdout, stderr = client.exec_command('apt list | head -n 11') #ввод команды
        data = stdout.read() + stderr.read()
    else:
        stdin, stdout, stderr = client.exec_command(f'apt list --all-versions {update.message.text}') #ввод команды
        data = stdout.read() + stderr.read()

    info = data.decode("utf-8")

    update.message.reply_text(info) # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога

def getServicesCommand(update: Update, context): #Cервисы
    stdin, stdout, stderr = client.exec_command('systemctl --type=service --state=running') #ввод команды
    data = stdout.read() + stderr.read()
    #client.close()
    info = data.decode("utf-8")
    update.message.reply_text(info)

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!') 

def saveEmailsCommand(update: Update, context):
    user_input = update.effective_message.text.lower()

    if user_input == 'y':
        found_list = context.user_data['found_list']

        try:
            conn = psycopg2.connect(**params)

            cur = conn.cursor()

            for email in found_list:
                cur.execute("INSERT INTO email (email) VALUES (%s)", (email,))

            conn.commit()

            update.message.reply_text('Данные успешно записаны в базу данных.')

        except (Exception, psycopg2.Error) as error:
            update.message.reply_text(f'Произошла ошибка при записи данных в базу данных: {error}')

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    elif user_input == 'n':
        update.message.reply_text('Запись данных отменена.')

    return ConversationHandler.END

def helpCommand(update: Update, context):
    commands_list = """
    Мои команды:
    1. Сбор информации о релизе:
        Команда: /get_release
    2. Сбор информации об архитектуре процессора, имени хоста системы и версии ядра. 
        Команда: /get_uname
    3. Сбор информации о времени работы
        Команда: /get_uptime
    4. Сбор информации о состоянии файловой системы. 
        Команда: /get_df
    5. Сбор информации о состоянии оперативной памяти. 
        Команда: /get_free
    6. Сбор информации о производительности системы. 
        Команда: /get_mpstat
    7. Сбор информации о работающих в данной системе пользователях. 
        Команда: /get_w
    8. Последние 10 входов в систему. 
        Команда: /get_auths
    9. Последние 5 критических событий. 
        Команда: /get_critical
    10. Сбор информации о запущенных процессах. 
        Команда: /get_ps
    11. Сбор информации об используемых портах. 
        Команда: /get_ss
    12. Сбор информации об установленных пакетах. 
        Команда: /get_apt_list
    13. Сбор информации о запущенных сервисах. 
        Команда: /get_services
    14. Найти номер среди текста
        Команда: /find_phone_number
    15. Вывести все номера, которые есть в базе.
        Команда: /get_phone_numbers
    16. Найти эмейл среди текста.
        Команда: /find_email
    17. Вывести все эмейлы из бд.
        Команда: /get_emails
            """
    update.message.reply_text(commands_list)





def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска почты: ')

    return 'findEmails'

def verify_passwordCommand(update: Update, context):
    update.message.reply_text('Давайте проверим ваш пароль')
    return "verify_password"

def verify_password(update: Update, context): 
    user_input =  update.message.text # Получаем текст

    pass_Regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$') #маска для пароля

    pass_List = pass_Regex.findall(user_input) #Проверяем условие дял нашего пароля

    if not pass_List:
        update.message.reply_text('Слабый пароль')
        return # Завершаем выполнение функции
    

    passNumbers = '' # Создаем строку, в которую будем записывать пароль
    for i in range(len(pass_List)):
        passNumbers += f'{i+1}. {pass_List[i]}\n' # Записываем пароль
        
    update.message.reply_text(passNumbers).reply_text("Сложеый пароль") # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога






def findEmails(update: Update, context):
    user_input = update.effective_message.text

    emailRegex = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')

    emailsList = emailRegex.findall(user_input)

    if not emailsList:
        update.message.reply_text('Почтовые адреса не найдены!')
        return

    emails_list = '\n'.join([f"{i+1}. {email}" for i, email in enumerate(emailsList)])

    update.effective_message.reply_text(emails_list)

    update.message.reply_text('Введите "y" для сохранения найденных email-адресов в базу данных или "n" для отмены:')

    context.user_data['found_list'] = emailsList

    return 'saveEmailsCommand'
      

#def echo(update: Update, context):
#update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'saveEmailsCommand': [MessageHandler(Filters.text & ~Filters.command, saveEmailsCommand)],
        },
        fallbacks=[]
    )
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbersCommand': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbersCommand)],
            'savePhoneNumbersCommand': [MessageHandler(Filters.text & ~Filters.command, savePhoneCommand)],
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )

    convHandlerFindPass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_passwordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )

    convHandlerAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', AptListCommand)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

    
		
	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerFindPass)
    dp.add_handler(CommandHandler("get_release", getreleaseCommand))
    dp.add_handler(CommandHandler("get_uname", getUnameCommand))
    dp.add_handler(CommandHandler("get_uptime", getUptimeCommand))
    dp.add_handler(CommandHandler("get_df", getDfCommand))
    dp.add_handler(CommandHandler("get_free", getFreeCommand))
    dp.add_handler(CommandHandler("get_mpstat", getMpstatCommand))
    dp.add_handler(CommandHandler("get_w", getWCommand))
    dp.add_handler(CommandHandler("get_auths", getLastCommand))
    dp.add_handler(CommandHandler("get_critical", getCritCommand))
    dp.add_handler(CommandHandler("get_ps", getPsCommand))
    dp.add_handler(CommandHandler("get_ss", getSsCommand))
    dp.add_handler(convHandlerAptList)
    dp.add_handler(CommandHandler("get_services", getServicesCommand))
    dp.add_handler(CommandHandler("get_emails", getEmails))
    dp.add_handler(CommandHandler("get_phone_numbers", getPhone))
    dp.add_handler(CommandHandler("get_repl_logs", getrepllogs))
    


	# Регистрируем обработчик текстовых сообщений
  # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота getUnameCommand
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    while True:
      main()



