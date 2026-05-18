# MediFlow — Next.js Frontend

Production scaffold for the Hospital OLTP system. Mirrors the design of
`../demo/index.html` and wires to the Flask API in `../api/`.

## Stack
- **Next.js 14** (App Router) + TypeScript
- **Tailwind CSS** (custom brand palette)
- **Lucide React** icons, **Recharts** charts
- `clsx` + `tailwind-merge` for class composition

## Quick start (mock mode — no backend)

```powershell
cd nextjs-app
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Open <http://localhost:3000>. Mock data is on by default
(`NEXT_PUBLIC_USE_MOCK=true`). Use any email/password to log in.

## Wire to the Flask backend

Terminal 1 (from the repo root):

```powershell
pip install -r requirements.txt
python -m api.app          # serves on 127.0.0.1:8080
```

Terminal 2:

```powershell
cd nextjs-app
# edit .env.local: set NEXT_PUBLIC_USE_MOCK=false
npm run dev
```

The app sends `X-User-Id` / `X-User-Role` headers (stub auth, matches
`api/auth.py`). Values are written to `localStorage` on login.

## Project layout

```
nextjs-app/
├── app/
│   ├── layout.tsx                # root layout, Inter font
│   ├── globals.css               # Tailwind + custom utilities
│   ├── page.tsx                  # redirects to /login or /dashboard
│   ├── login/page.tsx
│   └── (app)/                    # route group: shared sidebar shell
│       ├── layout.tsx
│       ├── dashboard/page.tsx
│       ├── patients/
│       │   ├── page.tsx
│       │   └── [id]/page.tsx
│       ├── appointments/page.tsx
│       ├── encounters/page.tsx
│       └── reports/page.tsx
├── components/
│   ├── sidebar.tsx
│   ├── header.tsx
│   ├── status-badge.tsx
│   ├── kpi-card.tsx
│   └── record-vitals-modal.tsx
├── lib/
│   ├── api.ts                    # typed API client with mock fallback
│   ├── types.ts                  # types matching MySQL schema
│   ├── mock-data.ts              # demo data
│   └── utils.ts                  # cn(), initials(), avatarColor()
└── ...config files
```

## Verifying the build

```powershell
npm run typecheck    # tsc --noEmit
npm run build
```

## Out of scope (yet)

- Real JWT auth — header stub today
- Pharmacy / Billing / Labs / Audit pages — stubs only
- xlsx / pdf exports — Flask returns 501 today
- Server-side rendering of API data — all client fetch for v0
