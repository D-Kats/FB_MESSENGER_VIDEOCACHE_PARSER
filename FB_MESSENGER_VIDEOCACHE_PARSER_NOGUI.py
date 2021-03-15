import os
import sqlite3
import json
import shutil
import ffmpeg
import datetime
from datetime import timezone


#----function definitions
def concatVidAudFile(copiedFilesFolder, currentVidID, vidNum):	
	videoFileList = []
	fileDict = {} # gia na sortarw ta files kai na ginei swsta to concat me th seira pou prepei
	vidFoundFlag = False

	if vidNum != 4:
		for file in os.listdir(copiedFilesFolder):		
			if file.startswith(f'{currentVidID}.null.{vidNum}'):
				vidFoundFlag = True			
				fpos = file.find('mp4.')+4
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
		return f'{copiedFilesFolder}\\output_{currentVidID}_{vidNum}.mkv'
	except Exception as e:
		print(e)
		return 'video conversion failed'	

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

#prepare files for parsing
# os.makedirs('report\\files')
copiedFilesFolder = os.path.abspath('report\\files')
#copy sygkentrwtika ola ta arxeia sto files
# for root, folders, files in os.walk('./ExoPlayerCacheDir'): #edw na valw to input folder sto GUI						
# 			for file in files:				
# 				rootAbsPath = os.path.abspath(root)								
# 				shutil.copy(os.path.join(rootAbsPath, file), f'C:\\Users\\mimakos\\Desktop\\Videocache\\report\\files\\{file}')



#db connection and query
conn = sqlite3.connect('threads_db2')
c = conn.cursor()
c.execute("SELECT _id, timestamp_ms, sender, attachments FROM messages")
data = c.fetchall()

#main data parsing
for row in data:
	if row[3] != None:
		attachmentString = row[3]
		attachmentJson = json.loads(attachmentString)
		if 'video' in attachmentJson[0]['mime_type']: #giati perikleietai apo [] sth vash to json opote mou to kanei lista h python
			currentVidID = attachmentJson[0]['id'] 	
			currentVideo1 = concatVidAudFile(copiedFilesFolder, currentVidID, 1)
			currentVideo2 = concatVidAudFile(copiedFilesFolder, currentVidID, 2)
			currentVideo3 = concatVidAudFile(copiedFilesFolder, currentVidID, 3)
			currentAudio = concatVidAudFile(copiedFilesFolder, currentVidID, 4)
			#html rest of info
			timestamp = datetime.datetime.fromtimestamp(row[1]/1000, tz=timezone.utc)
			senderString = row[2]
			senderJson = json.loads(senderString)						
			FB_id = senderJson['user_key'][senderJson['user_key'].find(':')+1:]
			FB_name = senderJson['name']

			if currentVideo1 == 'not found' and currentVideo2 == 'not found' and currentVideo3 == 'not found' and currentAudio == 'not found':
				html_code += f'\n<tr> \n <td>{row[0]}</td> \n <td>{timestamp}</td> \n <td>{FB_id}</td> \n <td>{FB_name}</td> \n<td> video not found in videocache folder</td>'
			else:
				html_code += f'\n<tr> \n <td>{row[0]}</td> \n <td>{timestamp}</td> \n <td>{FB_id}</td> \n <td>{FB_name}</td> \n<td>'
				if currentVideo1 != 'not found':
					html_vidName = ffmpegFinalConcat(currentVidID, currentVideo1, currentAudio, copiedFilesFolder, 1)
					if html_vidName != 'video conversion failed':
						html_code +=f' <a href="{html_vidName}">video </a>'
					else:
						html_code += 'video conversion failed '
				if currentVideo2 != 'not found':
					html_vidName = ffmpegFinalConcat(currentVidID, currentVideo2, currentAudio, copiedFilesFolder, 2)
					if html_vidName != 'video conversion failed':
						html_code +=f' <a href="{html_vidName}">video </a>'
					else:
						html_code += 'video conversion failed '
				if currentVideo3 != 'not found':
					html_vidName = ffmpegFinalConcat(currentVidID, currentVideo3, currentAudio, copiedFilesFolder, 3)
					if html_vidName != 'video conversion failed':
						html_code +=f' <a href="{html_vidName}">video </a>'
					else:
						html_code += 'video conversion failed '
				html_code += '</td>'

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

reportFolder = os.path.dirname(copiedFilesFolder)
with open(f'{reportFolder}\\report.html', 'w', encoding='utf8') as fout:
	fout.write(html_code)

with open(f'{reportFolder}\\style.css', 'w', encoding= 'utf8') as cssout:
            cssout.write(css_code)		

for file in os.listdir(copiedFilesFolder):
	if file.startswith('output_'):
		continue
	os.remove(f'{copiedFilesFolder}\\{file}')







