import matplotlib.pyplot as plt
import matplotlib.image as im
import pandas as pd
import pathlib
import os

import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import seaborn as sns


from heatmappy import Heatmapper
from PIL import Image


def create_scatter(df, path_to_back_img, save_path, width=1920, height=1080):
  img = im.imread(path_to_back_img)
  fig, ax = plt.subplots()
  ax.scatter(df.box_left, df.box_top, alpha=0.5, color='red')
  ax.imshow(img, extent=[0, width, 0, height])
  ax.axis('off')
  fig.set_size_inches(18.5, 10.5)
  fig.savefig(save_path + '.png', dpi=100, bbox_inches='tight')


def heat_map(df, path_to_back_img, save_path, width=1920, height=1080):
  print(df)
  map_img = mpimg.imread(path_to_back_img)
  hmax = sns.kdeplot(x=df['box_left'], y=df['box_top'], alpha=0.5, color='red', shade=True,
                      bw_method=.15)
  hmax.collections[0].set_alpha(0)
  fig = hmax.get_figure()
  plt.imshow(map_img, zorder=0, extent=[0, width, 0, height])
  fig.savefig(save_path + '.png', bbox_inches='tight')



def create_beautiful_heatmap(data, background):
  example_img_path = background
  example_img = Image.open(example_img_path)

  heatmapper = Heatmapper()
  heatmap = heatmapper.heatmap_on_img(data, example_img)
  heatmap.save('heatmap.png')