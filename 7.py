import logging
import re
import paramiko
import psycopg2

ssh_username = 'al1'
ssh_password = '1'
ssh_hostname =  'al2'
TOKEN = "6993763154:AAG9DRGWFYaeqD1QrdLn1pmrsIuErjU9eP4"         
db_host = "172.16.184.148"
db_port = "5432"
db_database = "db_ptstart"
db_username = "postgres"
db_password = "Qq12345"


from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
def run_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    return output

def ssh_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_hostname, username=ssh_username, password=ssh_password)
    return client

def get_release(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "cat /etc/*release")
    update.message.reply_text(release_info)
    client.close()
def get_uname(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "uname -a")
    update.message.reply_text(release_info)
    client.close()
def get_uptime(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "uptime")
    update.message.reply_text(release_info)
    client.close()
def get_df(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "df -h")
    update.message.reply_text(release_info)
    client.close()
def get_free(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "free -h")
    update.message.reply_text(release_info)
    client.close()
def get_mpstat(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "mpstat")
    update.message.reply_text(release_info)
    client.close()
def get_w(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "w")
    update.message.reply_text(release_info)
    client.close()
def get_auths(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "last -n 10")
    update.message.reply_text(release_info)
    client.close()
def get_critical(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "dmesg | tail -n 5")
    update.message.reply_text(release_info)
    client.close()
def get_ps(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "ps aux | head -n 10")
    update.message.reply_text(release_info)
    client.close()
def get_ss(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "ss -tuln")
    update.message.reply_text(release_info)
    client.close()
def get_apt_list(update: Update, context):
    client = ssh_connect()

    user_input = update.message.text

    if user_input == "0":
        release_info = run_command(client, "apt list --installed -qq | head -n 10")
    else:
        release_info = run_command(client, f"apt list -qq {user_input}")

    update.message.reply_text(release_info)
    client.close()

    return ConversationHandler.END
def get_repl_logs(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "cat /var/log/postgresql/postgresql-15-main.log | grep replication | tail -n 10")
    update.message.reply_text(release_info)
    client.close()

def get_services(update: Update, context):
    client = ssh_connect()
    release_info = run_command(client, "systemctl list-units --type=service | head -n 10")
    update.message.reply_text(release_info)
    client.close()
def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def get_emails(update: Update, context):
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_database,
            user=db_username,
            password=db_password
        )

        cur = conn.cursor()

        cur.execute("SELECT email FROM users")

        emails = cur.fetchall()

    except (Exception, psycopg2.Error) as error:
        update.message.reply_text(f'Произошла ошибка при получении адресов электронной почты: {error}')
        return

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    if emails:
        email_list = '\n'.join([f"{i+1}. {email[0]}" for i, email in enumerate(emails)])

        update.message.reply_text(f'Найденные адреса электронной почты:\n{email_list}')

    else:
        update.message.reply_text('Адреса электронной почты не найдены.')

def get_phones(update: Update, context):
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_database,
            user=db_username,
            password=db_password
        )

        cur = conn.cursor()

        cur.execute("SELECT phone FROM phones")

        phones = cur.fetchall()

    except (Exception, psycopg2.Error) as error:
        update.message.reply_text(f'Произошла ошибка при получении номеров: {error}')
        return

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    if phones:
        phone_list = '\n'.join([f"{i+1}. {phone[0]}" for i, phone in enumerate(phones)])

        update.message.reply_text(f'Найденные номера:\n{phone_list}')

    else:
        update.message.reply_text('Номера не найдены.')



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
    """
    update.message.reply_text(commands_list)


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'

def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска почтовых адресов: ')

    return 'findEmails'

def saveEmailsCommand(update: Update, context):
    user_input = update.effective_message.text.lower()

    if user_input == 'y':
        found_list = context.user_data['found_list']

        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_database,
                user=db_username,
                password=db_password
            )

            cur = conn.cursor()

            for email in found_list:
                cur.execute("INSERT INTO users (email) VALUES (%s)", (email,))

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

def savePhoneCommand(update: Update, context):
    user_input = update.effective_message.text.lower()

    if user_input == 'y':
        found_list = context.user_data['found_list']

        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_database,
                user=db_username,
                password=db_password
            )

            cur = conn.cursor()

            for phone_number in found_list:
                cur.execute("INSERT INTO phones (phone) VALUES (%s)", (phone_number,))

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


def checkPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки сложности: ')

    return 'checkPassword'

def get_apt_listCommand(update: Update, context):
    update.message.reply_text('Введите 0 для вывода всех пакетов или название пакета: ')

    return 'get_apt_list_input'

def checkPassword(update: Update, context):
    password = update.message.text

    if len(password) < 8 or not re.search(r'\d', password) or (not re.search(r'[a-z]', password) or\
                                                               not re.search(r'[A-Z]', password) or\
                                                               not re.search(r'[!@#$%^&*()]', password)):
        update.message.reply_text('Пароль простой')
    else:
        update.message.reply_text('Пароль сложный')

    return ConversationHandler.END

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



def echo(update: Update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbersCommand': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbersCommand)],
            'savePhoneNumbersCommand': [MessageHandler(Filters.text & ~Filters.command, savePhoneCommand)],
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'saveEmailsCommand': [MessageHandler(Filters.text & ~Filters.command, saveEmailsCommand)],
        },
        fallbacks=[]
    )
    convHandlerCheckPassword = ConversationHandler(
        entry_points=[CommandHandler('check_password', checkPasswordCommand)],
        states={
            'checkPassword': [MessageHandler(Filters.text & ~Filters.command, checkPassword)],
        },
        fallbacks=[]
    )
    convHandlerGet_apt_list = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_listCommand)],
        states={
            'get_apt_list_input': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )
    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerCheckPassword)
    dp.add_handler(convHandlerGet_apt_list)
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(CommandHandler('get_emails', get_emails))
    dp.add_handler(CommandHandler('get_phone_numbers', get_phones))
    # Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
