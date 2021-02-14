# Usage:
# ```
# eval "$(./login.sh 2FACODE)"
# ```
credentials=$(AWS_PROFILE=gartnerl2 aws sts get-session-token --serial-number arn:aws:iam::183626424367:mfa/kmamykin --token-code $1)

echo export AWS_ACCESS_KEY_ID=$(echo "$credentials" | jq .Credentials.AccessKeyId)
echo export AWS_SECRET_ACCESS_KEY=$(echo "$credentials" | jq .Credentials.SecretAccessKey)
echo export AWS_SESSION_TOKEN=$(echo "$credentials" | jq .Credentials.SessionToken)