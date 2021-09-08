import requests
import json
import time
import os
from os import system
from tkinter import *
from tkinter.ttk import Progressbar

root = Tk()
try:
    cwd = os.path.dirname(os.path.realpath(__file__))
    cwd=cwd.replace("\\","/")
    cwdcmd = os.path.dirname(os.path.realpath(__file__))
except:
    exit()
temp = Label(root, text="CurseForge Downloader")
temp.grid(padx=100,pady=0,row=0)

disable = Label(root, text="")
disable.grid(padx=50,pady=0,row=1)

temp = Label(root, text="Input modpack manifest filename", padx=0, pady=0)
temp.grid(row=2,column=0)

filename = Entry(root, width=35, borderwidth=2)
filename.grid(row=3, column=0, columnspan=3, padx=0, pady=5)
filename.insert(0, "manifest.json")

ver = Label(root, text="Game Version: ???")
ver.grid(padx=0,pady=0,row=7)

forgever = Label(root, text="ModLoader Version: ???")
forgever.grid(padx=0,pady=0,row=8)

name = Label(root, text="Name: ???")
name.grid(padx=0,pady=0,row=6)

count = Label(root, text="Modcount: ???")
count.grid(padx=0,pady=0,row=9)

valoutput = Label(root, text="N/A")
valoutput.grid(padx=0,pady=0,row=5)

progbar = Progressbar(root, length=300, mode='determinate')
progbar.grid(padx=0,pady=0,row=10)

def validateFileName():
    if disable.cget("text") == "":
        try:
            ver.config(text="Game Version: ???")
            forgever.config(text="ModLoader Version: ???")
            count.config(text="Filecount: ???")
            name.config(text="Name: ???")
            file=json.load(open(filename.get()))
            valoutput.config(text="File name valid!")
            ver.config(text="Game Version: "+file["minecraft"]["version"])
            forgever.config(text="ModLoader Version: "+file["minecraft"]["modLoaders"][0]["id"])
            count.config(text="Modcount: "+str(len(file['files'])))
            name.config(text="Name: '"+file['name']+"'")
            filename.config(state='disabled')
        except:
            valoutput.config(text="Error with '"+filename.get()+"'")
            filename.config(state='enabled')

dloutput = Label(root, text="N/A")
dloutput.grid(padx=0,pady=0,row=11)

#['error'] "in_queue"
#print(json.loads(requests.get("https://api.cfwidget.com/246333").text)['urls']['curseforge'])

def download():
    if disable.cget("text") == "":
        if valoutput.cget("text") == "File name valid!":
            total=0
            disable.config(text=" ")
            file=json.load(open(filename.get()))
            use=file['name']
            if use[len(use)-1:len(use)] == " ":
                use=use[0:len(use)-1]
            system('mkdir "'+cwdcmd+'\\'+use+'"')
            def out(tx):
                dloutput.config(text=tx)
                root.update()
            def getinfo(num):
                return json.loads(requests.get("https://api.cfwidget.com/"+str(num)).text)
            def download(js,num,modname):
                if len(num) == 7:
                    use=modname
                    if use[len(use)-1:len(use)] == " ":
                        use=use[0:len(use)-1]
                    displayname=""
                    for x in js['files']:
                        if str(x['id']) == num:
                            displayname=x['name']
                            break
                    if displayname == "":
                        return False
                    else:
                        print('https://media.forgecdn.net/files/'+num[0:4]+'/'+num[4:7]+'/'+displayname)
                        resp=requests.get('https://media.forgecdn.net/files/'+num[0:4]+'/'+num[4:7]+'/'+displayname)
                        file=open(cwdcmd+"\\"+use+"\\"+displayname,"wb")
                        file.write(resp.content)
                        file.close()
                        return True
                else:
                    out('Unexpected fileID length, skipping...')
                    time.sleep(1)
            loops=0
            result=[]
            for x in file['files']:
                loops+=1
                out("Getting link for: "+str(x['projectID']))
                code=getinfo(x['projectID'])
                if 'error' in code:
                    out("Error code: '"+str(code['error'])+"' in project ID '"+str(x['projectID'])+"', retrying 1...")
                    loopss=1
                    while ('error' in code):
                        code=getinfo(x['projectID'])
                        loopss+=1
                        if 'error' in code:
                            out("Error code: '"+str(code['error'])+"' in project ID '"+str(x['projectID'])+"', retrying "+str(loopss)+"...")
                        else:
                            break
                #if loops == 1:
                    #links.write(code['urls']['curseforge']+"/download/"+str(x['fileID']))
                #else:
                    #links.write("\n"+code['urls']['curseforge']+"/download/"+str(x['fileID']))
                result.append(code['urls']['curseforge']+"/download/"+str(x['fileID']))
                #system('start '+code['urls']['curseforge']+"/download/"+str(x['fileID']))
                progbar.config(value=((loops-0.5)*100)/len(file['files']))
                out("Downloading "+code['title']+"...")
                downloadresult=download(code,str(x['fileID']),file['name'])
                if downloadresult==True:
                    total+=1
                progbar.config(value=((loops)*100)/len(file['files']))
                firstrun=True
            out("Succeeded in downloading "+str(total)+" out of "+str(loops)+" mods.")
            #if vartest.get() == 1:
                #for x in result:
                    #system('start '+x)
            filename.config(state='enabled')
        else:
            dloutput.config(text="File is not validated or incompatible!")

temp = Button(root, text="Validate", command=validateFileName)
temp.grid(padx=0,pady=0,row=4)

temp = Button(root, text="Download", command=download)
temp.grid(padx=0,pady=0,row=12)

root.mainloop()
