from __future__ import print_function, division, absolute_import


descr = 'Process diffraction data to find grain orientations'
example = """
examples:
    hexrd find-orientations configuration.yml
"""


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'find-orientations',
        description = descr,
        help = descr
        )
    p.add_argument(
        'yml', type=str,
        help='YAML configuration file'
        )
    p.add_argument(
        '-q', '--quiet', action='store_true',
        help="don't report progress in terminal"
        )
    p.add_argument(
        '-f', '--force', action='store_true',
        help='overwrites existing analysis'
        )
    p.add_argument(
        '--hkls', metavar='HKLs', type=str, default=None,
        help="""\
list hkl entries in the materials file to use for fitting
if None, defaults to list specified in the yml file"""
        )
    p.set_defaults(func=execute)


def execute(args, parser):
    import os
    import logging

    import yaml

    from hexrd.findorientations import find_orientations


    if args.hkls is not None:
        args.hkls = [int(i) for i in args.hkls.split(',') if i]

    with open(args.yml) as f:
        cfg = [cfg for cfg in yaml.load_all(f)][0]

    # now we know where to save the log file
    logger = logging.getLogger('hexrd')
    fh = logging.FileHandler(
        os.path.join(
            cfg['working_dir'],
            cfg['analysis_name'],
            'find-orientations.log'
            )
        )
    log_level = logging.DEBUG if args.debug else logging.INFO
    fh.setLevel(log_level)

    find_orientations(
        cfg, verbose=not args.quiet, hkls=args.hkls, force=args.force
        )
