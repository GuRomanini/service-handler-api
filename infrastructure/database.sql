CREATE SCHEMA IF NOT EXISTS service_handler;
USE service_handler;

CREATE TABLE ServiceType(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO ServiceType (enumerator) VALUES
    ('command'),
    ('data'),
    ('event'),
    ('stream');


CREATE TABLE Service(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_key                 CHAR(36) NOT NULL UNIQUE,
    service_name                VARCHAR(100) NOT NULL UNIQUE,
    service_type_id             INT NOT NULL,
    is_active                   TINYINT(1),
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_service_type_service FOREIGN KEY (service_type_id)
        REFERENCES ServiceType(id)
);


CREATE TABLE UAVStatus(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO UAVStatus (enumerator) VALUES
    ('ready'),
    ('busy'),
    ('inactive');

CREATE TABLE UAV(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    uav_key                     CHAR(36) NOT NULL UNIQUE,
    uav_name                    VARCHAR(100) NOT NULL,
    uav_status_id               INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_uav_status_uav FOREIGN KEY (uav_status_id)
        REFERENCES UAVStatus(id)
);


CREATE TABLE UAVService(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    uav_service_key             CHAR(36) NOT NULL UNIQUE,
    uav_key                     CHAR(36) NOT NULL,
    service_key                 CHAR(36) NOT NULL,
    uav_id                      INT NOT NULL,
    service_id                  INT NOT NULL,
    base_url                    VARCHAR(300),
    is_active                   TINYINT(1),
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_uav_service_uav FOREIGN KEY (uav_id)
        REFERENCES UAV(id),
    CONSTRAINT fk_uav_service_service FOREIGN KEY (service_id)
        REFERENCES Service(id)
);


CREATE TABLE ServiceRequestStatus(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO ServiceRequestStatus (enumerator) VALUES
    ('scheduled'),
    ('on_queue'),
    ('in_progress'),
    ('completed'),
    ('cancelled'),
    ('aborted');


CREATE TABLE ServiceRequest(
    id		                    INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_request_key         CHAR(36) NOT NULL UNIQUE,
    uav_service_id              INT NOT NULL,
    service_request_status_id   INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_uav_service_service_request FOREIGN KEY (uav_service_id)
        REFERENCES UAVService(id),
    CONSTRAINT fk_service_request_status_service_request FOREIGN KEY (service_request_status_id)
        REFERENCES ServiceRequestStatus(id)
);   


CREATE TABLE ServiceRequestEvent(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_request_id          INT NOT NULL,
    service_request_status_id   INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_service_request_service_request_event FOREIGN KEY (service_request_id)
        REFERENCES ServiceRequest(id),
    CONSTRAINT fk_service_request_status_event FOREIGN KEY (service_request_status_id)
        REFERENCES ServiceRequestStatus(id)
);
