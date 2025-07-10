-- Table to store user profiles
DROP TABLE IF EXISTS profiles CASCADE;

CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY,
  username text UNIQUE NOT NULL,
  first_name text,
  last_name text,
  full_name text,
  bio text,
  profile_picture_url text,
  cover_photo_url text,
  followers_count integer DEFAULT 0,
  following_count integer DEFAULT 0,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now()
);

-- Table to store stories
CREATE TABLE IF NOT EXISTS stories (
  id serial PRIMARY KEY,
  user_id uuid REFERENCES profiles(id) ON DELETE CASCADE,
  media_url text NOT NULL,
  expires_at timestamp with time zone NOT NULL,
  created_at timestamp with time zone DEFAULT now()
);

-- Table to store registration info (if needed)
DROP TABLE IF EXISTS registrations;

-- We will not use a separate registrations table, instead use profiles table for user profile and registration info.

-- If you want to keep registrations table, it should match profiles table schema exactly:
CREATE TABLE IF NOT EXISTS registrations (
  id uuid PRIMARY KEY,
  username text UNIQUE NOT NULL,
  first_name text,
  last_name text,
  full_name text,
  bio text,
  profile_picture_url text,
  cover_photo_url text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now()
);

-- Enable Row Level Security and policies as needed
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;

-- Example policy to allow users to select their own profile
CREATE POLICY "Allow users to select their own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

-- Example policy to allow users to insert their own profile
DROP POLICY IF EXISTS "Allow users to insert their own profile" ON profiles;

CREATE POLICY "Allow users to insert their own profile" ON profiles
  FOR INSERT USING (true)
  WITH CHECK (true);

-- Allow users to update their own profile
CREATE POLICY "Allow users to update their own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- Allow users to delete their own profile
CREATE POLICY "Allow users to delete their own profile" ON profiles
  FOR DELETE USING (auth.uid() = id);

-- Example policy to allow users to select their own stories
-- CREATE POLICY "Allow users to select their own stories" ON stories
--   FOR SELECT USING (auth.uid() = user_id);

-- Example policy to allow users to insert their own stories
-- CREATE POLICY "Allow users to insert their own stories" ON stories
--   FOR INSERT WITH CHECK (auth.uid() = user_id);
