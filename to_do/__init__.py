__version__ = 1.0
__app_name__ = "to_do"


(
    SUCCESS,
    ERROR,
    DB_ERROR,
    DATA_ERROR
) = range(4)

ERRORS = {
    ERROR: "General Error",
    DB_ERROR: "Database Error",
    DATA_ERROR: "The data introduce is incorrect"
}
