a
    �T.f�  �                   @   s�   d dl Z d dlZd dlZd dlZeeed�dd�Zeeeed�dd�Z	e
dkr�ee jd	d� � e	e jd	 e jd
 e jd e jd � dS )�    N)�remote_summary�local_summary�returnc           
      C   s�   d}| d }|d }|dkr8|dkrJd}t d|� �� nd}t d|� �� | d }|d }|D ]$}||vr^t d	|� d
�� d} q�q^| d }|d }	|r�|	s�d}t d� | d r�|d s�d}t d� |S )NTZ	webserverZnginxZ	OpenRestyFz[WebServer][Local] Unsupported z [WebServer][Remote] Unsupported Zphpz[PHP][Local] z is not installedZmysqlz[MySql][Local] is not installedZftpsz![PureFtp][Local] is not installed)�print)
r   r   �is_matchingZremote_webserverZlocal_webserverZremote_phpsZ
local_phpsZ
remote_phpZremote_mysqlZlocal_mysql� r   �&/www/server/mdserver-web/bt_migrate.py�compare_env   s2    r	   )�hostname�port�username�passwordc                 C   s�  �ztt �| |||�}t �|�}t �|�}tdtj|dd�� t�� }tdtj|dd�� t||�}|�r^td� t �	||�\}	}
}|	r�td|	d � d�� t �
||	�}td	|� �� ntd
� |
�rtd|
d � d�� t�� }t �||d d |d d ||
�}td|� d�� ntd� |�rTtd|d � d�� t �||�}td|� d�� ntd� ntd� W |�r�|��  n|�r�|��  0 d S )Nzremote server
�   )�indentzlocal server
z*Remote and Local environemnts are matchingzStarted the site [Z	site_namez] migrationzSite migration status: zNo site selectedzStarted the DB [�nameZdatabase�rootr   zDB migration status: � zNo DB selectedzStarted the FTP [zFTP migration status: zNo FTP selectedzDPlease install necessary plugins: Openresty, mysql, php and pureftp!)�bt_migrate_remoteZ
get_client�checkZsummaryr   �json�dumps�bt_migrate_localr	   Zmigrate_wizardZmigrate_siteZget_mysql_passwordZ
migrate_dbZmigrate_ftp�close)r
   r   r   r   Z
ssh_clientZremote_resultr   r   r   ZsiteZdbZftp�statusZlocal_mysql_passwordr   r   r   �main*   s@    


"


�r   �__main__�   �   �   r   )�sysr   r   r   �dict�boolr	   �str�intr   �__name__r   �argvr   r   r   r   �<module>   s   #+