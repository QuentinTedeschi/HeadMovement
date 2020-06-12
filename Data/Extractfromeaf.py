import pympi
import glob
import os
import ffmpeg

def convert_to_hhmmss(input_time):
    hours = int(input_time/3600000)
    input_time = input_time - hours * 3600000
    minutes = int(input_time/60000)
    input_time = input_time - minutes * 60000
    seconds = int(input_time/1000)
    input_time = input_time - seconds * 1000
    
    result = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(input_time).zfill(3)
    print(result)
    return result

def trim_video_file(eaf, andir, viddir, outputdir, tiers_names):
    file = pympi.Elan.Eaf(andir + eaf)
    vidfile = viddir + eaf[:-3] + "mov"
    tiers = file.get_tier_names()
    for tier in tiers:
        if tier in tiers_names:
            annots = file.get_annotation_data_for_tier(tier)
            inputvid = ffmpeg.input(vidfile)
            print(tier)
            tier = tier.replace (r"/", "_")
            output = outputdir + tier.replace(" ", "_") + "/" + eaf[:-4]
            for annot in annots:
                print(annot)
                start_time = convert_to_hhmmss(annot[0])
                end_time = convert_to_hhmmss(annot[1])
                output_file = output + str(annot[0]) + str(annot[1]) + ".mp4"
                inputvid = ffmpeg.input(vidfile)
                inputvid = inputvid.trim(start = start_time, end = end_time)
                inputvid = inputvid.setpts('PTS-STARTPTS')
                outputvid = inputvid.output(output_file)
                ffmpeg.run(outputvid)
                print("Done")
                
names = ("Head Nodding", "Head Sideways Shake", "Head Tilt (left/right)")
anndir = "./Raw/Annotations/"
videodir = "./Raw/Videos/"
outputdir = "./Videos/"

for file in os.listdir(anndir):
    if file.endswith(".eaf"):
        print(file)
        trim_video_file(file, anndir, videodir, outputdir, names)


