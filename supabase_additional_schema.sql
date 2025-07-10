-- Table to store posts
CREATE TABLE IF NOT EXISTS posts (
  id serial PRIMARY KEY,
  user_id uuid REFERENCES profiles(id) ON DELETE CASCADE,
  content text NOT NULL,
  media_url text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now()
);

-- Table to store notifications
CREATE TABLE IF NOT EXISTS notifications (
  id serial PRIMARY KEY,
  user_id uuid REFERENCES profiles(id) ON DELETE CASCADE,
  type text NOT NULL,
  message text NOT NULL,
  is_read boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT now()
);

-- Table to store chat messages
CREATE TABLE IF NOT EXISTS chat_messages (
  id serial PRIMARY KEY,
  sender_id uuid REFERENCES profiles(id) ON DELETE CASCADE,
  receiver_id uuid REFERENCES profiles(id) ON DELETE CASCADE,
  message text NOT NULL,
  created_at timestamp with time zone DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Example policies for posts
CREATE POLICY "Allow users to select their own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Allow users to insert their own posts" ON posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Example policies for notifications
CREATE POLICY "Allow users to select their own notifications" ON notifications
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Allow users to insert their own notifications" ON notifications
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Example policies for chat_messages
CREATE POLICY "Allow users to select their own sent or received chat messages" ON chat_messages
  FOR SELECT USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

CREATE POLICY "Allow users to insert their own chat messages" ON chat_messages
  FOR INSERT WITH CHECK (auth.uid() = sender_id);
