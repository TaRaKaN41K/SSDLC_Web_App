class ErrorCode:
    # base
    SERVER_ERROR: int = 5000
    UNEXPECTED_ERROR: int = 5200

    # password
    INVALID_PASSWORD: int = 4001

    # token
    INVALID_TOKEN: int = 4002
    TOKEN_EXPIRED: int = 4003
    INVALID_TOKEN_TYPE: int = 4004

    # user
    USER_NO_ACTIVE: int = 4005
    FORBIDDEN: int = 4006

    # devise_id
    CLIENTE_IDENTIFICATION_ERROR: int = 4010

    # file
    INVALID_FILE_EXTENSION: int = 4020
    FILE_UPLOAD_ERROR: int = 4030
    FILE_DELETION_ERROR: int = 4031

    # db
    MODEL_NOT_DEFINED: int = 4040
    UNIQUE_CONSTRAINT_VIOLATION: int = 4041
    RECORD_NOT_FOUND: int = 4042
    FIELD_NOT_EXIST: int = 4043
    DATABASE_ERROR: int = 4044
