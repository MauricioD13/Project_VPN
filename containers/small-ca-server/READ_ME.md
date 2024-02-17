# Step 1
Execute the file "execution_ca.sh", its going to run the docker container that have smallstep ca server ready

# Step 2 
Execute the file "step_client_config.sh", this command tell the step client where is the ca server and when it tries to execute a step ca command its going to consult the CA server

# Step 3
Execute the file "sign_crt.sh", this command create a key and certificate file already signed. The password for the CA server must be in the directory