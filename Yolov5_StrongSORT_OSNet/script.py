import torch
import os
import cv2
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import creat_graphics
from heatmappy import Heatmapper
import sqlite3


from PIL import Image

def GetTXT():
    txtList = []
    mainFolderID = len(next(os.walk('runs/track'))[1])
    mainPath = f"runs/track/example{mainFolderID}"

    txtList.append(f"runs/track/example{mainFolderID}/human/tracks/" +
                   os.listdir(f"runs/track/example{mainFolderID}/human/tracks")[0])
    txtList.append(f"runs/track/example{mainFolderID}/jacket/tracks/" +

                   os.listdir(f"runs/track/example{mainFolderID}/jacket/tracks")[0])
    txtList.append(f"runs/track/example{mainFolderID}/pants/tracks/" +
                   os.listdir(f"runs/track/example{mainFolderID}/pants/tracks")[0])
    return txtList



def GetVIDEO(path_human):
    mas = path_human.split('/')
    mas = "/".join(mas[:-2]) + '/'

    video_path = mas + os.listdir(mas)[0]
    os.mkdir(mas + '/' + 'Warnings')

    mas += 'Warnings'
    return(video_path, mas)






path1, path2, path3 = GetTXT()
path_human = path1
df_human = pd.read_csv( path1, sep = " ")
df_jacket = pd.read_csv(path2, sep = " ")
df_pants = pd.read_csv(path3, sep = " ")

"""
df_1.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_2.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_3.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']

path_human = -1

df_list = [df_1, df_2, df_3]
for x in range(len(df_list)):
  value = df_list[x].iloc[0].class_object
  if value == 0:
    df_human = df_list[x].copy()
    path_human = path_list[x]
  if value == 1:
    df_jacket = df_list[x].copy()
  if value == 2:
    df_pants = df_list[x].copy()
"""


df_human.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_jacket.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_pants.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']


video_path, warning_path = GetVIDEO(path_human)
vidcap = cv2.VideoCapture(video_path)
vidcap.set(cv2.CAP_PROP_POS_FRAMES, 200)
res1, frame1 = vidcap.read()
mas = path_human.split('/')
mas = "/".join(mas[:-3]) + '/'
print(mas)
os.mkdir(mas + '/' + 'Graphics')
cv2.imwrite(mas + "background.png", frame1)
im = Image.open(mas + "background.png")
(width, height) = im.size


df_human['box_top'] = height - df_human['box_top'] - df_human.height / 2
df_jacket['box_top'] = height - df_jacket['box_top'] - df_jacket.height / 2
df_pants['box_top'] = height - df_pants['box_top'] - df_pants.height / 2
df_all = pd.concat([df_human, df_jacket, df_pants], ignore_index=True)
df_all = df_all.sort_values(by=['frame_id'])


df_human_valuable = df_human[df_human.groupby('object_id').object_id.transform('count')>250].copy()
df_jacket_valuable = df_jacket[df_jacket.groupby('object_id').object_id.transform('count')>1].copy()
df_pants_valuable = df_pants[df_pants.groupby('object_id').object_id.transform('count')>1].copy()


df_all_valuable = pd.concat([df_human_valuable, df_jacket_valuable, df_pants_valuable], ignore_index=True)
df_all_valuable = df_all.sort_values(by=['frame_id', 'class_object'])


df_all_valuable = df_all_valuable.reset_index().copy()  # make sure indexes pair with number of rows

list_by_frame = [[[0,1]]]
for index, row in df_all_valuable.iterrows():
    if row['frame_id'] == list_by_frame[-1][0][1]:
      list_by_frame[-1].append(row.values.tolist())
    else:
      list_by_frame.append([row.values.tolist()])

list_by_frame.pop(0)

def delete_all_duplicate_object_id(list_of_tuple):
  list_of_tuple = list_of_tuple
  result = []
  ids = []
  for x in list_of_tuple:
    ids.append(x[2])
  unike_ids = set(ids)
  one_id = []
  for id in unike_ids:
    if ids.count(id) == 1:
      one_id.append(id)
  for x in list_of_tuple:
    if x[2] in one_id:
      result.append(x)

  return result


