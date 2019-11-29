PATH = -s 119.0.0.8

# Por alguna razón no funciona nada. Con make compress, no reconoce comando tar, con otro, no reconoce python3. MAKEFAIL.

server:
	clear
	python3 server.py $(PATH)

client:
	clear
	python3 client.py $(PATH)

compress:
	tar -zcvf T3-ifgarces-fjji.tar.gz *.py *.md *.pdf makefile

clean:
	rm -rf __pycache__