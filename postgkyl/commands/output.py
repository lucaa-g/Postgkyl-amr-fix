import click
import numpy as np
import matplotlib.pyplot as plt
import os

dirPath = os.path.dirname(os.path.realpath(__file__))

def _colorbar(obj, _ax, _fig, redraw=False, aspect=None, label=''):
    """Add a colorbar adjacent to obj, with a matching height

    For use of aspect, see:
    http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.set_aspect
    """
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    _divider_ = make_axes_locatable(_ax)
    _cax_ = _divider_.append_axes("right", size="5%", pad=0.05)
    _cbar_ = _fig.colorbar(obj, cax=_cax_, label=label)
    if aspect is not None:
        _ax.set_aspect(aspect)
    if redraw:
        _fig.canvas.draw()
    return _cbar_

@click.command(help='Plot the data')
@click.option('--show/--no-show', default=True,
              help='Turn showing of the plot ON and OFF (default: ON)')
@click.option('--style', default=dirPath+'/postgkyl.mplstyle',
              help='Specify Matplotlib style file (default: Postgkyl style)')
@click.option('--fixed-axis', 'axismode', flag_value='image',
             default=True)
@click.option('--free-axis', 'axismode', flag_value='tight')
@click.option('--save/--no-save', '-s', default=False,
              help='Save figure as png')
@click.pass_context
def plot(ctx, show, style, axismode, save):
    fig, ax = plt.subplots()
    plt.style.use(style)
    numPlots = len(ctx.obj['values'])
    for i in range(numPlots):
        numDims = len(np.squeeze(ctx.obj['values'][i]).shape)
        if numDims == 1:
            im = ax.plot(ctx.obj['coords'][i][0],
                         np.squeeze(ctx.obj['values'][i]))
        elif numDims == 2:
            im = ax.pcolormesh(ctx.obj['coords'][i][0],
                               ctx.obj['coords'][i][1],
                               np.squeeze(ctx.obj['values'][i]).transpose())
            _colorbar(im, ax, fig)

    # format
    ax.axis(axismode)

    if show:
        plt.show()

    if save:
        fig.savefig('placeholder.png')
