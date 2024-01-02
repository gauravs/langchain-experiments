default: run

run:
	docker compose up app

db-init:
	rm -rf db/*
	curl -sLo db/Chinook_Sqlite.sql https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql
	cat db/Chinook_Sqlite.sql | sqlite3 db/Chinook.db

db-browse:
	sqlitebrowser db/Chinook.db

ask:
	@docker compose run --rm app python main.py $(QUESTION)

ask-ollama:
	@docker compose run --rm app python ollama.py $(QUESTION)

shell:
	@docker compose run --rm app bash
