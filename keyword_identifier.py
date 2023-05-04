import openai
import os
from collections import defaultdict
import spacy

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_image_prompts(story, num_prompts=5):
    nlp = spacy.load('en_core_web_sm')

    # Custom list of uninformative words
    uninformative_words = ['can', 'to', 'which', 'you', 'your', 'that','their','they']

    # Split the story into individual sentences
    doc = nlp(story)
    sentences = [sent.text.strip() for sent in doc.sents]

    # Find the main subject or noun phrase in each sentence
    main_subjects = []
    for sentence in sentences:
        doc = nlp(sentence.lower())
        for chunk in doc.noun_chunks:
            if chunk.root.dep_ == 'nsubj' and chunk.root.head.text.lower() != 'that':
                main_subjects.append(chunk)

    if main_subjects:
        main_subject = main_subjects[0]
    else:
        main_subject = None

    # Find the related words (adjectives, verbs) to the main subject
    related_words = defaultdict(list)
    for sentence in sentences:
        doc = nlp(sentence.lower())
        for tok in doc:
            # Avoid uninformative words and punctuation
            if tok.text in uninformative_words or not tok.text.isalnum():
                continue
            # If the token is a noun and it's not the main subject
            if (tok.pos_ == 'NOUN') and (main_subject is None or (tok.text != main_subject.text)):
                related_words[sentence].append(tok.text)

    # Create image prompts
    image_prompts = []
    for sentence, related in related_words.items():
        if main_subject is not None:
            prompt = f"{main_subject.text} {' '.join(related)} photorealistic"
        else:
            prompt = f"{sentence} photorealistic"
        image_prompts.append(prompt)

    # If we couldn't generate enough prompts, duplicate the existing ones
    if len(image_prompts) < num_prompts:
        print(f"Could only generate {len(image_prompts)} unique prompts out of the requested {num_prompts}. Duplicating prompts...")
        i = 0
        while len(image_prompts) < num_prompts:
            image_prompts.append(image_prompts[i])
            i = (i + 1) % len(image_prompts)  # cycle through existing prompts

    print("\nGenerated Image Prompts:")
    for idx, prompt in enumerate(image_prompts, start=1):
        print(f"{idx}: {prompt}")
    
    # Ask the user whether they want to proceed or enter their own prompts
    user_input = input("\nDo you want to proceed with these prompts? (y/n): ")
    if user_input.lower() == "y":
        return image_prompts
    elif user_input.lower() == "n":
        user_prompts = []
        print("\nEnter your own image prompts:")
        for i in range(num_prompts):
            user_prompt = input(f"Prompt {i+1}: ")
            user_prompts.append(user_prompt)
        return user_prompts
    else:
        print("Invalid input. Please enter 'y' to proceed with the generated prompts or 'n' to enter your own prompts.")
