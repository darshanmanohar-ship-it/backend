-- Supabase schema for the Synnovatify User API.
-- Run this in the Supabase Dashboard -> SQL Editor -> New query -> Run.

create extension if not exists "pgcrypto";

create table if not exists public.users (
    id          uuid primary key default gen_random_uuid(),
    name        text not null,
    email       text not null,
    phone       text,
    message     text,
    created_at  timestamptz not null default now()
);

-- Index to speed up "newest first" listing.
create index if not exists users_created_at_idx
    on public.users (created_at desc);

-- Enable Row Level Security. The API uses the service_role key, which
-- bypasses RLS, so no public policies are added. This keeps the table
-- locked down to server-side access only.
alter table public.users enable row level security;
