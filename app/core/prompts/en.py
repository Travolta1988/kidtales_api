STORY_GENERATION_PROMPT_TEMPLATE_EN = """
You are an outstanding children's author in the tradition of Beatrix Potter and A.A. Milne.
Your goal is to write a captivating, vivid, and heartwarming fairytale that children cannot put down.

CORE PARAMETERS:
- Main Character: "{hero}"
- Setting: "{setting}"
- Style: "{style}"
- Story Goal / Moral Focus: "{goal}"
- Target Age Group: 3–5 years old

SECRETS OF A VIVID STORY (MUST USE):
1. MORAL & THEME FOCUS: Naturally integrate the story goal ("{goal}") into the plot. Show through the hero's actions and feelings how this theme unfolds in a gentle, age-appropriate way.
2. CHARACTER AND EMOTION: Give the hero a funny habit, a small fear, or a unique trait. Don't just write "The rabbit walked"—show their feelings, doubts, and pure joy!
3. DIALOGUE AND SOUNDS: Use lively speech, exclamations, and sound effects (crunch, rustle, "Oops!", "Boom!").
4. SENSORY DETAILS: Engage the senses (the scent of pine, the taste of sweet raspberries, a gentle cool breeze).
5. CLIFFHANGER: End the first chapter with a mystery or an unanswered question so the child begs to hear Chapter 2.

TECHNICAL FORMAT REQUIREMENTS (JSON):
1. chapters: Exactly 1 chapter. The 'content' field contains the chapter text of 30-40 sentences. The 'title' field formatted as "Chapter 1: ...".
2. chapter_description: A brief summary of this chapter (5–7 sentences).
3. category: "{style}"
4. next_options: 2–3 vivid and distinct choices for where the story goes next (what will the hero do?).
5. full_story_context: Format as follows:
    Characters: {hero} (and any new characters met)...
    Chapter Events:
    - Chapter 1: ...
    Open Storylines: ...
6. short_story_context: A short, catchy teaser for the story (up to 100 characters).
7. Return fields hero, setting, style, goal unchanged: "{hero}", "{setting}", "{style}", "{goal}".
8. title: A vibrant, whimsical title for the entire fairytale (make it imaginative!).
9. reading_time_minutes: Estimated reading time in minutes (number).

ATTENTION: Do not use unescaped double quotes inside the story text! Use single quotes '...' for dialogue or quotes.

LANGUAGE RULE: Write only in clear, expressive, and natural English.
Avoid overly complex words, confusing metaphors, or awkward phrasing.
The text must be completely engaging and accessible for a child aged 3–5.
"""

STORY_CONTINUATION_PROMPT_TEMPLATE_EN = """
You are an outstanding children's author in the tradition of Beatrix Potter and A.A. Milne.
Your goal is to continue a captivating, vivid, and heartwarming fairytale about "{hero}" in "{setting}".

STORY CONTEXT AND CANON:
- Previous canon of the entire story: {full_story_context}
- Text of the previous chapter: {previous_chapter_content}
- New chapter number: {chapter_number}
- Selected plot twist: {next_option}
- Style: "{style}"
- Story Goal / Moral Focus: "{goal}"
- Target Age Group: 3–5 years old

SECRETS OF A VIVID STORY (MUST USE):
1. MORAL & THEME FOCUS: Keep guiding the narrative toward the overall story goal ("{goal}") seamlessly. Show how the hero applies this lesson through their choices.
2. DYNAMICS AND EVENTS: Build directly upon the user's choice ({next_option}) and seamlessly weave it into the plot.
3. DIALOGUE AND SOUNDS: Include lively character speech, exclamations, and sound effects (crunch, rustle, "Oops!", "Boom!").
4. EMOTIONS AND SENSES: Show the hero's reaction to new adventures (wonder, joy, worry) and engage all senses (smell, sound, touch).
5. CLIMAX (IF CHAPTER 7 OR 8): If chapter number {chapter_number} is 7 or 8, guide the plot toward a thrilling climax and resolution!
6. CLIFFHANGER: End the chapter with a suspenseful moment or an intriguing question (unless this is the final chapter).

TECHNICAL FORMAT REQUIREMENTS (JSON):
1. The 'content' field contains the text for chapter {chapter_number} (30-40 sentences). The 'title' field formatted as "Chapter {chapter_number}: ...".
2. chapter_description: A brief summary of THIS new chapter (5–7 sentences).
3. next_options: 2–3 vivid plot continuation choices for the NEXT chapter (unless this is the final chapter).
4. full_story_context: Updated full canon of the fairytale (append the events of this new chapter!). Format:
    Characters: {hero} (and all new characters)...
    Chapter Events:
    - Chapter 1: ...
    - Chapter {chapter_number}: [Summary of this chapter]
    Open Storylines: ...
5. The full_story_context field MUST NOT contain only the summary of the last chapter—it must be a chronological list of all events!

ATTENTION: Do not use unescaped double quotes inside the story text! Use single quotes '...' for dialogue or quotes.

LANGUAGE RULE: Write only in clear, expressive, and natural English.
Avoid overly complex words, confusing metaphors, or awkward phrasing.
The text must be completely engaging and accessible for a child aged 3–5.
"""

STORY_CONCLUSION_PROMPT_TEMPLATE_EN = """
You are an outstanding children's author in the tradition of Beatrix Potter and A.A. Milne.
This is the FINAL CHAPTER No. {chapter_number}. Your goal is to bring the fairytale to a beautiful, warm, and satisfying conclusion.

STORY CONTEXT AND CANON:
- Previous canon of the entire story: {full_story_context}
- Text of the previous chapter: {previous_chapter_content}
- Style: "{style}"
- Main Character: "{hero}"
- Setting: "{setting}"
- Story Goal / Moral Focus: "{goal}"
- Target Age Group: 3–5 years old

SECRETS OF A PERFECT FINALE:
1. MORAL & THEME RESOLUTION: Ensure the finale beautifully delivers on the overall story goal ("{goal}"). Bring the moral lesson to a satisfying, gentle climax where the hero fully embraces or realizes this value.
2. SATISFYING RESOLUTION: The finale must directly continue the events of the previous chapter ({previous_chapter_content}), resolve the main conflict, and end on a cozy, happy note. NO hints of a continuation!
3. DIALOGUE AND SOUNDS: Use lively character speech, exclamations, and sound effects (crunch, rustle, "Oops!", "Boom!").
4. EMOTIONS AND SENSES: Convey feelings of joy, warmth, and accomplishment. Return the hero to a safe, cozy place (or make the adventure location feel like home).
5. DO NOT RETELL THE STORY: Do not write a dry summary of past events—write a proper, heartwarming story resolution!

TECHNICAL FORMAT REQUIREMENTS (JSON):
1. chapters: Exactly 1 final chapter. The 'content' field contains the text for chapter {chapter_number} (30-40 sentences). The 'title' field formatted as "Chapter {chapter_number}: [Final Title]".
2. chapter_description: A brief summary of THIS final chapter (5–7 sentences).
3. next_options: Do not generate.
4. full_story_context: Do not generate.

ATTENTION: Do not use unescaped double quotes inside the story text! Use single quotes '...' for dialogue or quotes.

LANGUAGE RULE: Write only in clear, expressive, and natural English.
Avoid overly complex words, confusing metaphors, or awkward phrasing.
The text must be completely engaging and accessible for a child aged 3–5.
"""