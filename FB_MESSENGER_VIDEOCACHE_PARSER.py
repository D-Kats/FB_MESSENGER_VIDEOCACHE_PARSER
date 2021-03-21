# DKats 2021 
#
#---Thanks to---
# PySimpleGUI module from  MikeTheWatchGuy at https://pypi.org/project/PySimpleGUI/
# executable's icon downloaded from www.freeiconspng.com
import PySimpleGUI as sg
import json
import sqlite3
import datetime
from datetime import timezone, datetime
import os
import webbrowser
import shutil
import ffmpeg



#---functions definition
def concatVidAudFile(copiedFilesFolder, currentVidID, vidNum):	
	videoFileList = []
	fileDict = {} # gia na sortarw ta files kai na ginei swsta to concat me th seira pou prepei
	vidFoundFlag = False

	if vidNum != 4:
		for file in os.listdir(copiedFilesFolder):		
			if file.startswith(f'{currentVidID}.null.{vidNum}'):
				vidFoundFlag = True			
				fpos = file.find('mp4.')+4   #!!!!!!!!!!!!!! pi8ano provlima ston kwdika an den einai mp4 ta arxeia exo kai den periexoun to mp4. sto onoma tous
				fileDict[file] = int(file[fpos:file.find('.',fpos)])
		
		if vidFoundFlag:
			sDict = dict(sorted(fileDict.items(), key=lambda item: item[1]))
			# print(sDict)
			sList = list(sDict.keys())
			# print(sList)

			shutil.copy(f'{copiedFilesFolder}\\{sList[0]}', f'{copiedFilesFolder}\\vid{vidNum}_{currentVidID}_final.mp4')
			for i in range(1,len(sList)):
				with open(f'{copiedFilesFolder}\\vid{vidNum}_{currentVidID}_final.mp4', 'ab') as inp, open(f'{copiedFilesFolder}\\{sList[i]}', 'rb') as out:
					inp.write(out.read())
			return f'{copiedFilesFolder}\\vid{vidNum}_{currentVidID}_final.mp4'
		else:
			return f'not found'
	else: # creating the audio
		for file in os.listdir(copiedFilesFolder):		
			if file.startswith(f'{currentVidID}.null.4'):
				vidFoundFlag = True			
				fpos = file.find('mp4.')+4
				fileDict[file] = int(file[fpos:file.find('.',fpos)])
		
		if vidFoundFlag:
			sDict = dict(sorted(fileDict.items(), key=lambda item: item[1]))
			# print(sDict)
			sList = list(sDict.keys())
			# print(sList)

			shutil.copy(f'{copiedFilesFolder}\\{sList[0]}', f'{copiedFilesFolder}\\aud_{currentVidID}_final.mp4')
			for i in range(1,len(sList)):
				with open(f'{copiedFilesFolder}\\aud_{currentVidID}_final.mp4', 'ab') as inp, open(f'{copiedFilesFolder}\\{sList[i]}', 'rb') as out:
					inp.write(out.read())
			return f'{copiedFilesFolder}\\aud_{currentVidID}_final.mp4'
		else:
			return f'not found'


def ffmpegFinalConcat(currentVidID, vid, aud, copiedFilesFolder, vidNum):
	in1 = ffmpeg.input(vid)
	in2 = ffmpeg.input(aud)
	out = ffmpeg.output(in1, in2, f'{copiedFilesFolder}\\output_{currentVidID}_{vidNum}.mkv')
	try:
		out.run()
		return f'output_{currentVidID}_{vidNum}.mkv'
	except Exception as e:
		print('!!!!!!!!!!!!!!!!!!!!!!!!!')
		print(f'ffmpeg conversion for vid {vidNum} of video with ID: {currentVidID} failed')
		print(e)
		return 'video conversion failed'

#---menu definition
menu_def = [['File', ['Exit']],
			['Help', ['Documentation', 'About']],] 
#---layout definition
DBFrameLayout = [[sg.Text('Choose the threads_db2 database file to parse', background_color='#2a363b')],
					[sg.In(key='-DB-', readonly=True, background_color='#334147'), sg.FileBrowse(file_types=(('Database', '*.sqlite'),('Database', '*.db'), ('All files', '*.*')))],
					[sg.Text('Choose the videocache folder to parse', background_color='#2a363b')],
					[sg.In(key='-CACHE-', readonly=True, background_color='#334147'), sg.FolderBrowse()]]

OutputSaveFrameLayout = [[sg.Text('Choose folder to save the html report file', background_color='#2a363b')],
					[sg.In(key='-OUTPUT-', readonly=True, background_color='#334147'), sg.FolderBrowse()]] #key='-SAVEBTN-', disabled=True, enable_events=True

col_layout = [[sg.Frame('Input DB File and Videocache Folder', DBFrameLayout, background_color='#2a363b', pad=((0,0),(0,65)))],
				# [sg.Frame('Keywords (Optional - only for Documents)', KeywordsFrameLayout, background_color='#2a363b', pad=((0,0),(0,65))) ],				
				[sg.Frame('Output Folder', OutputSaveFrameLayout, background_color='#2a363b')],				
				[sg.Button('Exit', size=(7,1)), sg.Button('Parse', size=(7,1))]]

