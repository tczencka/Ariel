import pickle
import numpy as np
import re
import string
import json
import random
import os
import io

def find_title(title_page): 
    try:
        title = title_page[0]
    except IndexError:
        title = "Missing"
        pass
    return title

def find_writer(cover): 
    global lines
    writer_indicators = ['Created By ','written by','Written by','Written By','written by:','written by: ','Written by:','Written by: ','Written By:','Written By :','pilot by:','pilot by','by']
    screenwriter = "No Screenwriter"
    earliest_indicator = 500
    for word in writer_indicators:
        for i, line in enumerate(cover):       
            if (word in line):                    
                if i > earliest_indicator:
                    continue
                elif i == 0:
                    continue
                elif line[-2:]=='by' or line[-2:]=='By' or line[-3:]=='by:' or line[-3:]=='by ' or line[-3:]=='By ' or line[-3:]=='By:' or line[-4:]=='by: ' or line[-4:]=='By: ':
#                     print(line[-5:]) #check
                    earliest_indicator = i + 1
                    continue
                else:
                    earliest_indicator = i
                    continue
            else:
                continue
    if earliest_indicator == 500:
        screenwriter = "No Writer Indicators"
    else:
        screenwriter = cover[earliest_indicator]
#     print("screenwriter is: " + screenwriter) # check
#     print("earliest_indicator of screenplay[" + str(cover[0]) + "] was: " + str(earliest_indicator)) #check
    return screenwriter

def find_doctor(cover):
    global lines
    doctor = "No Script Doctor"
    earliest_indicator = 500
    for i, line in enumerate(cover):
        if re.search('^.?(Revis?.+by)', str(line)):
#             print(i, line) # check
            if i > earliest_indicator:
                pass
            else:
                earliest_indicator = i
                doctor = cover[i+1]
#     print (doctor) # check
    return doctor
    
def find_source_material(cover): 
    global lines
    source_material = "Original"
    earliest_indicator = 500
    for i, line in enumerate(cover):
        if re.search('^.?(Based?.+)', str(line)):
#             print(i, line) # check
            if i > earliest_indicator:
                pass
            else:
                earliest_indicator = i
                source_material = cover[i]
#     print(source_material) # check
    return source_material

def find_director(cover): 
    global lines
    earliest_indicator = 500
    director = "Director Not Listed"
    for i, line in enumerate(cover):
        match = re.search('^.+?(irected?.+)', str(line))
        if match:
#             print(i, line) # check
            if i > earliest_indicator:
                continue
            else:
                earliest_indicator = i
                director = cover[i+1]
#     print(director) # check
    return director

def find_tease_indicators(script):
    found_tease_indicators = []
    tease_indicators = ['VOICE-OVER','SLOW MOTION.  Small particles of glass rain down with snow. ','COLD OPEN','THE CAMERA PASSES','We HEAR','TEASER','FROM THE BLACK -- ','FADE IN','ACT ONE.','ACT ONE','FADE IN:','BATHING MONTAGE:','restrictions set forth above','EXT']
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
#             print(line.index()) # check
            break 
        elif re.search('(^We HEAR).+?', str(line)):
            tease_indicators.append(str(line))
#             print(line.index()) # check
            break 
    for word in tease_indicators:
        found_tease_indicators = [item for item in tease_indicators if item in script]
        return found_tease_indicators

def clip_title_page(script):
    global lines
    earliest_indicator = 500
    found_tease_indicators = find_tease_indicators(script)
    if len(found_tease_indicators)==0:
        raise NameError('No tease indicators for screenplays[' + str(screenplays.index(script)) + "]")
    while len(found_tease_indicators) >= 1: 
        for word in found_tease_indicators:
#             print(word) # check
            for i,line in enumerate(script):
                if(word in line):
#                     print(str(word) + str(i)) # check
    #               print("this word: " + word + " was at index: " + str(i)) #check
                    if i >= earliest_indicator:
    #                   print("Not earliest indicator") # check
                        del found_tease_indicators[0]
                        break
                    else:
                        earliest_indicator = i  
                        break
        else:
            title_page = script[:earliest_indicator]
    title = find_title(title_page)
    screenwriter = find_writer(title_page)
    doctor = find_doctor(title_page)
    source_material = find_source_material(title_page)
    director = find_director(title_page)
    nominal_dict = {"show":title,"screenwriter":screenwriter,"script_doctor":doctor,"source":source_material,"director":director,"title_page":title_page}

#         print(nominal_dict)
    return nominal_dict
    
def cull_cover_page(screenplays):
    nominal_dicts = []
    for index in range(len(screenplays)):
#         print(index)
        each_script = screenplays[index]
        nominal_dict = clip_title_page(each_script)        
        nominal_dicts.append(nominal_dict)
#     print(nominal_dicts)
    return nominal_dicts