import psutil
from pynput import keyboard 
from functools import partial
import json
import sys
import os 
import time


stored_shortcuts = {}

default_shortcuts = {
    '<ctrl>+<shift>+<alt>+e': lambda: key_listener.stop() # shortcut to stop key listener
    } 

running_processes = []


# kill all processes from given list
def process_kill(selected_processes):
    os.system('clear||cls')
    for process in psutil.process_iter():
        try:
            if process.name() in selected_processes:
                process.kill() 
                print(f'The process "{process.name()}" (PID: {process.pid}) was killed.') 
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    print()
    shortcuts_print(stored_shortcuts) 
    print('\nPress "<Ctrl> + <Shift> + <Alt> + E" to enter the editor.') 


# assign shortcut
def shortcut_assign(selected_hotkey, selected_processes):
    stored_shortcuts[selected_hotkey] = partial(process_kill, selected_processes) # partial used to not call the function immediately and to store its arguments


# remove shortcut
def shortcut_remove(selected_hotkey):
    del stored_shortcuts[selected_hotkey]


# list all running processes
def processes_list():
    processes_list = []
    for process in psutil.process_iter():
        processes_list.append(process.name())
    processes_list = list(dict.fromkeys(processes_list))
    processes_list.sort()
    print('\nCurrently running processes:')
    for i, item in enumerate(processes_list, start=1):
        print(f'{i}. {item}')
    return(processes_list) 


# check if hotkey is valid
def validate_hotkey(hotkey):
    try:
        keyboard.GlobalHotKeys({hotkey: lambda: None})
        return True
    except:
        os.system('clear||cls')
        print(f'The hotkey "{hotkey}" is invalid! Try Again!\n')
        return False
    

# print current shortcuts
def shortcuts_print(stored_shortcuts):
    if len(stored_shortcuts) != 0:
        print('Current shortcuts:')
        stored_shortcuts_list = list(stored_shortcuts)
        for i, item in enumerate(stored_shortcuts_list, start=1):
            print(f'{i}. {item}: {stored_shortcuts[item].args[0]}')
        return stored_shortcuts_list
    return {}


# confirm input
def input_confirm(prompt):
    while True:
        input_check = input(prompt) 
        if input_check == 'Y' or input_check == 'y':
            return 1
        elif input_check == 'N' or input_check == 'n':
            return 0
        else:
            os.system('clear||cls')
            print('Invalid input! Try again!\n')


# turn input string to list of strings (no check for int here)
def input_to_numbers(input):
    input_numbers = [] 
    current_number = '' 
    for character in input: 
        if character == ' ': 
            pass
        elif character == ',': 
            input_numbers.append(current_number) 
            current_number = '' 
        else:
            current_number += character 
    if current_number != '':
        input_numbers.append(current_number)
    return input_numbers


# get a shortcut from input and assign it
def input_shortcut_assign():

    # select processes
    selected_processes = []
    os.system('clear||cls') 
    while True:
        if selected_processes != []: #
            print('Selected processes:')
            for i, item in enumerate(selected_processes, start=1): 
                print(f'{i}. {item}')  
            print('')
        input_assign_mode = input('Enter "m" for manual or "s" for search mode, blank to continue: ') 
        if input_assign_mode == '': 
            os.system('clear||cls')
            break
        
        # search mode
        elif input_assign_mode == 's' or input_assign_mode == 'S':
            os.system('clear||cls') 
            running_processes = processes_list() 
            while True:
                found_processes = [] 
                input_process_search = input('\nEnter process name to search (case-insensitive), blank to continue: ') 
                if input_process_search == '': 
                    os.system('clear||cls')
                    break
                for item in running_processes:
                    if input_process_search.lower() in item.lower(): 
                        found_processes.append(item) 
                if found_processes == []: 
                    os.system('clear||cls')
                    processes_list()
                    print(f'\nNo process containing the phrase "{input_process_search}" was found!')
                    continue
                else: # successful search
                    os.system('clear||cls')
                    while True:
                        print('Found processes:')
                        for i, item in enumerate(found_processes, start=1):
                            print(f'{i}. {item}') 
                        input_process = input('\nEnter process numbers to select (separated by commas), blank to continue: ') 
                        if input_process == '': 
                            break
                        input_numbers = input_to_numbers(input_process)
                        os.system('clear||cls')                               
                        for input_number in input_numbers:
                            try:
                                input_number = int(input_number)
                            except ValueError:
                                print(f'Invalid input "{input_number}"! Try again!\n')
                                continue
                            if input_number < 1 or input_number > len(found_processes):
                                print(f'There is no process with number "{input_number}"!\n')
                            elif found_processes[input_number - 1] in selected_processes: 
                                print(f'Process "{found_processes[input_number - 1]}" is already selected.\n')
                            else: 
                                selected_processes.append(found_processes[input_number - 1])
                                print(f'Process "{found_processes[input_number - 1]}" was selected.\n')   
                    os.system('clear||cls')
                    break                          

        # manual mode
        elif input_assign_mode == 'm' or input_assign_mode == 'M':
            os.system('clear||cls') 
            running_processes = processes_list() 
            while True:
                input_process = input('\nEnter process numbers to select (separated by commas), blank to continue: ')
                if input_process == '':
                    os.system('clear||cls')
                    break
                input_numbers = input_to_numbers(input_process)
                os.system('clear||cls')
                processes_list()
                for input_number in input_numbers:
                    try: 
                        input_number = int(input_number) 
                    except ValueError:
                        print(f'\nInvalid input "{input_number}"! Try again!')
                        continue
                    if input_number < 1 or input_number > len(running_processes): 
                        print(f'\nThere is no process with number "{input_number}"!')
                    elif running_processes[input_number - 1] in selected_processes: 
                        print(f'\nProcess "{running_processes[input_number - 1]}" is already selected.')
                    else: 
                        selected_processes.append(running_processes[input_number - 1])
                        print(f'\nProcess "{running_processes[input_number - 1]}" was selected.')
        
        else:
            os.system('clear||cls')
            print('Invalid input! Try again!')

    # input and assign shortcut
    if selected_processes != []: 
        os.system('clear||cls') 
        while True:
            shortcuts_print(stored_shortcuts) 
            if stored_shortcuts != {}:
                print('')
            input_hotkey = input(f'Enter hotkey which will be assigned to kill {str(selected_processes)[1:-1]} (blank to cancel): ') 
            if input_hotkey == '':
                break
            elif validate_hotkey(input_hotkey):
                os.system('clear||cls')
                if input_confirm(f'You want to assign "{input_hotkey}" to kill {str(selected_processes)[1:-1]}, correct? (Y/N): '): 
                    shortcut_assign(input_hotkey, selected_processes) 
                    os.system('clear||cls')
                    print(f'Hotkey "{input_hotkey}" was assigned to kill {str(selected_processes)[1:-1]}.\n')
                    break
                os.system('clear||cls')


