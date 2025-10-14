TENANT_ID="58fc66f3-5586-4967-8302-03dc2a2f6513"
CLIENT_ID="d779dfb6-8dfd-459d-9403-3a84b9f241eb"
CLIENT_SECRET="lwD8Q~KinaJmvTuM.tWb9Tj1LhQE~tf2J2NXkbkU"

# Request token
curl -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "client_id=$CLIENT_ID&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&client_secret=$CLIENT_SECRET&grant_type=client_credentials"