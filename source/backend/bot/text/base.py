

class EnglishText:
    language_code: str = 'en'
    language_name: str = 'English'
    flag: str = '🇺🇸'

    choice_language_message: str = 'Please select a language'
    error_choice_message_name: str = 'Please select an answer on the keyboard'
    successfully_change_language_message: str = 'The language has been successfully changed'

    cancel: str = 'Cancel'
    return_to_main_menu: str = 'Return to the main menu'

    create_document_button_name: str = 'Create document'
    change_language_button_name: str = 'Change language'
    start_quizzes_button_name: str = '🧑‍💻 Start quiz'

    select_action_message: str = 'Choose an action on the keyboard'

    load_pdf_file_message: str = 'Upload PDF document based on which you want to take the quiz'
    document_loaded: str = 'The document has been received!'

    set_questions_count_message: str = 'Enter the number of questions you want to complete'

    star_quiz_message: str = ('All data for creating of the test has been received. '
                              'Wait, we\'re creating a task for you...')

    answer_question: str = 'Answer the question :\n{question}'

    answer_is_correct: str = 'Correct, {more}'

    quiz_completed: str = 'The test is completed, you have answered {correct} out of {all} questions'


class RussianText(EnglishText):
    language_name = 'Русский'
    language_code = 'ru'
    flag: str = '🇷🇺'

    choice_language_message: str = 'Пожалуйста выберите язык'
    error_choice_message_name: str = 'Пожалуйста выберите ответ на клавиатуре'
    successfully_change_language_message: str = 'Язык был успешно изменен'

    cancel: str = 'Отменить'
    return_to_main_menu: str = 'Вернуться в главное меню'

    create_document_button_name: str = 'Создать документ'
    change_language_button_name: str = 'Изменить язык'
    start_quizzes_button_name: str = '🧑‍💻 Начать проверку знаний'

    select_action_message: str = 'Выберите действие на клавиатуре'

    load_pdf_file_message: str = 'Загрузите PDF документ на основе которого хотите пройти тест'
    document_loaded: str = 'Документ получен!'

    set_questions_count_message: str = 'Введите количество вопросов которые вы хотите пройти '

    star_quiz_message: str = 'Все данные для формирования теста получены. Подождите мы создаем для вас задание...'

    answer_question: str = 'Ответьте на вопрос :\n{question}'

    answer_is_correct: str = 'Правильно, {more}'

    quiz_completed: str = 'Тест завершен, вы ответили на {correct} вопросов из {all}'