#---GUI Definition
layout = [[sg.Menu(menu_def, key='-MENUBAR-')],
			[sg.Column(col_layout, element_justification='c',background_color='#2a363b'), sg.Frame('Output Console',
			[[sg.Output(size=(50,25), key='-OUT-', background_color='#334147', text_color='#fefbd8')]], background_color='#2a363b')],
			[sg.Text('FB Messenger VideoCache Parser Ver. 1.0.1', background_color='#2a363b', text_color='#b2c2bf')]]

window = sg.Window('FB Messenger VideoCache Parser', layout, background_color='#2a363b') 

#---run
while True:
	event, values = window.read()
	# print(event, values)
	if event in (sg.WIN_CLOSED, 'Exit'):
		break
#---menu events
	if event == 'Documentation':
		try:
			webbrowser.open_new('https://github.com/D-Kats/FB_MESSENGER_VIDEOCACHE_PARSER/blob/main/README.md')
		except:
			sg.PopupOK('Visit https://github.com/D-Kats/FB_MESSENGER_VIDEOCACHE_PARSER/blob/main/README.md for documentation', title='Documentation', background_color='#2a363b')
	if event == 'About':
		sg.PopupOK('FB Messenger VideoCache Parser Ver. 1.0.1 \n\n --DKats 2021', title='-About-', background_color='#2a363b')
	
