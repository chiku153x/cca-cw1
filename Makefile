all: deploy

stack=cw1-cca-$(stage)
bucket=chiku-deployment
profile=default
message="Initial deployment"
region="eu-west-1"
version=$(build_version)
BucketName=csv2sql$(stage)
Stage=$(stage)

deploy: build package build_layers upload
	aws cloudformation deploy --template-file $(stack)-output.yaml --stack-name $(stack) \
	--capabilities CAPABILITY_IAM --profile $(profile) --region $(region) \
	--parameter-overrides \
    DeployBucket=$(bucket) \
    Version=$(version) \
	BucketName=$(BucketName) \
    s3BasePath="$(BucketName)/"

init:
	rm -fr ./env
	python3.8 -m venv ./env
	./env/bin/pip3 install  -r src/requirements.txt
build: build_package build_layers upload

build_package:
	mkdir -p release/$(version)
	mkdir -p bin/src
	mkdir -p bin/process_csv
	mkdir -p bin/get_signed_url
	cp -R src/* bin/src ; cd bin/src ; rm -rf tests ; rm -rf __test.py
	cp -R src/process_csv/* bin/process_csv
	cp -R src/get_signed_url/* bin/get_signed_url

	cd src/process_csv/ && zip -r process_csv.zip * && mv process_csv.zip ../../release/$(version) 
	cd src/get_signed_url/ && zip -r get_signed_url.zip * && mv get_signed_url.zip ../../release/$(version)


build_layers:
	mkdir -p release/$(version)/deps/python/lib/python3.8/site-packages
	cp -r ./env/lib/python3.8/site-packages/*  release/$(version)/deps/python/lib/python3.8/site-packages
	cd release/$(version)/deps && zip -r layer.zip * && mv layer.zip ../
	rm -fr release/$(version)/deps

upload:
	aws s3 sync ./release/$(version)	s3://$(bucket)/csv2sql$(stage)/$(version) --profile $(profile)


package:
	aws cloudformation package --template-file stack.yaml --output-template-file $(stack)-output.yaml --s3-bucket $(bucket) --s3-prefix $(bucket)  --profile $(profile) --region $(region)
.PHONY: package




