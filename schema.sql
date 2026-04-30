-- PLACEIQ AI PLATFORM - SUPABASE SQL SCHEMA
-- Execute this in your Supabase SQL Editor to initialize the database

-- 1. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT auth.uid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cgpa NUMERIC(3,2) CHECK (cgpa >= 0 AND cgpa <= 10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Skills Catalog
CREATE TABLE IF NOT EXISTS public.skills (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- 3. User Skills Mapping
CREATE TABLE IF NOT EXISTS public.user_skills (
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES public.skills(id) ON DELETE CASCADE,
    level TEXT CHECK (level IN ('Beginner', 'Intermediate', 'Expert')),
    PRIMARY KEY (user_id, skill_id)
);

-- 4. Job Roles & Requirements
CREATE TABLE IF NOT EXISTS public.job_roles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    required_skills JSONB NOT NULL, -- List of skill names/IDs
    industry TEXT,
    min_cgpa NUMERIC(3,2) DEFAULT 0
);

-- 5. AI Analysis Results
CREATE TABLE IF NOT EXISTS public.analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    readiness_score NUMERIC(5,2),
    skill_match NUMERIC(5,2),
    job_fit NUMERIC(5,2),
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 6. Skill Gaps Table
CREATE TABLE IF NOT EXISTS public.skill_gaps (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    skill_name TEXT NOT NULL,
    match_percent NUMERIC(5,2)
);

-- 7. Personalized Recommendations
CREATE TABLE IF NOT EXISTS public.recommendations (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    type TEXT, -- 'Skill', 'Project', 'Course'
    content TEXT NOT NULL,
    priority TEXT CHECK (priority IN ('High', 'Medium', 'Low')),
    is_completed BOOLEAN DEFAULT false
);

-- 8. Future Generation: Learning History
CREATE TABLE IF NOT EXISTS public.learning_history (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    event_type TEXT, -- 'Skill Acquired', 'Project Finished'
    event_data JSONB,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ENABLE RLS (Row Level Security)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analysis_results ENABLE ROW LEVEL SECURITY;

-- Basic Policies (User can only see their own data)
CREATE POLICY "Users can view their own profile" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own profile" ON public.users FOR UPDATE USING (auth.uid() = id);
