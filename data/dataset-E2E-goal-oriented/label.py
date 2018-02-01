import os
import json

intents = ["greeting", "intent_resturant_search", "slots_wait", "slots_fill", "confirm"]
ffile = "dialog-task1API-kb1_atmosphere-distr0.5-trn10000-new.json"
if not os.path.exists(ffile):
    print "file not found:" + ffile
    exit(0)
data = json.load(open(ffile, 'r'))
mdict = {}
for d in data:
    intent = d["intent"]
    history = d["utterances"]
    if history[-1] != "<silence>" and intent and intent in intents and history[-1] not in mdict:
        mdict[history[-1]] = intent
print 'size of mdict:' + str(len(mdict))
for d in data:
    intent = d["intent"]
    history = d["utterances"]
    if (not intent and history[-1] != "<silence>") or (intent and intent not in intents):
        if history[-1] in mdict:
            d["intent"] = mdict[history[-1]]
            continue
        if history[-1].endswith('let\'s do that'):
            d['intent'] = 'slots_fill'
            continue
        if history[-1].startswith('let me check if') or history[-1].endswith('and there are so many other options') or\
            history[-1].endswith('let\'s see') or\
            history[-1].endswith('but perhaps i should pick something else entirely') or\
            history[-1].endswith('but it\'s not ideal') or\
            'but i\'m afraid' in history[-1]:
            d['intent'] = 'slots_wait'
            continue
        print "intent:" + intent
        print "last utterance:" + history[-1]
        new_intent = raw_input("pls input new intent:")
        if not new_intent or new_intent == "c":
            continue
        if new_intent == "q":
            break
        if new_intent not in intents:
            continue
        mdict[history[-1]] = new_intent
        d["intent"] = new_intent

tfile = "dialog-task1API-kb1_atmosphere-distr0.5-trn10000-1.json"
json.dump(data, open(tfile, 'w'))
os.remove(ffile)
os.rename(tfile, ffile)
