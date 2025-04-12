import psutil # for process tasks
from pynput import keyboard # for keyboard shortcuts
from functools import partial # to store function arguments
import json # to store shortcuts
import sys # to close the program
import os # to clear the terminal

# dictionary that stores all global shortcuts, retrieved from json file
stored_shortcuts = {}

# dictionary that stores all default shortcuts
default_shortcuts = {
    '<ctrl>+<shift>+<alt>+e': lambda: h.stop() # add a shortcut to stop key listener
    } 

# array for storing currently running processes
running_processes = []


# kills all the processes from the given list
def process_kill(selected_processes):
    for process in psutil.process_iter(): # goes through all running processes
        try:
            if process.name() in selected_processes: # checks if current process is in the list of stored processes
                process.kill() # kills the process
                print(f'The process "{process.name()}" (PID: {process.pid}) was killed.') # prints out which process has been killed
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

# assign shortcut
def shortcut_assign(selected_hotkey, selected_processes):
    stored_shortcuts[selected_hotkey] = partial(process_kill, selected_processes) # partial used to not call the function immediately and to store its arguments


# remove shortcut
def shortcut_remove(selected_hotkey):
    del stored_shortcuts[selected_hotkey]


# list all running processes
def processes_list():
    processes_list = [] # empty list to store
    for process in psutil.process_iter(): # goes through all running processes
        processes_list.append(process.name()) # adds each of them to the list
    processes_list = list(dict.fromkeys(processes_list)) # removes duplicates
    processes_list.sort() # sorts the list
    print('\nCurrently running processes:')
    for i, item in enumerate(processes_list, start=1): # goes through the list to add indexes to the output
        print(f'{i}. {item}') # prints the list of running processes
    return(processes_list) # returns list of all running processes

# check if hotkey is a valid
def validate_hotkey(hotkey):
    try:
        keyboard.GlobalHotKeys({hotkey: None}) # try to create a dummy global hotkey
        return True
    except:
        print(f'The hotkey "{hotkey}" is invalid! Try Again!')
        return False
    

# print current shortcuts
def shortcuts_print(stored_shortcuts):
    if len(stored_shortcuts) != 0: # check if there is at least one existing shortcut
        print('\nCurrent shortcuts:')
        stored_shortcuts_list = list(stored_shortcuts) # create a list of all assigned hotkeys
        for i, item in enumerate(stored_shortcuts_list, start=1): # goes through the list to add indexes to the output
            print(f"{i}. {item}: {stored_shortcuts[item].args[0]}") # prints the list of all shortcuts
        return stored_shortcuts_list


# confirm input
def input_confirm(prompt):
    while True: # confirmation loop
        input_check = input(prompt) 
        if input_check == 'Y' or input_check == 'y':
            return 1
        elif input_check == 'N' or input_check == 'n':
            print('Cancelling.')
            return 0
        else:
            print('Invalid input! Try again!')


# get a shortcut from input and assign it
def input_shortcut_assign():
    # select the processes
    selected_processes = [] # empty array to store selected processes
    while True:
        if selected_processes != []: # if selected processes not empty
            print('\nSelected processes:')
            for i, item in enumerate(selected_processes, start=1): # goes through the list to add indexes to the output
                print(f'{i}. {item}')  # print all selected processes
        input_assign_mode = input('\nEnter "m" for manual or "s" for search mode, blank to continue: ') # get process input
        if input_assign_mode == '': # if blank continue with hotkey input
            break
        
        # search mode
        elif input_assign_mode == 's' or input_assign_mode == 'S':
            os.system('clear||cls') # to clear the terminal
            running_processes = processes_list() # print all running processes and save them
            while True:
                found_processes = [] # dictionary to store found processes
                input_process_search = input('\nEnter process name to search (case-insensitive), blank to continue: ') # search phrase from input
                if input_process_search == '': # if blank exit search mode
                    break
                print('\nFound processes:')
                for item in running_processes:
                    if input_process_search.lower() in item.lower(): # search for processes
                        found_processes.append(item) # add process to found list if found
                if found_processes == []: # check if nothing found
                    print(f'No process containing the phrase "{input_process_search}" was found!')
                    continue
                else: # if successful search
                    for i, item in enumerate(found_processes, start=1): # goes through the list to add indexes to the output
                        print(f'{i}. {item}')  # print all found processes
                    while True:
                        input_process = input('\nEnter process number to add it to selected, blank to continue: ') # get process input
                        if input_process == '': # if blank continue to next search
                            break
                        try: # error handling
                            input_process = int(input_process) # input from str to int
                        except ValueError:
                            print('Invalid input! Try again!')
                            continue
                        if input_process < 1 or input_process > len(found_processes): # check if selected process is within range of all found processes
                            print(f'There is no process with number "{input_process}"!')
                        elif found_processes[input_process - 1] in selected_processes: # check if process is already selected
                            print(f'Process "{found_processes[input_process - 1]}" is already selected.')
                        else: # otherwise add process to list of selected
                            selected_processes.append(found_processes[input_process - 1])
                            print(f'Process "{found_processes[input_process - 1]}" was selected.')                    

        # manual mode
        elif input_assign_mode == 'm' or input_assign_mode == 'M':
            os.system('clear||cls') # to clear the terminal
            running_processes = processes_list() # print all running processes and save them
            while True:
                input_process = input('\nEnter process number to add it to selected, blank to continue: ')
                if input_process == '': # if blank exit manual mode
                    break
                try: # error handling
                    input_process = int(input_process) # input from str to int
                except ValueError:
                    print('Invalid input! Try again!')
                    continue
                if input_process < 1 or input_process > len(running_processes): # check if selected process is within range of all running processes
                    print(f'There is no process with number "{input_process}"!')
                elif running_processes[input_process - 1] in selected_processes: # check if process is already selected
                    print(f'Process "{running_processes[input_process - 1]}" is already selected.')
                else: # otherwise add process to list of selected
                    selected_processes.append(running_processes[input_process - 1])
                    print(f'Process "{running_processes[input_process - 1]}" was selected.')
        
        else:
            print('Invalid input! Try again!')

    # enter and assign the shortcut
    if selected_processes != []: # checks if at least one process was selected
        os.system('clear||cls') # to clear the terminal
        while True:
            shortcuts_print(stored_shortcuts) # print all current shortcuts
            input_hotkey = input(f'\nEnter hotkey which will be assigned to kill {str(selected_processes)[1:-1]}, blank to cancel (default shortcuts will not be overwritten): ') # get hotkey from input
            if input_hotkey == '': # if blank exit
                break
            elif validate_hotkey(input_hotkey): # check if valid hotkey
                if input_confirm(f'You want to assign "{input_hotkey}" to kill {str(selected_processes)[1:-1]}, correct? (Y/N): '): # input confirm
                    shortcut_assign(input_hotkey, selected_processes) # assign shortcut
                    break


