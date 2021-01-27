import click

from postgkyl.commands.util import vlog, pushChain
from postgkyl.data import Data
import postgkyl.diagnostics as diag

@click.command()
@click.option('--array', '-a',
              default='array', show_default=True,
              help="Tag for array to be rotated")
@click.option('--rotator', '-r',
              default='rotator', show_default=True,
              help="Tag for rotator (data used for the rotation)")
@click.option('--outtag', '-o',
              default='rotarrayperp', show_default=True,
              help='Tag for the resulting rotated array perpendicular to rotator')
@click.option('--label', '-l',
              default='rotarrayperp', show_default=True,
              help="Custom label for the result")
@click.pass_context
def perprotate(ctx, **kwargs):
    """Rotate an array perpendicular to the unit vectors of a second array.
    For two arrays u and v, where v is the rotator, operation is u - (u dot v_hat) v_hat.
    """
    vlog(ctx, 'Starting rotation perpendicular to rotator array')
    pushChain(ctx, 'rotarraypar', **kwargs)
    
    data = ctx.obj['data'] # shortcut
    
    for a, rot in zip(data.iterator(kwargs['array']),
                      data.iterator(kwargs['rotator'])):
        grid, outrot = diag.perprotate(a, rot)
        # Create new GData structure with appropriate outtag and labels to store output.
        out = Data(tag=kwargs['outtag'],
                   stack=ctx.obj['stack'],
                   compgrid=ctx.obj['compgrid'],
                   label=kwargs['label'],
                   meta=a.meta)
        out.push(outrot, grid)
        data.add(out)
    #end

    data.deactivateAll(tag=kwargs['array'])
    data.deactivateAll(tag=kwargs['rotator'])

    vlog(ctx, 'Finishing rotation perpendicular to rotator array')
#end
