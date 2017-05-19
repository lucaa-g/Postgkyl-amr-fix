
import click

import postgkyl.commands as cmd
from postgkyl.data.load import GData
from postgkyl.data.interp import GInterpZeroOrder

@click.group(chain=True)
@click.option('--filename', '-f', multiple=True,
              help='Specify one or more file(s) to work with.')
@click.pass_context
def cli(ctx, filename):
    if filename == ():
        click.echo('No data file given. Specify file(s) with \'-f\'')
        ctx.exit()
    
    ctx.obj['files'] = filename
    ctx.obj['numFiles'] = len(filename)
    ctx.obj['data'] = []
    ctx.obj['coords'] = []
    ctx.obj['values'] = []
    for i, fl in enumerate(filename):
        ctx.obj['data'].append(GData(fl))
        dg = GInterpZeroOrder(ctx.obj['data'][i])
        coords, values = dg.project(0)
        ctx.obj['coords'].append(coords)
        ctx.obj['values'].append(values)

cli.add_command(cmd.info.info)
cli.add_command(cmd.output.plot)
cli.add_command(cmd.project.project)
cli.add_command(cmd.transform.mult)
cli.add_command(cmd.transform.norm)

if __name__ == '__main__':
    cli(obj={})