# get a shortcut from input and remove it
def input_shortcut_remove():
    while True:
        if len(stored_shortcuts) == 0: # check if there is at least one shortcut
            print('There are no assigned shortcuts to remove!')
            break
        stored_shortcuts_list = shortcuts_print(stored_shortcuts) # print all current shortcuts
        input_shortcut = input('\nChoose which shortcut to remove, blank to exit: ')
        if input_shortcut == '': # if blank input exits the remove function
            break
        try: # error handling
            input_shortcut = int(input_shortcut) # input from str to int
        except ValueError:
            print('Invalid input! Try again!')
            continue
        if input_shortcut < 1 or input_shortcut > len(stored_shortcuts_list): # check if selected shortcut is not within range of all assigned shortcuts
            print(f'There is no shortcut with number "{input_shortcut}"!')
        else: # otherwise removes the shortcut
            if input_confirm(f'You want to remove the shortcut "{stored_shortcuts_list[input_shortcut - 1]}: {stored_shortcuts[stored_shortcuts_list[input_shortcut - 1]].args[0]}", correct? (Y/N): '): # input confirm
                shortcut_remove(stored_shortcuts_list[input_shortcut - 1])
                break


# import shortcuts from json file
def import_shortcuts():
    try:
        with open('stored_shortcuts.json', 'r') as file: # retrieve shortcuts from json file
            imported_shortcuts = json.load(file) 
    except:
        return {}
    
    for item in imported_shortcuts:
        imported_shortcuts[item] = partial(process_kill, imported_shortcuts[item]) # change imported shortcuts to correct format

    return imported_shortcuts


# export shortcuts to json file
def export_shortcuts(stored_shortcuts):
    exported_shortcuts = stored_shortcuts.copy() # copy dictonary
    
    for item in exported_shortcuts:
        exported_shortcuts[item] = exported_shortcuts[item].args[0] # save only arguments (processes) for each shortcut

    with open('stored_shortcuts.json', 'w') as file: # write shortcuts to json
        json.dump(exported_shortcuts, file)


# to exit the program
def programm_exit(prompt):
    if len(stored_shortcuts) != 0:
        export_shortcuts(stored_shortcuts) # save shortcuts to json file
    os.system('clear||cls') # to clear the terminal
    print(prompt) # print the exit prompt
    sys.exit() # closes the program


# shortcut editor
def enter_editor():
    try:
        while True:
            os.system('clear||cls') # to clear the terminal
            
            shortcuts_print(stored_shortcuts) # print all current shortcuts
            
            # get command from input
            input_action = input('\nWelcome to the Editor. Enter one of the following commands:\n' + 
                                '- "assign" or "a" to assign new shortcut\n' +
                                '- "remove" or "r" to remove existing shortcut\n' +
                                '- "continue" or "c" to close the editor\n' +
                                '- "exit" or "e" to exit the program\n') 
            
            os.system('clear||cls') # to clear the terminal

            if input_action == 'assign' or input_action == 'a':
                input_shortcut_assign()
            elif input_action == 'remove' or input_action == 'r':
                input_shortcut_remove()
            elif input_action == 'continue' or input_action == 'c':
                print('Closing the editor. Shortcuts are active again!')
                return
            elif input_action == 'exit' or input_action == 'e':
                programm_exit('Exiting...') # exit the program
    
    except KeyboardInterrupt: # e.g. via Ctrl + C
        programm_exit('Exiting via Ctrl+C...') # exit the program





# main function
stored_shortcuts = import_shortcuts() # import shortcuts from json
while True:
    shortcuts_print(stored_shortcuts) # print current shortcuts

    print('\nPress "<Ctrl> + <Shift> + <Alt> + E" to enter the editor.') # info

    all_shortcuts = stored_shortcuts | default_shortcuts # merge stored and default shortcuts (default shortcuts have higher priority)
    try:
        with keyboard.GlobalHotKeys(all_shortcuts) as h: # run key listener with all assigned shortcuts
            h.join()
    except KeyboardInterrupt: # e.g. via Ctrl + C
        programm_exit('Exiting via Ctrl+C...') # exit the program
    
    enter_editor() # enter the editor when key listener stops