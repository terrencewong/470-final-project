# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"
cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

package 'python' do
  action :install
end
execute 'python-setup' do
  command 'sudo apt-get install python3'
end
cookbook_file "get-pip.py" do
  path "/etc/get-pip.py"
end
execute 'pip-setup' do
  command 'python3 /etc/get-pip.py'
end

execute 'git-setup' do
  command 'sudo apt-get install git'
end

execute 'django-setup' do
  command 'git clone https://github.com/django/django.git'
  command 'mkdir ~/.virtualenvs'
  command 'sudo apt-get install python3-pip'
  command 'sudo pip3 install virtualenv'
  command 'virtualenv ~/.virtualenvs/djangodev'
  command '. ~/.virtualenvs/djangodev/bin/activate'
  command 'pip install django'
  command 'pip install django-stripe-payments'
end

execute 'run-server' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/finalproject'
  command 'nohup python3 ./manage.py runserver 0.0.0.0:8080&'
end

execute 'create-database' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/finalproject'
  command 'nohup python3 ./manage.py migrate'
end

execute 'database-setup' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/finalproject'
  command 'nohup python3 ./manage.py loaddata users.json'  
end

execute 'user-setup' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/finalproject'
  command 'nohup python3 ./manage.py loaddata initial_data.json'  
end

execute 'usertype-setup' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/finalproject'
  command 'nohup python3 ./manage.py loaddata usertype.json'
end