# get shortcut from input and remove it
def input_shortcut_remove():
    while True:
        if len(stored_shortcuts) == 0: 
            print('There are no assigned shortcuts to remove!\n')
            break
        stored_shortcuts_list = shortcuts_print(stored_shortcuts)
        input_shortcut = input('\nChoose which shortcut to remove, blank to exit: ')
        if input_shortcut == '': 
            os.system('clear||cls')
            break
        try: 
            input_shortcut = int(input_shortcut) 
        except ValueError:
            os.system('clear||cls')
            print('Invalid input! Try again!\n')
            continue
        if input_shortcut < 1 or input_shortcut > len(stored_shortcuts_list): 
            os.system('clear||cls')
            print(f'There is no shortcut with number "{input_shortcut}"!\n')
        else:
            os.system('clear||cls')
            removed_shortcut = f'{stored_shortcuts_list[input_shortcut - 1]}: {stored_shortcuts[stored_shortcuts_list[input_shortcut - 1]].args[0]}'
            if input_confirm(f'You want to remove the shortcut "{removed_shortcut}", correct? (Y/N): '): 
                shortcut_remove(stored_shortcuts_list[input_shortcut - 1])
                os.system('clear||cls')
                print(f'Shortcut "{removed_shortcut}" was removed.\n')
                break
            os.system('clear||cls')


# import shortcuts from json file
def import_shortcuts():
    try:
        with open('stored_shortcuts.json', 'r') as file: 
            imported_shortcuts = json.load(file) 
    except:
        return {}
    
    for item in imported_shortcuts:
        imported_shortcuts[item] = partial(process_kill, imported_shortcuts[item]) 

    return imported_shortcuts


# export shortcuts to json file
def export_shortcuts(stored_shortcuts):
    if export_shortcuts == {}:
        with open('stored_shortcuts.json', 'w') as file: 
            json.dump({}, file)   
    
    else:
        exported_shortcuts = stored_shortcuts.copy()
    
        for item in exported_shortcuts:
            exported_shortcuts[item] = exported_shortcuts[item].args[0]

        with open('stored_shortcuts.json', 'w') as file: 
            json.dump(exported_shortcuts, file, indent=4)


# exit program
def program_exit(prompt):
    export_shortcuts(stored_shortcuts) 
    os.system('clear||cls')
    print(prompt) 
    sys.exit() 


# shortcut editor
def enter_editor():
    try:
        os.system('clear||cls') 
        while True:

            shortcuts_print(stored_shortcuts) 
            if stored_shortcuts != {}:
                print('')
            
            input_action = input('Welcome to the Editor. Enter one of the following commands:\n' + 
                                '- "assign" or "a" to assign new shortcut\n' +
                                '- "remove" or "r" to remove existing shortcut\n' +
                                '- "continue" or "c" to close the editor\n' +
                                '- "exit" or "e" to exit the program\n') 
            
            os.system('clear||cls') 

            if input_action == 'assign' or input_action == 'a':
                input_shortcut_assign()
            elif input_action == 'remove' or input_action == 'r':
                input_shortcut_remove()
            elif input_action == 'continue' or input_action == 'c':
                print('Closing the editor. Shortcuts are active again!\n')
                return
            elif input_action == 'exit' or input_action == 'e':
                program_exit('Exiting...\n') 
            else:
                os.system('clear||cls')
                print('Invalid input! Try again!\n')
                
    
    except KeyboardInterrupt: 
        program_exit('Exiting via Keyboard Interrupt...\n') 




# 'main' function
stored_shortcuts = import_shortcuts() 

os.system('clear||cls')

while True:
    shortcuts_print(stored_shortcuts) 

    if stored_shortcuts != {}:
        print('')

    print('Press "<Ctrl> + <Shift> + <Alt> + E" to enter the editor.') 

    all_shortcuts = stored_shortcuts | default_shortcuts 
    key_listener = keyboard.GlobalHotKeys(all_shortcuts)
    key_listener.start()

    try:
        while key_listener.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        key_listener.stop()
        program_exit('Exiting via Keyboard Interrupt...\n')

    enter_editor() # enter the editor when key listener stops
