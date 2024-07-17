import numpy as np
import click

from postgkyl.data import GData
from postgkyl.commands.util import verb_print

@click.command()
@click.pass_context

def stitch(ctx, **kwargs):
    """Data from all active datasets is collected and combined into one dataset,
    used for adaptive mesh refinement simulation plotting and animation
    """
    #currently working on 1d adaptation

    #data = ctx.obj['data']

    #for dat in data.iterator():
        #click.echo(dat.get_values())
        #click.echo(dat.get_grid())
    
    verb_print(ctx, 'Starting stitch')
    data = ctx.obj['data']

    #Uses frametag parameter in loadgroup function to tag each loaded file
    #according to their frame then sort each frame for correct ordering during animation

    tagList = np.array(list(data.tagIterator()))
    tag_idx = np.argsort(tagList.astype(float))
    sortedTagList = tagList[tag_idx]



    for tag in sortedTagList:
    
        grid = []
        values = []

        #sorts dataList by grid lower bound so that appending in new grid is in the right order
        dataList = np.array(list(data.iterator(tag)))
        lower_bound_list = np.array([])
        for dat in dataList:
            lower_bound_list = np.append(lower_bound_list, dat.get_bounds()[0][0])
        idx = np.argsort(lower_bound_list)
        dataList = dataList[idx]

        for dat in dataList:
            for val in dat.get_values():
                values.append(val)
            if not grid:
                grid.append(dat.get_grid()[0])
            else:
                grid[0] = np.append(grid[0], dat.get_grid()[0])
        values = np.array(values)
        grid[0] = np.unique(grid[0])
            

        data.deactivateAll(tag)
        
        output = GData()
        output.push(grid, values)
        data.add(output)


    

    verb_print(ctx, 'Finishing stitch')
    
    
