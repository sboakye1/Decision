-- Student Mental Health Resource Decision Support System (DSS)
-- MySQL schema for normalized relational database design

CREATE DATABASE IF NOT EXISTS student_mental_health_dss
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_mental_health_dss;

CREATE TABLE users (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'counselor', 'admin') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE students (
    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    program VARCHAR(150) NOT NULL,
    level VARCHAR(100) NOT NULL,
    gpa DECIMAL(3,2) CHECK (gpa BETWEEN 0.00 AND 4.00),
    attendance_percentage DECIMAL(5,2) CHECK (attendance_percentage BETWEEN 0 AND 100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_students_user_id (user_id),
    CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE counselors (
    counselor_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    department VARCHAR(150) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_counselors_user_id (user_id),
    CONSTRAINT fk_counselors_user FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE survey_questions (
    question_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(1000) NOT NULL,
    category ENUM('stress', 'sleep', 'anxiety', 'academic', 'social') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE survey_responses (
    response_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    question_id INT UNSIGNED NOT NULL,
    answer_value VARCHAR(255) NOT NULL,
    score SMALLINT UNSIGNED NOT NULL,
    survey_month CHAR(7) NOT NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_response_student_question_month (student_id, question_id, survey_month),
    INDEX idx_survey_responses_student_month (student_id, survey_month),
    INDEX idx_survey_responses_question (question_id),
    CONSTRAINT fk_survey_responses_student FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_survey_responses_question FOREIGN KEY (question_id) REFERENCES survey_questions(question_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE survey_summary (
    summary_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    survey_month CHAR(7) NOT NULL,
    total_score INT NOT NULL,
    stress_level ENUM('Low', 'Medium', 'High') NOT NULL,
    risk_level ENUM('Low', 'Medium', 'High') NOT NULL,
    recommendation TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_survey_summary_student_month (student_id, survey_month),
    INDEX idx_survey_summary_risk (risk_level),
    CONSTRAINT fk_survey_summary_student FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE appointments (
    appointment_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    counselor_id INT UNSIGNED NOT NULL,
    appointment_date DATETIME NOT NULL,
    status ENUM('Pending', 'Approved', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Pending',
    notes TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_appointments_student (student_id),
    INDEX idx_appointments_counselor (counselor_id),
    INDEX idx_appointments_date (appointment_date),
    CONSTRAINT fk_appointments_student FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_appointments_counselor FOREIGN KEY (counselor_id) REFERENCES counselors(counselor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dss_logs (
    log_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    action_taken VARCHAR(500) NOT NULL,
    risk_level ENUM('Low', 'Medium', 'High') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_dss_logs_student (student_id),
    INDEX idx_dss_logs_risk (risk_level),
    CONSTRAINT fk_dss_logs_student FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE counselor_assignments (
    assignment_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    counselor_id INT UNSIGNED NOT NULL,
    status ENUM('active', 'closed') NOT NULL DEFAULT 'active',
    assigned_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_assignment_student_counselor (student_id, counselor_id),
    INDEX idx_counselor_assignments_counselor (counselor_id),
    INDEX idx_counselor_assignments_student (student_id),
    CONSTRAINT fk_counselor_assignments_student FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_counselor_assignments_counselor FOREIGN KEY (counselor_id) REFERENCES counselors(counselor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE counselor_notes (
    note_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    counselor_id INT UNSIGNED NOT NULL,
    note_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_counselor_notes_student (student_id),
    INDEX idx_counselor_notes_counselor (counselor_id),
    CONSTRAINT fk_counselor_notes_student FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_counselor_notes_counselor FOREIGN KEY (counselor_id) REFERENCES counselors(counselor_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
