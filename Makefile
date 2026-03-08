.PHONY: dev backend frontend

dev:
	$(MAKE) -j2 backend frontend

backend:
	cd apps/backend && ../../.venv/bin/uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd apps/frontend && yarn install && yarn dev
