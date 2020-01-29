"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    i = 0
    while i < len(paragraphs):
        if select(paragraphs[i]):
            if k == 0:
                return paragraphs[i]
            else:
                k -= 1
        i += 1
    return ''
    # END PROBLEM 1

def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def help_check(paragraph):
        paragraph = lower(paragraph)
        for word in split(paragraph):
            word = remove_punctuation(word)
            if word in topic:
                return True
        return False
    return help_check
    # END PROBLEM 2

def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    k, accuracy_count = 0, 0

    if not typed_words or not reference_words:
        return 0.0

    for k in range(min(len(typed_words), len(reference_words))):
        if typed_words[k] == reference_words[k]:
            accuracy_count += 1
        k += 1
    return (accuracy_count/len(typed_words)) * 100

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    num_char = len(list(typed))
    return (num_char/5) * (60/elapsed)
    # END PROBLEM 4;


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    diff_value = diff_function(user_word, valid_words[0], limit)
    diff_index = 0
    i = 1
    if user_word in valid_words:
        return user_word
    else:
        while i < len(valid_words):
            element = diff_function(user_word, valid_words[i], limit)
            if element < diff_value:
                diff_value = element
                diff_index = i
            i += 1
    if diff_value > limit:
        return user_word
    else:
        return valid_words[diff_index]
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def help_swap(index, counter):
        if counter > limit:
            return counter + 1000
        elif index == len(start) or index == len(goal):
                return counter
        elif start[index] != goal[index]:
            return help_swap(index + 1, counter + 1)
        else:
            return help_swap(index + 1, counter)
    return help_swap(0, abs(len(start) - len(goal)))
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if start == goal or limit < 0:
        return 0

    elif not len(start) * len(goal):
        return len(start) + len(goal)

    else:
        if goal[0] == start[0]:
            substitute_diff = edit_diff(start[1:], goal[1:], limit)
        else:
            substitute_diff = edit_diff(start[1:], goal[1:], limit-1) + 1

        add_diff = edit_diff(start, goal[1:], limit - 1) + 1
        remove_diff = edit_diff(start[1:], goal, limit - 1) + 1

        return min(substitute_diff, add_diff, remove_diff)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    i = 0
    while i < len(typed) and typed[i] == prompt[i]:
        i += 1

    send({'id': id, 'progress': i/len(prompt)})
    return i/len(prompt)
    # END PROBLEM 8

def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    word_list = []
    for _ in range(n_players):
        word_list += [[]]

    for word_num in range(1, n_words + 1):
        current_word = word(word_times[0][word_num])
        diff_lst = []
        min_time_diff = 0

        for player_num in range(n_players):
            diff_lst += [elapsed_time(word_times[player_num][word_num]) - \
                elapsed_time(word_times[player_num][word_num - 1])]

        min_time_diff = min(diff_lst)
        for player_num in range(n_players):
            if diff_lst[player_num] <= min_time_diff + margin:
                word_list[player_num] += [current_word]

    return word_list
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)