# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end

execute 'apt_update' do
  command 'apt-get update'
end

execute 'apt_upgrade' do
  command 'apt-get upgrade -y'
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



# Start of my additions to this configuration file:

package "python3.5"
package "libpython3.5-dev"
package "python3.5-dev"
package "python3-pip"

execute 'install_django' do
  command 'pip3 install Django'
end



package "postgresql"
package "postgresql-server-dev-all"

execute 'install_psycopg2' do     #Dependent on 'postgresql-server-dev-all'
  command 'pip3 install psycopg2'
  #ALTERNATIVELY: command apt-get install python3-psycopg2
end

execute 'create_postgresql_db' do
  command 'echo "CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;" | sudo -u postgres psql'
end



package "libpcre3"
package "libpcre3-dev"

execute 'install_uwsgi' do
  command 'pip3 install uwsgi'
end

cookbook_file "rc.local-default" do
  path "/etc/rc.local"
end

execute 'start_uwsgi' do
  command '/etc/rc.local'
end



package "nginx"

cookbook_file "nginx-default" do
  path "/etc/nginx/sites-available/default"
end

execute 'restart_nginx' do
  command 'service nginx restart'
end



execute 'migrate_schema' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/webroot'
  command 'python3.5 manage.py migrate'
end

#WHEN YOU ARE READY TO LOAD DATA INTO THE DATABASE, UNCOMMENT THIS BLOCK:
#execute 'load_data_into_database' do
#  user 'ubuntu'
#  cwd '/home/ubuntu/project/webroot'
#  command 'python3.5 manage.py loaddata dbdump.json'
#end

execute 'collect_static_files' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/webroot'
  command 'python3.5 manage.py collectstatic --noinput'
end



#This is only used if running the web application using the development web server:
#execute 'run_webserver' do
#  user 'ubuntu'
#  cwd '/home/ubuntu/project/webroot'
#  command 'nohup python3.5 manage.py runserver 0.0.0.0:80 &'
#end



#python3.5 ~/project/webroot/manage.py dbshell
#select * from polls_question;

#sudo cat /var/log/uwsgi.log  <-- uWSGI log file (name and location as chosen by you).

#sudo cat /var/log/postgresql/postgresql-9.5-main.log  <-- PostgresQL log file.

#curl -i http://localhost:8000  <-- run from inside virtual machine ('vagrant ssh').