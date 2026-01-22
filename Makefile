# GIT commands

log:
	git log --oneline


# alembic commands
mm:
	@if "$(m)"=="" (echo Makefile: Write a migrate message & exit 1)
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head