import plotly.graph_objects as go
from datetime import datetime

tasks = []
#создание файла для загрузки
def load_tasks_from_txt():
    try:
        with open('to-do list.txt', 'r', encoding='utf-8') as file:
            for line in file:
                description, deadline_str, priority, completed_str = line.strip().split('|')
                tasks.append({
                    'description': description,
                    'deadline': datetime.strptime(deadline_str, "%d-%m-%Y"),
                    'priority': priority,
                    'completed': completed_str == 'True'
                })
    except FileNotFoundError:
        print("Файл to-do list.txt не найден.")
#сохранение задач в файл
def save_tasks_to_txt():
    with open('to-do list.txt', 'w', encoding='utf-8') as file:
        for task in tasks:
            file.write(f"{task['description']}|{task['deadline'].strftime('%d-%m-%Y')}|{task['priority']}|{task['completed']}\n")
    print('Создали файл to-do list.txt для вашего удобства!')
#добавление задачи
def add_task():
    description = input("Введите описание задачи: ")
    while True:
        try:
            deadline = input("Введите дедлайн (ДД-ММ-ГГГГ): ")
            deadline_date = datetime.strptime(deadline, "%d-%m-%Y")
            break
        except ValueError:
            print("Неправильный формат даты. Пожалуйста, попробуйте ещё раз.")

    while True:
        priority = input("Введите тип приоритета - высокий, средний или низкий (в/с/н): ").lower()
        if priority in ['в', 'с', 'н']:
            break
        print("Пожалуйста, попробуйте ещё раз.")

    tasks.append({
        'description': description,
        'deadline': deadline_date,
        'priority': priority,
        'completed': False
    })
    print("Задача добавлена.")
#список (не)выполенных задач задач
def list_tasks():
    if not tasks:
        print("Список задач пуст.")
        return

    for i, task in enumerate(tasks, 1):
        status = "\u0336".join(task['description']) + "\u0336" if task['completed'] else task['description']
        completion_status = "Ура! Задача выполнена!" if task['completed'] else "Еще не выполнено"
        overdue_message = " Упс, просрочено..." if not task['completed'] and datetime.now() > task['deadline'] else ""

        print(f"{i}. {status}. {task['deadline']}. {task['priority']}. {completion_status}. {overdue_message}")
#завершить задачу
def complete_task():
    list_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("Номер задачи для завершения: ")) - 1
        if 0 <= task_number < len(tasks):
            tasks[task_number]['completed'] = True
            print("Задача завершена!")
        else:
            print("Неверный номер задачи.")
    except ValueError:
        print("Введите номер задачи.")
#список просрочки
def show_overdue():
    overdue_tasks = [task for task in tasks if datetime.now() > task['deadline'] and not task['completed']]

    if not overdue_tasks:
        print("Нет просроченных задач.")
        return

    print("Просроченные задачи:")
    for task in overdue_tasks:
        overdue_days = (datetime.now() - task['deadline']).days
        print(f"{task['description']} - {task['deadline'].strftime('%d-%m-%Y')} - Просрочено на {overdue_days} дней")
#сортировка по приоритету, дедлайну
def sort_tasks_by_priority():
    tasks.sort(key=lambda x: {'в': 0, 'с': 1, 'н': 2}[x['priority']])
    print("Задачи отсортированы по приоритету.")

def sort_tasks_by_deadline():
    tasks.sort(key=lambda x: x['deadline'])
    print("Задачи отсортированы по дедлайну.")
#граф.визуализация по сделанным задачам
def plot_task_completion():
    completed_tasks = sum(1 for task in tasks if task['completed'])
    total_tasks = len(tasks)

    if total_tasks == 0:
        print("Нет задач для отображения.")
        return

    completed_percentage = (completed_tasks / total_tasks) * 100
    not_completed_percentage = 100 - completed_percentage

    labels = ['Выполнено', 'Не выполнено']
    sizes = [completed_percentage, not_completed_percentage]

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3,
                                 marker=dict(colors=['#87CEFA', '#9370db']))])
    fig.update_layout(title="Процент выполненных задач", showlegend=True)
    fig.show()
#функция для меню
def show_menu():
    print("\nМеню:")
    print("1. Добавить задачу")
    print("2. Показать список задач")
    print("3. Завершить задачу")
    print("4. Показать просроченные задачи")
    print("5. Сортировать задачи по приоритету")
    print("6. Сортировать задачи по дедлайну")
    print("7. Показать процент выполненных задач")
    print("8. Завершить программу и выйти")
load_tasks_from_txt()

#отображение меню после каждого действия
while True:
    show_menu()

    choice = input("Выберите вариант 1-8: ")

    if choice == '1':
        add_task()
        save_tasks_to_txt()
    elif choice == '2':
        list_tasks()
    elif choice == '3':
        complete_task()
    elif choice == '4':
        show_overdue()
    elif choice == '5':
        sort_tasks_by_priority()
    elif choice == '6':
        sort_tasks_by_deadline()
    elif choice == '7':
        plot_task_completion()
    elif choice == '8':
        save_tasks_to_txt()
        print("Программа завершена. Было круто!")
        break
    else:
        print("Выберите цифру от 1 до 8.")
