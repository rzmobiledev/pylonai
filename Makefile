help:			## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
run:            ## Run local server port 8000
	@flask --app app run

export:         ## export requirements.txt
	@pip freeze > requirements.txt

psql:           ## run local psql
	@psql -h localhost -p 5432 -U rizal