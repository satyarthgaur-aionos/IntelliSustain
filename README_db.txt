📘 DATABASE SETUP GUIDE – Inferrix AI Agent

This guide walks you through setting up PostgreSQL for the backend.

---

📦 DATABASE: `inferrix_ai`
TABLE: `users`

---

✅ STEP 1: Create Database

Open psql terminal or pgAdmin, then run:

```sql
CREATE DATABASE inferrix_ai;
```

You should now see `inferrix_ai` in pgAdmin.

---

✅ STEP 2: Create Table Schema

If you're using terminal:

```bash
psql -U postgres -d inferrix_ai -f postgres/schema.sql
```

If it doesn't work, provide absolute path:

```bash
psql -U postgres -d inferrix_ai -f "C:/Path/To/Your/Project/postgres/schema.sql"
```

If you're using pgAdmin:
- Open SQL tab for `inferrix_ai`
- Paste contents of `postgres/schema.sql`
- Click ▶️ Run

---

✅ STEP 3: Insert Dummy Users

```bash
psql -U postgres -d inferrix_ai -f postgres/dummy_users.sql
```

This adds:
- **tech@inferrix.com / admin@123** (default test login)

---

✅ STEP 4: Verify in pgAdmin

1. Expand `inferrix_ai` → `Schemas` → `public` → `Tables`
2. Right-click `Tables` → Refresh
3. You should see: `users`
4. Right-click → View/Edit Data → All Rows

---

🛠️ TROUBLESHOOTING

- Use absolute paths if relative paths fail
- Ensure your user is `postgres` or the same as your DB user
- Make sure PostgreSQL is running locally
- Ensure `schema.sql` has valid `CREATE TABLE`

---

This DB is used in `backend/database.py` and `auth_db.py` to support login flow with JWT.

💡 Use `.env` to set your connection URL:
```
POSTGRES_URL=postgresql://postgres:<your_password>@localhost:5432/inferrix_ai