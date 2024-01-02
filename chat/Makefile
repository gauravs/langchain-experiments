default: run

run:
	docker compose up app

db-browse:
	sqlitebrowser db/test.db

start:
	uvicorn main:app --reload --port 8080

# not working outside docker
test-call:
	docker compose exec app \
		curl -XPOST http://127.0.0.1:8080/chat/stream_log \
		-H "Accept: text/event-stream" \
		-H "Content-Type: application/json" \
		-d'{"input" : { "question": "how to make an api cal" }}'
