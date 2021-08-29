import PySimpleGUI as sg
from shutil import move
from os import listdir
from os.path import isfile, join, isdir, splitext, abspath
from tkinter import messagebox

def updateFileList():
  fnames = [
        f
        for f in files
        if isfile(join(to_move_folder_path, f))
    ]
  window['scanned_files_list'].update(fnames)

def moveApplicableFiles():
  for filename in files:
    # check if the patient has a folder in the destination folder and if a file of the same name doesn't already exist in the patient's folder. if true, move the file ()

    # splitext removes the .<ext> and split separates the file name on spaces; both return an array
    patient_folder_path = join(organize_in_folder_path, splitext(filename)[0].split()[0])
    potential_file_in_dest_path = join(patient_folder_path, filename)
    file_to_be_moved_path = join(to_move_folder_path, filename)

    if isdir(patient_folder_path) and not isfile(potential_file_in_dest_path):
      move(file_to_be_moved_path, patient_folder_path)
      print('moved', file_to_be_moved_path, 'to', patient_folder_path)

# create GUI layout
layout = [[sg.Text('Scanned Files Folder'),
        sg.In('Source', size=(23, 1), enable_events=True, key='scanned_files_directory'),sg.FolderBrowse()], 
        [sg.Listbox( values=[], enable_events=True, size=(40, 15), key='scanned_files_list')],
        [sg.Text('Folder of Patient Folders'),
        sg.In('Destination', size=(20, 1), enable_events=True, key='patient_folders_directory'),sg.FolderBrowse()],
        [sg.Button('Organize away!', button_color=(sg.theme_background_color()), font=('Courier', 13))]]

# create the window
window = sg.Window('File Organizer', layout)

# create an event loop
while True:
  event, values = window.read()
  # End program if user closes window
  if event == sg.WIN_CLOSED:
    break
  if event == 'scanned_files_directory':
    # get folder path
    to_move_folder_path = values['scanned_files_directory']
    print('Scanned Files Folder Path: ', to_move_folder_path)
    try:
        # Get list of files in folder
        files = listdir(to_move_folder_path)
        print('File Names:', files)
    except:
        files = []
    updateFileList() # update the file list box
  elif event == 'patient_folders_directory':
    # get folder path
    organize_in_folder_path = values['patient_folders_directory']
    print('Folder of Patient Folder Path: ', organize_in_folder_path)
  elif event == 'Organize away!':
    # move files to correct destination
    try:
      moveApplicableFiles() # moves files while avoiding duplicates
      updateFileList() # update the file list box
      # alert if files weren't moved
      if (len(listdir(to_move_folder_path)) > 0):
        messagebox.showinfo('Head\'s up!', str(len([f for f in listdir(to_move_folder_path) if isfile(join(to_move_folder_path, f))])) + ' files could not be moved. You can view unmoved files in the file list box. They may not have been moved because duplicates exist in their destination folder, the patient\'s folder hasn\'t been created yet, or the file was incorrectly named.')
      else:
        messagebox.showinfo('Success!', 'All files were able to be moved! You may close the program!')
    except:
      messagebox.showwarning('Oops!', 'Something may have went wrong. Contact the developer for help.')          

window.close()