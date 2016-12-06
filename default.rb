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

package 'nginx' do
  action :install
end
cookbook_file "nginx-default" do
  path "/etc/nginx/sites-available/default"
end
execute 'nginx_restart' do
  command 'service nginx restart'
end

package 'postgresql' do
  action :install
end
execute 'postgresql_setup' do
  command 'echo "CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;" | sudo -u postgres psql'
end

package 'postgresql-server-dev-all' do
  action :install
end
package 'libpython-dev' do
  action :install
end

package 'python' do
  action :install
end
execute 'python-setup' do
  command 'sudo apt-get install python3'
end
package 'python3-pip' do
  action :install
end
cookbook_file "get-pip.py" do
  path "/etc/get-pip.py"
end
execute 'pip-setup' do
  command 'python3 /etc/get-pip.py'
end

execute 'psycopg2-install' do
  command 'pip install psycopg2'
end
package 'uwsgi' do
  action :install
end
cookbook_file "uwsgi.ini" do
  path "/usr/local/bin/uwsgi"
end
ruby_block "insert_line" do
  block do
    file = Chef::Util::FileEdit.new("/etc/rc.local")
    file.insert_line_if_no_match("#!/bin/sh", "#!/bin/sh")
    file.insert_line_if_no_match("sleep 10", "sleep 10")
    file.insert_line_if_no_match("/usr/local/bin/uwsgi --ini /home/ubuntu/project/mysite/uwsgi.ini --daemonize /var/log/mysite.log/", "/usr/local/bin/uwsgi --ini /home/ubuntu/project/mysite/uwsgi.ini --daemonize /var/log/mysite.log")
    file.write_file
  end
end

execute 'uwsgi-setup' do
  user 'ubuntu'
  command '/etc/rc.local'
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
end

#execute 'run-server' do
#  user 'ubuntu'
#  cwd '/home/ubuntu/project/mysite'
#  command 'nohup python3 ./manage.py runserver 0.0.0.0:8080&'
#end

execute 'create-database' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/mysite'
  command 'nohup python3 ./manage.py migrate'
end

execute 'database-setup' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/mysite'
  command 'nohup python3 ./manage.py loaddata initial_data.json'
end

execute 'static-setup' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/mysite'
  command 'nohup python3 manage.py collectstatic --noinput'
end
