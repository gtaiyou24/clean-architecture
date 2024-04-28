#!/bin/bash

project_id=$1
project_number=`gcloud projects list | grep $1 | awk '{print $3}'`

echo $project_number