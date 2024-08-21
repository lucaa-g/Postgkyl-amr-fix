from time import time
import sys
import numpy as np

from cycler import cycler
import click

def verb_print(ctx, message):
  if ctx.obj['verbose']:
    elapsedTime = time() - ctx.obj['startTime']
    click.echo(click.style('[{:f}] {:s}'.format(elapsedTime, message),
                           fg='green'))
  #end
#end

def load_style(ctx, fn):
  fh = open(fn, 'r')
  for line in fh.readlines():
    key = line.split(':')[0]
    key_len = int(len(key))
    key = key.strip()
    value = line[(key_len+1):].strip()
    if value[:6] == 'cycler':
      arg = eval(value[16:-1])
      value = cycler(color=arg)
    #end
    ctx.obj['rcParams'][key] = value
  #end
  fh.close()
#end

#sets frame in block ctx attribute using block file name
def set_frame(ctx):
  
  data = ctx.obj['data']

  #load in file names
  files = [dat._file_name for dat in data.iterator()]

  #iterate through file names and find smallest index where file names differ, this is where the file name is
  #this is assuming that the file names are default from gkyl
  #short file is used to iterate in order to prevent indexing error
  short_file = min(files, key=len)
  num_frame_idx = np.inf
  for i in range(len(files)):
    for j in range(len(short_file)):
      if short_file[j] != files[i][j] and j < num_frame_idx:
        num_frame_idx = j
      #end
    #end
  #end

  #isolate frame number in file name and append it to big frame_list
  frame_list = []
  for f in files:
    f = f.split('.gkyl')[0]
    frame = f[num_frame_idx:].split('_')[0]
    frame_list.append(int(frame))
  #end
    
  #data objects in iterator have same index as corresponding frame in frame_list
  #this loop sets frame ctx attribute
  for i, dat in data.iterator(enum=True):
    dat.ctx['frame'] = frame_list[i]
  #end

  #return sorted frame list for use in animate function
  sorted_frame_list = np.unique(np.sort(frame_list))
  return sorted_frame_list
