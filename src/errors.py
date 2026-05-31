class PiCalcError(Exception):
    """Base exception for PI calculator errors."""


class CliUsageError(PiCalcError):
    """Invalid CLI usage or arguments."""


class InputParseError(PiCalcError):
    """Unable to parse user-provided input."""


class InputValidationError(PiCalcError):
    """Parsed input failed semantic validation."""


class DataLoadError(PiCalcError):
    """Unable to load data from storage."""


class DataIntegrityError(PiCalcError):
    """Loaded data is structurally invalid or inconsistent."""


class UnknownMaterialError(InputValidationError):
    """A referenced material ID is not known."""


class UnknownMaterialNameError(InputValidationError):
    """A referenced material name is not known."""
