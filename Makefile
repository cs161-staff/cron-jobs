deploy-grade-feedback:
	gcloud config set project cs161-logistics
	gcloud functions deploy grade_feedback --trigger-http --runtime python39