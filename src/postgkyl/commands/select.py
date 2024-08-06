import click
import numpy as np

import postgkyl.data.select
from postgkyl.data import GData
from postgkyl.commands.util import verb_print

@click.command()
@click.option('--z0',  default=None,
              help="Indices for 0th coord (either int, float, or slice)")
@click.option('--z1', default=None,
              help="Indices for 1st coord (either int, float, or slice)")
@click.option('--z2', default=None,
              help="Indices for 2nd coord (either int, float, or slice)")
@click.option('--z3', default=None,
              help="Indices for 3rd coord (either int, float, or slice)")
@click.option('--z4', default=None,
              help="Indices for 4th coord (either int, float, or slice)")
@click.option('--z5', default=None,
              help="Indices for 5th coord (either int, float, or slice)")
@click.option('--comp', '-c', default=None,
              help="Indices for components (either int, slice, or coma-separated)")
@click.option('--use', '-u',
              help='Specify a \'tag\' to apply to (default all tags).')
@click.option('--tag', '-t',
              help='Optional tag for the resulting array')
@click.option('--label', '-l',
              help="Custom label for the result")
@click.option('--multib', '-mb', is_flag=True)
@click.pass_context
def select(ctx, **kwargs):
  r"""Subselect data from the active dataset(s). This command allows, for
  example, to choose a specific component of a multi-component
  dataset, select a index or coordinate range. Index ranges can also
  be specified using python slice notation (start:end:stride).

  """
  verb_print(ctx, 'Starting select')
  data = ctx.obj['data']


  if kwargs['multib']:
    botlef_point = []
    for dim in [0,1]:
      botlef_point.append(min([dat.get_bounds()[0][dim] for dat in data.iterator(kwargs['use'])]))
    if kwargs['z0'] is not None:
      for dat in data.iterator(kwargs['use']):
        if dat.get_bounds()[0][0] <= float(kwargs['z0']) <= dat.get_bounds()[1][0] and dat.get_bounds()[0][1] == botlef_point[1]:
          block = dat
    if kwargs['z1'] is not None:
      for dat in data.iterator(kwargs['use']):
        if dat.get_bounds()[0][1] <= float(kwargs['z1']) <= dat.get_bounds()[1][1] and dat.get_bounds()[0][0] == botlef_point[0]:
          block = dat
    block.neighbors(data.iterator(kwargs['use']))

    
    value_list = []
    if kwargs['z0'] is not None:
      grid, values = postgkyl.data.select(block,
                                          z0=kwargs['z0'],
                                          comp=kwargs['comp'])
      grid_list = grid
      for val in values[0]:
        value_list.append(val)
      while block._neighbors[(1, True)] is not None:
        block = block._neighbors[(1,True)]
        block.neighbors(data.iterator(kwargs['use']))
        grid, values = postgkyl.data.select(block,
                                            z0=kwargs['z0'],
                                            comp=kwargs['comp'])
        grid_list[1] = np.append(grid_list[1], grid[1])
        for val in values[0]:
          value_list.append(val)
      grid_list[1] = np.unique(grid_list[1])
      value_list = np.array([value_list])


        
    if kwargs['z1'] is not None:
      grid, values = postgkyl.data.select(block,
                                            z1=kwargs['z1'],
                                            comp=kwargs['comp'])
      grid_list = grid
      for val in values:
        value_list.append(val)
      while block._neighbors[(0, True)] is not None:
        block = block._neighbors[(0,True)]
        block.neighbors(data.iterator(kwargs['use']))
        grid, values = postgkyl.data.select(block,
                                            z1=kwargs['z1'],
                                            comp=kwargs['comp'])
        grid_list[0] = np.append(grid_list[0], grid[0])
        for val in values:
          value_list.append(val)
      grid_list[0] = np.unique(grid_list[0])
      value_list = np.array(value_list)




    
    data.deactivateAll()
    
    out = GData(tag=kwargs['tag'],
                label=kwargs['label'],
                comp_grid=ctx.obj['compgrid'])
    out.push(grid_list, value_list)
    data.add(out)
    
    
  else:
    for dat in data.iterator(kwargs['use']):
      if kwargs['tag']:
        out = GData(tag=kwargs['tag'],
                    label=kwargs['label'],
                    comp_grid=ctx.obj['compgrid'],
                    ctx=dat.ctx)
        grid, values = postgkyl.data.select(dat,
                                            z0=kwargs['z0'],
                                            z1=kwargs['z1'],
                                            z2=kwargs['z2'],
                                            z3=kwargs['z3'],
                                            z4=kwargs['z4'],
                                            z5=kwargs['z5'],
                                            comp=kwargs['comp'])
        click.echo(grid)
        out.push(grid, values)
        data.add(out)

        
      else:
        postgkyl.data.select(dat, overwrite=True,
                             z0=kwargs['z0'], z1=kwargs['z1'],
                             z2=kwargs['z2'], z3=kwargs['z3'],
                             z4=kwargs['z4'], z5=kwargs['z5'],
                             comp=kwargs['comp'])
      #end
    #end
  verb_print(ctx, 'Finishing select')
#end
