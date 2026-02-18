from django.db import migrations


def forwards(apps, schema_editor):
    Quote = apps.get_model("journal", "Quote")
    quotes = [
        {"text": "Self-care is how you take your power back.", "author": "Lalah Delia"},
        {"text": "Thoughts are only thoughts. They are not you. You belong to yourself, even when your thoughts don't.", "author": "John Green"},
        {"text": "It is our choices, Harry, that show what we truly are, far more than our abilities.", "author": "J.K. Rowling (Albus Dumbledore)"},
        {"text": "One small crack does not mean that you are broken, it means that you were put to the test and you didn’t fall apart.", "author": "Linda Poindexter"},
        {"text": "Actually, the problem is that I can't lose my mind. It's inescapable.", "author": "John Green"},
        {"text": "Rock bottom became the solid foundation on which I rebuilt my life.", "author": "J.K. Rowling"},
        {"text": "You, yourself, as much as anybody in the entire universe, deserve your love and affection.", "author": "Buddha"},
        {"text": "Happiness can be found even in the darkest of times, if only one remembers to turn on the light.", "author": "J.K. Rowling (Albus Dumbledore)"},
        {"text": "Whatever you're worried about, you're bigger than the worries.", "author": "John Green"},
        {"text": "Owning your story is the bravest thing you’ll ever do.", "author": "Brené Brown"},
        {"text": "I would never slay the dragon, because the dragon was always me.", "author": "John Green"},
        {"text": "Recovery is not one and done. It is a lifelong journey that takes place one day, one step at a time.", "author": "Unknown"},
        {"text": "Numbing the pain for a while will make it worse when you finally feel it.", "author": "J.K. Rowling (Albus Dumbledore)"},
        {"text": "There is hope, even when your brain tells you there isn’t.", "author": "John Green"},
        {"text": "You don't have to control your thoughts; you just have to stop letting them control you.", "author": "Dan Millman"},
        {"text": "Of course it is happening inside your head, Harry, but why on earth should that mean that it is not real?", "author": "J.K. Rowling (Albus Dumbledore)"},
        {"text": "The thing about a spiral is, if you follow it inward, it never actually ends. It just keeps tightening, infinitely.", "author": "John Green"},
        {"text": "Be brave enough to heal yourself even when it hurts.", "author": "Bianca Sparacino"},
        {"text": "I have never been remotely ashamed of having been depressed. Never. What's to be ashamed of? I went through a really rough time and I am quite proud that I got out of that.", "author": "J.K. Rowling"},
        {"text": "You can't ever know someone else's hurt, not really—just like touching someone else's body isn't the same as having someone else's body.", "author": "John Green"},
        {"text": "The world is full of wonderful things you haven't seen yet. Don't ever give up on the chance of seeing them.", "author": "J.K. Rowling"},
        {"text": "Promise me you'll always remember: you're braver than you believe, stronger than you seem, and smarter than you think.", "author": "A.A. Milne"},
        {"text": "We need never be hopeless, because we can never be irreparably broken.", "author": "John Green"},
        {"text": "It is impossible to live without failing at something, unless you live so cautiously that you might as well not have lived at all—in which case, you fail by default.", "author": "J.K. Rowling"},
        {"text": "Your now is not your forever.", "author": "John Green"},
        {"text": "You are allowed to be both a masterpiece and a work in progress simultaneously.", "author": "Sophia Bush"},
        {"text": "We do not need magic to change the world, we carry all the power we need inside ourselves already: we have the power to imagine better.", "author": "J.K. Rowling"},
        {"text": "You don't have to struggle in silence.", "author": "John Green"},
        {"text": "The best way out is always through.", "author": "Robert Frost"},
        {"text": "Life is often painful, but always valuable. Sometimes we need to change the way we’re looking at it, or ask for help.", "author": "J.K. Rowling"},
    ]
    for q in quotes:
        Quote.objects.get_or_create(text=q["text"], defaults={"author": q["author"]})


def backwards(apps, schema_editor):
    Quote = apps.get_model("journal", "Quote")
    texts = [
        "Self-care is how you take your power back.",
        "Thoughts are only thoughts. They are not you. You belong to yourself, even when your thoughts don't.",
        "It is our choices, Harry, that show what we truly are, far more than our abilities.",
        "One small crack does not mean that you are broken, it means that you were put to the test and you didn’t fall apart.",
        "Actually, the problem is that I can't lose my mind. It's inescapable.",
        "Rock bottom became the solid foundation on which I rebuilt my life.",
        "You, yourself, as much as anybody in the entire universe, deserve your love and affection.",
        "Happiness can be found even in the darkest of times, if only one remembers to turn on the light.",
        "Whatever you're worried about, you're bigger than the worries.",
        "Owning your story is the bravest thing you’ll ever do.",
        "I would never slay the dragon, because the dragon was always me.",
        "Recovery is not one and done. It is a lifelong journey that takes place one day, one step at a time.",
        "Numbing the pain for a while will make it worse when you finally feel it.",
        "There is hope, even when your brain tells you there isn’t.",
        "You don't have to control your thoughts; you just have to stop letting them control you.",
        "Of course it is happening inside your head, Harry, but why on earth should that mean that it is not real?",
        "The thing about a spiral is, if you follow it inward, it never actually ends. It just keeps tightening, infinitely.",
        "Be brave enough to heal yourself even when it hurts.",
        "I have never been remotely ashamed of having been depressed. Never. What's to be ashamed of? I went through a really rough time and I am quite proud that I got out of that.",
        "You can't ever know someone else's hurt, not really—just like touching someone else's body isn't the same as having someone else's body.",
        "The world is full of wonderful things you haven't seen yet. Don't ever give up on the chance of seeing them.",
        "Promise me you'll always remember: you're braver than you believe, stronger than you seem, and smarter than you think.",
        "We need never be hopeless, because we can never be irreparably broken.",
        "It is impossible to live without failing at something, unless you live so cautiously that you might as well not have lived at all—in which case, you fail by default.",
        "Your now is not your forever.",
        "You are allowed to be both a masterpiece and a work in progress simultaneously.",
        "We do not need magic to change the world, we carry all the power we need inside ourselves already: we have the power to imagine better.",
        "You don't have to struggle in silence.",
        "The best way out is always through.",
        "Life is often painful, but always valuable. Sometimes we need to change the way we’re looking at it, or ask for help.",
    ]
    Quote.objects.filter(text__in=texts).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0002_alter_entry_mood"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
