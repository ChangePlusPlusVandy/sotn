## Database
PostgreSQL

Will store:
- People: athlete/volunteer/coach/donor/org
    - Relationships between people for referrals
- Intake form submissions
    - Fields differ by user type, might require more flexibility
- Programs
- Staff/admin users
- Educational resources
- Postgres’ JSONB columns can be used for variable JSON data
    - MySQL’s JSON type is weaker (indexing and querying more complicated)

## Frontend
React + Next.js, TypeScript
- server-side rendering, quicker loads for intake landing page
- better SEO than React + Vite SPA

## Backend
FastAPI, Python

## Auth
Clerk
- easily integrate with Next.js, FastAPI
- supports password-less (email/magic link) login if needed

## Components
shadcn/ui: 
- built on Radix, Tailwind

## ORM:
SQLAlchemy
- standard choice
- handles JSONB and referral relationships well

## Emails
Resend with React Email

## Images
NextJS's <Image> for anything shipped with the site

Cloudflare R2 / S3 + Cloudfront (AWS) for uploaded resources

## Video Embeddings
Embed fom YouTube

## Deployment


