from .logger import AppLogger

loggers = {
    "db":
        AppLogger(
            log_file="logs/app.log",
            category="db").get_logger(),
    "utils":
        AppLogger(
            log_file="logs/app.log",
            category="utils").get_logger(),
    "auth":
        AppLogger(
            log_file="logs/app.log",
            category="auth").get_logger(),
    "client":
        AppLogger(
            log_file="logs/app.log",
            category="client").get_logger(),
    "app":
        AppLogger(
            log_file="logs/app.log",
            category="app").get_logger(),
}
