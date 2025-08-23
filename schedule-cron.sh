* * * * * echo "cron start $(date '+%Y-%m-%d %H:%M:%S')" >> /var/log/cron.log 2>&1
* * * * * curl -H "Content-Type: application/json" -d '{"usernames":["tuyet.nt.115"]}' -X POST http://instagram_api:5000/api/scraping_instagram >> /var/log/cron.log 2>&1