human_pants = []
human_jacket = []

pants_object_id = []
jacket_object_id = []
for x in list_by_frame:
    humans_on_frame = []
    humans_distance_jacket = []
    humans_distance_pants = []
    for y in x:
        if y[7] == 0 and y[2] not in humans_on_frame:
            humans_on_frame.append(y)

        if y[7] == 1 and y[2] not in jacket_object_id:
            for human in humans_on_frame:
                distance = abs(human[3] - y[3]) + abs(human[4] - y[4])
                if distance < 200:
                    humans_distance_jacket.append((human[2], distance, y[2]))

        if y[7] == 2 and y[2] not in pants_object_id:
            for human in humans_on_frame:
                distance = abs(human[3] - y[3]) + abs(human[4] - y[4])
                if distance < 200:
                    humans_distance_pants.append([human[2], distance, y[2]])

        humans_distance_jacket_match = delete_all_duplicate_object_id(humans_distance_jacket)
        humans_distance_pants_match = delete_all_duplicate_object_id(humans_distance_pants)

        if len(humans_distance_jacket_match) > 0:
            for x in humans_distance_jacket:
                jacket_object_id.append(x[2])
                human_jacket.append([x[0], x[2]])

        if len(humans_distance_pants_match) > 0:
            for x in humans_distance_pants:
                pants_object_id.append(x[2])
                human_pants.append([x[0], x[2]])



df_human_valuable_track = df_human_valuable.copy()

df_res_frame_without_pants_jacket = []
df_res_frame_without_pants = []
df_res_frame_without_jacket = []
df_without_jacket = df_jacket_valuable.copy()
df_without_pants_jacket = df_without_jacket.copy()
df_without_pants = df_pants.copy()

if len(df_human_valuable_track) !=  0:
    for human_id, jacket_id in human_jacket:
        df_human_valuable_track.loc[(df_human_valuable_track.object_id == human_id) & (df_human_valuable_track.prediction > 0.70),'jacket_id'] = jacket_id

    for human_id, pants_id in human_pants:
        df_human_valuable_track.loc[(df_human_valuable_track.object_id == human_id) & (df_human_valuable_track.prediction > 0.70), 'pants_id'] = pants_id


    df_without_pants_jacket = df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull()) & (df_human_valuable_track['pants_id'].isnull())]
    df_without_pants = df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull() == False) & (df_human_valuable_track['pants_id'].isnull())]
    df_without_jacket = df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull()) & (df_human_valuable_track['pants_id'].isnull() == False)]


    without_pants_jacket = dict(df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull()) & (df_human_valuable_track['pants_id'].isnull())].object_id.value_counts())
    without_pants_jacket_1 = list(without_pants_jacket.keys())

    without_pants = dict(df_without_pants.loc[(df_without_pants['jacket_id'].isnull() == False) & (df_without_pants['pants_id'].isnull())].object_id.value_counts())
    without_pants = list(without_pants.keys())

    without_jacket = dict(df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull()) & (df_human_valuable_track['pants_id'].isnull() == False)].object_id.value_counts())
    without_jacket = list(without_jacket.keys())

    for human_id in without_pants_jacket:
        k = df_without_pants_jacket.loc[df_without_pants_jacket.object_id == human_id].iloc[0]
        df_res_frame_without_pants_jacket.append([k.frame_id, k.object_id])


    for human_id in without_pants:
        k = df_without_pants.loc[df_without_pants.object_id == human_id].iloc[0]
        df_res_frame_without_pants.append([k.frame_id, k.object_id])


    for human_id in without_jacket:
        k = df_without_jacket.loc[df_without_jacket.object_id == human_id].iloc[0]
        df_res_frame_without_jacket.append([k.frame_id, k.object_id])



for x in df_res_frame_without_pants_jacket:
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, x[0])
    res, frame = vidcap.read()
    cv2.imwrite(warning_path + "/frame%d.png" % x[0], frame)


