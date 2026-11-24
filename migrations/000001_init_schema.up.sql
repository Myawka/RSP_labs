CREATE TABLE users (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'examinee'
       CHECK (role IN ('examinee', 'author')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tests (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  time_limit_seconds INT NOT NULL CHECK (time_limit_seconds > 0),
  questions_count INT NOT NULL CHECK (questions_count > 0),
  is_published BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE questions (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
  question_text TEXT NOT NULL,
  question_type VARCHAR(20) NOT NULL DEFAULT 'single'
       CHECK (question_type IN ('single', 'multiple')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE answer_options (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  question_id BIGINT NOT NULL REFERENCES questions (id) ON DELETE CASCADE,
  option_text TEXT NOT NULL,
  is_correct BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE test_questions (
  test_id BIGINT NOT NULL REFERENCES tests (id) ON DELETE CASCADE,
  question_id BIGINT NOT NULL REFERENCES questions (id) ON DELETE RESTRICT,
  question_order INT NOT NULL CHECK (question_order > 0),
  PRIMARY KEY (test_id, question_id)
);

CREATE TABLE attempts (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  test_id BIGINT NOT NULL REFERENCES tests (id) ON DELETE RESTRICT,
  user_id BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  score INT NOT NULL DEFAULT 0 CHECK (score >= 0),
  max_score INT NOT NULL DEFAULT 0 CHECK (max_score >= 0),
  status VARCHAR(20) NOT NULL DEFAULT 'in_progress'
       CHECK (status IN ('in_progress', 'finished', 'expired')),
  CONSTRAINT chk_score_le_max CHECK (score <= max_score),
  CONSTRAINT chk_finished_after_start
       CHECK (finished_at IS NULL OR finished_at >= started_at)
);

CREATE TABLE attempt_questions (
  attempt_id BIGINT NOT NULL REFERENCES attempts (id) ON DELETE CASCADE,
  question_id BIGINT NOT NULL REFERENCES questions (id) ON DELETE RESTRICT,
  question_number INT NOT NULL CHECK (question_number > 0),
  PRIMARY KEY (attempt_id, question_id)
);

CREATE TABLE attempt_answers (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  attempt_id BIGINT NOT NULL REFERENCES attempts (id) ON DELETE CASCADE,
  question_id BIGINT NOT NULL REFERENCES questions (id) ON DELETE RESTRICT,
  answer_option_id BIGINT NOT NULL REFERENCES answer_options (id) ON DELETE RESTRICT,
  answered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (attempt_id, question_id, answer_option_id)
);

CREATE INDEX idx_tests_author_id ON tests (author_id);
CREATE INDEX idx_tests_is_published ON tests (is_published);
CREATE INDEX idx_questions_author_id ON questions (author_id);
CREATE INDEX idx_answer_options_question_id ON answer_options (question_id);
CREATE INDEX idx_test_questions_question_id ON test_questions (question_id);
CREATE INDEX idx_attempts_user_id ON attempts (user_id);
CREATE INDEX idx_attempts_test_id ON attempts (test_id);
CREATE INDEX idx_attempt_questions_question_id ON attempt_questions (question_id);
CREATE INDEX idx_attempt_answers_attempt_id ON attempt_answers (attempt_id);
CREATE INDEX idx_attempt_answers_question_id ON attempt_answers (question_id);
CREATE INDEX idx_attempt_answers_option_id ON attempt_answers (answer_option_id);