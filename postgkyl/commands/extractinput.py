import click
import base64

from postgkyl.commands.util import vlog, pushChain

@click.command(help='Extract embedded input file from compatible BP files')
@click.option('--use', '-u',
              help='Specify a \'tag\' to apply to (default all tags).')
@click.pass_context
def extractinput(ctx, **kwargs):
    vlog(ctx, 'Starting ')
    pushChain(ctx, 'extractinput', **kwargs)
    data = ctx.obj['data']
        
    for dat in data.iterator(kwargs['use']):
        encInp = dat.getInputFile()
        if encInp:
            inpfile = base64.decodebytes(encInp.encode('utf-8')).decode('utf-8')
            click.echo(inpfile)
        else:
            click.echo("No embedded input file!")
        #end
    #end
    vlog(ctx, 'Finishing extractinput')
#end
