Profile feature setup

1) Apply migrations to create new models (run from project root `d:\All_Project\Food\durgesh`):

```powershell
cd d:\All_Project\Food\durgesh
python manage.py makemigrations
python manage.py migrate
```

2) (Optional) Create a superuser to view orders in admin:

```powershell
python manage.py createsuperuser
```

3) Run the development server:

```powershell
python manage.py runserver
```

4) How it works:
- The profile page is at `/profile/` and fetches data from `/api/profile/`.
- When an authenticated user completes checkout via `/api/cart/checkout/`, the order is persisted into the database (models: `Order`, `OrderItem`).
- Saved items are available at `/api/profile/saved/` (POST to add, DELETE to remove).
- Frontend uses polling (every 3s) to update purchase history and cart without a manual refresh. For true push (WebSocket) you can integrate Django Channels later.

5) Notes & next steps:
- Make sure `durgesh` is listed in `INSTALLED_APPS` (already added in settings).
- Uploaded profile pictures are stored under the `media/` folder (`MEDIA_ROOT`). Ensure your development server serves media (settings configured when `DEBUG=True`).
- If you want real-time push rather than polling, I can add Django Channels + Redis or socket.io integration next.
