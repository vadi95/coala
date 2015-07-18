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

from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.processes.Processing import execute_all_sections
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.misc.Exceptions import get_exitcode


def main():
    log_printer = ConsolePrinter()
    exitcode = 0
    try:
        yielded_results = False
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(lambda *args: True, log_printer)

        section_results = execute_all_sections(sections,
                                               targets,
                                               log_printer,
                                               global_bears,
                                               local_bears)
        for section_result in section_results:
            yielded_results = yielded_results or section_result[1][0]

        if yielded_results:
            exitcode = 1
    except Exception as exception:  # pylint: disable=broad-except
        exitcode = exitcode or get_exitcode(exception, log_printer)

    return exitcode
