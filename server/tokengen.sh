TOKEN=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 50; echo)
echo "ADMIN_TOKEN=$TOKEN" > .env

echo "Token generated: $TOKEN"
echo "Save this to connect to the admin panel"