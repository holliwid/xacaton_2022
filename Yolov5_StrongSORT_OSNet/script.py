import torch
import os
import cv2
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


from PIL import Image


def GetTXT():
    txtList = []
    mainFolderID = len(next(os.walk('runs/track'))[1])
    mainPath = f"runs/track/example{mainFolderID}"
    for i in range(len(next(os.walk(f"runs/track/example{mainFolderID}"))[1])):
        if i == 0:
            txtList.append(f"runs/track/example{mainFolderID}/exp/tracks/" +
                           os.listdir(f"runs/track/example{mainFolderID}/exp/tracks")[0])
        else:
            txtList.append(f"runs/track/example{mainFolderID}/exp{i + 1}/tracks/" +
                           os.listdir(f"runs/track/example{mainFolderID}/exp{i + 1}/tracks")[0])
    return txtList


path1, path2, path3 = GetTXT()
df_1 = pd.read_csv(path1, sep = " ")
df_2 = pd.read_csv(path2, sep = " ")
df_3 = pd.read_csv(path3, sep = " ")

df_1.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_2.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_3.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']


df_list = [df_1, df_2, df_3]
for df in df_list:
  if df.iloc[0].all() == 0:
    df_human = df_1.copy()
  if df.iloc[0].all() == 1:
    df_jacket = df_1.copy()
  if df.iloc[0].all() == 2:
    df_pants = df_1.copy()

df_human.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_jacket.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']
df_pants.columns = ['frame_id', 'object_id', 'box_left', 'box_top', 'width', 'height', 'class_object', 'prediction', 'trash_1', 'trash_2', 'trash_3']

df_human['box_top'] = 1080 - df_human['box_top'] - df_human.height / 2
df_jacket['box_top'] = 1080 - df_jacket['box_top'] - df_jacket.height / 2
df_pants['box_top'] = 1080 - df_pants['box_top'] - df_pants.height / 2
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
        if y[7] == 1 and y[2] not in humans_on_frame:
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
for human_id, jacket_id in human_jacket:
  df_human_valuable_track.loc[(df_human_valuable_track.object_id == human_id) & (df_human_valuable_track.prediction > 0.70),'jacket_id'] = jacket_id

for human_id, pants_id in human_pants:
  df_human_valuable_track.loc[(df_human_valuable_track.object_id == human_id) & (df_human_valuable_track.prediction > 0.70), 'pants_id'] = pants_id


df_without_pants_jacket = df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull()) & (df_human_valuable_track['pants_id'].isnull())]
without_pants_jacket = dict(df_human_valuable_track.loc[(df_human_valuable_track['jacket_id'].isnull()) & (df_human_valuable_track['pants_id'].isnull())].object_id.value_counts())
without_pants_jacket = list(without_pants_jacket.keys())


df_res_frame = []
for human_id in without_pants_jacket:
  k = df_without_pants_jacket.loc[df_without_pants_jacket.object_id == human_id].iloc[0]
  df_res_frame.append([k.frame_id, k.object_id])
df_res_frame


vidcap = cv2.VideoCapture("")
mainFolderID = len(next(os.walk('runs/track'))[1])
mainPath = f"runs/track/example{mainFolderID}"
folderName = f"warnings{len(next(os.walk(mainPath))[1]) + 1}"
os.popen(f"mkdir \\runs\\track\\{folderName}")
project_path = f"{os.path.dirname(__file__)}\\runs\\track\\{folderName}"

for x in df_res_frame:
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, x[0])
    res, frame = vidcap.read()
    cv2.imwrite("runs/track//frame%d.jpg" % x[0], frame)