import pickle
import numpy as np
import re
import string
import json
import random
import os
import io

def is_direction(line):#detect directions
    global lines 
    direction_list = ['ROOFTOP',"OMITTED",'Omitted','END TEASER','(ECU)', """(CONT'D)""",'(MORE)',"Shooting Script","CONTINUED",'BACK TO','CLOSE ON','DISSOLVE TO',
                     'TIGHT ON ','ACT ONE','ACT TWO','ACT THREE','ACT FOUR','OVER BLACK','INSERT','ON STAGE','THE END','QUICK MONTAGE','ONSCREEN','FADE','TO CAMERA','CLOSEUP','SUPERIMPOSE','9/27/13','Revised','REVISED','Revision','PAGES',
                     'END EPISODE','END OF','END ACT','END OF SHOW','SUPER:','END PILOT','FLASHBACK','SCREENPLAY','OMIT','SHOOTING SCRIPT','"IN DARKNESS" SCRIPT',' POV',')B(']
    for direction in direction_list:
        if(direction in line):
            return True
    return False

def is_scene(line):#deteck scene changer lines
    global lines  
    sc_list = ['INTERIORS','EXTERIORS',"EXT.","INT.","EXT ","INT ","INT:","EXT:","TEASER","FADE IN","DECK ","ROOM","ELEVATOR","ON THE ","SLAM TO","INT/EXT","I/E.","TITLE",'TRANSITION TO',
               'LATER','NIGHT','THAT','APARTMENT','CUT TO','INTERCUT','SCENE','SFX OVER','VFX:','DISSOLVE ']
    for sc in sc_list:
        if(sc in line):
            return True
    return False

def find_page_counts(script):
    global lines
    page_count = []
    for line in script:
        if re.search('(^\d+)(\.$)', str(line)):
            page_count.append(line)
        elif re.search('(\d+\.$)', str(line)):
            page_count.append(line)
        else:
            pass
#     print("page_count: " + str(len(page_count))) # check
    return page_count       

def is_cast_name(script):
    global lines
#     counts_dict = {}
    names_list = []
    scenes_count = 0
    dialogue_count = 0
    lines_count = 0
    for i, line in enumerate(script):
        if line == " ":
            pass
        else:
            lines_count += 1
        if line.isupper():
            if is_scene(line):
                scenes_count += 1
                pass
            elif is_direction(line):
                pass
            elif len(line)<2:
                pass
            elif line[-1] == '.' or line[-1] == ':' or line[-1] == '!' or line[-1] == '-' or line[-2] == '!':
                pass
            elif re.search('\W?\s$', str(line)):
                pass
    #         if is_all_caps(line):
            else:
                dialogue_count += 1
                if("CONT" in line or "O.S." in line or "O.C." in line or "V.O" in line or "MORE" in line):
                    script[i] = line.strip("V.O.")
                    script[i] = line.strip("CONT.")
                    script[i] = line.strip("O.C.")
                    script[i] = line.strip("O.S.")
                    pass
                elif line not in names_list:
                    names_list.append(line)
                else:
                    pass 
    page_count = find_page_counts(script)
    characters_count = str(len(names_list))
    counts_dict = {"lines_count": lines_count, "dialogue_count": dialogue_count, "scenes_count": scenes_count,
                  "characters_count" : characters_count,"page_count": len(page_count), "characters_list": names_list, "pilot_script":script }
    return counts_dict

def find_tease_indicators(script):
    found_tease_indicators = []
    tease_indicators = ['VOICE-OVER','COLD OPEN','THE CAMERA PASSES','We HEAR','TEASER','FROM THE BLACK -- ','FADE IN','ACT ONE.','ACT ONE','FADE IN:','BATHING MONTAGE:','restrictions set forth above','EXT']
    for line in script:
        if re.search('(^EXT).+?', str(line)):
            tease_indicators.append(str(line))
            break 
        elif re.search('(^INT).+?', str(line)):
            tease_indicators.append(str(line))
#             print(line.index()) # check
            break 
        elif re.search('(^TIGHT ON).+?', str(line)) or re.search('(^THE CAMERA PASSES).+?', str(line)):
            tease_indicators.append(str(line))
        elif re.search('(^We HEAR).+?', str(line)):
            tease_indicators.append(str(line))
            break 
    for word in tease_indicators:
        found_tease_indicators = [item for item in tease_indicators if item in script]
        return found_tease_indicators

def simple_clean(lines):
    for i,line in enumerate(lines):
        lines[i] = lines[i].replace("’","'")
        lines[i] = lines[i].replace('(MORE)','')#replace all (MORE)
        lines[i] = lines[i].replace('EXT:','EXT.') # default is 'EXT.', not 'EXT:'
        lines[i] = lines[i].replace("cont'd","CONT")
        lines[i] = lines[i].replace('(Cont.)',"(CONT)")
        lines[i] = lines[i].replace("""(CONT'D)""","(CONT)")
    return lines

    
def clip_script_body(script):
    global lines
    earliest_indicator = 500
    found_tease_indicators = find_tease_indicators(script)
    if len(found_tease_indicators)==0:
        raise NameError('No tease indicators for screenplays[' + str(screenplays.index(script)) + "]")
    while len(found_tease_indicators) >= 1: 
        for word in found_tease_indicators:
#             print(word) # check
            for i, line in enumerate(script):
                if(word in line):
#                     print(str(word) + str(i)) # check
#                     print("this word: " + word + " was at index: " + str(i)) #check
                    if i >= earliest_indicator:
    #                   print("Not earliest indicator") # check
                        del found_tease_indicators[0]
                        break
                    else:
                        earliest_indicator = i  
                        break
        else:
            script_body = script[i:]
#             print(earliest_indicator) # check
            return script_body


            
def count_voiceover(body):
    voiceovers = 0
    for i, line in enumerate(body):
        if "V.O." in line:
            voiceovers += 1
            continue
        if "O.C." in line:
            voiceovers +=1
            continue
#     print("voiceovers: " + str(voiceovers))
    return voiceovers

def count_questions(body):
    question_count = 0
    for line in body:
        if "?" in str(line):
            question_count += 1
    return question_count
    
def count_exclamations(body):
    exclamation_count = 0
    for line in body:
        if "!" in str(line):
            exclamation_count +=1
    return exclamation_count
        

def run_counts(screenplays):
    counts_dicts = []
    for index in range(len(screenplays)):
        each_script = screenplays[index]
        body = clip_script_body(each_script)
        body = simple_clean(body)
        voiceover_lines = count_voiceover(body)
        question_count = count_questions(body)
        exclamation_count = count_exclamations(body)
        counts_dict = is_cast_name(body)
        counts_dict['voiceover_lines'] = voiceover_lines
        counts_dict['question_count'] = question_count
        counts_dict['exclamation_count'] = exclamation_count
        counts_dicts.append(counts_dict)
    return counts_dicts

# script_body = clip_script_body(screenplays[3])
# counts_dict = is_cast_name(script_body)
