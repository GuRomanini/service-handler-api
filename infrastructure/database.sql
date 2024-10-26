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

CREATE TABLE ServiceStatus(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO ServiceStatus (enumerator) VALUES
    ('active'),
    ('inactive');

CREATE TABLE Service(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_key                 CHAR(36) NOT NULL UNIQUE,
    service_type_id             INT NOT NULL,
    service_status_id           INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_service_type_service FOREIGN KEY (service_type_id)
        REFERENCES ServiceType(id),
    CONSTRAINT fk_service_status_service FOREIGN KEY (service_status_id)
        REFERENCES ServiceStatus(id)
);

CREATE TABLE ServiceRequestStatus(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    enumerator                  VARCHAR(50) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);

INSERT INTO ServiceRequestStatus (enumerator) VALUES
	 ('on_queue'),
	 ('in_progress'),
	 ('completed'),
     ('cancelled'),
     ('aborted');

CREATE TABLE ServiceRequest(
    id		                    INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_request_key         CHAR(36) NOT NULL UNIQUE,
    service_id                  INT NOT NULL,
    service_request_status_id   INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_service_service_request FOREIGN KEY (service_id)
        REFERENCES Service(id),
    CONSTRAINT fk_service_request_status_service_request FOREIGN KEY (service_request_status_id)
        REFERENCES ServiceRequestStatus(id)
);   

CREATE TABLE ServiceRequestEvent(
    id                          INT NOT NULL UNIQUE AUTO_INCREMENT,
    service_request_id          INT  NOT NULL,
    service_request_status_id   INT NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_service_request_service_request_event FOREIGN KEY (service_request_id)
        REFERENCES ServiceRequest(id),
    CONSTRAINT fk_service_request_status_event FOREIGN KEY (service_request_status_id)
        REFERENCES ServiceRequestStatus(id)
);
