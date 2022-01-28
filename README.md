# DiscordConvBot
Python based bot for premade conversations in discord

Requirements:
Python >3.10;
requests;
windows-curses;

/если выбивает какую-либо ошибку, вы СНАЧАЛА САМИ ГУГЛИТЕ решение а только потом строчите мне/

***УСТАНОВКА И ЗАПУСК***
1. Качаем питон, главное включаем PATH variables при установке*
2. Качаем файлы main.py и disSendClass.py из github и закидываем в одну папку
3. Если питон поставили правильно, прописываем команды "pip install windows-curses" и "pip install requests" в кмд
4. Через кмд переходим в репозиторию бота и прописываем "python main.py"**

***ИСПОЛЬЗОВАНИЕ***
- ВНИМАНИЕ желатильно запускать кмд во весь экран во избежания ненужных ошибок
- заполняем cfg файл для каждого разговора по примеру, можно через ЗАПЯТУЮ С ПРОБЕЛОМ указывать очередь выполнения
- используем стрелки ввверх и вниз для навигации между разговорами


***ПРИМЕР CFG ФАЙЛА*** *(соблюдаем конкретно этот порядок, сохраняем в формате .cfg, убедитесь что в конце строк нет пробелов или других лишних знаков)*

- txt file name     (имя текстового файла с его разширением .txt)

- token 1

- token 2

(дискорд токены, получеаем зайдя в дискорд через браузер и следуя этим указаниям F12 -> Network -> F5 (ждём пока перезагрузится) -> science -> Headers -> authorization копируем значение, вы можете использовать этот токен до тех пор пока не выйдите из сессии в браузере, а так можно закрывать окно браузера)
                  
- chat_id           (айди чата в котором будет происходить разговор, заходим через браузер в дискорд и на нужный чат, в строке адреса это последнии набор цыфр)

![Screenshot 2022-01-28 132228](https://user-images.githubusercontent.com/85110229/151538664-45e13e0d-b53f-472e-bfb4-13e95fdc76f8.png)

- delay             (задержка между сообшениями в секундах, советую ставить под 30, задержу между сообшениями в дс оно само учитует)

*(через запятую указываем что использовать полсе окончания отправки последнего сообшения в диалоге, пример: token 1, token 2)*



Если выбило ошибку, и не понятно почему, есть папка logs в которую записует ошибки и проблемы, окрываем ее и сами фиксим, если не вышло то пишем мне



*https://tutorial.djangogirls.org/ru/python_installation/

**http://mojainformatika.ru/studentam-povtias/komandnaya-stroka-windows/143-komanda-smeny-tekushhego-kataloga-cd.html


*кстати я так подумал и для вл думаю 10-15% сойдет (с профита продажи или минта) и 50% если вы апаете типу лвл (советую по баксов 50 сливать) *если не согласны то предложения приветствуются*
