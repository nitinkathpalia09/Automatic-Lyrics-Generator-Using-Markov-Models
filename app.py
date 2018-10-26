import random
import markovify #uses markov models to generate new sentences
import ast  
from rhyme import rhyme_finder #uses cmudict to find rhyming words based on phonetics
from sylco import sylco  #to find number of syllables 
""" Preprocessing_Stage
Includes cleaning text files, 
removing punctuations 
and demarking lines clearly   
"""
# Open and model lyrics
with open('lavigne_verse.txt') as f:
    verse_text = f.read()
with open('lavigne_chorus.txt') as f:
    chorus_text = f.read()
with open('lyrics_tokenize.txt') as f:
    tokenized_text = f.read()

verse_model = markovify.NewlineText(verse_text, state_size=2) #to demark new lines in verse raw text 
chorus_model = markovify.NewlineText(chorus_text, state_size=2) #to demark new lines in chorus raw text 

# Evaluate tokenized_text as a list
tokenized_text = ast.literal_eval(tokenized_text)

# Specify then remove punctuation
punc = set([',','.','"','?','!'])

def clean(str):
    if str[-1] in punc:
        return str[:-1]
    return str

# Generate line that rhymes with stem of verse line 1
def match_rhyme(stem, verse_model):

    # Check if rhymes exist
    try:
        ls = rhyme_finder(stem, tokenized_text)
    except KeyError:
        return None
    if not ls:
        return None

    # If rhymes exist generate lines
    for n in range(100):
        while True:
            rhyme_line = verse_model.make_sentence() #make random sentence with proper syntax and semantics from verse model

            if rhyme_line is not None:

                # Keep syllables within range
                syl_count = sylco(rhyme_line)
                if syl_count > 16 or syl_count < 6:
                    continue

                # Get stem of rhyme_line
                rhyme_stem = clean(rhyme_line.rsplit(None, 1)[-1])

                # Check for rhyme
                if rhyme_stem in ls:
                    return rhyme_line

                break


    return None

# Generate 4-line verse
def make_verse(verse_model):
    verse = ''
    stem = None

    # Markovify for each line
    for _ in range(4):
        while True:

            # Try to find rhyming match between lines 1 and 3
            if _ == 2:
                match = match_rhyme(stem, verse_model)

                # If match, add to verse.
                if match is not None:
                    verse += (match + '\n')
                    break

            # Otherwise add non-random markovify line
            line = verse_model.make_sentence()

            if line is not None:

                # Keep syllables within range
                syl_count = sylco(line)
                if syl_count > 16 or syl_count < 6:
                    continue

                # Cache line for rhyming
                if _ == 0:
                    stem = clean(line.rsplit(None, 1)[-1])

                verse += (line + '\n')
                break

    return verse

# Construct chorus
def make_chorus(chorus_model):
    chorus = '[Chorus]' + '\n'

    # Two short lines
    for _ in range(2):
        while True:

            line = chorus_model.make_sentence()
            if line is not None:

                # Keep syllables less than 11
                syl_count = sylco(line)
                if syl_count > 10:
                    continue

                chorus += (line + '\n')
                break

    # Two line reprieve
    while True:
        repeat = chorus_model.make_sentence()

        if repeat is not None:
            chorus += (repeat + '\n')
            chorus += (repeat + '\n')
            break

    return chorus

# Construct song
def make_song(chorus_model, verse_model):

    song_chorus = make_chorus(chorus_model)
"""can change according to the structure 
needed for the song
(this one has a verse followed by a chorus 
followed by 2 verses and then a the same chorus twice)
"""
    song = make_verse(verse_model) + '\n' + song_chorus + '\n' \
            + make_verse(verse_model) + '\n' + make_verse(verse_model) + '\n'\
            + (2 * (song_chorus + '\n'))

    return song

print (make_song(chorus_model, verse_model))


