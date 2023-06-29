default: env

.PHONY: env
env:
	python3 -m venv .env && .env/bin/pip3 install -r requirements.txt

# deploy:
# 	ssh max@takserver.ru "rm -rf ~/TG_BOT; mkdir TG_BOT"
# 	scp *.py max@takserver.ru:~/TG_BOT/
# 	scp run.sh max@takserver.ru:~/TG_BOT/
# 	scp Makefile max@takserver.ru:~/TG_BOT/
# 	scp requirements.txt max@takserver.ru:~/TG_BOT/
# 	scp config.yml max@takserver.ru:~/TG_BOT/
# 	scp -r img max@takserver.ru:~/TG_BOT/
# 	scp -r courses max@takserver.ru:~/TG_BOT/
