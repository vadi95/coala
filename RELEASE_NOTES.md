# coala 0.4.0

New features:

 * Auto-apply can be enabled/disabled through the `autoapply` setting in a
   coafile.
 * Auto-applied actions print the actual file where something happened.
 * A new bear was added, the GitCommitBear! It allows to check your current
   commit message at HEAD from git!
 * Filenames of results are now printed relatively to the execution directory.
   (https://github.com/coala-analyzer/coala/issues/1124)

Bugfixes:

 * coala-json outputted results for file-ranges that were excluded.
   (https://github.com/coala-analyzer/coala/issues/1165)
 * Auto-apply actions that failed are now marked as unprocessed so the user can
   decide manually what he wants to do with them.
   (https://github.com/coala-analyzer/coala/issues/1202)
 * SpaceConsistencyBear: Fixed misleading message when newline at EOF is
   missing.
   (https://github.com/coala-analyzer/coala/issues/1185)
 * Results from global bears slipped through our processing facility. Should not
   happen any more.

# coala 0.3.0

We are dropping Python 3.2 support (and so PyPy). Also we are removing
translations, the default language is English.

This release contains these following feature changes:

 * Auto-apply feature added! Results can directly be processed without user
   interaction specifying the desired action!
 * A missing coafile that is explicitly wanted through the `--config` flag
   throws an error instead of a warning. Only default coafile names (ending with
   `.coafile`) raise a warning.
 * Various new bears integrating existing linter tools, e.g. for C/C++, Python,
   Ruby, JSON and many more!
 * Allow to ignore files inside the coafile.
 * Results can now be stored and tagged with an identifier for accessing them
   later.
 * OpenEditorAction lets the user edit the real file instead of a temporary one.
 * All usable bears can now be shown with `--show-all-bears`.
 * Only `#` is supported for comments in the configuration file syntax.
 * Multiple actions can now be executed on the CLI.
 * Patches can now be shown on the CLI.
 * A `coala-format` binary was added that allows customized formatting for
   results to ease integration in other systems.
 * Printing utilities have moved into the PyPrint library.

Bear API changes:

 * A bear can implement `check_prerequisites` to determine whether it can
   execute in the current runtime.
 * The PatchResult class was merged into the Result class.

Bear changes:

 * SpaceConsistencyBear offers more verbose and precise information about the
   problem.

# coala 0.2.0

This release features the following feature changes:

 * `--find-config` flag: Searches for .coafile in all parent directories.
 * Add code clone detection bears and algorithms using CMCD approach.
 * Console color gets properly disabled now for non-supporting platforms (like
   Windows).
 * coala results can be outputted to JSON format using the `coala-json`
   command.
 * Automatically add needed flags to open a new process for some editors.
 * Save backup before applying actions to files.
 * Return nonzero when erroring or yielding results.
 * Write newlines before beginning new sections in coafiles when appropriate.
 * The default_coafile can now be used for arbitrary system-wide settings.
 * coala can now be configured user-wide with a ~/.coarc configuration file.
 * Manual written documentation is now hosted at http://coala.rtfd.org/.
 * Changed logging API in Bears (now: debug/warn/err).
 * clang python bindings were added to the bearlib.
 * Exitcodes were organized and documented.
   (http://coala.readthedocs.org/en/latest/Users/Exit_Codes/)
 * Handling of EOF/Keyboard Interrupt was improved.
 * Console output is now colored.
 * Bears can now easily convert settings to typed lists or dicts.
 * Bears have no setUp/tearDown mechanism anymore.
 * Colons cannot be used for key value seperation in configuration files
   anymore as that clashes with the new dictionary syntax. Use `=` instead.
 * The `--job-count` argument was removed for technical reasons. It will be
   re-added in the near future.
 * A `--show-bears` parameter was added to get metainformation of bears.
 * The coala versioning scheme was changed to comply PEP440.
 * `coala --version` now gives the version number. A released `dev` version has
   the build date appended, 0 for local versions installed from source.
 * A `coala-dbus` binary will now be installed that spawns up a dbus API for
   controlling coala. (Linux only.)
 * The StringProcessing libary is there to help bear writers deal with regexes
   and similar things.
 * A new glob syntax was introduced and documented.
   (http://coala.readthedocs.org/en/latest/Users/Glob_Patterns/)
 * The `--apply-changes` argument was removed as its concept does not fit
   anymore.
 * Bears can now return any iterable. This makes it possible to `yield`
   results.

New bears:

 * ClangCloneDetectionBear
 * LanguageToolBear
 * PyLintBear

Infrastructural changes:

 * Tests are executed with multiple processes.
 * Branch coverage raised to glorious 100%.
 * We switched from Travis CI to CircleCI as Linux CI.
 * AppVeyor (Windows CI) was added.
 * Travis CI was added for Mac OS X.
 * Development releases are automatically done from master and available via
   `pip install coala --pre`.
 * Rultor is now used exclusively to push on master. Manual pushes to master
   are not longer allowed to avoid human errors. Rultor deploys translation
   strings to Zanata and the PyPI package before pushing the fastforwarded
   master.

Internal code changes:

 * Uncountable bugfixes.
 * Uncountable refactorings touching the core of coala. Code has never been
   more beautiful.

We are very happy that 7 people contributed to this release, namely Abdeali
Kothari, Mischa Krüger, Udayan Tandon, Fabian Neuschmidt, Ahmed Kamal and
Shivani Poddar (sorted by number of commits). Many thanks go to all of those!

coala's code base has grown sanely to now over 12000 NCLOC with almost half of
them being tests.

We are happy to announce that Mischa Krüger is joining the maintainers team of
coala.

Furthermore we are happy to announce basic Windows and Mac OS X support. This
would not have been possible without Mischa and Abdeali. coala is fully tested
against Python 3.3 and 3.4 on Windows and 3.2, 3.3, 3.4 and Pypy3 on Mac while
not all builtin bears are tested. coala is also tested against Pypy3 and
Python 3.5 beta (in addition to 3.3 and 3.4) on Linux.

# coala 0.1.1 alpha

This patch release fixes a major usability issue where data entered into the
editor may be lost.

For more info, see release 0.1.0.

# coala 0.1.0 alpha

### Attention: This release is old and experimenental.

coala 0.1 provides basic functionality. It is not feature complete but already
useful according to some people.

For information about the purpose of coala please look at the README provided
with each source distribution.

Note that this is a prerelease, thus this release will be supported with only
important bugfixes for limited time (at least until 0.2.0 is released). Linux
is the only supported platform.

Documentation for getting started with coala is provided here:
https://github.com/coala-analyzer/coala/blob/v0.1.0-alpha/TUTORIAL.md

If you want to write static code analysis routines, please check out this guide:
https://github.com/coala-analyzer/coala/blob/v0.1.0-alpha/doc/getting_involved/WRITING_BEARS.md

We love bugs - if you find some, be sure to share them with us:
https://github.com/coala-analyzer/coala/issues
