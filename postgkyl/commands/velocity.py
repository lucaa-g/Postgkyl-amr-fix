import click

from postgkyl.commands.util import vlog, pushChain
from postgkyl.data import Data

@click.command()
@click.option('--density', '-d',
              default='density', show_default=True,
              help="Tag for density")
@click.option('--momentum', '-m',
              default='momentum', show_default=True,
              help="Tag for momentum")
@click.option('--outtag', '-o',
              default='velocity', show_default=True,
              help='Tag for the result')
@click.option('--label', '-l',
              default='velocity', show_default=True,
              help="Custom label for the result")
@click.pass_context
def velocity(ctx, **kwargs):
    vlog(ctx, 'Starting velocity')
    pushChain(ctx, 'velocity', **kwargs)
    
    data = ctx.obj['data'] # shortcut
    
    for m0, m1 in zip(data.iterator(kwargs['density']),
                      data.iterator(kwargs['momentum'])):
        grid = m0.getGrid()        
        valsM0 = m0.getValues()
        valsM1 = m1.getValues()
            
        out = Data(tag=kwargs['outtag'],
                   compgrid=ctx.obj['compgrid'],
                   label=kwargs['label'],
                   meta=m0.meta)
        out.push(grid, valsM1/valsM0)
        data.add(out)
    #end

    data.deactivateAll(tag=kwargs['density'])
    data.deactivateAll(tag=kwargs['momentum'])

    vlog(ctx, 'Finishing velocity')
#end
