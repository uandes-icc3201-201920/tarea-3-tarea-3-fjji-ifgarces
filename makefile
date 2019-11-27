PATH = -s /home/elsocket

# Por alguna razón no funciona nada. Con make compress, no reconoce comando tar, etc. Tonto makefail.

server:
	python3 server.py $(PATH)

client:
	python3 client.py $(PATH)

compress:
	tar -zcvf T3-ifgarces-fjji.tar.gz *.py *.md *.pdf makefile

clean:
	rm -rf __pycache__