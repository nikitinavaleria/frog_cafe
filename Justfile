run:
  docker compose up -d
  source venv/bin/activate && uvicorn src.main:app --reload

psql:
  POSTGRES_USER=$(grep -E '^POSTGRES_USER=' .env | cut -d '=' -f2- | sed -e 's/^"//' -e 's/"$//') && \
  POSTGRES_DB=$(grep -E '^POSTGRES_DB=' .env | cut -d '=' -f2- | sed -e 's/^"//' -e 's/"$//') && \
  echo "$POSTGRES_USER" && \
  echo "$POSTGRES_DB" && \
  docker compose exec -it frog-db psql -U $POSTGRES_USER -d $POSTGRES_DB

migrate:
  POSTGRES_USER=$(grep -E '^POSTGRES_USER=' .env | cut -d '=' -f2- | sed -e 's/^"//' -e 's/"$//') && \
  POSTGRES_DB=$(grep -E '^POSTGRES_DB=' .env | cut -d '=' -f2- | sed -e 's/^"//' -e 's/"$//') && \
  echo "$POSTGRES_USER" && \
  echo "$POSTGRES_DB" && \
  cat ./sql_code/InitDB.sql | docker compose exec -T frog-db psql -U $POSTGRES_USER -d $POSTGRES_DB