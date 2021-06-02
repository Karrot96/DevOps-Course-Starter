#!/bin/bash

set -ev
curl -dH -X POST "$(terraform output -raw cd_webhook)"