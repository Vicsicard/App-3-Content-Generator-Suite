-- Add notification tracking columns to user_projects table
-- This migration adds columns to track when website creation notifications are sent

-- Check if user_projects table exists, create if it doesn't
CREATE TABLE IF NOT EXISTS user_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email TEXT NOT NULL,
    project_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_email, project_id)
);

-- Add notification tracking columns if they don't exist
DO $$
BEGIN
    -- Add notification_sent column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'user_projects' AND column_name = 'notification_sent'
    ) THEN
        ALTER TABLE user_projects ADD COLUMN notification_sent BOOLEAN DEFAULT FALSE;
    END IF;

    -- Add notification_sent_at column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'user_projects' AND column_name = 'notification_sent_at'
    ) THEN
        ALTER TABLE user_projects ADD COLUMN notification_sent_at TIMESTAMP WITH TIME ZONE;
    END IF;

    -- Add notification_status column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'user_projects' AND column_name = 'notification_status'
    ) THEN
        ALTER TABLE user_projects ADD COLUMN notification_status TEXT;
    END IF;

    -- Add notification_status_code column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'user_projects' AND column_name = 'notification_status_code'
    ) THEN
        ALTER TABLE user_projects ADD COLUMN notification_status_code INTEGER;
    END IF;
END
$$;
