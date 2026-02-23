

##########################################################################
nginx configuration :


upstream grafana {
    server 127.0.0.1:3000;
}

server {
    listen 80;  # Ou 8080 si tu veux garder le défaut, mais 80 est standard pour http://localhost
    server_name localhost;  # Ou ton IP/domaine

    location / {
        proxy_pass http://grafana;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSO/OAuth headers (pour Keycloak/OAuth2 dans ton grafana.ini)
        proxy_set_header X-WEBAUTH-USER $http_x_webauth_user;
        proxy_set_header X-User-Roles $http_x_user_roles;

        # Timeouts & Buffers
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
        proxy_buffering off;

        # WebSocket (dashboards live)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

##################@@
grafana.ini

[server]
http_port = 3000
root_url = http://localhost:3000/

[auth]
disable_login_form = true

[auth.proxy]
enabled = true
header_name = X-WEBAUTH-USER
header_property = username
auto_sign_up = true
whitelist = 127.0.0.1, ::1
headers = Email:X-WEBAUTH-EMAIL

[users]
auto_assign_org = true
auto_assign_org_role = Editor
default_home_dashboard_path = /dashboards

[auth.anonymous]
enabled = false

[dashboards]
default_home_dashboard_path = /dashboards
