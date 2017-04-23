Kerberos Key Distribution Center Proxy
======================================

An `asyncio`-based Python 3 implementation of [MS-KKDCP](http://msdn.microsoft.com/en-us/library/hh553774.aspx),
a protocol to proxy Kerberos ticket requests via HTTP(S).

Deployment
----------

Make sure you have gunicorn and this package installed in your virtualenv.

```
pip install gunicorn
pip install -e .
```

Now you can run the service in Gunicorn, like so:

```
gunicorn -w4 kkdcp:app -b 127.0.0.1:8126 --worker-class aiohttp.GunicornWebWorker --access-logfile -
```

Ideally, you use a reverse proxy server to front this and handle SSL, like so:

```
server {
	listen 443;
	listen [::]:443;
	server_name kdcproxy.demo.kblin.org;

	ssl on;
	ssl_certificate /etc/ssl/certs/kdcproxy.pem;
	ssl_certificate_key /etc/ssl/private/kdcproxy.key;

	root /var/www/kdxproxy;
	index index.html;

	location /KdcProxy {
		proxy_pass http://127.0.0.1:8126/;
		include proxy_params;
		add_header Cache-Control "no-cache, no-store, must-revalidate";
		add_header Pragma no-cache;
		add_header Expires 0;
	}
}
```

Microsoft suggests `/KdcProxy` as an endpoint, but at least with MIT Kerberos' client tools other paths work as well.

License
-------

This software is licensed under the GNU GPL v3 (or later), see [`LICENSE`](LICENSE) for details.
