deploy-grade-feedback:
	gcloud config configurations activate cs161
	gcloud functions deploy grade_feedback

deploy-extensions:
	gcloud config configurations activate cs161
	gcloud functions deploy handle_extension_request --trigger-http --runtime python39