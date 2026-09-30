STORY_GENERATION_PROMPT_TEMPLATE_EN="""You are a professional children's writer.
Create a story for children aged 3 to 10 years old. Simple style, easy to understand.
No repetitions of words and phrases. Simple and clear exposition.
Write in the style "{style}".
Create the first chapter of the story about the hero "{hero}" in the location "{setting}".

Rules:
1. In chapters - exactly one chapter. Its content - text of the first chapter (TEXT LENGTH: from 1500 to 2000 characters).
2. chapter_description - a brief summary of the current chapter (5-7 sentences).
3. category - duplicate the style field here.
4. next_options - options for continuing the story. Where will the plot go.
5. The full_story_context field must contain 5-7 sentences describing the plot of the first chapter. By template:
    Heroes: ...
    Events by chapters:
    - Chapter 1: ...
    Open lines: ...
6. Do not write in full_story_context only the summary of the current chapter and do not start with «In this chapter».
7. The fields hero, setting, style return as is: "{hero}", "{setting}", "{style}".
8. The title field - come up with a title of the story, based on the theme and style.
9. The reading_time_minutes field - come up with the reading time of the story, based on the length of the first chapter text.
10. short_story_context - a brief summary of the story plot. Maximum 100 characters.
"""

STORY_CONTINUATION_PROMPT_TEMPLATE_EN="""
"""

STORY_CONCLUSION_PROMPT_TEMPLATE_EN="""
"""

STORY_GENERATION_PROMPT_TEMPLATE_UK="""Ты — профессиональный детский писатель.
Создай сказку для детей в возрасте от 3 до 10 лет. Простой стиль, легкий для понимания.
Без повторений слов и фраз. Простое и понятное изложение.
Пиши в стиле "{style}".
Создай первую главу сказки про героя "{hero}" в локации "{setting}".

Правила:
1. В chapters — ровно одна глава. Её content — текст первой главы. Должно быть 20-30 предложений.
Её title - придумай название первой главы, основываясь на теме и стиле в формате "Глава 1: ...". 
2. chapter_description — краткий пересказ текущей главы (5-7 предложений).
3. category — дублируй поле style сюда.
4. next_options - варианты продолжения сказки. Куда поведет сюжет.
5. Поле full_story_context — должно содержать 5-7 предложений описания сюжета первой главы. По шаблону:
    Герои: ...
    События по главам:
    - Глава 1: ...
    Открытые линии: ...
6. Не пиши в full_story_context только пересказ текущей главы и не начинай с «В этой главе».
7. Поля hero, setting, style верни как есть: "{hero}", "{setting}", "{style}".
8. Поле title - придумай название сказки, основываясь на теме и стиле.
9. Поле reading_time_minutes - придумай время чтения сказки, основываясь на длине текста первой главы.
10. short_story_context - краткое описание сюжета сказки. Максимум 100 символов.
"""

STORY_CONTINUATION_PROMPT_TEMPLATE_UK="""Продолжи сказку в стиле "{style}" про героя "{hero}" в локации "{setting}".
Предыдущий канон всей сказки: {full_story_context}
Текст предыдущей главы: {previous_chapter_content}
Номер новой главы: {chapter_number}.
Вариант продолжения сказки выбранный пользователем: {next_option}
Краткий пересказ текущей главы (5-7 предложений) запиши в chapter_description
Если номер 7 или 8 — веди сюжет к кульминации.
Правила:
1. Поле content — текст новой главы. Должно быть 20-30 предложений.
2. Поле next_options - варианты продолжения сказки.
3. Поле full_story_context — должно содержать 5-7 предложений описания сюжета: chapter_description + previous_chapter_content. По Шаблону:
    Герои: ...
    События по главам:
    - Глава 1: ...
    - Глава 2: ...
    Открытые линии: ...
4. Не пиши в full_story_context только пересказ текущей главы."""

STORY_CONCLUSION_PROMPT_TEMPLATE_UK="""Это ФИНАЛЬНАЯ глава № {chapter_number}.
Стиль: "{style}". Герой: "{hero}". Локация: "{setting}".
Предыдущий канон всей сказки: {full_story_context}
Краткий пересказ текущей главы (5-7 предложений) запиши в chapter_description
Текст предыдущей главы: {previous_chapter_content}.
Сказка должна завершаться без намека на продолжение.
Не пересказывай всю сказку заново.
Поле content — развязка, которая продолжает ИМЕННО предыдущую главу.
Не генерируй новый full_story_context, next_options."""

PROMPTS = {
    "STORY_GENERATION_PROMPT_TEMPLATE_EN": STORY_GENERATION_PROMPT_TEMPLATE_EN,
    "STORY_CONTINUATION_PROMPT_TEMPLATE_EN": STORY_CONTINUATION_PROMPT_TEMPLATE_EN,
    "STORY_CONCLUSION_PROMPT_TEMPLATE_EN": STORY_CONCLUSION_PROMPT_TEMPLATE_EN,

    "STORY_GENERATION_PROMPT_TEMPLATE_UK": STORY_GENERATION_PROMPT_TEMPLATE_UK,
    "STORY_CONTINUATION_PROMPT_TEMPLATE_UK": STORY_CONTINUATION_PROMPT_TEMPLATE_UK,
    "STORY_CONCLUSION_PROMPT_TEMPLATE_UK": STORY_CONCLUSION_PROMPT_TEMPLATE_UK,
}