#---buttons events
	if event == "Parse":
		if values['-DB-'] == '': # den exei epileksei db gia analysh
			sg.PopupOK('Please choose the threads_db2 database to parse!', title='!', background_color='#2a363b')
		elif values['-CACHE-'] == '': # den exei epileksei db gia analysh
			sg.PopupOK('Please choose the videocache folder to parse!', title='!', background_color='#2a363b')
		elif values['-OUTPUT-'] == '': #den exei epileksei fakelo gia output			
			sg.PopupOK('Please choose a folder to save the html report to!', title='!', background_color='#2a363b')
		else:
			now = datetime.now()
			currentLocalTime = now.strftime("%H:%M:%S")
			print(f'Script started executing at {currentLocalTime}')
			print('Initializing...')
			try: #catching db connection error 
				db = values['-DB-']
				conn = sqlite3.connect(db)
				c = conn.cursor()
				c.execute("SELECT _id, timestamp_ms, sender, attachments FROM messages")
				data = c.fetchall()														
			except Exception as e: #db conn error
				print('!!!!!!!!!!!!!!!!!!!!!!!!!')
				print(f'ERROR: {e}')
				sg.PopupOK('Error connecting to the database!\nCheck Output Console for more details', title='!', background_color='#2a363b')
			else: #db connected successfully
				print('Database connection successful')
				outputFolder = values['-OUTPUT-']
				inputFolder = values['-CACHE-']
				# try except else block for exo files copying
				try: #trying to copy exo files to my report files folder
					print('creating html report/files folder in output folder')
					os.makedirs(f'{outputFolder}\\report\\files')
					copiedFilesFolder = f'{outputFolder}\\report\\files'
					print('copying exo files to html report files folder')

					# copy sygkentrwtika ola ta arxeia sto files gia na kanw ta concat
					for root, folders, files in os.walk(inputFolder): 						
						for file in files:				
							rootAbsPath = os.path.abspath(root)								
							shutil.copy(os.path.join(rootAbsPath, file), f'{copiedFilesFolder}\\{file}')
					print('copying exo files to html report files folder finished successfully')
				except Exception as e: #exo copying error
					print('!!!!!!!!!!!!!!!!!!!!!!!!!')
					print(f'ERROR: {e}')
					sg.PopupOK('Error copying exo files to output folder!\nCheck output folder permission and\n Output Console for more details', title='!', background_color='#2a363b')
				else: #exo files copied successfully, main parsing begins
					print('main parsing begins')							
					
					
					#----html string
					html_code ='''<!DOCTYPE html>
					<html>
					<head>
					<meta charset="utf-8" />
					<title> Report </title>
					<meta name="viewport" content="width=device-width, initial-scale=1">
					<link rel="stylesheet" type="text/css" media="screen" href="style.css" />
					</head>
					<body>
					<div class="wrapper">
					<div class="header">                        
					<H1> Report </H1>
					</div>'''

					html_code += '\n<table align="center"> \n <caption><h2><b>Facebook Messenger Videos</b></h2></caption>'
					html_code += '\n<tr style="background-color:DarkGrey"> \n <th>Database RecordID</th> \n <th>Video Send Timestamp (UTC)</th> \n <th>Sender Facebook ID</th> \n <th>Sender Facebook Name</th> \n <th>Video</th>'
					try: #trying to catch any json errors
						for row in data:
							if row[3] != None:
								attachmentString = row[3]
								attachmentJson = json.loads(attachmentString)
								if 'video' in attachmentJson[0]['mime_type']: #giati perikleietai apo [] sth vash to json opote mou to kanei lista h python
									currentVidID = attachmentJson[0]['id'] 	
									print(f'concatenating exo files for ID:{currentVidID} video')
									currentVideo1 = concatVidAudFile(copiedFilesFolder, currentVidID, 1)
									currentVideo2 = concatVidAudFile(copiedFilesFolder, currentVidID, 2)
									currentVideo3 = concatVidAudFile(copiedFilesFolder, currentVidID, 3)
									currentAudio = concatVidAudFile(copiedFilesFolder, currentVidID, 4)
									#html rest of info
									timestamp = datetime.fromtimestamp(row[1]/1000, tz=timezone.utc)
									senderString = row[2]
									senderJson = json.loads(senderString)						
									FB_id = senderJson['user_key'][senderJson['user_key'].find(':')+1:]
									FB_name = senderJson['name']

									if currentVideo1 == 'not found' and currentVideo2 == 'not found' and currentVideo3 == 'not found' and currentAudio == 'not found':
										print(f'Video with ID:{currentVidID} not found on videocache folder')
										html_code += f'\n<tr> \n <td>{row[0]}</td> \n <td>{timestamp}</td> \n <td>{FB_id}</td> \n <td>{FB_name}</td> \n<td> video not found in videocache folder</td>'
									else:
										print(f'Fragments for video with ID:{currentVidID} found. FFmpeg conversion commencing')
										html_code += f'\n<tr> \n <td>{row[0]}</td> \n <td>{timestamp}</td> \n <td>{FB_id}</td> \n <td>{FB_name}</td> \n<td>'
										if currentVideo1 != 'not found':
											html_vidName = ffmpegFinalConcat(currentVidID, currentVideo1, currentAudio, copiedFilesFolder, 1)
											if html_vidName != 'video conversion failed':
												html_code +=f' <a href=".\\files\\{html_vidName}">video </a>'
											else:
												html_code += 'video conversion failed '
										if currentVideo2 != 'not found':
											html_vidName = ffmpegFinalConcat(currentVidID, currentVideo2, currentAudio, copiedFilesFolder, 2)
											if html_vidName != 'video conversion failed':
												html_code +=f' <a href=".\\files\\{html_vidName}">video </a>'
											else:
												html_code += 'video conversion failed '
										if currentVideo3 != 'not found':
											html_vidName = ffmpegFinalConcat(currentVidID, currentVideo3, currentAudio, copiedFilesFolder, 3)
											if html_vidName != 'video conversion failed':
												html_code +=f' <a href=".\\files\\{html_vidName}">video </a>'
											else:
												html_code += 'video conversion failed '
										html_code += '</td>'
						print('main parsing completed!')
						html_code += '\n</table> \n<br> \n<div class="push"></div> \n</div> \n <div class="footer">--DEE 7o</div>\n</body>\n</html>'

						css_code = '''table{border-collapse:collapse;}
						th{text-align:center;background-color:#4a4343;color=white;}
						table,th,td{border:1px solid #000;}
						tr{text-align:center;background-color:#595555; color:white;}

						html, body {
						height: 100%;
						margin: 0;
						}

						.wrapper {
						min-height: 100%;
						background-color: #4a4349;
						/* Equal to height of footer */
						/* But also accounting for potential margin-bottom of last child */
						margin-bottom: -50px;
						font-family: "Courier New", sans-serif;
						color=white;

						}

						.header{
						background-color: dark grey;
						color=white;
						}
						.header h1 {
						text-align: center;
						font-family: "Courier New", sans-serif;
						color=red;
						}
						.push {
						height: 50px;
						background-color: #4a4349;
						}
						.footer {
						height: 50px;
						background-color: #4a4349;
						color=white;
						text-align: right;
						}		'''

						print('deleting exo files from output folder...')
						for file in os.listdir(copiedFilesFolder):
							if file.startswith('output_'):
								continue
							os.remove(f'{copiedFilesFolder}\\{file}')
						print('exo files deleted!')

						#----reporting
						reportFolder = f'{outputFolder}\\report'

						print('creating HTML report!')
						with open(f'{reportFolder}\\report.html', 'w', encoding='utf8') as fout:
							fout.write(html_code)

						with open(f'{reportFolder}\\style.css', 'w', encoding= 'utf8') as cssout:
						            cssout.write(css_code)
						print('HTML report created successfully')

						now = datetime.now()
						currentLocalTime = now.strftime("%H:%M:%S")
						print(f'Script finished executing at {currentLocalTime}')
						with open(f'{reportFolder}\\FB_MESSENGER_VIDEOCACHE_PARSER.log', 'w', encoding='utf-8') as Logfout:						
							Logfout.write(window['-OUT-'].Get())
							print('Log file was created successfully!')
						
						
						sg.PopupOK(f'Parsing completed!\nHTML report created successfully at {reportFolder}.', title=': )', background_color='#2a363b')

					except Exception as e: #possible json error
						print('!!!!!!!!!!!!!!!!!!!!!!!!!')
						print(f'ERROR: {e}')
						sg.PopupOK('Error during main parsing!\nCheck Output Console for more details', title='!', background_color='#2a363b')

	
window.close()
