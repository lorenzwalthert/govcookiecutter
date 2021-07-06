from pathlib import Path
from cookiecutter.main import cookiecutter
from govcookiecutter import __version__
import click

# Define the file path to the project template
dir_template = Path(__file__).resolve().parent.joinpath("govcookiecutter")


# Relevant `click` options taken from `cookiecutter` version 1.7.3
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, u"-V", u"--version")
@click.option(
    "--no-input",
    is_flag=True,
    help="Do not prompt for parameters and only use `cookiecutter.json` file content",
)
@click.option(
    "--replay",
    is_flag=True,
    help="Do not prompt for parameters and only use information entered previously",
)
@click.option(
    "-f",
    "--overwrite-if-exists",
    is_flag=True,
    help="Overwrite the contents of the output directory if it already exists",
)
@click.option(
    "-s",
    "--skip-if-file-exists",
    is_flag=True,
    help="Skip the files in the corresponding directories if they already exist",
    default=False,
)
@click.option(
    "-o",
    "--output-dir",
    default=".",
    type=click.Path(),
    help="Where to output the generated project dir into",
)
@click.option(
    "--config-file", type=click.Path(), default=None, help="User configuration file"
)
@click.option(
    "--default-config",
    is_flag=True,
    help="Do not load a config file. Use the defaults instead",
)
def main(
    no_input,
    replay,
    overwrite_if_exists,
    output_dir,
    config_file,
    default_config,
    skip_if_file_exists,
) -> None:
    """Generate a ``govcookiecutter`` template using ``cookiecutter``.

    Options are those available from ``cookiecutter`` v1.7.3 that are compatible with
    ``govcookiecutter``.

    """
    cookiecutter(
        template=str(dir_template),
        no_input=no_input,
        replay=replay,
        overwrite_if_exists=overwrite_if_exists,
        output_dir=output_dir,
        config_file=config_file,
        default_config=default_config,
        skip_if_file_exists=skip_if_file_exists,
    )


if __name__ == "__main__":
    main()
