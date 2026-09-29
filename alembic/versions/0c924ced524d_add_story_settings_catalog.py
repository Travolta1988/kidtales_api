"""add story settings catalog

Revision ID: 0c924ced524d
Revises: 40948f1c9887
Create Date: 2026-09-28 17:42:55.891547

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0c924ced524d"
down_revision: Union[str, Sequence[str], None] = "40948f1c9887"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _color(value: str) -> int:
    return int(value, 16)


CATALOG = {
    "en": {
        "heroes": [
            {
                "id": "princess",
                "title": "Brave princess",
                "hint": "A kind royal who is not afraid of a hard choice.",
                "color": _color("FFEC407A"),
            },
            {
                "id": "fox",
                "title": "Clever fox",
                "hint": "A quick thinker who talks their way out of trouble.",
                "color": _color("FFFF8A65"),
            },
            {
                "id": "dragon",
                "title": "Kind dragon",
                "hint": "A huge friend with a gentle heart.",
                "color": _color("FF66BB6A"),
            },
            {
                "id": "wizard",
                "title": "Young wizard",
                "hint": "A learner of small, sparkly spells.",
                "color": _color("FF7E57C2"),
            },
            {
                "id": "cat",
                "title": "Talking cat",
                "hint": "A witty companion with a secret plan.",
                "color": _color("FF8D6E63"),
            },
            {
                "id": "knight",
                "title": "Lost knight",
                "hint": "A traveler looking for the way home.",
                "color": _color("FF5C6BC0"),
            },
            {
                "id": "fairy",
                "title": "Forest fairy",
                "hint": "A tiny helper who watches over the trees.",
                "color": _color("FF26A69A"),
            },
            {
                "id": "boy",
                "title": "Curious boy",
                "hint": "He asks questions until the mystery opens.",
                "color": _color("FF42A5F5"),
            },
            {
                "id": "girl",
                "title": "Brave girl",
                "hint": "She runs toward the problem, not away.",
                "color": _color("FFAB47BC"),
            },
            {
                "id": "giant",
                "title": "Tiny giant",
                "hint": "Small in size, enormous in courage.",
                "color": _color("FFFFA726"),
            },
        ],
        "locations": [
            {
                "id": "forest",
                "title": "Enchanted forest",
                "hint": "Old trees, hidden paths, and whispering leaves.",
                "color": _color("FF43A047"),
            },
            {
                "id": "castle",
                "title": "Royal castle",
                "hint": "Tall towers, secret corridors, and a grand hall.",
                "color": _color("FF5C6BC0"),
            },
            {
                "id": "village",
                "title": "Seaside village",
                "hint": "Boats, bakeries, and stories from across the water.",
                "color": _color("FF29B6F6"),
            },
            {
                "id": "mountain",
                "title": "Candy mountain",
                "hint": "Sweet rivers and a trail that smells like cake.",
                "color": _color("FFEC407A"),
            },
            {
                "id": "clouds",
                "title": "Cloud kingdom",
                "hint": "Soft roads in the sky and palaces of mist.",
                "color": _color("FF7E57C2"),
            },
            {
                "id": "cave",
                "title": "Crystal cave",
                "hint": "Glowing walls and an echo that answers back.",
                "color": _color("FF26C6DA"),
            },
            {
                "id": "library",
                "title": "Magical library",
                "hint": "Books that open into other worlds.",
                "color": _color("FF8D6E63"),
            },
            {
                "id": "oasis",
                "title": "Desert oasis",
                "hint": "Cool water, date trees, and a map in the sand.",
                "color": _color("FF26A69A"),
            },
            {
                "id": "ice",
                "title": "Ice palace",
                "hint": "Frozen halls that shine like stars.",
                "color": _color("FF42A5F5"),
            },
            {
                "id": "garden",
                "title": "Hidden garden",
                "hint": "Doors of vines and flowers that remember names.",
                "color": _color("FF66BB6A"),
            },
        ],
        "styles": [
            {
                "id": "andersen",
                "title": "Hans Christian Andersen",
                "hint": "Gentle, lyrical, a little bittersweet.",
                "color": _color("FF7E57C2"),
            },
            {
                "id": "perrault",
                "title": "Charles Perrault",
                "hint": "Courtly fairy-tale manners and a clear moral.",
                "color": _color("FFEC407A"),
            },
            {
                "id": "grimm",
                "title": "Brothers Grimm",
                "hint": "Forest folklore with a brave, old-world tone.",
                "color": _color("FF5D4037"),
            },
            {
                "id": "comic",
                "title": "Comic book",
                "hint": "Bright scenes, punchy lines, heroic energy.",
                "color": _color("FFFFA726"),
            },
            {
                "id": "bedtime",
                "title": "Bedtime story",
                "hint": "Soft, calm, and cozy enough to fall asleep to.",
                "color": _color("FF5C6BC0"),
            },
            {
                "id": "modern",
                "title": "Modern adventure",
                "hint": "Fast, funny, and full of clever twists.",
                "color": _color("FF26A69A"),
            },
        ],
    },
    "uk": {
        "heroes": [
            {
                "id": "princess",
                "title": "Хоробра принцеса",
                "hint": "Добра принцеса, яка не боїться складного вибору.",
                "color": _color("FFEC407A"),
            },
            {
                "id": "fox",
                "title": "Кмітлива лисиця",
                "hint": "Швидко думає і викручується зі скрутних ситуацій.",
                "color": _color("FFFF8A65"),
            },
            {
                "id": "dragon",
                "title": "Добрий дракон",
                "hint": "Величезний друг із лагідним серцем.",
                "color": _color("FF66BB6A"),
            },
            {
                "id": "wizard",
                "title": "Юний чарівник",
                "hint": "Учень маленьких іскристих заклять.",
                "color": _color("FF7E57C2"),
            },
            {
                "id": "cat",
                "title": "Балакучий кіт",
                "hint": "Дотепний супутник із таємним планом.",
                "color": _color("FF8D6E63"),
            },
            {
                "id": "knight",
                "title": "Загублений лицар",
                "hint": "Мандрівник, який шукає дорогу додому.",
                "color": _color("FF5C6BC0"),
            },
            {
                "id": "fairy",
                "title": "Лісова фея",
                "hint": "Крихітна помічниця, що береже дерева.",
                "color": _color("FF26A69A"),
            },
            {
                "id": "boy",
                "title": "Допитливий хлопчик",
                "hint": "Ставить питання, доки таємниця не відкриється.",
                "color": _color("FF42A5F5"),
            },
            {
                "id": "girl",
                "title": "Хоробра дівчинка",
                "hint": "Біжить до проблеми, а не від неї.",
                "color": _color("FFAB47BC"),
            },
            {
                "id": "giant",
                "title": "Крихітний велетень",
                "hint": "Маленький на зріст, величезний у сміливості.",
                "color": _color("FFFFA726"),
            },
        ],
        "locations": [
            {
                "id": "forest",
                "title": "Зачарований ліс",
                "hint": "Старі дерева, потаємні стежки і шепіт листя.",
                "color": _color("FF43A047"),
            },
            {
                "id": "castle",
                "title": "Королівський замок",
                "hint": "Високі вежі, таємні коридори і парадна зала.",
                "color": _color("FF5C6BC0"),
            },
            {
                "id": "village",
                "title": "Приморське село",
                "hint": "Човни, пекарні й історії з-за моря.",
                "color": _color("FF29B6F6"),
            },
            {
                "id": "mountain",
                "title": "Цукрова гора",
                "hint": "Солодкі ріки і стежка, що пахне тортом.",
                "color": _color("FFEC407A"),
            },
            {
                "id": "clouds",
                "title": "Хмарне королівство",
                "hint": "М'які дороги в небі й палаци з туману.",
                "color": _color("FF7E57C2"),
            },
            {
                "id": "cave",
                "title": "Кришталева печера",
                "hint": "Стіни, що світяться, і луна, яка відповідає.",
                "color": _color("FF26C6DA"),
            },
            {
                "id": "library",
                "title": "Чарівна бібліотека",
                "hint": "Книжки, що відчиняються в інші світи.",
                "color": _color("FF8D6E63"),
            },
            {
                "id": "oasis",
                "title": "Пустельний оазис",
                "hint": "Прохолодна вода, фінікові пальми і мапа на піску.",
                "color": _color("FF26A69A"),
            },
            {
                "id": "ice",
                "title": "Крижаний палац",
                "hint": "Замерзлі зали, що сяють, наче зорі.",
                "color": _color("FF42A5F5"),
            },
            {
                "id": "garden",
                "title": "Таємний сад",
                "hint": "Двері з лози і квіти, що пам'ятають імена.",
                "color": _color("FF66BB6A"),
            },
        ],
        "styles": [
            {
                "id": "andersen",
                "title": "Ганс Крістіан Андерсен",
                "hint": "Ніжно, лірично, трохи гірко-солодко.",
                "color": _color("FF7E57C2"),
            },
            {
                "id": "perrault",
                "title": "Шарль Перро",
                "hint": "Придворні казкові манери і зрозуміла мораль.",
                "color": _color("FFEC407A"),
            },
            {
                "id": "grimm",
                "title": "Брати Грімм",
                "hint": "Лісовий фольклор зі сміливим старовинним тоном.",
                "color": _color("FF5D4037"),
            },
            {
                "id": "comic",
                "title": "Комікс",
                "hint": "Яскраві сцени, влучні фрази, героїчна енергія.",
                "color": _color("FFFFA726"),
            },
            {
                "id": "bedtime",
                "title": "Казка на ніч",
                "hint": "М'яко, спокійно і затишно, щоб заснути.",
                "color": _color("FF5C6BC0"),
            },
            {
                "id": "modern",
                "title": "Сучасна пригода",
                "hint": "Швидко, смішно і з кмітливими поворотами.",
                "color": _color("FF26A69A"),
            },
        ],
    },
}


def upgrade() -> None:
    op.create_table(
        "story_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("catalog", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    )
    op.create_index("ix_story_settings_id", "story_settings", ["id"])
    bind = op.get_bind()
    insert = sa.text(
        "INSERT INTO story_settings (catalog) VALUES (CAST(:catalog AS jsonb))"
    )
    for language in ("en", "uk"):
        bind.execute(insert, {"catalog": json.dumps({language: CATALOG[language]})})


def downgrade() -> None:
    op.drop_index("ix_story_settings_id", table_name="story_settings")
    op.drop_table("story_settings")
