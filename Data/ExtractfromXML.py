import xml.etree.ElementTree as ET
import os
import ffmpeg
from AMIDict import Letter_Dict

def convert_to_hhmmss(input_time):
    
    hours = int(input_time/3600)
    input_time = input_time - hours * 3600
    minutes = int(input_time/60)
    input_time = input_time - minutes * 60
    seconds = int(input_time)
    input_time = input_time - seconds
    
    result = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + '.' + (str(input_time)[2:])[:2]
    
    return result

def get_right_video(namefile):
    scenario = namefile[:7]
    right_number = Letter_Dict[scenario][namefile[8]]
    return(right_number)

def trim_video_file(xml, andir, viddir, outputdir, names):
    tree = ET.parse(andir + xml)
    root = tree.getroot()
    nbr = get_right_video(xml)
    elim = 0
    vidfile = viddir + xml[:-11] + "/video/" + xml[:-10] + "Closeup" + nbr + ".avi"
    for child in root:
        form = child.get('form')
        output = outputdir + "/" + xml[:-4]
        if form in names:
            output = outputdir + form + "/" + xml.replace(".", "_")[:-4]
            start = float(child.get('starttime'))
            end = float(child.get('endtime'))
            if (end - start) < 0.25:
                print("Too Short!")
                continue
            start_time = convert_to_hhmmss(start)
            end_time = convert_to_hhmmss(end)
            output_file = output + str(int(start)) + str(int(end)) + ".mp4"
            inputvid = ffmpeg.input(vidfile)
            inputvid = inputvid.trim(start = start_time, end = end_time)
            inputvid = inputvid.setpts('PTS-STARTPTS')
            outputvid = inputvid.output(output_file)
            try:
                ffmpeg.run(outputvid, capture_stdout=True, capture_stderr=True, overwrite_output=True)
            except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e
            print("Done")
                
names = ("nod", "shake")
anndir = "./Raw/AMIAnnotations/"
videodir = "./Raw/AMIVideos/"
outputdir = "./VideosAMI/"

for file in os.listdir(anndir):
    if file.endswith(".xml"):
        test = trim_video_file(file, anndir, videodir, outputdir, names)


