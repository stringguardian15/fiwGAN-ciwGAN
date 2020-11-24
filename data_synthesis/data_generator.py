import re

# a few function definitions
def get_initial_consonant_sound(word):
    m = re.match('([^aeiouAEIOU]*)([aeiou].*)',word)
    initial_sound = m.group(1)
    remaining_word = m.group(2)
    return (initial_sound,remaining_word)

def epenthesize_initial_sound(cons):
    #if the initial cons should be epenthesized, return u+initial cons.
    epenthesized_set = {'sh','s','f'}
    if cons in epenthesized_set:
        return 'u'+cons
    else: return cons

#load data
def produce_full_word_list():
    word_endings = []
    middle_vowels = []
    initial_consonants = []
    final_words = []
    root_words = []
    prefixes = []
    input_filepath = 'Inputs/'
    output_filepath = 'Outputs/'
    output_file = 'words.out'
    with open(input_filepath+'word_endings.txt','r') as fi:
        for line in fi:
            line = line.strip()
            word_endings.append(line)
    with open(input_filepath+'middle_vowels.txt','r') as fi:
        for line in fi:
            line = line.strip()
            middle_vowels.append(line)
    with open(input_filepath+'initial_consonants.txt','r') as fi:
        for line in fi:
            line = line.strip()
            initial_consonants.append(line)
    with open(input_filepath+'prefixes.txt','r') as fi:
        for line in fi:
            line = line.strip()
            prefixes.append(line)


    # Build the roots
    for we in word_endings:
        for mv in middle_vowels:
            for ic in initial_consonants:
                w = ic+mv+we
                root_words.append(w)

    # build the prefix compounds
    compound_word_list = []
    for pref in prefixes:
        for w in root_words:
            (initial_sound, remaining_word) = get_initial_consonant_sound(w)
            initial_sound_epenth = epenthesize_initial_sound(initial_sound)
            root_epenth = initial_sound_epenth + remaining_word
            compound_word = pref+root_epenth
            compound_word_list.append(compound_word)
    final_words = root_words + compound_word_list




    with open(output_filepath+output_file,'w') as fo:
        for word in final_words:
            fo.write(word+"\n")

def produce_list_for_table():
    table_columns = 8
    table_rows = 114
    root_to_comp = {}
    word_endings = []
    middle_vowels = []
    initial_consonants = []
    final_words = []
    root_words = []
    prefixes = []
    input_filepath = 'Inputs/'
    output_filepath = 'Outputs/'
    output_file = 'words_for_table.out'
    with open(input_filepath+'word_endings.txt','r') as fi:
        for line in fi:
            line = line.strip()
            word_endings.append(line)
    with open(input_filepath+'middle_vowels.txt','r') as fi:
        for line in fi:
            line = line.strip()
            middle_vowels.append(line)
    with open(input_filepath+'initial_consonants.txt','r') as fi:
        for line in fi:
            line = line.strip()
            initial_consonants.append(line)
    with open(input_filepath+'prefixes.txt','r') as fi:
        for line in fi:
            line = line.strip()
            prefixes.append(line)

    # Build the roots
    for we in word_endings:
        for mv in middle_vowels:
            for ic in initial_consonants:
                w = ic+mv+we
                root_words.append(w)

    # build the prefix compounds
    compound_word_list = []
    for pref in prefixes:
        if pref == "ik":
            continue
        for w in root_words:
            (initial_sound, remaining_word) = get_initial_consonant_sound(w)
            if initial_sound.lower() in ['t','k','p']:
                # No prefixed stops
                continue
            initial_sound_epenth = epenthesize_initial_sound(initial_sound)
            root_epenth = initial_sound_epenth + remaining_word
            compound_word = pref+root_epenth
            compound_word_list.append(compound_word)
            root_to_comp[w] = compound_word
    final_words = root_words + compound_word_list
    final_words = sorted(final_words)

    #Print the words
    with open(output_filepath+output_file,'w') as fo:
        reached_end = False
        total_words_written = 0
        word_ind = 0
        while word_ind < len(final_words):
            rows = []
            for c in range(table_columns):
                if reached_end==True:
                    break
                l = []
                for r in range(table_rows):
                    try:
                        w = final_words[word_ind]
                    except:
                        reached_end = True
                        break
                    word_ind+=1
                    l.append(w)
                rows.append(l)
            for c in range(len(rows)):
                fo.write("Words\t")
            fo.write("\n")
            for r in range(len(rows[0])):
                for c in range(len(rows)):
                    try:
                        fo.write(rows[c][r]+"\t")
                    except:
                        pass
                fo.write("\n")
            fo.write("\n")




if __name__ == '__main__':
    #produce_full_word_list()
    produce_list_for_table()