creat_graphics.create_scatter(df_human_valuable_track, mas + "background.png", mas + 'Graphics/human', width, height)
creat_graphics.create_scatter(df_without_jacket, mas + "background.png", mas + 'Graphics/without_jacket', width, height)
creat_graphics.create_scatter(df_without_pants_jacket, mas + "background.png", mas + 'Graphics/without_pants_jacket', width, height)
creat_graphics.create_scatter(df_without_pants, mas + "background.png", mas + 'Graphics/without_pants', width, height)


creat_graphics.heat_map(df_human_valuable_track, mas + "background.png", mas + 'Graphics/heat_human', width, height)
creat_graphics.heat_map(df_without_jacket, mas + "background.png", mas + 'Graphics/heat_without_jacket', width, height)
creat_graphics.heat_map(df_without_pants_jacket, mas + "background.png", mas + 'Graphics/heat_without_pants_jacket', width, height)
creat_graphics.heat_map(df_without_pants, mas + "background.png", mas + 'Graphics/heat_without_pants', width, height)


df_human_valuable_list = df_human_valuable[['box_left', 'box_top']].values.tolist()
creat_graphics.create_beautiful_heatmap(df_human_valuable_list, './assets/Test.png')



db = sqlite3.connect("reports.db")
cursor = db.cursor()
lastExampleID = len(next(os.walk('runs/track'))[1])
Heat_Human_path = f"runs/track/example{lastExampleID}/Graphics/heat_human.png"
Heat_Without_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/heat_without_jacket.png"
Heat_Without_Pants_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/heat_without_pants_jacket.png"
Heat_Without_Pants_path = f"runs/track/example{lastExampleID}/Graphics/heat_without_pants.png"
Human_path = f"runs/track/example{lastExampleID}/Graphics/human.png"
Without_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/without_jacket.png"
Without_Pants_Jacket_path = f"runs/track/example{lastExampleID}/Graphics/without_pants_jacket.png"
Without_Pants_path = f"runs/track/example{lastExampleID}/Graphics/without_pants.png"
Video_Path = f"data/video/{video_path.split('/')[-1]}"
print(Video_Path)
cursor.execute(f"""
    insert into Reports(
        Heat_Human_path,
        Heat_Without_Jacket_path,
        Heat_Without_Pants_Jacket_path,
        Heat_Without_Pants_path,
        Human_path,
        Without_Jacket_path,
        Without_Pants_Jacket_path,
        Without_Pants_path,
        Video_Path)
    values(
        '{Heat_Human_path}',
        '{Heat_Without_Jacket_path}',
        '{Heat_Without_Pants_Jacket_path}',
        '{Heat_Without_Pants_path}',
        '{Human_path}',
        '{Without_Jacket_path}',
        '{Without_Pants_Jacket_path}',
        '{Without_Pants_path}',
        '{Video_Path}');
""")
db.commit()

report_id = cursor.execute(f"select ID from Reports ORDER BY ID DESC LIMIT 1;").fetchall()[0][0]
# (1, "Человек без рабочей куртки и штанов");
# (2, "Человек без рабочих штанов");
# (3, "Человек без рабочей куртки");
# (4, "Человек в опасной зоне");
print(report_id)

for warning in df_res_frame_without_pants_jacket:
    print(warning[1])
    print(warning[0])
    cursor.execute(f"""
        insert into Warnings(
            Report_ID,
            Event_ID,
            Object_ID,
            Frame_path
        )
        values(
            {report_id},
            1,
            {int(warning[1])},
            '{warning_path + "/frame" + str(int(warning[0])) + ".png"}'
        );
    """)
    db.commit()


for warning in df_res_frame_without_pants:
    cursor.execute(f"""
        insert into Warnings(
            Report_ID,
            Event_ID,
            Object_ID,
            Frame_path
        )
        values(
            {report_id},
            2,
            {int(warning[1])},
            '{warning_path + "/frame" + str(int(warning[0])) + ".png"}'
        );
    """)
    db.commit()


for warning in df_res_frame_without_jacket:
    cursor.execute(f"""
        insert into Warnings(
            Report_ID,
            Event_ID,
            Object_ID,
            Frame_path
        )
        values(
            {report_id},
            3,
            {int(warning[1])},
            '{warning_path + "/frame" + str(int(warning[0])) + ".png"}'
        );
    """)
    db.commit()
