###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2014'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'

import os
import errno
import sys
import logging
import ntpath
import re
import gzip


def is_float(s):
    """Check if a string can be converted to a float.

    Parameters
    ----------
    s : str
        String to evaluate.

    Returns
    -------
    boolean
        True if string can be converted, else False.
    """

    try:
        float(s)
    except ValueError:
        return False

    return True


def concatenate_files(input_files, output_file):
    """Concatenate several files into a single file.

    Creates a compressed file if the extension of
    the output file ends with .gz.

    Parameters
    ----------
    input_files : iterable
        Files to concatenate.
    output_file : str
        Name of output file.
    """

    if output_file.endswith('.gz'):
        open_file = gzip.open
    else:
        open_file = open

    with open_file(output_file, "wb") as outfile:
        for f in input_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


def alphanumeric_sort(l):
    """Sorts the given iterable alphanumerically.

    http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python

    Parameters
    ----------
    l : iterable
        The iterable to be sorted.

    Returns
    -------
    iterable
        Iterable sorted alphanumerically.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def check_file_exists(input_file):
    """Check if file exists."""
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        logger = logging.getLogger()
        logger.error('  [Error] Input file does not exists: ' + input_file + '\n')
        sys.exit()


def check_dir_exists(input_dir):
    """Check if directory exists."""
    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        logger = logging.getLogger()
        logger.error('  [Error] Input directory does not exists: ' + input_dir + '\n')
        sys.exit()


def make_sure_path_exists(path):
    """Create directory if it does not exist."""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            logger = logging.getLogger()
            logger.error('  [Error] Specified path does not exist: ' + path + '\n')
            sys.exit()


def remove_extension(filename, extension=None):
    """Remove extension from filename.

    A specific extension can be specified, otherwise
    the extension is taken as all characters after the
    last period.
    """
    f = ntpath.basename(filename)

    if extension and f.endswith(extension):
        f = f[0:f.rfind(extension)]
    else:
        f = os.path.splitext(f)[0]

    if f[-1] == '.':
        f = f[0:-1]

    return f
