# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import functools

from coalib.output.ConsoleInteraction import (nothing_done,
                                              acquire_settings,
                                              print_section_beginning,
                                              print_results,
                                              finalize,
                                              show_bears)
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.processes.Processing import execute_all_sections
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.misc.Exceptions import get_exitcode


def main():
    log_printer = ConsolePrinter()
    console_printer = ConsolePrinter()
    exitcode = 0
    try:
        yielded_results = False
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(acquire_settings, log_printer)

        if bool(sections["default"].get("show_bears", "False")):
            show_bears(local_bears,
                       global_bears,
                       console_printer)
            did_nothing = False
        else:
            section_begin = functools.partial(print_section_beginning,
                                              console_printer)
            section_results = execute_all_sections(sections,
                                                   targets,
                                                   log_printer,
                                                   global_bears,
                                                   local_bears,
                                                   section_begin,
                                                   print_results,
                                                   finalize)
            did_nothing = len(section_results) == 0
            for section_result in section_results:
                yielded_results = yielded_results or section_result[1][0]

        if did_nothing:
            nothing_done(console_printer)

        if yielded_results:
            exitcode = 1
    except Exception as exception:  # pylint: disable=broad-except
        exitcode = exitcode or get_exitcode(exception, log_printer)

    return exitcode
