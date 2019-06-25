from Languini import app
import click


@click.command()
@click.option('-m', '--mode', type=str, default="prod", help='Set Config to test, prod or debug')
def deploy(mode):

    if mode is not "prod" or mode is not "debug" or mode is not "test":

        app.run(debug=True)


if __name__ == '__main__':
    deploy()