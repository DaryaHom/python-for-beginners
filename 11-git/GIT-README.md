# Домашнее задание (Git)
1. Создать локальный репозиторий с помощью системы контроля версий Git.
2. Инициализировать Git-репозиторий в выбранной директории.
3. Создать файл проекта с расширением .md (README.md).
4. В файле с расширением .md написать инструкцию по работе с командами Git (аналогично материалам лекции). 
Инструкция должна содержать (как минимум) описание следующих команд:  
    · git init — инициализация локального репозитория;  
    · git status — получение информации о текущем состоянии репозитория;  
    · git add — добавление файлов к следующему коммиту;  
    · git commit -m "message" — создание коммита;  
    · git log — вывод истории коммитов с их хеш-кодами.  

    Инструкцию допускается расширять с использованием синтаксиса Markdown(заголовки, списки, изображения, ссылки и т. д.), а также добавлять дополнительную информацию по желанию. Цель – попрактиковаться в работе с MD.

    Каждое изменение файла должно сопровождаться отдельным коммитом.
Минимальное количество коммитов — 4.

5. Разместить локальный репозиторий на платформе GitHub.
6. В системе сдачи приложить:  
    · ссылку на репозиторий на GitHub (репозиторий – публичный, не делаем приватный);  
    · архив с локальным репозиторием (вся папка проекта целиком). 

# Инструкция по работе с командами Git
## Что такое Git
**Git** — распределённая система контроля версий, разработанная Линусом Торвальдсом в 2005 году для управления исходным кодом ядра Linux. Сегодня Git — стандарт индустрии разработки ПО.

## Зачем нужен Git
- Хранит полную историю изменений проекта
- Позволяет видеть, кто, когда и что изменил
- Поддерживает ветвление и слияние
- Даёт возможность отката к любому состоянию
- Каждый разработчик имеет локальную копию репозитория

## Установка
Windows: https://git-scm.com  
macOS:
```sh
brew install git  
```
Linux:
```sh
sudo apt install git
```

## Первоначальная настройка
```sh
git config --global user.name "Ваше Имя"
git config --global user.email "your@email.com"
git config --list
```

## Создание репозитория
Создать новый:
```sh
git init
```

Клонировать существующий:
```sh
git clone https://github.com/username/repository.git
```

## Основные команды
Проверка статуса:
```sh
git status
```

Добавление файлов в индекс:
```sh
git add filename.txt
git add .
git add *.js
```

Создание коммита:
```sh
git commit -m "Описание изменений"
```

## Просмотр истории
```sh
git log
git log --oneline
git log --graph
git show <commit-hash>
```

Просмотр изменений:
```sh
git diff
git diff --staged
```

## Ветки
Ветка — указатель на коммит.
По умолчанию: main (или master)

Просмотр веток:
```sh
git branch
git branch -a
```

Создание ветки:
```sh
git branch feature-name
```

Переключение:
```sh
git checkout feature-name
git switch feature-name
```

Создание и переключение:
```sh
git checkout -b feature-name
git switch -c feature-name
```

Слияние:
```sh
git checkout main
git merge feature-name
```

Удаление:
```sh
git branch -d feature-name
git branch -D feature-name
```

## Merge vs Rebase
Merge:
- сохраняет историю
- создаёт коммит слияния
- подходит для командной работы

Rebase:
- переписывает историю
- делает её линейной
- подходит для личных веток

## Удалённые репозитории
Добавление:
```sh
git remote add origin https://github.com/username/repo.git
```

Просмотр:
```sh
git remote -v
```

Отправка:
```sh
git push origin main
git push -u origin feature-name
```

Получение:
```sh
git fetch origin
git pull origin main
```

## Fork и Clone
Clone — локальная копия репозитория  
Fork — копия репозитория в вашем аккаунте (GitHub/GitLab)

## Конфликты
Причины:
- изменения одних и тех же строк
- удаление файла, изменённого в другой ветке

Разрешение:
```sh
git status
```
Маркеры конфликта: <<<<<<< HEAD  
Ваши изменения: =======  
Чужие изменения: >>>>>>> feature-branch  
Завершение:
```sh
git add file.txt
git commit -m "Resolve merge conflict"
```
Полезные команды:
```sh
git merge --abort
git log --merge
```
## Дополнительные полезные команды на рвзные случаи жизни
### Больше не отслеживать изменения файла (аналог .gitignore)
```sh
git update-index --assume-unchanged ./cmd/license
```

#### Убрать файл из индекса неотслеживаемых файлов
```sh
git update-index --no-assume-unchanged ./cmd/license
```

### Коммит не в ту ветку:
#### Отменить последний коммит, но оставить изменения доступными
```sh
git reset HEAD~ --soft
git stash
```

#### Переключаемся на нужную ветку.
```sh
git checkout name-of-the-correct-branch
git stash pop
```

#### Добавьте конкретные файл или не парьтесь и закиньте все сразу.
```sh
git add .
git commit -m «Тут будет ваше сообщение»
```
Теперь ваши изменения в нужной ветке.  

Многие в такой ситуации предлагают использовать **cherry-pick**, так что можете выбрать, что вам больше по душе.
```sh
git checkout name-of-the-correct-branch
```
#### Берём последний коммит из мастера.
```sh
git cherry-pick master
```
#### Удаляем его из мастера.
```sh
git checkout master
git reset HEAD~ --hard
```

### Перенести изменения в другую ветку через файл:
Вначале делаем git diff и сохраняем все в файл
```sh
git diff > mychange.diff
```
Cам файл сохраняем в надежное место, ну мало чего.
Теперь можно удалить локальные изменения:
```sh
git checkout .
```

Перейти на нужную ветку:
```sh
git checkout develop-release-13.x
```

И там "накатить изменения".
```sh
git apply mychange.diff
```

### Откатить уже опубликованный коммит 
#### Отменяем последний коммит, доступный по указателю HEAD
```sh
git revert HEAD
```
#### фиксируем отмену в новом коммите
```sh
git commit -m'reverted the last commit'
```

Если вы абсолютно уверены, что вы запушили «лишний» коммит в собственную ветку, что её никто не замержил в стабильную ветку и просто так не начал разработку от последнего вашего коммита, можно откатить локальную ветку к предыдущему коммиту, а потом переписать изменения в удалённой:
```sh
git reset HEAD~
git push -f
```

### Игнорировать изменения режима файла в git:
```sh
git config core.Filemode false
```

### Переименовать ветку:
```sh
git branch -m oldname newname
git push origin HEAD
```

### Удалить ветку:
```Bash
git push -d <remote_name> <branchname>   # Delete remote
git branch -d <branchname>               # Delete local
```

### Отменить несколько коммитов в одном:
```bash
git revert --no-commit D
git revert --no-commit C
git revert --no-commit B
git commit -m "the commit message for all of them"
```

### Stash
```sh
git stash -u # Отложить неотслеживаемые файлы
git stash save "add style to our site"
git stash -p # отложить отдельные изменения. Команда будет выполняться для каждого измененного участка кода, запрашивая подтверждение на откладывание
git stash list # просмотреть список созданных наборов
git stash show # просмотреть сводные данные по набору отложенных изменений
git stash show -p # просмотреть разницу между наборами изменений
git stash pop stash@{2}
git stash drop stash@{1}
git stash clear # Очистка
git stash apply # применить изменения к рабочей копии, не удаляя их из набора отложенных
# При проверке нужно указать, применялась ли методология оценки и отметить отсутствие reflog.
```

### Worktree
```sh
cd /projects/my-project
git worktree add /projects/wt.my-project feat/some-feature 
git worktree remove /projects/wt.my-project
```
