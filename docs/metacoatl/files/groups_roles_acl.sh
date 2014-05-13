#!/bin/bash

echo "Creating groups"
standard_group_id=$( dcm-create-group -n 'Standard Group' -d 'Standard Group')
intermediate_group_id=$( dcm-create-group -n 'Intermediate Group' -d 'Intermediate Group')
advanced_group_id=$( dcm-create-group -n 'Advanced Group' -d 'Advanced Group')

echo "Creating roles"
standard_role_id=$( dcm-create-role -n 'Standard Role' -d 'Standard Role')
intermediate_role_id=$( dcm-create-role -n 'Intermediate Role' -d 'Intermediate Role')
advanced_role_id=$( dcm-create-role -n 'Advanced Role' -d 'Advanced Role')

dcm-set-acl -r $standard_role_id -u http://es-onprem-customization.s3.amazonaws.com/roldcm/standard_user.json
dcm-set-acl -r $intermediate_role_id -u http://es-onprem-customization.s3.amazonaws.com/roldcm/intermediate_user.json
dcm-set-acl -r $advanced_role_id -u http://es-onprem-customization.s3.amazonaws.com/roldcm/advanced_user.json

echo "Assigning roles."
dcm-set-role -g $standard_group_id -r $standard_role_id
dcm-set-role -g $intermediate_group_id -r $intermediate_role_id
dcm-set-role -g $advanced_group_id -r $advanced_role_id

echo "Done."
