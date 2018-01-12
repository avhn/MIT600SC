# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5
#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word
    def is_word_in(self, text):
        for i in string.punctuation:
            text = text.replace(i, ' ')
        text = text.lower().split()
        
        return self.word.lower() in text
            
# TODO: TitleTrigger

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, object):
        return self.is_word_in(object.get_title())

# TODO: SubjectTrigger

class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, object):
        return self.is_word_in(object.get_subject())

# TODO: SummaryTrigger

class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, object):
        return self.is_word_in(object.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, object):
        return not self.trigger.evaluate(object)
        
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    def evaluate(self, object):
        return self.trig1.evaluate(object) and self.trig2.evaluate(object)
        
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    def evaluate(self, object):
        return self.trig1.evaluate(object) or self.trig2.evaluate(object)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(object):
    def __init__(self, phrase):
        self.phrase = phrase
    def evaluate(self, object):
        """
        Gets NewsStory object. """
        text = object.get_subject() + object.get_title() + object.get_summary()
        return self.phrase in text

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10

    evaluated = list()
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                evaluated.append(story)
                break
    return evaluated

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones


    # Subfunctions to help
    def find_line(key, lines):
        """
        returns: associated line as str.
        """
        for line in lines:
            if line.startswith(key):
                return line[line.find(' ')+1:]
    
    def return_trig(trig, lines):
        """
        Recursive function.

        returns: trigger as an object. 
        """
        
        line = find_line(trig, lines).split(' ', 1) # Parse trigger name and args
        trig_name = line[0][:1] + line[0][1:].lower() + 'Trigger'
        args = line[1]
        
        if line[0] not in ['OR', 'AND']: # WordTriggers, PhaseTrigger
            return eval( trig_name + "('"+args+"')" )
        else: # CompositeTriggers
            trigs = list()
            for trig in args.split():
                trigs += [return_trig(trig, lines)]
            return eval(trig_name)(trigs[0],trigs[1])
        
    # Function core
    add_list = []
    for line in lines:
        if line.startswith('ADD'):
            add_list += line.split()[1:]

    triggers = []
    for trig in add_list:
        triggers += [return_trig(trig, lines)]
    return triggers
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print("Polling...")

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print("Sleeping...")
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

