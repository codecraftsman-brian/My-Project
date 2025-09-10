-- PostgreSQL schema
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(120) NOT NULL,
    phone VARCHAR(50),
    address VARCHAR(255),
    cv_path VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    permissions VARCHAR(50) DEFAULT 'editor',
    created_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    benefits TEXT,
    salary VARCHAR(100),
    location VARCHAR(120),
    company VARCHAR(120),
    category VARCHAR(120),
    posted_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'open'
);

CREATE INDEX IF NOT EXISTS ix_jobs_category ON jobs(category);
CREATE INDEX IF NOT EXISTS ix_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS ix_jobs_status ON jobs(status);

CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    application_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'submitted',
    cover_letter TEXT,
    resume_path VARCHAR(255),
    CONSTRAINT uq_user_job_once UNIQUE (user_id, job_id)
);

CREATE TABLE IF NOT EXISTS email_logs (
    id SERIAL PRIMARY KEY,
    to_address VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'queued',
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    sent_at TIMESTAMP
);

-- Sample Jobs
INSERT INTO jobs (title, description, requirements, benefits, salary, location, company, category, status) VALUES
('Software Developer (Remote)', 'Build web apps in a distributed team.', '3+ years Python/JS, Git, CI/CD', 'Remote stipend, health insurance', '$60k-$90k', 'Remote', 'TechNova', 'Technology', 'open'),
('Marketing Manager', 'Lead digital campaigns for Middle East market.', '5+ years marketing, Arabic a plus', 'Housing allowance, bonus', '$70k-$95k', 'Dubai, UAE', 'DesertBrands', 'Marketing', 'open'),
('Nurse', 'Provide compassionate patient care in a hospital setting.', 'RN license, 2+ years experience', 'Relocation support, benefits', '$55k-$75k', 'Toronto, Canada', 'Maple Health', 'Healthcare', 'open'),
('Construction Engineer', 'Oversee site operations and safety.', 'Civil Eng degree, PMP preferred', 'Visa sponsorship, allowance', '$80k-$110k', 'Sydney, Australia', 'BuildRight', 'Engineering', 'open'),
('Hotel Manager', 'Manage a 5-star property and staff.', 'Hospitality degree, 5+ years', 'Housing, meals, bonus', '$65k-$100k', 'Singapore', 'Lion Hospitality', 'Hospitality', 'open'),
('English Teacher', 'Teach ESL to high-school students.', 'TEFL/TESOL, bachelor degree', 'Accommodation, airfare', '$30k-$45k', 'Tokyo, Japan', 'Sakura Schools', 'Education', 'open'),
('Data Analyst', 'Analyze business data to guide decisions.', 'SQL, Python, BI tools', 'Flexible work, training budget', '€50k-€70k', 'Berlin, Germany', 'DataHaus GmbH', 'Technology', 'open'),
('Chef', 'Lead kitchen operations in a boutique hotel.', 'Culinary diploma, 4+ years', 'Accommodation, meals', '£28k-£40k', 'London, UK', 'Harbor Hotel', 'Hospitality', 'open'),
('Mechanical Engineer', 'Design and maintain mechanical systems.', 'ME degree, CAD tools', 'Tax-free salary, relocation', 'QAR 18k-25k/month', 'Doha, Qatar', 'QatarTech', 'Engineering', 'open'),
('Customer Service Representative', 'Support customers via phone and email.', 'Excellent English, CRM tools', 'Health, PTO', '$35k-$45k', 'Austin, USA', 'Bright Support', 'Customer Service', 'open');
