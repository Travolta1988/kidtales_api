
STORY_GENERATION_PROMPT_TEMPLATE="""Ты — профессиональный сказочник.
Пиши в стиле "{style}".
Создай первую главу сказки про героя "{hero}" в локации "{setting}".

Правила:
1. В chapters — ровно одна глава. Её content — текст первой главы (ДЛИНА ТЕКСТА: от 1500 символов до 2000 символов). 
2. chapter_description — краткий пересказ текущей главы (5-7 предложений).
3. author — твой никнейм.
4. category — придумай категорию сказки, основываясь на теме и стиле.
5. next_options - варианты продолжения сказки.
6. Поле full_story_context — должно содержать 5-7 предложений описания сюжета первой главы. По шаблону:
    Герои: ...
    События по главам:
    - Глава 1: ...
    Открытые линии: ...
7. Не пиши в full_story_context только пересказ текущей главы и не начинай с «В этой главе».
8. Поля hero, setting, style верни как есть: "{hero}", "{setting}", "{style}"."""

STORY_CONTINUATION_PROMPT_TEMPLATE="""Продолжи сказку в стиле "{style}" про героя "{hero}" в локации "{setting}".
Предыдущий канон всей сказки: {full_story_context}
Текст предыдущей главы: {previous_chapter_content}
Номер новой главы: {chapter_number}.
Вариант продолжения сказки выбранный пользователем: {next_option}
Краткий пересказ текущей главы (5-7 предложений) запиши в chapter_description
Если номер 7 или 8 — веди сюжет к кульминации.
Правила:
1. Поле content — текст новой главы (ДЛИНА ТЕКСТА: от 1500 символов до 2000 символов).
2. Поле next_options - варианты продолжения сказки.
3. Поле full_story_context — должно содержать 5-7 предложений описания сюжета: chapter_description + previous_chapter_content. По Шаблону:
    Герои: ...
    События по главам:
    - Глава 1: ...
    - Глава 2: ...
    Открытые линии: ...
4. Не пиши в full_story_context только пересказ текущей главы."""

STORY_CONCLUSION_PROMPT_TEMPLATE="""Это ФИНАЛЬНАЯ глава № {chapter_number}.
Стиль: "{style}". Герой: "{hero}". Локация: "{setting}".
Предыдущий канон всей сказки: {full_story_context}
Краткий пересказ текущей главы (5-7 предложений) запиши в chapter_description
Текст предыдущей главы: {previous_chapter_content}
Не пересказывай всю сказку заново.
Поле content — развязка, которая продолжает ИМЕННО предыдущую главу.
Поле full_story_context:
- скопируй предыдущий канон как есть;
- оставь главы 1–9 без переписывания;
- добавь одну короткую строку «Глава 10: …»;
- «Открытые линии: нет, история завершена»."""

PROMPTS = {
    "STORY_GENERATION_PROMPT_TEMPLATE": STORY_GENERATION_PROMPT_TEMPLATE,
    "STORY_CONTINUATION_PROMPT_TEMPLATE": STORY_CONTINUATION_PROMPT_TEMPLATE,
    "STORY_CONCLUSION_PROMPT_TEMPLATE": STORY_CONCLUSION_PROMPT_TEMPLATE
}